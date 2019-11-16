import math
from math import sqrt
from numpy import array, absolute, isnan
from numpy.linalg import norm
import pandas as pd

from valurap import printer, commands
from .asg import Asg, ProfileSegment, PathSegment


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


def solve_model_simple(in_v, target_plato_v, target_out_v, target_x, accel_t,
                       plato_t, decel_t):
    vtoa_k = 65536
    xtov_k = 2 ** 32 / 50000
    xtoa_k = vtoa_k * xtov_k

    accel_a = (target_plato_v - in_v) / accel_t * vtoa_k * 1.5
    accel_j = accel_a / accel_t * 2 * 2
    accel_jj = -accel_j / accel_t * 2

    #print("accel_a:", accel_a)
    #print("accel_j:", accel_j)
    #print("accel_jj:", accel_jj)

    int_accel_jj = ir(accel_jj)
    int_accel_j = ir(-int_accel_jj * accel_t / 2)
    #print("int_accel_j:", int_accel_j)
    #print("int_accel_jj:", int_accel_jj)

    int_accel_x = int_x(accel_t, in_v * vtoa_k, 0, int_accel_j, int_accel_jj)
    int_accel_v = int_v(accel_t, in_v * vtoa_k, 0, int_accel_j, int_accel_jj)

    decel_a = (target_out_v - target_plato_v) / decel_t * vtoa_k * 1.5
    decel_j = decel_a / decel_t * 2 * 2
    decel_jj = -decel_j / decel_t * 2

    int_decel_jj = ir(decel_jj)
    int_decel_j = ir(-int_decel_jj * decel_t / 2)

    int_decel_x = int_x(decel_t, target_plato_v * vtoa_k, 0, int_decel_j, int_decel_jj)
    int_decel_v = int_v(decel_t, target_plato_v * vtoa_k, 0, int_decel_j, int_decel_jj)

    plato_x = target_x * xtoa_k - int_accel_x - int_decel_x
    plato_v = plato_x / plato_t

    int_plato_v = ir(plato_v)
    int_plato_x = int_x(plato_t, int_plato_v, 0, 0, 0)

    return {
        "accel_j": int_accel_j,
        "accel_jj": int_accel_jj,
        "plato_v": int_plato_v / vtoa_k,
        "decel_j": int_decel_j,
        "decel_jj": int_decel_jj,
        "accel_x": int_accel_x / xtoa_k,
        "plato_x": int_plato_x / xtoa_k,
        "decel_x": int_decel_x / xtoa_k,
    }

class FakeApg():
    def __init__(self, name):
        self.name = name


