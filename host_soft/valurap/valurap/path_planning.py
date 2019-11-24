import math
from collections import namedtuple
from math import sqrt
from numpy import array, absolute, isnan
from numpy.linalg import norm
import pandas as pd
from scipy.optimize import minimize


from valurap import printer, commands
from .asg import Asg, ProfileSegment

import logging
logger = logging.getLogger(__name__)
#logger.setLevel(logging.DEBUG)


class ApgState(object):
    def __init__(self):
        self.x = 0
        self.v = 0
        self.a = 0
        self.j = 0
        self.jj = 0
        self.target_v = 0
        self.target_v_set = False

    def load(self, seg):
        if seg.x is not None:
            self.x = seg.x * 2 ** 32
        if seg.v is not None:
            self.v = seg.v
        if seg.a is not None:
            self.a = seg.a
        if seg.j is not None:
            self.j = seg.j
        if seg.jj is not None:
            self.jj = seg.jj
        if seg.target_v is not None:
            self.target_v = seg.target_v
            self.target_v_set = True
        else:
            self.target_v_set = False

    def step(self):
        next_x = self.x + self.v * 50000
        next_v = int(self.v + (self.a / 65536))
        next_a = self.a + self.j
        next_j = self.j + self.jj
        next_jj = self.jj
        if self.target_v_set:
            if self.v == self.target_v:
                next_jj = 0
                next_j = 0
                next_a = 0
                next_v = self.target_v
            elif ((self.v < self.target_v and next_v > self.target_v) or
                  (self.v > self.target_v and next_v < self.target_v)):
                next_jj = 0
                next_j = 0
                next_v = self.target_v
                next_a = (self.target_v - self.v) * 65536

        # effective_v = (self.v + next_v) / 2
        effective_v = next_v

        self.x = next_x
        self.v = next_v
        self.a = next_a
        self.j = next_j
        self.jj = next_jj


def emulate(profile, verbose=0, apg_states=None):
    if apg_states is None:
        apg_states = {}

    for a in ["X", "Y", "Z"]:
        apg_states.setdefault(a, ApgState())

    ts = 0
    steps = {}
    for dt, segs in profile:
        if verbose > 0:
            print(dt)
        ts_start = ts
        ts += dt
        for seg in segs:
            if verbose > 0:
                print("  ", seg)
            state = apg_states[seg.apg.name]
            state.load(seg)
            prefix = seg.apg.name + "_"

            if verbose == 1:
                print("    {:6d} {:10.3f} {:10.1f} {:10.1f}".format(ts_start, state.x / 2.0 ** 32, state.v, state.a))
                print("                 ...")

            last_v = None
            first_v = 0
            for i in range(dt):
                step_data = steps.setdefault(ts_start + i, {'ts': ts_start + i})
                step_data[prefix + "jj"] = state.jj
                step_data[prefix + "j"] = state.j
                step_data[prefix + "a"] = state.a
                step_data[prefix + "v"] = state.v / 65536
                step_data[prefix + "x"] = state.x / 2 ** 32

                if state.v != last_v:
                    if verbose > 1:
                        if first_v > 0:
                            if first_v > 1:
                                print("        ... {} ...".format(first_v - 1))
                            print("    {:6d} {:10.3f} {:10.1f} {:10.1f}".format(ts_start + i - 1, prev_x / 2.0 ** 32,
                                                                                prev_v, prev_a))
                        print("    {:6d} {:10.3f} {:10.1f} {:10.1f}".format(ts_start + i, state.x / 2.0 ** 32, state.v,
                                                                            state.a))
                    last_v = state.v
                    first_v = 0
                else:
                    if verbose == 1 and first_v == 0:
                        print(
                            "    {:6d} {:10.3f} {:10.1f} {:10.1f}".format(ts_start + i - 1, prev_x / 2.0 ** 32, prev_v,
                                                                          prev_a))

                    first_v += 1

                prev_x = state.x
                prev_v = state.v
                prev_a = state.a
                state.step()

            if verbose > 1:
                if first_v != 0:
                    if first_v > 1:
                        print("           ... {} ...".format(first_v - 1))
                    print("    {:6d} {:10.3f} {:10.1f} {:10.1f}".format(ts_start + i, state.x / 2.0 ** 32, state.v,
                                                                        state.a))
            elif verbose == 1:
                if first_v > 1:
                    print("                 ...")

                print(
                    "    {:6d} {:10.3f} {:10.1f} {:10.1f}".format(ts_start + i, state.x / 2.0 ** 32, state.v, state.a))

    steps = [a[1] for a in sorted(steps.items())]
    steps = pd.DataFrame(steps)
    return steps


