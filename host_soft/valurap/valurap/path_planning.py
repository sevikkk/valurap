import math
from collections import namedtuple
from math import sqrt

import numpy
from numpy import array, absolute, isnan
from numpy.linalg import norm
import pandas as pd
from scipy.optimize import minimize


import logging

from valurap.asg import ProfileSegment

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

EPS = 1e-3


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
            elif (self.v < self.target_v and next_v > self.target_v) or (
                self.v > self.target_v and next_v < self.target_v
            ):
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
                print(
                    "    {:6d} {:10.3f} {:10.1f} {:10.1f}".format(
                        ts_start, state.x / 2.0 ** 32, state.v, state.a
                    )
                )
                print("                 ...")

            last_v = None
            first_v = 0
            for i in range(dt):
                step_data = steps.setdefault(ts_start + i, {"ts": ts_start + i})
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
                            print(
                                "    {:6d} {:10.3f} {:10.1f} {:10.1f}".format(
                                    ts_start + i - 1, prev_x / 2.0 ** 32, prev_v, prev_a
                                )
                            )
                        print(
                            "    {:6d} {:10.3f} {:10.1f} {:10.1f}".format(
                                ts_start + i, state.x / 2.0 ** 32, state.v, state.a
                            )
                        )
                    last_v = state.v
                    first_v = 0
                else:
                    if verbose == 1 and first_v == 0:
                        print(
                            "    {:6d} {:10.3f} {:10.1f} {:10.1f}".format(
                                ts_start + i - 1, prev_x / 2.0 ** 32, prev_v, prev_a
                            )
                        )

                    first_v += 1

                prev_x = state.x
                prev_v = state.v
                prev_a = state.a
                state.step()

            if verbose > 1:
                if first_v != 0:
                    if first_v > 1:
                        print("           ... {} ...".format(first_v - 1))
                    print(
                        "    {:6d} {:10.3f} {:10.1f} {:10.1f}".format(
                            ts_start + i, state.x / 2.0 ** 32, state.v, state.a
                        )
                    )
            elif verbose == 1:
                if first_v > 1:
                    print("                 ...")

                print(
                    "    {:6d} {:10.3f} {:10.1f} {:10.1f}".format(
                        ts_start + i, state.x / 2.0 ** 32, state.v, state.a
                    )
                )

    steps = [a[1] for a in sorted(steps.items())]
    steps = pd.DataFrame(steps)
    return steps


def ir(x):
    return int(round(x))


def int_x(t, v, a, j, jj):
    return ir(
        v * t
        + a * t * (t - 1) / 2
        + j * t * (t - 1) * (t - 2) / 6
        + jj * t * (t - 1) * (t - 2) * (t - 3) / 24
    )


def int_v(t, v, a, j, jj):
    return ir(v + a * t + j * t * (t - 1) / 2 + jj * t * (t - 1) * (t - 2) / 6)


def int_a(t, v, a, j, jj):
    return ir(a + j * t + jj * t * (t - 1) / 2)


vtoa_k = 65536.0
xtov_k = 2 ** 32 / 50000.0
xtoa_k = vtoa_k * xtov_k