def plan_path(path, apgs=None, fatal=True):
    if apgs is None:
        apgs = {}

    apg_x = apgs.get("X", FakeApg("X"))
    apg_y = apgs.get("Y", FakeApg("Y"))
    apg_z = apgs.get("Z", FakeApg("Z"))

    max_a = array([3000.0, 3000.0])

    pr_opt = []

    in_x = array([0, 0])
    in_target = array([0, 0])
    in_v = array([0, 0])
    in_avail = array([0, 0])

    for i, seg in enumerate(path):
        try:
            target_x, target_y, target_v = seg

            cur_target = array([target_x, target_y])

            cur_d = cur_target - in_target
            assert (norm(cur_d) > 0)
            assert (target_v > 0)

            if i == len(path) - 1:
                out_v = array([0, 0])
                out_avail = array([0, 0])
            else:
                next_x, next_y, next_v = path[i + 1]
                next_target = array([next_x, next_y])
                next_d = next_target - cur_target
                assert (norm(next_d) > 0)

                out_v = next_v * next_d / norm(next_d)
                out_avail = next_d / 2

            cur_avail = cur_d
            plato_v = target_v * cur_d / norm(cur_d)

            print("speeds:", in_v, plato_v, out_v)
            print("avails:", in_avail, cur_avail, out_avail)

            # Enter
            enter_delta_v = plato_v - in_v
            print("enter_delta_v:", enter_delta_v)

            enter_time = max(list(absolute(enter_delta_v) / max_a))
            print("enter_time:", enter_time)

            enter_a = enter_delta_v / enter_time
            print("enter_a:", enter_a)
            enter_speed_filter = absolute(enter_delta_v) > 0.1

            enter_delta_x = in_v * enter_time + enter_a * enter_time ** 2 / 2
            print("enter_delta_x:", enter_delta_x)

            enter_t_first = (enter_time * plato_v[enter_speed_filter] - enter_delta_x[enter_speed_filter]) / enter_delta_v[
                enter_speed_filter]
            enter_t_second = enter_time - enter_t_first
            print("enter_t_first:", enter_t_first)
            print("enter_t_second:", enter_t_second)
            assert ((enter_t_first >= 0).all())
            assert ((enter_t_second >= 0).all())

            enter_need_first = in_v[enter_speed_filter] * enter_t_first
            enter_need_second = plato_v[enter_speed_filter] * enter_t_second
            print("enter_need_first:", enter_need_first)
            print("enter_need_second:", enter_need_second)
            enter_need_first_filter = absolute(enter_need_first) > 0.01
            enter_need_second_filter = absolute(enter_need_second) > 0.01
            print("in_avail assert:",
                  in_avail[enter_speed_filter][enter_need_first_filter] / enter_need_first[enter_need_first_filter])
            assert (
                (in_avail[enter_speed_filter][enter_need_first_filter] / enter_need_first[enter_need_first_filter] > 1.0).all())
            assert ((cur_avail[enter_speed_filter][enter_need_second_filter] / enter_need_second[
                enter_need_second_filter] > 2.0).all())
            cur_avail[enter_speed_filter] = cur_avail[enter_speed_filter] - enter_need_second

            # Exit
            exit_delta_v = out_v - plato_v
            print("exit_delta_v:", exit_delta_v)

            exit_time = max(list(absolute(exit_delta_v) / max_a))
            print("exit_time:", exit_time)

            exit_a = exit_delta_v / exit_time
            print("exit_a:", exit_a)
            exit_speed_filter = absolute(exit_delta_v) > 0.1

            exit_delta_x = plato_v * exit_time + exit_a * exit_time ** 2 / 2
            print("exit_delta_x:", exit_delta_x)

            exit_t_first = (exit_time * out_v[exit_speed_filter] - exit_delta_x[exit_speed_filter]) / exit_delta_v[
                exit_speed_filter]
            exit_t_second = exit_time - exit_t_first

            print("exit_t_first:", exit_t_first)
            print("exit_t_second:", exit_t_second)
            assert ((exit_t_first >= 0).all())
            assert ((exit_t_second >= 0).all())

            exit_need_first = plato_v[exit_speed_filter] * exit_t_first
            exit_need_second = out_v[exit_speed_filter] * exit_t_second
            print("exit_need_first:", exit_need_first)
            print("exit_need_second:", exit_need_second)
            exit_need_first_filter = absolute(exit_need_first) > 0.01
            exit_need_second_filter = absolute(exit_need_second) > 0.01
            # print("exit_first_filter:", exit_first_filter)
            # print("exit_second_filter:", exit_second_filter)
            print("cur_avail assert:",
                  cur_avail[exit_speed_filter][exit_need_first_filter] / exit_need_first[exit_need_first_filter])
            assert (
                ((cur_avail[exit_speed_filter][exit_need_first_filter] / exit_need_first[exit_need_first_filter]) > 1.0).all())
            assert (((out_avail[exit_speed_filter][exit_need_second_filter] / exit_need_second[
                exit_need_second_filter]) > 2.0).all())

            if norm(in_v) > 0:
                # remaining path from first step from end of last accel to start of new accel
                # performing with constant speed
                #  remaining path
                prev_plato = (in_target - in_x)
                prev_plato[enter_speed_filter] -= enter_need_first
                #  required time in ms
                prev_t = int(round(1000 * norm(prev_plato) / norm(in_v)))

                #  recalcalcalculated speed (possible with small jerk)
                prev_v = prev_plato / (prev_t / 1000)
                prev_v_x = int(round(prev_v[0] * 80 * 2 ** 32 / 50000000))
                prev_v_y = int(round(prev_v[1] * 80 * 2 ** 32 / 50000000))

                print("prev_plato_jerk:", in_v - prev_v)
                # new accel start point
                accel_start = in_x + array([prev_v_x, prev_v_y]) * prev_t / (80 * 2 ** 32 / 50000000) / 1000
            else:
                prev_t = 0
                prev_v = in_v
                accel_start = in_x

            # new decel finish_point
            print("cur_target:", cur_target)
            decel_end = cur_target
            decel_end[exit_speed_filter] += exit_need_second
            print("decel_end:", decel_end)

            plato_t = int(round(1000 * (norm(cur_d) / norm(plato_v) - enter_t_second[0] - exit_t_first[0])))
            accel_t = int(round(1000 * (enter_t_first[0] + enter_t_second[0])))
            decel_t = int(round(1000 * (exit_t_first[0] + exit_t_second[0])))

            print("accel_start:", accel_start)
            target_x = decel_end - accel_start
            print("target_x:", target_x)

            args_x = dict(
                in_v=int(round(prev_v[0] * 80 * 2 ** 32 / 50000000)),
                target_plato_v=int(round(plato_v[0] * 80 * 2 ** 32 / 50000000)),
                target_out_v=int(round(out_v[0] * 80 * 2 ** 32 / 50000000)),
                target_x=int(round(target_x[0] * 80)),
                accel_t=accel_t,
                plato_t=plato_t,
                decel_t=decel_t,
            )
            print("args_x:", args_x)
            solution_x = solve_model_simple(**args_x)
            assert (solution_x)

            args_y = dict(
                in_v=int(round(prev_v[1] * 80 * 2 ** 32 / 50000000)),
                target_plato_v=int(round(plato_v[1] * 80 * 2 ** 32 / 50000000)),
                target_out_v=int(round(out_v[1] * 80 * 2 ** 32 / 50000000)),
                target_x=int(round(target_x[1] * 80)),
                accel_t=accel_t,
                plato_t=plato_t,
                decel_t=decel_t,
            )

            print("args_y:", args_y)
            solution_y = solve_model_simple(**args_y)
            assert (solution_x)
            print("sol_x:", solution_x)
            print("sol_y:", solution_y)
            if prev_t > 0:
                pr_opt += [
                    [int(round(prev_t)), [
                        ProfileSegment(apg=apg_x, v=prev_v_x),
                        ProfileSegment(apg=apg_y, v=prev_v_y),
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
                    [plato_t, [
                        ProfileSegment(apg=apg_x, v=solution_x["plato_v"]),
                        ProfileSegment(apg=apg_y, v=solution_y["plato_v"]),
                        ProfileSegment(apg=apg_z, v=-400000),
                    ]],
                    [decel_t, [
                        ProfileSegment(apg=apg_x, j=solution_x["decel_j"], jj=solution_x["decel_jj"]),
                        ProfileSegment(apg=apg_y, j=solution_y["decel_j"], jj=solution_y["decel_jj"]),
                        ProfileSegment(apg=apg_z, v=-400000),
                    ]],
                    [5, [
                        ProfileSegment(apg=apg_x, v=0),
                        ProfileSegment(apg=apg_y, v=0),
                        ProfileSegment(apg=apg_z, v=0),

                    ]]

                ]

            print("i:", i)
            plato_v = array([solution_x["plato_v"], solution_y["plato_v"]]) / (80.0 * 2 ** 32 / 50000000)

            print()
            in_v = plato_v
            in_target = cur_target
            in_x = accel_start + array([solution_x["accel_x"], solution_y["accel_x"]]) / 80
            in_avail = in_target - in_x
        except:
            if fatal:
                raise
            print("Failed to plan full path")
            break

    return pr_opt