def ir(x):
    return int(round(x))


def int_x(t, v, a, j, jj):
    return ir(
        v * t + a * t * (t - 1) / 2 + j * t * (t - 1) * (t - 2) / 6 + jj * t * (t - 1) * (t - 2) * (t - 3) / 24)


def int_v(t, v, a, j, jj):
    return ir(v + a * t + j * t * (t - 1) / 2 + jj * t * (t - 1) * (t - 2) / 6)


def int_a(t, v, a, j, jj):
    return ir(a  + j * t  + jj * t * (t - 1) / 2)


vtoa_k = 65536
xtov_k = 2 ** 32 / 50000
xtoa_k = vtoa_k * xtov_k


def solve_model_simple(in_v, target_v, target_x, accel_t, plato_t, errors = None):

    if in_v == target_v or accel_t == 0:
        return {
            "accel_j": 0,
            "accel_jj": 0,
            "plato_v": target_v,
            "accel_x": 0,
            "accel_middle_x": 0,
            "plato_x": target_x,
        }

    accel_a = (target_v - in_v) / accel_t * vtoa_k * 1.5
    accel_j = accel_a / accel_t * 2 * 2
    accel_jj = -accel_j / accel_t * 2

    #print("accel_a:", accel_a)
    #print("accel_j:", accel_j)
    #print("accel_jj:", accel_jj)

    int_accel_jj = ir(accel_jj)
    int_accel_j = ir(-int_accel_jj * accel_t / 2)
    #print("int_accel_j:", int_accel_j)
    #print("int_accel_jj:", int_accel_jj)


    k_e_a = 1e-8
    k_e_delta_v = 1e-6
    k_e_jerk = 1e-6
    k_e_target = 0
    k_dj = int_accel_j * 0.01
    k_djj = int_accel_jj * 0.01

    def get_errors(dj, djj):
        int_accel_x = int_x(accel_t, in_v * vtoa_k, 0, int_accel_j + dj, int_accel_jj + djj)
        int_accel_v = int_v(accel_t, in_v * vtoa_k, 0, int_accel_j + dj, int_accel_jj + djj)
        int_accel_a = int_a(accel_t, in_v * vtoa_k, 0, int_accel_j + dj, int_accel_jj + djj)

        plato_x = target_x * xtoa_k - int_accel_x
        plato_v = plato_x / plato_t

        int_plato_v = ir(plato_v)
        int_plato_x = int_x(plato_t, int_plato_v, 0, 0, 0)

        e_delta_v = target_v - int_plato_v / vtoa_k
        e_jerk = int_plato_v / vtoa_k - int_accel_v / vtoa_k
        e_a = int_accel_a
        e_target = target_x - int_plato_x + int_accel_x

        return e_a, e_delta_v, e_jerk, e_target

    def get_errors_2(x):
        e_a, e_delta_v, e_jerk, e_target = get_errors(x[0]*k_dj, x[1]*k_djj)
        return sqrt(
            (e_a * k_e_a) ** 2
            + (e_delta_v * k_e_delta_v) ** 2
            + (e_jerk * k_e_jerk) ** 2
            + (e_target * k_e_target) ** 2
        )

    if 1:
        res = minimize(get_errors_2, [0, 0])
        print(res)
        print("old", int_accel_j, int_accel_jj)
        int_accel_j = ir(int_accel_j + k_dj * res.x[0])
        int_accel_jj = ir(int_accel_jj + k_djj * res.x[1])
        print("new", int_accel_j, int_accel_jj)

    int_accel_x = int_x(accel_t, in_v * vtoa_k, 0, int_accel_j, int_accel_jj)
    int_accel_v = int_v(accel_t, in_v * vtoa_k, 0, int_accel_j, int_accel_jj)
    int_accel_middle_x = int_x(int(accel_t/2), in_v * vtoa_k, 0, int_accel_j, int_accel_jj)

    plato_x = target_x * xtoa_k - int_accel_x
    plato_v = plato_x / plato_t

    int_plato_v = ir(plato_v)
    int_plato_x = int_x(plato_t, int_plato_v, 0, 0, 0)

    return {
        "accel_j": int_accel_j,
        "accel_jj": int_accel_jj,
        "plato_v": int_plato_v / vtoa_k,
        "accel_x": int_accel_x / xtoa_k,
        "accel_middle_x": int_accel_middle_x / xtoa_k,
        "plato_x": int_plato_x / xtoa_k,
    }