def solve_model_simple(in_v, target_v, target_x, accel_t, plato_t):
    print("accel_t:", accel_t)
    print("plato_t:", plato_t)

    if in_v == target_v or accel_t == 0:
        int_target_v = ir(target_v * vtoa_k)
        int_plato_x = int_x(plato_t, int_target_v, 0, 0, 0)
        int_accel_x = int_x(plato_t, int_target_v, 0, 0, 0)
        return {
            "accel_j": 0,
            "accel_jj": 0,
            "plato_v": int_target_v / vtoa_k,
            "accel_x": int_accel_x / xtoa_k,
            "accel_middle_x": int_accel_x / 2 / xtoa_k,
            "plato_x": int_plato_x / xtoa_k,
            "accel_t": accel_t,
            "plato_t": plato_t,
        }

    accel_a = (target_v - in_v) / accel_t * vtoa_k * 1.5
    accel_j = accel_a / accel_t * 2 * 2
    accel_jj = -accel_j / accel_t * 2

    print("accel_a:", accel_a)
    print("accel_j:", accel_j)
    print("accel_jj:", accel_jj)

    int_accel_jj = ir(accel_jj)
    int_accel_j = ir(-int_accel_jj * accel_t / 2)
    print("int_accel_j:", int_accel_j)
    print("int_accel_jj:", int_accel_jj)

    k_e_a = 1e-5
    k_e_delta_v = 1e-2
    k_e_jerk = 1e-2
    k_e_target = 1e-3
    k_dj = int_accel_j * 0.1
    k_djj = int_accel_jj * 0.1

    int_in_v = ir(in_v * vtoa_k)

    def get_errors(dj, djj):
        int_accel_x = int_x(accel_t, int_in_v, 0, int_accel_j + dj, int_accel_jj + djj)
        int_accel_v = int_v(accel_t, int_in_v, 0, int_accel_j + dj, int_accel_jj + djj)
        int_accel_a = int_a(accel_t, int_in_v, 0, int_accel_j + dj, int_accel_jj + djj)

        target_plato_x = target_x * xtoa_k - int_accel_x
        int_plato_x1 = int_x(plato_t, int_accel_v, 0, 0, 0)
        int_plato_v = ir(int_accel_v * 1.0 * target_plato_x / int_plato_x1)

        if abs(target_v) < EPS:
            int_plato_v = 0

        int_plato_x = int_x(plato_t, int_plato_v, 0, 0, 0)

        e_delta_v = abs(int_plato_v / vtoa_k - target_v)
        if e_delta_v > 100:
            e_delta_v += (e_delta_v - 100) * 100

        e_jerk = abs(int_plato_v - int_accel_v) / vtoa_k
        if e_jerk > 100:
            e_jerk += (e_jerk - 100) * 100

        e_a = int_accel_a  # residual acceleration
        e_target = abs(target_x - (int_plato_x + int_accel_x) / xtoa_k)  # target X error
        if e_target > 1:
            e_target += (e_target - 1) * 100

        return e_a, e_delta_v, e_jerk, e_target

    def get_errors_2(x):
        e_a, e_delta_v, e_jerk, e_target = get_errors(x[0] * k_dj, x[1] * k_djj)
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

    int_accel_x = int_x(accel_t, int_in_v, 0, int_accel_j, int_accel_jj)
    int_accel_v = int_v(accel_t, int_in_v, 0, int_accel_j, int_accel_jj)
    int_accel_middle_x = int_x(ir(accel_t / 2), int_in_v, 0, int_accel_j, int_accel_jj)
    print("int_accel_v:", int_accel_v, int_accel_v / vtoa_k / xtov_k / 80 * 1000)
    print("int_accel_x:", int_accel_x, int_accel_x / xtoa_k / 80)

    target_plato_x = target_x * xtoa_k - int_accel_x
    int_plato_x1 = int_x(plato_t, int_accel_v, 0, 0, 0)
    int_plato_v = ir(int_accel_v * 1.0 * target_plato_x / int_plato_x1)
    if abs(target_v) < EPS:
        int_plato_v = 0

    int_plato_x = int_x(plato_t, int_plato_v, 0, 0, 0)

    print("int_plato_v:", int_plato_v, int_plato_v / vtoa_k / xtov_k / 80 * 1000)
    e_target = target_x - (int_plato_x + int_accel_x) / xtoa_k  # target X error
    e_delta_v = int_plato_v / vtoa_k - target_v
    e_jerk = (int_plato_v - int_accel_v) / vtoa_k
    print("e_target:", e_target / 80)
    print("e_delta_v:", e_delta_v)
    print("e_jerk:", e_jerk)

    return {
        "accel_j": int_accel_j,
        "accel_jj": int_accel_jj,
        "target_v": target_v,
        "plato_v": int_plato_v / vtoa_k,
        "accel_x": int_accel_x / xtoa_k,
        "accel_middle_x": int_accel_middle_x / xtoa_k,
        "plato_x": int_plato_x / xtoa_k,
        "e_target": e_target,
        "e_delta_v": e_delta_v,
        "e_jerk": e_jerk,
        "accel_t": accel_t,
        "plato_t": plato_t,
    }


class FakeApg:
    def __init__(self, name):
        self.name = name


PathSegment = namedtuple("PathSegment", "x y speed")
PathLimits = namedtuple(
    "PathLimits", "max_x_v max_y_v max_x_a max_y_a max_x_j max_y_j max_middle_delta"
)


class PathPlanner:
    def __init__(self, path: [PathSegment], limits: PathLimits, extras: [str, [float]] = None):
        path = self.cast_path(path)
        path_ok = self.check_path(path)
        if not path_ok:
            raise ValueError("bad path", path)
        self.path = path
        self.limits = limits
        extras = self.cast_extras(extras)
        extras_ok = self.check_extras(extras)
        if not extras_ok:
            raise ValueError("bad extras", extras)
        self.extras = extras

    def cast_path(self, path):
        return [PathSegment(a[0], a[1], a[2]) for a in path]

    def cast_extras(self, extras):
        if not extras:
            return []
        new_extras = []
        for name, data in extras:
            new_data = [float(a) for a in data]
            new_extras.append([name, new_data])
        return new_extras

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

            if abs(path[i].x - path[i - 1].x) + abs(path[i].y - path[i - 1].y) == 0:
                logger.warning("active segments length must be > 0")
                return False

        return True

    def check_extras(self, extras):
        for name, data in extras:
            if len(data) != len(self.path):
                logger.warning("length of extras series must be the same as path")
                return False

        return True

    def plan_path_in_floats(self, slowdowns=None, with_extras=False):
        max_a = array([self.limits.max_x_a, self.limits.max_y_a])

        plan = []
        plan_errors = []
        if slowdowns is None:
            slowdowns = [1.0] * (len(self.path) - 1)

        in_x = array(
            [self.path[0].x * 1.0, self.path[0].y * 1.0]
        )  # end of accel position for previous segment
        in_target = array(in_x)  # target position of previous segment
        in_v = array([0.0, 0.0])  # plato speed of previous segment
        need_abort = False

        start_x = in_x * 1.0
        path = []
        extras = []
        in_extras = []
        if with_extras:
            for name, data in self.extras:
                in_extras.append(data[0])

        in_extras = array(in_extras)
        start_extras = in_extras * 1.0

        log_ids = []
        for i, seg in enumerate(self.path[1:]):
            end_x = array([seg.x, seg.y])
            seg_v = seg.speed
            splits = slowdowns[i]
            if not type(splits) == list:
                splits = [[splits, 1.0]]

            total = 0.0
            for _, split in splits:
                total += split

            vec_x = (end_x - start_x) / total

            if with_extras:
                end_extras = []
                for name, data in self.extras:
                    end_extras.append(data[i + 1])
                end_extras = array(end_extras)
                vec_extras = (end_extras - start_extras) / total

                if seg_v > EPS:
                    seg_vec_time = norm(vec_x) / seg_v
                else:
                    assert norm(vec_extras) < EPS
                    vec_extras = vec_extras * 0.0
                    seg_vec_time = 1

            for j, (k, split) in enumerate(splits):
                seg_x = start_x + vec_x * split
                path.append(PathSegment(seg_x[0], seg_x[1], seg.speed * k))
                log_ids.append((i, j))
                start_x = seg_x
                if with_extras:
                    seg_extras = start_extras + vec_extras * split
                    seg_time = seg_vec_time * split / k
                    seg_speeds = (seg_extras - start_extras) / seg_time
                    extras.append([seg_extras, seg_speeds])
                    start_extras = seg_extras

        plan_notes = {i: {} for i in range(len(path))}
        extras_plan = []
        extras_in_target = start_extras

        for i, seg in enumerate(path):
            try:
                cur_target = array([seg.x * 1.0, seg.y * 1.0])
                target_v = seg.speed

                cur_d = cur_target - in_target  # this segment theoretical target vector

                if i >= len(path) - 2:
                    out_v = array([0.0, 0.0])  # next segment target speed
                else:
                    next_x, next_y, next_v = path[i + 1]
                    next_v = next_v
                    next_target = array([next_x * 1.0, next_y * 1.0])
                    next_d = next_target - cur_target
                    out_v = next_v * next_d / norm(next_d)

                cur_avail = cur_d + 0.0  # full length is available for now

                plato_v = cur_d * 0.0
                cd_filter = abs(cur_d) > EPS
                plato_v[cd_filter] = target_v * cur_d[cd_filter] / norm(cur_d)  # target plato speed

                logger.debug(
                    "x: in {} in_target {} cur_target {}".format(in_x, in_target, cur_target)
                )
                logger.debug("speeds: prev {} current {} next {}".format(in_v, plato_v, out_v))
                logger.debug("avails: current {}".format(cur_avail))

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

                enter_delta_x = (
                    in_v * enter_time + enter_a * enter_time ** 2 / 2
                )  # total required length of enter
                logger.debug("enter_delta_x: %s", enter_delta_x)

                edv_filter = abs(enter_delta_v) > EPS

                enter_t_first = plato_v * 0.0
                enter_t_first[edv_filter] = (
                    enter_time * plato_v[edv_filter] - enter_delta_x[edv_filter]
                ) / enter_delta_v[edv_filter]
                enter_t_first[enter_t_first <= EPS] = 0.0

                enter_t_second = enter_time - enter_t_first
                enter_t_second[enter_t_second <= EPS] = 0.0

                logger.debug("enter_t_first: %s", enter_t_first)
                logger.debug("enter_t_second: %s", enter_t_second)
                assert (enter_t_first >= 0).all()
                assert (enter_t_second >= 0).all()

                enter_need_first = (
                    in_v * enter_t_first
                )  # length required from prev and curremt segments
                enter_need_second = plato_v * enter_t_second
                logger.debug("enter_need_first: %s", enter_need_first)
                logger.debug("enter_need_second: %s", enter_need_second)

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
                exit_t_first[edv_filter] = (
                    exit_time * out_v[edv_filter] - exit_delta_x[edv_filter]
                ) / exit_delta_v[edv_filter]
                exit_t_first[exit_t_first < EPS] = 0.0

                exit_t_second = exit_time - exit_t_first
                exit_t_second[exit_t_second < EPS] = 0.0

                logger.debug("exit_t_first: %s", exit_t_first)
                logger.debug("exit_t_second: %s", exit_t_second)
                assert (exit_t_first >= 0).all()
                assert (exit_t_second >= 0).all()

                exit_need_first = plato_v * exit_t_first
                exit_need_second = out_v * exit_t_second
                logger.debug("exit_need_first: %s", exit_need_first)
                logger.debug("exit_need_second: %s", exit_need_second)

                cur_d_filter = abs(cur_d) > EPS
                cur_avail = cur_avail - exit_need_first  # adjust avail length
                cur_avail_assert = numpy.sqrt(
                    (cur_avail + cur_d)[cur_d_filter] / cur_d[cur_d_filter]
                )

                if not (cur_avail_assert > 1.0).all():
                    plan_errors.append((i, "cur_avail", cur_avail_assert, 1.0))
                    need_abort = True
                else:
                    plan_notes[i]["cur_avail"] = (cur_avail_assert, 1.0)

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
                    assert norm(enter_need_first) < EPS
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

                    logger.debug(
                        "non straigh factor: %s", norm(in_v) + norm(plato_v) - norm(in_v + plato_v)
                    )
                    accel_middle = accel_start + (in_v + (plato_v - in_v) / 4) * accel_t / 2
                    middle_delta = norm(accel_middle - in_target)

                    if middle_delta > self.limits.max_middle_delta:
                        plan_errors.append(
                            (
                                i,
                                "middle_delta",
                                [sqrt(self.limits.max_middle_delta / middle_delta)],
                                1.0,
                            )
                        )
                        need_abort = True
                    else:
                        plan_notes[i]["middle_delta"] = (middle_delta, self.limits.max_middle_delta)

                a, b = log_ids[i - 1]
                prev_log_id = "{}".format(a)
                if b != 0:
                    prev_log_id += "_{}".format(b)

                a, b = log_ids[i]
                cur_log_id = "{}".format(a)
                if b != 0:
                    cur_log_id += "_{}".format(b)

                if prev_t > 0:
                    plan += [
                        [
                            prev_t,
                            accel_start[0],
                            accel_start[1],
                            in_v[0],
                            in_v[1],
                            "plato_{}".format(prev_log_id),
                        ]
                    ]
                    if with_extras:
                        assert i > 0

                        extras_in_target = extras[i - 1][0]
                        extras_in_speed = extras[i - 1][1]

                        if norm(in_v) > 0:
                            equiv_in_time = norm(enter_need_first) / norm(in_v)
                        else:
                            equiv_in_time = 0

                        extras_plan += [
                            [
                                prev_t,
                                extras_in_target - extras_in_speed * equiv_in_time,
                                extras_in_speed,
                                "plato_{}".format(prev_log_id),
                            ]
                        ]

                plan += [
                    [
                        accel_t,
                        accel_end[0],
                        accel_end[1],
                        plato_v[0],
                        plato_v[1],
                        "accel_{}".format(cur_log_id),
                    ]
                ]

                if with_extras:
                    if i > 0:
                        extras_in_target = extras[i - 1][0]
                    else:
                        extras_in_target = in_extras

                    extras_speed = extras[i][1]
                    if norm(plato_v) > 0:
                        equiv_out_time = norm(enter_need_second) / norm(plato_v)
                    else:
                        equiv_out_time = 0

                    extras_plan += [
                        [
                            accel_t,
                            extras_in_target + extras_speed * equiv_out_time,
                            extras_speed,
                            "accel_{}".format(prev_log_id),
                        ]
                    ]

                if i == len(path) - 1:
                    plan += [[5, accel_end[0], accel_end[1], 0.0, 0.0, "final"]]

                logger.debug("i: %d", i)

                in_v = plato_v
                in_target = cur_target
                in_x = accel_end

                plan_notes[i]["path_details"] = {
                    "accel_t": accel_t,
                    "decel_t": decel_t,
                    "plato_t": plato_t,
                    "plato_v": plato_v,
                    "plato_start": in_x,
                    "plato_end": decel_start,
                    "log_id": log_ids[i],
                }

                if need_abort:
                    logger.warning("Failed to plan full path")
                    break
            except:
                raise

        extras_out = []
        if with_extras:
            for i, (name, data) in enumerate(self.extras):
                extras_out.append([name, [(p[0], p[1][i], p[2][i]) for p in extras_plan]])

        return plan, plan_errors, plan_notes, extras_out

    def plan_with_slow_down(self):
        slowdowns = numpy.array([1.0] * (len(self.path) - 1))
        while True:
            plan, errors, notes, _ = self.plan_path_in_floats(slowdowns)
            if not errors:
                return plan, slowdowns, notes

            k = 1.0
            for e in errors:
                _, _, v, target_v = e
                k = max(target_v / min(v), k)

            if k > 1.0:
                slowdowns = slowdowns / k / 1.05
            else:
                raise RuntimeError()

    def plan_speedup(self, initial_slowdowns, initial_notes):
        slowdowns = list(initial_slowdowns)
        notes = initial_notes
        for i, note in notes.items():
            details = note.get("path_details", None)
            if not details:
                continue

            orig_i, j = details["log_id"]

            if type(slowdowns[orig_i]) is list:  # not yet split
                continue

            cur_segment = self.path[orig_i + 1]
            prev_segment = self.path[orig_i]
            segment_length = norm(
                array([prev_segment.x - cur_segment.x, prev_segment.y - cur_segment.y])
            )

            plato_len = norm(details["plato_end"] - details["plato_start"])
            current_plato_v = details["plato_v"]
            logger.debug("current_plato_v: %s", current_plato_v)
            current_k = slowdowns[orig_i]
            target_plato_v = current_plato_v / current_k
            logger.debug("target_plato_v: %s", target_plato_v)
            plato_delta_v = target_plato_v - current_plato_v
            logger.debug("plato_delta_v: %s", plato_delta_v)
            logger.debug(
                "plato_speedup_tv: %s",
                plato_delta_v / array([self.limits.max_x_a, self.limits.max_y_a]),
            )
            plato_speedup_t = max(plato_delta_v / array([self.limits.max_x_a, self.limits.max_y_a]))
            logger.debug("plato_speedup_t: %s", plato_speedup_t)
            plato_min_len = norm(plato_speedup_t * (current_plato_v + target_plato_v))  # / 2 * 2
            logger.debug("plato_min_len: %s", plato_min_len)

            if plato_len < 3:  # 3mm of plato
                logger.info("plato is less than 3mm")
                continue

            if plato_len < plato_min_len * 2:  # at least half of plato will be constant speed
                logger.info("plato is too short")
                continue

            sd = slowdowns[orig_i]
            try_slowdowns = slowdowns[:]
            try_slowdown = [
                [sd, segment_length / 4],
                [1.0, segment_length / 2],
                [sd, segment_length / 4],
            ]
            # print("try_slowdown", try_slowdown)
            try_slowdowns[orig_i] = try_slowdown
            # print("try_slowdowns", try_slowdowns)
            try_plan, try_errors, try_notes, _ = self.plan_path_in_floats(try_slowdowns)
            if try_errors:
                logger.info("first planning ended with errors: %s", try_errors)
                continue

            new_notes = {0: None, 1: None, 2: None}
            for k, n in try_notes.items():
                n_details = n.get("path_details", None)
                n_orig_i, n_j = n_details["log_id"]
                if n_orig_i == orig_i:
                    new_notes[n_j] = n_details

            accel_notes = new_notes[0]
            accel_plato_len = norm(accel_notes["plato_end"] - accel_notes["plato_start"])
            logger.debug("ACCEL old_len: %s plato_len: %s", try_slowdown[0][1], accel_plato_len)
            new_accel_len = (try_slowdown[0][1] - accel_plato_len) * 1.2

            plato_notes = new_notes[1]
            decel_notes = new_notes[2]
            decel_plato_len = norm(decel_notes["plato_end"] - decel_notes["plato_start"])
            logger.debug("DECEL old_len: %s plato_len: %s", try_slowdown[2][1], decel_plato_len)
            new_decel_len = (try_slowdown[2][1] - decel_plato_len) * 1.2

            try_slowdown = [
                [sd, new_accel_len],
                [1.0, segment_length - new_accel_len - new_decel_len],
                [sd, new_decel_len],
            ]
            # print("try_slowdown", try_slowdown)
            try_slowdowns[orig_i] = try_slowdown
            # print("try_slowdowns", try_slowdowns)
            try_plan, try_errors, try_notes, _ = self.plan_path_in_floats(try_slowdowns)
            if try_errors:
                print("errors", try_errors)
                continue

            # print("final_notes", try_notes)
            # print("plan", try_plan)
            slowdowns[orig_i] = try_slowdown
            notes = try_notes

        return slowdowns

    def solve_segment(
        self,
        prev_x,
        prev_y,
        prev_vx,
        prev_vy,
        acc_t,
        acc_x,
        acc_y,
        acc_vx,
        acc_vy,
        plato_t,
        plato_x,
        plato_y,
        plato_vx,
        plato_vy,
    ):
        print(
            "solve_segment:",
            prev_x,
            prev_y,
            prev_vx,
            prev_vy,
            "\n",
            acc_t,
            acc_x,
            acc_y,
            acc_vx,
            acc_vy,
            "\n",
            plato_t,
            plato_x,
            plato_y,
            plato_vx,
            plato_vy,
        )
        res_x = solve_model_simple(
            prev_vx / 1000 * 80 * xtov_k,
            acc_vx / 1000 * 80 * xtov_k,
            (plato_x - prev_x) * 80,
            ir(acc_t * 1000),
            ir(plato_t * 1000),
        )
        res_y = solve_model_simple(
            prev_vy / 1000 * 80 * xtov_k,
            acc_vy / 1000 * 80 * xtov_k,
            (plato_y - prev_y) * 80,
            ir(acc_t * 1000),
            ir(plato_t * 1000),
        )
        return res_x, res_y

    def plan_to_int(self, plan):
        prev_x, prev_y, prev_vx, prev_vy = self.path[0].x, self.path[0].y, 0.0, 0.0
        acc_t, acc_x, acc_y, acc_vx, acc_vy, _ = plan[0]
        _, plato_x, plato_y, plato_vx, plato_vy, _ = plan[0]
        plato_t = 0
        int_plan = []
        for p in plan[1:]:
            next_t, next_x, next__y, next_vx, next_vy, _ = p
            assert next_t > 0
            if abs(next_vx - acc_vx) + abs(next_vy - acc_vy) > EPS:
                sol = self.solve_segment(
                    prev_x,
                    prev_y,
                    prev_vx,
                    prev_vy,
                    acc_t,
                    acc_x,
                    acc_y,
                    acc_vx,
                    acc_vy,
                    plato_t,
                    plato_x,
                    plato_y,
                    plato_vx,
                    plato_vy,
                )
                int_plan.append(sol)
                prev_x, prev_y, prev_vx, prev_vy = (
                    prev_x + (sol[0]["accel_x"] + sol[0]["plato_x"]) / 80,
                    prev_y + (sol[1]["accel_x"] + sol[1]["plato_x"]) / 80,
                    sol[0]["plato_v"] * 1000 / 80 / xtov_k,
                    sol[1]["plato_v"] * 1000 / 80 / xtov_k,
                )
                acc_t, acc_x, acc_y, acc_vx, acc_vy, _ = p
                _, plato_x, plato_y, plato_vx, plato_vy, _ = p
                plato_t = 0
            else:
                plato_t += next_t
                _, plato_x, plato_y, plato_vx, plato_vy, _ = p

        if acc_t > 0:
            int_plan.append(
                self.solve_segment(
                    prev_x,
                    prev_y,
                    prev_vx,
                    prev_vy,
                    acc_t,
                    acc_x,
                    acc_y,
                    acc_vx,
                    acc_vy,
                    plato_t,
                    plato_x,
                    plato_y,
                    plato_vx,
                    plato_vy,
                )
            )

        return int_plan

    def plan(self):
        plan, slowdowns, notes = self.plan_with_slow_down()
        speedup_slowdowns = self.plan_speedup(slowdowns, notes)
        plan, errors, notes, _ = self.plan_path_in_floats(speedup_slowdowns)
        int_plan = self.plan_to_int(plan)
        return int_plan

    def format(self, plan, apgs=None):
        if apgs is None:
            apgs = {}

        apg_x = apgs.get("X", FakeApg("X"))
        apg_y = apgs.get("Y", FakeApg("Y"))
        apg_z = apgs.get("Z", FakeApg("Z"))

        pr_opt = []

        for sol_x, sol_y in plan:
            if sol_x["accel_t"] > 0:
                pr_opt += [
                    [
                        sol_x["accel_t"],
                        [
                            ProfileSegment(apg=apg_x, j=sol_x["accel_j"], jj=sol_x["accel_jj"]),
                            ProfileSegment(apg=apg_y, j=sol_y["accel_j"], jj=sol_y["accel_jj"]),
                            # ProfileSegment(apg=apg_z, v=-400000),
                        ],
                    ]
                ]
            if sol_x["plato_t"] > 0:
                pr_opt += [
                    [
                        sol_x["plato_t"],
                        [
                            ProfileSegment(apg=apg_x, v=ir(sol_x["plato_v"])),
                            ProfileSegment(apg=apg_y, v=ir(sol_y["plato_v"])),
                            # ProfileSegment(apg=apg_z, v=-400000),
                        ],
                    ]
                ]

        pr_opt += [
            [
                5,
                [
                    ProfileSegment(apg=apg_x, v=0),
                    ProfileSegment(apg=apg_y, v=0),
                    ProfileSegment(apg=apg_z, v=0),
                ],
            ]
        ]

        return pr_opt