class FakeApg():
    def __init__(self, name):
        self.name = name


def plan_path(start, path, apgs=None, fatal=True, plan_errors=None, plan_notes=None, max_middle_delta = 0.2):
    if apgs is None:
        apgs = {}

    if plan_errors is None:
        plan_errors = []

    if plan_notes is None:
        plan_notes = {}

    for i in range(len(path)):
        plan_notes.setdefault(i, {})

    apg_x = apgs.get("X", FakeApg("X"))
    apg_y = apgs.get("Y", FakeApg("Y"))
    apg_z = apgs.get("Z", FakeApg("Z"))

    max_a = array([3000.0, 2000.0])

    pr_opt = []

    in_x = array(start)         # end of accel position for previous segment
    in_target = array(start)    # target position of previous segment
    in_v = array([0, 0])        # plato speed of previous segment
    in_avail = array([0, 0])    # length left in previous segment after end of accel
    need_abort = False

    for i, seg in enumerate(path):
        try:
            target_x, target_y, target_v = seg # this segment target and speed

            cur_target = array([target_x, target_y])

            in_v[abs(in_v) < 0.1] = 0

            small_diff = abs(in_target - in_x) < 0.1
            in_target[small_diff] = in_x[small_diff]

            small_diff = abs(cur_target - in_target) < 0.1
            cur_target[small_diff] = in_target[small_diff]

            cur_d = cur_target - in_target # this segment theoretical target vector

            if i == len(path) - 1:
                assert (norm(cur_d) < 1e-3)
                assert (target_v < 1e-3)
                out_v = array([0, 0])       # next segment target speed
                out_avail = array([0, 0])   # available length in next segment for next speed accel
            elif i == len(path) - 2:
                assert (norm(cur_d) > 0)
                assert (target_v > 0)
                out_v = array([0, 0])       # next segment target speed
                out_avail = array([0, 0])   # available length in next segment for next speed accel
            else:
                assert (norm(cur_d) > 0)
                assert (target_v > 0)
                next_x, next_y, next_v = path[i + 1]
                next_target = array([next_x, next_y])
                next_d = next_target - cur_target
                next_d[abs(next_d) < 0.1] = 0
                assert (norm(next_d) > 0)

                out_v = next_v * next_d / norm(next_d)
                out_avail = next_d / 2

            cur_avail = cur_d + 0                       # full length is available for now
            plato_v = target_v * cur_d / (norm(cur_d) + 1e-6)    # target plato speed

            print("x: in {} in_target {} cur_target {}".format(in_x, in_target, cur_target))
            print("speeds: prev {} current {} next {}".format(in_v, plato_v, out_v))
            print("avails: prev {} current {} next {}".format(in_avail, cur_avail, out_avail))

            # Enter
            enter_delta_v = plato_v - in_v
            print("enter_delta_v:", enter_delta_v)

            enter_time = max(list(absolute(enter_delta_v) / max_a))
            print("enter_time:", enter_time)

            enter_a = enter_delta_v / enter_time
            print("enter_a:", enter_a)

            enter_delta_x = in_v * enter_time + enter_a * enter_time ** 2 / 2 # total required length of enter
            print("enter_delta_x:", enter_delta_x)

            enter_t_first = (enter_time * plato_v - enter_delta_x) / (enter_delta_v + 1e-6)
            enter_t_second = enter_time - enter_t_first
            print("enter_t_first:", enter_t_first)
            print("enter_t_second:", enter_t_second)
            assert ((enter_t_first >= 0).all())
            assert ((enter_t_second >= 0).all())

            enter_need_first = in_v * enter_t_first         # length required from prev and curremt segments
            enter_need_second = plato_v * enter_t_second
            print("enter_need_first:", enter_need_first)
            print("enter_need_second:", enter_need_second)

            in_avail_enter_assert = (in_avail / (enter_need_first + 1e-6))[enter_need_first > 0]
            if not (in_avail_enter_assert > 1.0).all():
                print("in_avail enter assert:", in_avail_enter_assert)
                assert not fatal
                plan_errors.append((i, "in_avail_enter", in_avail_enter_assert, 1.0))
                need_abort = True
            else:
                plan_notes[i]["in_avail_enter"] = (in_avail_enter_assert, 1.0)

            cur_avail_enter_assert = (cur_avail / (enter_need_second + 1e-6))[enter_need_second>0]
            if not (cur_avail_enter_assert > 2.0).all():
                print("cur_avail enter assert:", cur_avail_enter_assert)
                assert not fatal
                plan_errors.append((i, "cur_avail_enter", cur_avail_enter_assert, 2.0))
                need_abort = True
            else:
                plan_notes[i]["cur_avail_enter"] = (cur_avail_enter_assert, 2.0)

            cur_avail = cur_avail - enter_need_second # adjust avail length

            # Exit
            exit_delta_v = out_v - plato_v
            exit_delta_v[abs(exit_delta_v) <  1e-3] = 0
            print("exit_delta_v:", exit_delta_v)

            exit_time = max(list(absolute(exit_delta_v) / max_a))
            print("exit_time:", exit_time)

            exit_a = exit_delta_v / (exit_time + 1e-6)
            print("exit_a:", exit_a)

            exit_delta_x = plato_v * exit_time + exit_a * exit_time ** 2 / 2
            print("exit_delta_x:", exit_delta_x)

            exit_t_first = (exit_time * out_v - exit_delta_x) / (exit_delta_v + 1e-6)
            exit_t_first[abs(exit_a) < 1e-3 ] = 0
            exit_t_first[exit_time < 1e-6] = 0

            exit_t_second = exit_time - exit_t_first
            exit_t_second[abs(exit_a) < 1e-3 ] = 0
            exit_t_second[exit_time < 1e-6] = 0

            print("exit_t_first:", exit_t_first)
            print("exit_t_second:", exit_t_second)
            assert ((exit_t_first >= 0).all())
            assert ((exit_t_second >= 0).all())

            exit_need_first = plato_v * exit_t_first
            exit_need_second = out_v * exit_t_second
            print("exit_need_first:", exit_need_first)
            print("exit_need_second:", exit_need_second)

            cur_avail_exit_assert = (cur_avail / (exit_need_first + 1e-8))[exit_need_first > 0]
            if not (cur_avail_exit_assert > 1.0).all():
                print("cur_avail exit assert:", cur_avail_exit_assert)
                assert not fatal
                plan_errors.append((i, "cur_avail_exit", cur_avail_exit_assert, 1.0))
                need_abort = True
            else:
                plan_notes[i]["cur_avail_exit"] = (cur_avail_exit_assert, 1.0)

            out_avail_exit_assert = (out_avail / (exit_need_second + 1e-8))[exit_need_second > 0]
            if not (out_avail_exit_assert > 1.0).all():
                print("out_avail exit assert:", out_avail_exit_assert)
                assert not fatal
                plan_errors.append((i, "out_avail_exit", out_avail_exit_assert, 1.0))
                need_abort = True
            else:
                plan_notes[i]["out_avail_exit"] = (out_avail_exit_assert, 1.0)

            if norm(in_v) > 0:
                # remaining path from first step from end of last accel to start of new accel
                # performing with constant speed
                #  remaining path
                prev_plato = in_target - in_x
                prev_plato -= enter_need_first
                #  required time in ms
                prev_t = norm(prev_plato) / norm(in_v)

                # new accel start point
                accel_start = in_x + in_v * prev_t
            else:
                assert(norm(enter_need_first) < 1e-6)
                prev_t = 0
                accel_start = in_x

            # new decel finish_point
            print("cur_target:", cur_target)
            decel_end = cur_target + exit_need_second
            print("decel_end:", decel_end)

            decel_start = cur_target - exit_need_first
            print("decel_start:", decel_start)

            plato_t = ir(1000 * (norm(cur_d) / (norm(plato_v) + 1e-6) - enter_t_second[0] - exit_t_first[0]))
            accel_t = ir(1000 * (enter_t_first[0] + enter_t_second[0]))
            decel_t = ir(1000 * (exit_t_first[0] + exit_t_second[0]))

            print("accel_start:", accel_start)
            target_x = decel_start - accel_start
            print("target_x:", target_x)

            args_x = dict(
                in_v=ir(in_v[0] * 80 * xtov_k / 1000),
                target_v=ir(plato_v[0] * 80 * xtov_k / 1000),
                target_x=ir(target_x[0] * 80),
                accel_t=accel_t,
                plato_t=plato_t,
            )
            print("args_x:", args_x)
            solution_x = solve_model_simple(**args_x)
            assert (solution_x)
            print("cur_target:", cur_target)

            args_y = dict(
                in_v=ir(in_v[1] * 80 * xtov_k / 1000),
                target_v=ir(plato_v[1] * 80 * xtov_k / 1000),
                target_x=ir(target_x[1] * 80),
                accel_t=accel_t,
                plato_t=plato_t,
            )

            print("args_y:", args_y)
            solution_y = solve_model_simple(**args_y)
            assert (solution_x)
            print("sol_x:", solution_x)
            print("sol_y:", solution_y)

            if (
                    norm(in_v) > 0
                    and norm(plato_v) > 0
                    and norm(in_v) + norm(plato_v) - norm(in_v + plato_v) > 1
            ):

                print("non straigh factor:", norm(in_v) + norm(plato_v) - norm(in_v + plato_v))
                accel_middle = array([solution_x["accel_middle_x"], solution_y["accel_middle_x"]]) / 80 + accel_start
                middle_delta = norm(accel_middle - in_target)

                if middle_delta > max_middle_delta:
                    print("middle_delta too big", middle_delta)
                    assert not fatal
                    plan_errors.append((i, "middle_delta", [max_middle_delta / middle_delta], 1.0))
                    need_abort = True
                else:
                    plan_notes[i]["middle_delta"] = (middle_delta, max_middle_delta)

            if prev_t > 0:
                pr_opt += [
                    [int(round(prev_t * 1000)), [
                        ProfileSegment(apg=apg_x, v=ir(in_v[0] * 80 * xtov_k /1000)),
                        ProfileSegment(apg=apg_y, v=ir(in_v[1] * 80 * xtov_k /1000)),
                        ProfileSegment(apg=apg_z, v=-400000),
                    ]]
                ]

            pr_opt += [
                [accel_t, [
                    ProfileSegment(apg=apg_x, j=solution_x["accel_j"], jj=solution_x["accel_jj"]),
                    ProfileSegment(apg=apg_y, j=solution_y["accel_j"], jj=solution_y["accel_jj"]),
                    ProfileSegment(apg=apg_z, v=-400000),
                ]]
            ]

            if i == len(path) - 1:
                pr_opt += [
                    [5, [
                        ProfileSegment(apg=apg_x, v=0),
                        ProfileSegment(apg=apg_y, v=0),
                        ProfileSegment(apg=apg_z, v=0),

                    ]]

                ]

            print("i:", i)
            plato_v = array([solution_x["plato_v"], solution_y["plato_v"]]) / (80.0 * xtov_k / 1000)

            print()
            in_v = plato_v
            in_target = cur_target
            in_x = accel_start + array([solution_x["accel_x"], solution_y["accel_x"]]) / 80
            in_avail = in_target - in_x

            plan_notes[i]["path_details"] = {
                "accel_t": accel_t,
                "decel_t": decel_t,
                "plato_t": plato_t,
                "plato_v": plato_v,
                "plato_start": in_x,
                "plato_end": decel_start,
            }

            if need_abort:
                print("Failed to plan full path")
                break
        except:
            raise

    return pr_opt


PathSegment = namedtuple("PathSegment", "x y speed")
PathLimits = namedtuple("PathLimits", "max_x_v max_y_v max_x_a max_y_a max_x_j max_y_j max_middle_delta")


class PathPlanner:
    def __init__(self, path: [PathSegment], limits: PathLimits):
        path = self.cast_path(path)
        path_ok = self.check_path(path)
        if path_ok is False:
            raise ValueError("bad path", path)
        self.path = path
        self.limits = limits

    def cast_path(self, path):
        return [PathSegment(a[0], a[1], a[2]) for a in path]

    def check_path(self, path):
        if len(path) < 3:
            logger.warning("Path can't be shorter than 3 elements")
            return False

        if path[0].speed != 0:
            logger.warning("initial speed must be 0")
            return False

        if path[-1].speed != 0:
            logger.warning("final speed must be 0")
            return False

        if path[-2].x != path[-1].x:
            logger.warning("final movement must be 0")
            return False

        if path[-2].y != path[-1].y:
            logger.warning("final movement must be 0")
            return False

        for i in range(1, len(path) - 1):
            if path[i].speed == 0:
                logger.warning("active segments speeds must be > 0")
                return False

            if abs(path[i].x - path[i-1].x) + abs(path[i].y - path[i-1].y)== 0:
                logger.warning("active segments length must be > 0")
                return False


    def plan_path_in_floats(self, slowdowns=None):
        max_a = array([self.limits.max_x_a, self.limits.max_y_a])

        EPS = 1e-3
        plan = []
        plan_errors = []
        plan_notes = {i: {} for i in range(len(self.path))}
        if slowdowns is None:
            slowdowns = [ 1.0 ] * (len(self.path) - 1)

        in_x = array([self.path[0].x * 1.0, self.path[0].y * 1.0])  # end of accel position for previous segment
        in_target = array(in_x)  # target position of previous segment
        in_v = array([0.0, 0.0])  # plato speed of previous segment
        in_avail = array([0.0, 0.0])  # length left in previous segment after end of accel
        need_abort = False

        path = self.path[1:]

        for i, seg in enumerate(path):
            try:
                cur_target = array([seg.x * 1.0, seg.y * 1.0])
                target_v = seg.speed * slowdowns[i]

                cur_d = cur_target - in_target  # this segment theoretical target vector

                if i >= len(path) - 2:
                    out_v = array([0.0, 0.0])  # next segment target speed
                    out_avail = array([0.0, 0.0])  # available length in next segment for next speed accel
                else:
                    next_x, next_y, next_v = path[i + 1]
                    next_v = next_v * slowdowns[i+1]
                    next_target = array([next_x * 1.0, next_y * 1.0])
                    next_d = next_target - cur_target
                    out_v = next_v * next_d / norm(next_d)
                    out_avail = next_d / 2

                cur_avail = cur_d + 0.0  # full length is available for now

                plato_v = cur_d * 0.0
                cd_filter = abs(cur_d) > EPS
                plato_v[cd_filter] = target_v * cur_d[cd_filter] / norm(cur_d)  # target plato speed

                logger.debug("x: in {} in_target {} cur_target {}".format(in_x, in_target, cur_target))
                logger.debug("speeds: prev {} current {} next {}".format(in_v, plato_v, out_v))
                logger.debug("avails: prev {} current {} next {}".format(in_avail, cur_avail, out_avail))

                # Enter
                enter_delta_v = plato_v - in_v
                enter_delta_v[abs(enter_delta_v) <= EPS] = 0.0
                logger.debug("enter_delta_v: %s", enter_delta_v)

                enter_time = max(list(absolute(enter_delta_v) / max_a))
                logger.debug("enter_time: %s", enter_time)

                if enter_time > EPS:
                    enter_a = enter_delta_v / enter_time
                else:
                    enter_a = enter_delta_v * 0.0

                logger.debug("enter_a: %s", enter_a)

                enter_delta_x = in_v * enter_time + enter_a * enter_time ** 2 / 2  # total required length of enter
                logger.debug("enter_delta_x: %s", enter_delta_x)

                edv_filter = abs(enter_delta_v) > EPS

                enter_t_first = plato_v * 0.0
                enter_t_first[edv_filter] = (enter_time * plato_v[edv_filter] - enter_delta_x[edv_filter]) / enter_delta_v[edv_filter]
                enter_t_first[enter_t_first <= EPS] = 0.0

                enter_t_second = enter_time - enter_t_first
                enter_t_second[enter_t_second <= EPS] = 0.0

                logger.debug("enter_t_first: %s", enter_t_first)
                logger.debug("enter_t_second: %s", enter_t_second)
                assert ((enter_t_first >= 0).all())
                assert ((enter_t_second >= 0).all())

                enter_need_first = in_v * enter_t_first  # length required from prev and curremt segments
                enter_need_second = plato_v * enter_t_second
                logger.debug("enter_need_first: %s", enter_need_first)
                logger.debug("enter_need_second: %s", enter_need_second)

                enf_filter = abs(enter_need_first) > EPS
                in_avail_enter_assert = in_avail[enf_filter] / enter_need_first[enf_filter]
                if not (in_avail_enter_assert > 1.0).all():
                    plan_errors.append((i, "in_avail_enter", in_avail_enter_assert, 1.0))
                    need_abort = True
                else:
                    plan_notes[i]["in_avail_enter"] = (in_avail_enter_assert, 1.0)

                ens_filter = abs(enter_need_second) > 0
                cur_avail_enter_assert = cur_avail[ens_filter] / enter_need_second[ens_filter]
                if not (cur_avail_enter_assert > 2.0).all():
                    plan_errors.append((i, "cur_avail_enter", cur_avail_enter_assert, 2.0))
                    need_abort = True
                else:
                    plan_notes[i]["cur_avail_enter"] = (cur_avail_enter_assert, 2.0)

                cur_avail = cur_avail - enter_need_second  # adjust avail length

                # Exit
                exit_delta_v = out_v - plato_v
                exit_delta_v[abs(exit_delta_v) < EPS] = 0.0
                logger.debug("exit_delta_v: %s", exit_delta_v)

                exit_time = max(list(absolute(exit_delta_v) / max_a))
                logger.debug("exit_time: %s", exit_time)

                if exit_time > EPS:
                    exit_a = exit_delta_v / exit_time
                else:
                    exit_a = exit_delta_v * 0.0

                logger.debug("exit_a: %s", exit_a)

                exit_delta_x = plato_v * exit_time + exit_a * exit_time ** 2 / 2
                logger.debug("exit_delta_x: %s", exit_delta_x)

                exit_t_first = exit_delta_v * 0.0
                edv_filter = abs(exit_delta_v) > EPS
                exit_t_first[edv_filter] = (exit_time * out_v[edv_filter] - exit_delta_x[edv_filter]) / exit_delta_v[edv_filter]
                exit_t_first[exit_t_first < EPS] = 0.0

                exit_t_second = exit_time - exit_t_first
                exit_t_second[exit_t_second < EPS] = 0.0

                logger.debug("exit_t_first: %s", exit_t_first)
                logger.debug("exit_t_second: %s", exit_t_second)
                assert ((exit_t_first >= 0).all())
                assert ((exit_t_second >= 0).all())

                exit_need_first = plato_v * exit_t_first
                exit_need_second = out_v * exit_t_second
                logger.debug("exit_need_first: %s", exit_need_first)
                logger.debug("exit_need_second: %s", exit_need_second)

                enf_filter = abs(exit_need_first) > EPS
                cur_avail_exit_assert = cur_avail[enf_filter] / exit_need_first[enf_filter]
                if not (cur_avail_exit_assert > 1.0).all():
                    plan_errors.append((i, "cur_avail_exit", cur_avail_exit_assert, 1.0))
                    need_abort = True
                else:
                    plan_notes[i]["cur_avail_exit"] = (cur_avail_exit_assert, 1.0)

                ens_filter = abs(exit_need_second) > EPS
                out_avail_exit_assert = out_avail[ens_filter] / exit_need_second[ens_filter]
                if not (out_avail_exit_assert > 1.0).all():
                    plan_errors.append((i, "out_avail_exit", out_avail_exit_assert, 1.0))
                    need_abort = True
                else:
                    plan_notes[i]["out_avail_exit"] = (out_avail_exit_assert, 1.0)

                if norm(in_v) > EPS:
                    # remaining path from first step from end of last accel to start of new accel
                    # performing with constant speed
                    #  remaining path
                    prev_plato = in_target - in_x - enter_need_first
                    #  required time in ms
                    prev_t = norm(prev_plato) / norm(in_v)

                    # new accel start point
                    accel_start = in_x + in_v * prev_t
                else:
                    assert (norm(enter_need_first) < EPS)
                    prev_t = 0
                    accel_start = in_x

                accel_end = accel_start + enter_need_first + enter_need_second

                # new decel finish_point
                logger.debug("cur_target: %s", cur_target)
                decel_end = cur_target + exit_need_second
                logger.debug("decel_end: %s", decel_end)

                decel_start = cur_target - exit_need_first
                logger.debug("decel_start: %s", decel_start)

                accel_t = enter_t_first[0] + enter_t_second[0]
                decel_t = exit_t_first[0] + exit_t_second[0]
                if norm(plato_v) > EPS:
                    plato_t = norm(decel_start - accel_end) / norm(plato_v)
                else:
                    plato_t = 0

                if (
                        norm(in_v) > 0
                        and norm(plato_v) > 0
                        and norm(in_v) + norm(plato_v) - norm(in_v + plato_v) > 1
                ):

                    logger.debug("non straigh factor: %s", norm(in_v) + norm(plato_v) - norm(in_v + plato_v))
                    accel_middle = accel_start + (in_v + (plato_v - in_v) / 4) * accel_t / 2
                    middle_delta = norm(accel_middle - in_target)

                    if middle_delta > self.limits.max_middle_delta:
                        plan_errors.append((i, "middle_delta", [sqrt(self.limits.max_middle_delta / middle_delta)], 1.0))
                        need_abort = True
                    else:
                        plan_notes[i]["middle_delta"] = (middle_delta, self.limits.max_middle_delta)

                if prev_t > 0:
                    plan += [[prev_t, accel_start[0], accel_start[1], in_v[0], in_v[1], "plato_{}".format(i-1)]]

                plan += [[accel_t, accel_end[0], accel_end[1], plato_v[0], plato_v[1], "accel_{}".format(i)]]

                if i == len(path) - 1:
                    plan += [[5, accel_end[0], accel_end[1], 0.0, 0.0, "final"]]

                logger.debug("i: %d", i)

                in_v = plato_v
                in_target = cur_target
                in_x = accel_end
                in_avail = in_target - in_x

                plan_notes[i]["path_details"] = {
                    "accel_t": accel_t,
                    "decel_t": decel_t,
                    "plato_t": plato_t,
                    "plato_v": plato_v,
                    "plato_start": in_x,
                    "plato_end": decel_start,
                }

                if need_abort:
                    logger.warning("Failed to plan full path")
                    break
            except:
                raise

        return plan, plan_errors, plan_notes


    def plan_with_slow_down(self):
        slowdowns = [1.0] * (len(self.path) - 1)
        while True:
            plan, errors, notes = self.plan_path_in_floats(slowdowns)
            if not errors:
                return plan, slowdowns, notes

            k = 1.0
            for e in errors:
                _, _, v, target_v = e
                k = max(target_v/min(v), k)

            if k > 1.0:
                slowdowns = slowdowns / k / 1.05
                print(slowdowns)
            else:
                raise RuntimeError()



