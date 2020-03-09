import math
from collections import namedtuple
from math import sqrt

import numpy
from numpy import array, absolute, isnan, minimum, maximum, arange, around
from numpy.linalg import norm
from scipy.optimize import minimize

try:
    import pandas as pd
except ImportError:
    pd = None

import logging

from valurap.asg import ProfileSegment

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

EPS = 1e-6


class ApgState(object):
    def __init__(self, accel_step=50000):
        self.x = 0
        self.v = 0
        self.a = 0
        self.j = 0
        self.jj = 0
        self.target_v = 0
        self.target_v_set = False
        self.accel_step = accel_step

    def __str__(self):
        return f"<ApgState x={self.x} v={self.v} a={self.a} j={self.j} jj={self.jj}>"

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
        next_x = self.x + self.v * self.accel_step
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


def emulate(profile, verbose=0, apg_states=None, accel_step=50000):
    if apg_states is None:
        apg_states = {}

    for a in ["X", "Y", "Z"]:
        apg_states.setdefault(a, ApgState(accel_step=accel_step))

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
    if pd:
        steps = pd.DataFrame(steps)
        steps["t"] = steps["ts"] * accel_step / 50000000.0
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
    # print("accel_t:", accel_t)
    # print("plato_t:", plato_t)

    if (abs(in_v - target_v) < EPS) or (accel_t == 0):
        int_target_v = ir(target_v * vtoa_k)
        int_in_v = ir(in_v * vtoa_k)
        int_accel_x = int_x(accel_t, int_in_v, 0, 0, 0)
        int_plato_x = int_x(plato_t, int_target_v, 0, 0, 0)
        e_target = target_x - (int_plato_x + int_accel_x) / xtoa_k  # target X error
        e_delta_v = int_target_v / vtoa_k - target_v
        e_jerk = (int_target_v - int_in_v) / vtoa_k
        return {
            "accel_j": 0,
            "accel_jj": 0,
            "accel_a": 0,
            "plato_x": int_plato_x / xtoa_k,
            "plato_v": int_target_v / vtoa_k,
            "accel_x": int_accel_x / xtoa_k,
            "accel_middle_x": int_accel_x / 2 / xtoa_k,
            "accel_t": accel_t,
            "plato_t": plato_t,
            "target_v": target_v,
            "e_target": e_target,
            "e_delta_v": e_delta_v,
            "e_jerk": e_jerk,
        }

    if True or accel_t < 20:
        int_target_v = ir(target_v * vtoa_k)
        int_in_v = ir(in_v * vtoa_k)

        int_accel_a = ir((int_target_v - int_in_v) / accel_t)

        int_accel_x = int_x(accel_t, int_in_v, int_accel_a, 0, 0)
        int_accel_v = int_v(accel_t, int_in_v, int_accel_a, 0, 0)

        if 0:
            target_plato_x = target_x * xtoa_k - int_accel_x
            int_plato_x1 = int_x(plato_t, int_target_v, 0, 0, 0)
            if int_plato_x1 != 0:
                int_plato_v = ir(int_target_v * 1.0 * target_plato_x / int_plato_x1)
            else:
                int_plato_v = 0

            if abs(target_v) < EPS:
                int_plato_v = 0
        else:
            int_plato_v = int_target_v

        int_plato_x = int_x(plato_t, int_plato_v, 0, 0, 0)

        e_target = target_x - (int_plato_x + int_accel_x) / xtoa_k  # target X error
        e_delta_v = int_target_v / vtoa_k - target_v
        e_jerk = (int_target_v - int_accel_v) / vtoa_k
        return {
            "accel_j": 0,
            "accel_jj": 0,
            "accel_a": int_accel_a,
            "plato_x": int_plato_x / xtoa_k,
            "plato_v": int_plato_v / vtoa_k,
            "accel_x": int_accel_x / xtoa_k,
            "accel_middle_x": int_accel_x / 2 / xtoa_k,
            "accel_t": accel_t,
            "plato_t": plato_t,
            "target_v": target_v,
            "e_target": e_target,
            "e_delta_v": e_delta_v,
            "e_jerk": e_jerk,
        }

    accel_a = (target_v - in_v) / accel_t * vtoa_k * 1.5
    accel_j = accel_a / accel_t * 2 * 2
    accel_jj = -accel_j / accel_t * 2

    # print("accel_a:", accel_a)
    # print("accel_j:", accel_j)
    # print("accel_jj:", accel_jj)

    int_accel_jj = ir(accel_jj)
    int_accel_j = ir(-int_accel_jj * accel_t / 2)
    # print("int_accel_j:", int_accel_j)
    # print("int_accel_jj:", int_accel_jj)

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
        if int_plato_x1 != 0:
            int_plato_v = ir(int_accel_v * 1.0 * target_plato_x / int_plato_x1)
        else:
            int_plato_v = 0

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
        # print(res)
        # print("old", int_accel_j, int_accel_jj)
        int_accel_j = ir(int_accel_j + k_dj * res.x[0])
        int_accel_jj = ir(int_accel_jj + k_djj * res.x[1])
        # print("new", int_accel_j, int_accel_jj)

    int_accel_x = int_x(accel_t, int_in_v, 0, int_accel_j, int_accel_jj)
    int_accel_v = int_v(accel_t, int_in_v, 0, int_accel_j, int_accel_jj)
    int_accel_middle_x = int_x(ir(accel_t / 2), int_in_v, 0, int_accel_j, int_accel_jj)
    # print("int_accel_v:", int_accel_v, int_accel_v / vtoa_k / xtov_k * 1000)
    # print("int_accel_x:", int_accel_x, int_accel_x / xtoa_k)

    target_plato_x = target_x * xtoa_k - int_accel_x
    int_plato_x1 = int_x(plato_t, int_accel_v, 0, 0, 0)
    if int_plato_x1 != 0:
        int_plato_v = ir(int_accel_v * 1.0 * target_plato_x / int_plato_x1)
    else:
        int_plato_v = 0

    if abs(target_v) < EPS:
        int_plato_v = 0

    int_plato_x = int_x(plato_t, int_plato_v, 0, 0, 0)

    # print("int_plato_v:", int_plato_v, int_plato_v / vtoa_k / xtov_k * 1000)
    e_target = target_x - (int_plato_x + int_accel_x) / xtoa_k  # target X error
    e_delta_v = int_plato_v / vtoa_k - target_v
    e_jerk = (int_plato_v - int_accel_v) / vtoa_k
    # print("e_target:", e_target)
    # print("e_delta_v:", e_delta_v)
    # print("e_jerk:", e_jerk)

    return {
        "accel_j": int_accel_j,
        "accel_jj": int_accel_jj,
        "accel_a": 0,
        "plato_x": int_plato_x / xtoa_k,
        "plato_v": int_plato_v / vtoa_k,
        "accel_x": int_accel_x / xtoa_k,
        "accel_middle_x": int_accel_middle_x / xtoa_k,
        "accel_t": accel_t,
        "plato_t": plato_t,
        "target_v": target_v,
        "e_target": e_target,
        "e_delta_v": e_delta_v,
        "e_jerk": e_jerk,
    }


class FakeApg:
    def __init__(self, name):
        self.name = name


PathSegment = namedtuple("PathSegment", "x y speed")
PathLimits = namedtuple(
    "PathLimits", "max_x_v max_y_v max_x_a max_y_a max_x_j max_y_j max_middle_delta"
)


class PathPlanner:
    def __init__(
        self, path: [PathSegment], limits: PathLimits, extras: [str, float, [float]] = None
    ):
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
        for name, spmm, data in extras:
            new_data = [float(a) for a in data]
            new_extras.append([name, float(spmm), new_data])
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
        for name, spmm, data in extras:
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
            for name, spmm, data in self.extras:
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
                for name, spmm, data in self.extras:
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
                    next_target = None
                    next_v = None
                else:
                    next_x, next_y, next_v = path[i + 1]
                    next_v = next_v
                    next_target = array([next_x * 1.0, next_y * 1.0])
                    next_d = next_target - cur_target
                    if norm(next_d) > EPS:
                        out_v = next_v * next_d / norm(next_d)
                    else:
                        out_v = next_d * 0.0

                cur_avail = cur_d + 0.0  # full length is available for now

                plato_v = cur_d * 0.0
                cd_filter = abs(cur_d) > EPS
                plato_v[cd_filter] = target_v * cur_d[cd_filter] / norm(cur_d)  # target plato speed

                logger.debug(
                    "x: in {} in_target {} cur_target {} next_target {}".format(
                        in_x, in_target, cur_target, next_target
                    )
                )
                logger.debug("next_v: {}".format(next_v))
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
                    plan += [[0.005, accel_end[0], accel_end[1], 0.0, 0.0, "final"]]
                    if with_extras:
                        extras_plan += [
                            [
                                0.005,
                                extras_in_target + extras_speed * equiv_out_time,
                                extras_speed * 0.0,
                                "final",
                            ]
                        ]

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
            for i, (name, spmm, data) in enumerate(self.extras):
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
            elif numpy.isnan(k):
                slowdowns = slowdowns * 0.8
            else:
                print(errors)
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

            sd = slowdowns[orig_i]
            if 1.0 - sd < EPS:
                logger.info("not slowed down")
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
                # print("errors", try_errors)
                continue

            # print("final_notes", try_notes)
            # print("plan", try_plan)
            slowdowns[orig_i] = try_slowdown
            notes = try_notes

        return slowdowns

    def solve_in_ints(self, acc_t, plato_t, prev_x, prev_v, target_x, target_v, steps_per_mm):
        res = solve_model_simple(
            prev_v / 1000 * steps_per_mm * xtov_k,
            target_v / 1000 * steps_per_mm * xtov_k,
            (target_x - prev_x) * steps_per_mm,
            ir(acc_t * 1000),
            ir(plato_t * 1000),
        )
        res["accel_x"] /= steps_per_mm
        res["accel_middle_x"] /= steps_per_mm
        res["plato_x"] /= steps_per_mm
        res["plato_v_int"] = res["plato_v"]
        res["plato_v"] /= steps_per_mm / 1000 * xtov_k
        res["target_v"] /= steps_per_mm / 1000 * xtov_k

        return res

    def plan_to_int(self, plan, extras_plan=None):
        prev_x, prev_y, prev_vx, prev_vy = self.path[0].x, self.path[0].y, 0.0, 0.0
        acc_t, acc_x, acc_y, acc_vx, acc_vy, _ = plan[0]
        _, plato_x, plato_y, plato_vx, plato_vy, _ = plan[0]

        prev_extras = []
        acc_extras = []
        plato_extras = []
        spmms = []
        if extras_plan:
            extras_num = len(self.extras)
            for i, (name, spmm, data) in enumerate(self.extras):
                prev_extras.append((data[0], 0))
                spmms.append(spmm)
                et, ex, ev = extras_plan[i][1][0]
                assert et == acc_t
                acc_extras.append((ex, ev))
                plato_extras.append((ex, ev))

        plato_t = 0
        int_plan = []
        for i, p in enumerate(plan[1:] + [None]):
            if p:
                next_t, next_x, next__y, next_vx, next_vy, _ = p
                if extras_plan:
                    next_extras = []
                    for j in range(extras_num):
                        try:
                            et, ex, ev = extras_plan[j][1][i + 1]
                        except:
                            print(extras_plan[j][1])
                            print(i, len(extras_plan[j][1]))
                            print(len(plan), len(extras_plan[0][1]))
                            raise
                        assert et == next_t
                        next_extras.append((ex, ev))

            if p is None or (abs(next_vx - acc_vx) + abs(next_vy - acc_vy) > EPS):
                sol_x = self.solve_in_ints(acc_t, plato_t, prev_x, prev_vx, plato_x, plato_vx, 80)
                sol_y = self.solve_in_ints(acc_t, plato_t, prev_y, prev_vy, plato_y, plato_vy, 80)
                cur_step = [sol_x, sol_y]
                prev_x, prev_y, prev_vx, prev_vy = (
                    prev_x + sol_x["accel_x"] + sol_x["plato_x"],
                    prev_y + sol_y["accel_x"] + sol_y["plato_x"],
                    sol_x["plato_v"],
                    sol_y["plato_v"],
                )
                if extras_plan:
                    end_extras = []
                    for j in range(extras_num):
                        sol_e = self.solve_in_ints(
                            acc_t,
                            plato_t,
                            prev_extras[j][0],
                            prev_extras[j][1],
                            plato_extras[j][0],
                            plato_extras[j][1],
                            spmms[j],
                        )
                        end_extras.append(
                            (
                                prev_extras[j][0] + sol_e["accel_x"] + sol_e["plato_x"],
                                sol_e["plato_v"],
                            )
                        )
                        cur_step.append(sol_e)
                    prev_extras = end_extras

                int_plan.append(cur_step)
                if p:
                    acc_t, acc_x, acc_y, acc_vx, acc_vy, _ = p
                    _, plato_x, plato_y, plato_vx, plato_vy, _ = p
                    plato_t = 0
                    if extras_plan:
                        plato_extras = next_extras
                        acc_extras = next_extras
            else:
                plato_t += next_t
                _, plato_x, plato_y, plato_vx, plato_vy, _ = p
                if extras_plan:
                    plato_extras = next_extras

        return int_plan

    def plan(self):
        plan, slowdowns, notes = self.plan_with_slow_down()
        speedup_slowdowns = self.plan_speedup(slowdowns, notes)
        if not self.extras:
            plan, errors, notes, _ = self.plan_path_in_floats(speedup_slowdowns)
            int_plan = self.plan_to_int(plan)
        else:
            plan, errors, notes, plan_extras = self.plan_path_in_floats(
                speedup_slowdowns, with_extras=True
            )
            int_plan = self.plan_to_int(plan, plan_extras)
        return int_plan

    def format(self, plan, apgs=None):
        if apgs is None:
            apgs = {}

        apg_x = apgs.get("X", FakeApg("X"))
        apg_y = apgs.get("Y", FakeApg("Y"))
        apg_z = apgs.get("Z", FakeApg("Z"))

        pr_opt = []

        for sols in plan:
            sol_x = sols[0]
            sol_y = sols[1]

            if sol_x["accel_t"] > 0:
                segs = [
                    ProfileSegment(
                        apg=apg_x, a=sol_x["accel_a"], j=sol_x["accel_j"], jj=sol_x["accel_jj"]
                    ),
                    ProfileSegment(
                        apg=apg_y, a=sol_y["accel_a"], j=sol_y["accel_j"], jj=sol_y["accel_jj"]
                    ),
                ]
                if len(sols) > 2:
                    sol_z = sols[2]
                    segs.append(
                        ProfileSegment(
                            apg=apg_z, a=sol_z["accel_a"], j=sol_z["accel_j"], jj=sol_z["accel_jj"]
                        )
                    )

                pr_opt += [[sol_x["accel_t"], segs]]

            if sol_x["plato_t"] > 0:
                segs = [
                    ProfileSegment(apg=apg_x, v=ir(sol_x["plato_v_int"])),
                    ProfileSegment(apg=apg_y, v=ir(sol_y["plato_v_int"])),
                ]
                if len(sols) > 2:
                    sol_z = sols[2]
                    segs.append(ProfileSegment(apg=apg_z, v=ir(sol_z["plato_v_int"])))

                pr_opt += [[sol_x["plato_t"], segs]]

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


##################################
# More pandas implementation

def make_path(seg):
    path = pd.DataFrame({
        "x": seg[:, 0],
        "y": seg[:, 1],
        "v": seg[:, 2],
        "e": seg[:, 3],
    })

    dx = path["x"] - path["x"].shift(1)
    dy = path["y"] - path["y"].shift(1)
    l = norm([dx, dy], axis=0)
    l[0] = 1.0
    l[len(l) - 1] = 1.0

    path = path[l > 0.01]

    px = path["x"].shift(1)
    py = path["y"].shift(1)
    pe = path["e"].shift(1)

    dx = path["x"] - px
    dy = path["y"] - py
    de = path["e"] - pe

    path["src_idx"] = range(len(dx))

    path["dx"] = dx
    path["dy"] = dy
    path["l"] = norm([dx, dy], axis=0)
    path["de"] = de

    path["px"] = px
    path["py"] = py
    path["pe"] = pe
    path["pv"] = path["v"].shift(1)
    path["pdx"] = path["dx"].shift(1).fillna(0)
    path["pdy"] = path["dy"].shift(1).fillna(0)
    path["pl"] = path["l"].shift(1).fillna(0)
    path["pde"] = path["de"].shift(1).fillna(0)

    path["nx"] = path["x"].shift(-1)
    path["ny"] = path["y"].shift(-1)
    path["ne"] = path["e"].shift(-1)
    path["nv"] = path["v"].shift(-1)
    path["ndx"] = path["dx"].shift(-1)
    path["ndy"] = path["dy"].shift(-1)
    path["nde"] = path["de"].shift(-1)
    path["nl"] = path["l"].shift(-1)

    path["dt"] = path["l"] / path["v"]
    path["t"] = path["dt"].cumsum().shift(1).fillna(0)

    path = path[1:-1]

    path = path.set_index("t")

    slowdowns = pd.DataFrame()
    slowdowns["corner"] = path["v"] * 0.0 + 1.0
    slowdowns["plato"] = path["v"] * 0.0 + 1.0

    return path, slowdowns


max_xa = 1000
max_ya = 1000
max_delta = 0.1


def gen_speeds(path, slowdowns):
    speeds = pd.DataFrame()
    speeds["path"] = path["v"]
    speeds["c_in"] = path["pv"]*slowdowns["corner"]
    speeds["c_out"] = path["v"]*slowdowns["corner"]
    speeds["out"] = path["v"]*(slowdowns["corner"].shift(-1).fillna(0))
    speeds["plato_base"] = numpy.minimum(speeds["c_out"], speeds["out"])
    speeds["plato_delta"] = path["v"] - speeds["plato_base"]
    speeds["plato"] = speeds["plato_base"] + speeds["plato_delta"] * slowdowns["plato"]
    for k in ["c_in", "c_out", "plato", "out"]:
        if k == "c_in":
            xp = "p"
        else:
            xp = ""
        speeds[k + "_x"] = speeds[k] * path[xp + "dx"] / path[xp + "l"]
        speeds[k + "_y"] = speeds[k] * path[xp + "dy"] / path[xp + "l"]
        speeds[k + "_x"][speeds[k] == 0] = 0
        speeds[k + "_y"][speeds[k] == 0] = 0

    max_a_x = numpy.abs(speeds["plato"] * max_xa / speeds["plato_x"].fillna(numpy.inf))
    max_a_y = numpy.abs(speeds["plato"] * max_ya / speeds["plato_y"].fillna(numpy.inf))
    max_a = numpy.minimum(max_a_x, max_a_y)
    speeds["max_a"] = max_a

    return speeds


def process_corner_errors(path, slowdowns):
    speeds = gen_speeds(path, slowdowns)

    cc = pd.DataFrame()
    cc["dvx"] = speeds["c_out_x"] - speeds["c_in_x"]
    cc["dvy"] = speeds["c_out_y"] - speeds["c_in_y"]
    cc["dtx"] = numpy.abs(cc["dvx"] / max_xa)
    cc["dty"] = numpy.abs(cc["dvy"] / max_ya)
    cc["dt"] = numpy.maximum(cc["dtx"], cc["dty"])
    cc["ax"] = (cc["dvx"] / cc["dt"]).fillna(0)
    cc["ay"] = (cc["dvy"] / cc["dt"]).fillna(0)
    cc["mdx"] = cc["ax"] * numpy.square(cc["dt"] / 2) / 2
    cc["mdy"] = cc["ay"] * numpy.square(cc["dt"] / 2) / 2
    cc["mvx"] = (speeds["c_out_x"] + speeds["c_in_x"]) / 2
    cc["mvy"] = (speeds["c_out_y"] + speeds["c_in_y"]) / 2
    cc["md"] = norm(cc[['mdx', 'mdy']].values, axis=1)
    cc["md"][0] = 0

    cc["error_slowdown"] = 1.0 / numpy.sqrt(numpy.maximum(cc["md"] / max_delta, 1.0))

    new_slowdowns = slowdowns.copy()
    new_slowdowns["corner"] = slowdowns["corner"] * cc["error_slowdown"]
    return new_slowdowns, cc


def process_corner_space(path, slowdowns):
    speeds = gen_speeds(path, slowdowns)

    cc = pd.DataFrame()
    cc["dvx"] = speeds["c_out_x"] - speeds["c_in_x"]
    cc["dvy"] = speeds["c_out_y"] - speeds["c_in_y"]
    cc["dtx"] = numpy.abs(cc["dvx"] / max_xa)
    cc["dty"] = numpy.abs(cc["dvy"] / max_ya)
    cc["dt"] = numpy.maximum(cc["dtx"], cc["dty"])
    cc["cdt"] = cc["dt"] / 2

    cc["in_l"] = cc["cdt"] * speeds["c_in"]
    cc["in_dx"] = -cc["cdt"] * speeds["c_in_x"]
    cc["in_dy"] = -cc["cdt"] * speeds["c_in_y"]
    cc["pl"] = path["pl"]
    cc["in_slowdown"] = 1.0 / numpy.sqrt(numpy.maximum(1.0, cc["in_l"] / path["pl"] * 2))
    cc["in_slowdown"][cc["in_l"] == 0] = 1.0
    cc["out_l"] = cc["cdt"] * speeds["c_out"]
    cc["out_dx"] = cc["cdt"] * speeds["c_out_x"]
    cc["out_dy"] = cc["cdt"] * speeds["c_out_y"]
    cc["l"] = path["l"]
    cc["out_slowdown"] = 1.0 / numpy.sqrt(numpy.maximum(1.0, cc["out_l"] / path["l"] * 2))
    cc["out_slowdown"][cc["out_l"] == 0] = 1.0
    cc["slowdown"] = numpy.minimum(cc["in_slowdown"], cc["out_slowdown"])
    new_slowdowns = slowdowns.copy()
    new_slowdowns["corner"] = slowdowns["corner"] * cc["slowdown"]
    return new_slowdowns, cc


def process_plato(path, slowdowns):
    speeds = gen_speeds(path, slowdowns)

    cc = pd.DataFrame()
    # corner in and out
    cc["c_dvx"] = speeds["c_out_x"] - speeds["c_in_x"]
    cc["c_dvy"] = speeds["c_out_y"] - speeds["c_in_y"]
    cc["c_dtx"] = numpy.abs(cc["c_dvx"] / max_xa)
    cc["c_dty"] = numpy.abs(cc["c_dvy"] / max_ya)
    cc["c_dt"] = numpy.maximum(cc["c_dtx"], cc["c_dty"])
    cc["c_cdt"] = cc["c_dt"] / 2
    cc["c_l"] = cc["c_cdt"] * speeds["c_out"]
    cc["c_pl"] = cc["c_cdt"] * speeds["c_in"]

    # next corner in from next step
    cc["o_l"] = cc["c_pl"].shift(-1).fillna(0)

    # skip plato
    nc = pd.DataFrame()

    nc["n_dvx"] = speeds["out_x"] - speeds["c_out_x"]
    nc["n_dvy"] = speeds["out_y"] - speeds["c_out_y"]
    nc["n_dtx"] = numpy.abs(nc["n_dvx"] / max_xa)
    nc["n_dty"] = numpy.abs(nc["n_dvy"] / max_ya)
    nc["n_dt"] = numpy.maximum(nc["n_dtx"], nc["n_dty"])

    nc["n_ax"] = (nc["n_dvx"] / nc["n_dt"]).fillna(0)
    nc["n_ay"] = (nc["n_dvy"] / nc["n_dt"]).fillna(0)

    nc["n_dx"] = nc["n_ax"] * numpy.square(nc["n_dt"]) / 2 + speeds["c_out_x"] * nc["n_dt"]
    nc["n_dy"] = nc["n_ay"] * numpy.square(nc["n_dt"]) / 2 + speeds["c_out_y"] * nc["n_dt"]

    nc["n_l"] = norm(nc[['n_dx', 'n_dy']].values, axis=1)
    nc["n_avail_l"] = path["l"] - cc["c_l"] - cc["o_l"]
    nc["n_k"] = (nc["n_avail_l"] / nc["n_l"]).fillna(1.0).replace([numpy.inf, -numpy.inf], 1.0)

    nc["n_real_dt"] = nc["n_dt"] * nc["n_k"]
    nc["n_real_ax"] = (nc["n_dvx"] / nc["n_real_dt"]).fillna(0)
    nc["n_real_ay"] = (nc["n_dvy"] / nc["n_real_dt"]).fillna(0)

    stable_dt = nc["n_avail_l"] / norm(speeds[['out_x', 'out_y']].values, axis=1)
    nc["n_real_dt"][nc["n_dt"] == 0] = stable_dt[nc["n_dt"] == 0]

    nc["n_dvx_in"] = speeds["plato_x"] - speeds["c_out_x"]
    nc["n_dvy_in"] = speeds["plato_y"] - speeds["c_out_y"]
    nc["n_dvx_out"] = speeds["out_x"] - speeds["plato_x"]
    nc["n_dvy_out"] = speeds["out_y"] - speeds["plato_y"]

    for part, base_speed in [("in", "c_out_"), ("out", "plato_")]:
        nc["n_dtx_" + part] = numpy.abs(nc["n_dvx_" + part] / max_xa)
        nc["n_dty_" + part] = numpy.abs(nc["n_dvy_" + part] / max_ya)
        nc["n_dt_" + part] = numpy.maximum(nc["n_dtx_" + part], nc["n_dty_" + part])
        nc["n_ax_" + part] = (nc["n_dvx_" + part] / nc["n_dt_" + part]).fillna(0)
        nc["n_ay_" + part] = (nc["n_dvy_" + part] / nc["n_dt_" + part]).fillna(0)

        nc["n_dx_" + part] = nc["n_ax_" + part] * numpy.square(nc["n_dt_" + part]) / 2 + speeds[base_speed + "x"] * nc["n_dt_" + part]
        nc["n_dy_" + part] = nc["n_ay_" + part] * numpy.square(nc["n_dt_" + part]) / 2 + speeds[base_speed + "y"] * nc["n_dt_" + part]
        nc["n_l_" + part] = norm(nc[['n_dx_' + part, 'n_dy_' + part]].values, axis=1)
        nc["n_avail_" + part] = (path["l"] - cc["c_l"] - cc["o_l"])/2 - nc["n_l_" + part]

    # summary
    sc = pd.DataFrame()

    sc["l"] = path["l"]
    sc["c_l"] = cc["c_l"]
    sc["o_l"] = cc["o_l"]
    sc["n_l"] = nc["n_l"]
    sc["free_l_n"] = sc["l"] - sc["c_l"] - sc["o_l"] - sc["n_l"]
    sc["slowdown_1"] = 1.0 / numpy.sqrt(numpy.maximum((sc["c_l"] + sc["o_l"] + sc["n_l"]) / sc["l"] * 1.01, 1.0))
    sc["slowdown_2"] = sc["slowdown_1"].shift(1).fillna(1.0)
    sc["slowdown"] = numpy.minimum(sc["slowdown_1"], sc["slowdown_2"])

    new_slowdowns = slowdowns.copy()
    new_slowdowns["corner"] = slowdowns["corner"] * sc["slowdown"]
    stage_ok = (sc["slowdown"] > 0.999).all()
    return new_slowdowns, stage_ok, cc, nc, sc


def build_segments(path, slowdowns):
    final_slowdowns, stage_ok, cc1, nc1, sc1 = process_plato(path, slowdowns)
    ce_slowdowns, ce1 = process_corner_errors(path, slowdowns)
    cs_slowdowns, cs1 = process_corner_space(path, slowdowns)
    speeds = gen_speeds(path, slowdowns)

    start_segments = pd.DataFrame()
    start_segments["x0"] = path["px"] + ce1["mdx"]
    start_segments["y0"] = path["py"] + ce1["mdy"]
    start_segments["vx0"] = ce1["mvx"]
    start_segments["vy0"] = ce1["mvy"]
    start_segments["ax0"] = ce1["ax"]
    start_segments["ay0"] = ce1["ay"]
    start_segments["x1"] = path["px"] + cs1["out_dx"]
    start_segments["y1"] = path["py"] + cs1["out_dy"]
    start_segments["vx1"] = speeds["c_out_x"]
    start_segments["vy1"] = speeds["c_out_y"]
    start_segments["ax1"] = ce1["ax"]
    start_segments["ay1"] = ce1["ay"]
    start_segments["dt"] = ce1["dt"] / 2

    start_segments["idx"] = arange(len(ce1)) * 10 + 1
    start_segments["src_idx"] = path["src_idx"]
    start_segments["src_part"] = norm([cs1["out_dx"], cs1["out_dy"]], axis=0) / path["l"]
    start_segments["seg_type"] = "start"

    start_segments.iloc[0, start_segments.columns.get_loc('x0')] = path.iloc[0]["px"]
    start_segments.iloc[0, start_segments.columns.get_loc('y0')] = path.iloc[0]["py"]
    start_segments.iloc[0, start_segments.columns.get_loc('vx0')] = 0.0
    start_segments.iloc[0, start_segments.columns.get_loc('vy0')] = 0.0
    start_segments.iloc[0, start_segments.columns.get_loc('dt')] = ce1.iloc[0]["dt"]

    end_segments = pd.DataFrame()
    end_segments["x0"] = path["x"] + cs1["in_dx"].shift(-1).fillna(0)
    end_segments["y0"] = path["y"] + cs1["in_dy"].shift(-1).fillna(0)
    end_segments["vx0"] = speeds["c_in_x"].shift(-1).fillna(0)
    end_segments["vy0"] = speeds["c_in_y"].shift(-1).fillna(0)
    end_segments["ax0"] = ce1["ax"].shift(-1).fillna(0)
    end_segments["ay0"] = ce1["ay"].shift(-1).fillna(0)

    end_segments["x1"] = path["x"] + ce1["mdx"].shift(-1).fillna(0)
    end_segments["y1"] = path["y"] + ce1["mdy"].shift(-1).fillna(0)
    end_segments["vx1"] = ce1["mvx"].shift(-1).fillna(0)
    end_segments["vy1"] = ce1["mvy"].shift(-1).fillna(0)
    end_segments["ax1"] = ce1["ax"].shift(-1).fillna(0)
    end_segments["ay1"] = ce1["ay"].shift(-1).fillna(0)
    end_segments["dt"] = ce1["dt"].shift(-1).fillna(0) / 2

    end_segments["idx"] = arange(len(ce1)) * 10 + 9
    end_segments["src_idx"] = path["src_idx"]
    end_segments["src_part"] = norm([cs1["in_dx"].shift(-1).fillna(0), cs1["in_dy"].shift(-1).fillna(0)],
                                              axis=0) / path["l"]
    end_segments["seg_type"] = "end"

    plato_segments = pd.DataFrame()
    plato_segments["x0"] = path["px"] + cs1["out_dx"]
    plato_segments["y0"] = path["py"] + cs1["out_dy"]
    plato_segments["vx0"] = speeds["c_out_x"]
    plato_segments["vy0"] = speeds["c_out_y"]
    plato_segments["ax0"] = nc1["n_real_ax"]
    plato_segments["ay0"] = nc1["n_real_ay"]
    plato_segments["x1"] = path["x"] + cs1["in_dx"].shift(-1).fillna(0)
    plato_segments["y1"] = path["y"] + cs1["in_dy"].shift(-1).fillna(0)
    plato_segments["vx1"] = speeds["c_in_x"].shift(-1).fillna(0)
    plato_segments["vy1"] = speeds["c_in_y"].shift(-1).fillna(0)
    plato_segments["ax1"] = nc1["n_real_ax"]
    plato_segments["ay1"] = nc1["n_real_ay"]
    plato_segments["dt"] = nc1["n_real_dt"]

    plato_segments["idx"] = arange(len(ce1)) * 10 + 5
    plato_segments["src_idx"] = path["src_idx"]
    plato_segments["src_part"] = norm([
        plato_segments["x1"] - plato_segments["x0"],
        plato_segments["y1"] - plato_segments["y0"]
    ], axis=0) / path["l"]

    plato_segments["src_idx"] = path["src_idx"]
    plato_segments["seg_type"] = "plato"

    if 1:
        short_start_segments = start_segments["dt"] < 1e-3
        ok_start_segments = numpy.logical_not(short_start_segments)

        plato_segments.loc[short_start_segments, "x0"] = start_segments["x0"][short_start_segments]
        plato_segments.loc[short_start_segments, "y0"] = start_segments["y0"][short_start_segments]
        plato_segments.loc[short_start_segments, "vx0"] = start_segments["vx0"][short_start_segments]
        plato_segments.loc[short_start_segments, "vy0"] = start_segments["vy0"][short_start_segments]
        plato_segments.loc[short_start_segments, "dt"] = plato_segments["dt"][short_start_segments] + \
                                                         start_segments["dt"][short_start_segments]
        plato_segments.loc[short_start_segments, "src_part"] = plato_segments["src_part"][short_start_segments] + \
                                                               start_segments["src_part"][short_start_segments]

        start_segments = start_segments[ok_start_segments]

        short_end_segments = end_segments["dt"] < 1e-3
        ok_end_segments = numpy.logical_not(short_end_segments)

        plato_segments.loc[short_end_segments, "x1"] = end_segments["x1"][short_end_segments]
        plato_segments.loc[short_end_segments, "y1"] = end_segments["y1"][short_end_segments]
        plato_segments.loc[short_end_segments, "vx1"] = end_segments["vx1"][short_end_segments]
        plato_segments.loc[short_end_segments, "vy1"] = end_segments["vy1"][short_end_segments]
        plato_segments.loc[short_end_segments, "dt"] = plato_segments["dt"][short_end_segments] + end_segments["dt"][
            short_end_segments]
        plato_segments.loc[short_end_segments, "src_part"] = plato_segments["src_part"][short_end_segments] + \
                                                             end_segments["src_part"][short_end_segments]
        end_segments = end_segments[ok_end_segments]

    can_speedup = (cs1["l"] - cs1["in_l"] - cs1["out_l"]) > 1
    can_speedup_fully = (cs1["l"] - nc1["n_l_in"] - nc1["n_l_out"] - cs1["in_l"] - cs1["out_l"]) > 1

    cannot_speedup = ~ can_speedup
    can_speedup[can_speedup_fully] = False
    cannot_speedup[can_speedup_fully] = False

    short_plato_segments = plato_segments[cannot_speedup].copy()
    short_plato_segments["seg_type"] = "short_plato"

    middle_plato_segments = plato_segments[can_speedup].copy()
    middle_plato_segments["seg_type"] = "middle_plato"

    lps = plato_segments[can_speedup_fully].copy()
    lp_nc = nc1[can_speedup_fully]
    lp_path = path[can_speedup_fully]
    lp_speeds = speeds[can_speedup_fully]
    lps["x2"] = lps["x0"] + lp_nc["n_dx_in"]
    lps["y2"] = lps["y0"] + lp_nc["n_dy_in"]
    lps["x3"] = lps["x1"] - lp_nc["n_dx_out"]
    lps["y3"] = lps["y1"] - lp_nc["n_dy_out"]

    lps_in = pd.DataFrame()
    lps_in["x0"] = lps["x0"]
    lps_in["y0"] = lps["y0"]
    lps_in["vx0"] = lps["vx0"]
    lps_in["vy0"] = lps["vy0"]
    lps_in["ax0"] = lp_nc["n_ax_in"]
    lps_in["ay0"] = lp_nc["n_ay_in"]
    lps_in["x1"] = lps["x2"]
    lps_in["y1"] = lps["y2"]
    lps_in["vx1"] = lp_speeds["plato_x"]
    lps_in["vy1"] = lp_speeds["plato_y"]
    lps_in["ax1"] = lp_nc["n_ax_in"]
    lps_in["ay1"] = lp_nc["n_ay_in"]
    lps_in["dt"] = lp_nc["n_dt_in"]

    lps_in["src_idx"] = lps["src_idx"]
    lps_in["src_part"] = norm([
        lps_in["x1"] - lps_in["x0"],
        lps_in["y1"] - lps_in["y0"]
    ], axis=0) / lp_path["l"]

    lps_in["idx"] = lps["idx"] - 1
    lps_in["seg_type"] = "long_plato_in"

    lps_main = pd.DataFrame()
    lps_main["x0"] = lps["x2"]
    lps_main["y0"] = lps["y2"]
    lps_main["vx0"] = lp_speeds["plato_x"]
    lps_main["vy0"] = lp_speeds["plato_y"]
    lps_main["ax0"] = 0
    lps_main["ay0"] = 0
    lps_main["x1"] = lps["x3"]
    lps_main["y1"] = lps["y3"]
    lps_main["vx1"] = lp_speeds["plato_x"]
    lps_main["vy1"] = lp_speeds["plato_y"]
    lps_main["ax1"] = 0
    lps_main["ay1"] = 0

    lps_main["dt"] = norm([
        lps_main["x1"] - lps_main["x0"],
        lps_main["y1"] - lps_main["y0"]
    ], axis=0) / lp_speeds["plato"]

    lps_main["src_idx"] = lps["src_idx"]
    lps_main["src_part"] = norm([
        lps_main["x1"] - lps_main["x0"],
        lps_main["y1"] - lps_main["y0"]
    ], axis=0) / lp_path["l"]

    lps_main["idx"] = lps["idx"]
    lps_main["seg_type"] = "long_plato_main"

    lps_out = pd.DataFrame()
    lps_out["x0"] = lps["x3"]
    lps_out["y0"] = lps["y3"]
    lps_out["vx0"] = lp_speeds["plato_x"]
    lps_out["vy0"] = lp_speeds["plato_y"]
    lps_out["ax0"] = lp_nc["n_ax_out"]
    lps_out["ay0"] = lp_nc["n_ay_out"]
    lps_out["x1"] = lps["x1"]
    lps_out["y1"] = lps["y1"]
    lps_out["vx1"] = lps["vx1"]
    lps_out["vy1"] = lps["vy1"]
    lps_out["ax1"] = lp_nc["n_ax_out"]
    lps_out["ay1"] = lp_nc["n_ay_out"]
    lps_out["dt"] = lp_nc["n_dt_out"]

    lps_out["src_idx"] = lps["src_idx"]
    lps_out["src_part"] = norm([
        lps_out["x1"] - lps_out["x0"],
        lps_out["y1"] - lps_out["y0"]
    ], axis=0) / lp_path["l"]
    lps_out["idx"] = lps["idx"] + 1
    lps_out["seg_type"] = "long_plato_out"

    all_segments = start_segments.append(short_plato_segments, sort=False)
    all_segments = all_segments.append(middle_plato_segments, sort=False)
    all_segments = all_segments.append(lps_in[lps_in["dt"] > 0], sort=False)
    all_segments = all_segments.append(lps_main, sort=False)
    all_segments = all_segments.append(lps_out[lps_out["dt"] > 0], sort=False)
    all_segments = all_segments.append(end_segments, sort=False)

    all_segments = all_segments.set_index('idx').sort_index()
    all_segments["t"] = numpy.cumsum(all_segments["dt"])

    ext_path = pd.DataFrame()
    ext_path["src_idx"] = path["src_idx"]
    ext_path["src_de"] = path["de"]
    all_segments = all_segments.merge(ext_path, on='src_idx')
    all_segments["de"] = all_segments["src_de"] * all_segments["src_part"]

    return all_segments


def format_segments(all_segments, apgs=None, acc_step=1000):
    if apgs is None:
        apgs = {}

    apg_states = {}

    apg_x = apgs.get("X", FakeApg("X"))
    apg_y = apgs.get("Y", FakeApg("Y"))
    apg_z = apgs.get("Z", FakeApg("Z"))

    v_step = 50000000
    v_mult = v_step / acc_step
    spm = 80
    spme = 837

    pr_opt = []
    first_row = all_segments.iloc[0]
    last_x = first_row["x0"]
    last_y = first_row["y0"]
    last_vx = first_row["vx0"]
    last_vy = first_row["vy0"]
    assert last_vx == 0
    assert last_vy == 0
    segs = [
        ProfileSegment(
            apg=apg_x, x=last_x * spm, v=0, a=0
        ),
        ProfileSegment(
            apg=apg_y, x=last_y * spm, v=0, a=0
        ),
    ]

    sub_profile = [[5, segs]]
    pr_opt += sub_profile

    emulate(sub_profile, apg_states=apg_states, accel_step=50000000 / acc_step)
    print(apg_states["X"], apg_states["Y"])

    for index, up_row in all_segments.iterrows():
        if 0:
            if index > 55:
                print("last_x:", last_x, "last_y:", last_y)
                print("last_vx:", last_vx, "last_vy:", last_vy)
                break

        print("index:", index, up_row["seg_type"])

        if up_row["dt"] < 0.2:
            rows = [up_row]
        else:
            splits = int(up_row["dt"] / 0.15)
            print("long segment, split up", splits)
            tx0 = up_row["x0"]
            ty0 = up_row["y0"]
            tx1 = up_row["x1"]
            ty1 = up_row["y1"]
            tvx0 = up_row["vx0"]
            tvy0 = up_row["vy0"]
            tvx1 = up_row["vx1"]
            tvy1 = up_row["vy1"]
            lx1 = tx0
            ly1 = ty0
            lvx1 = tvx0
            lvy1 = tvy0
            dvx = (tvx1 - tvx0) / splits
            dvy = (tvy1 - tvy0) / splits
            dt = up_row["dt"] / splits
            rows = []
            for i in range(splits):
                cvx1 = lvx1 + dvx
                cvy1 = lvy1 + dvy
                cx1 = lx1 + (lvx1 + dvx / 2) * dt
                cy1 = ly1 + (lvy1 + dvy / 2) * dt
                if i == splits - 1:
                    cvx1 = tvx1
                    cvy1 = tvy1
                    cx1 = tx1
                    cy1 = ty1
                rows.append(
                    {
                        "x0": lx1,
                        "y0": ly1,
                        "x1": cx1,
                        "y1": cy1,
                        "vx0": lvx1,
                        "vy0": lvy1,
                        "vx1": cvx1,
                        "vy1": cvy1,
                        "dt": dt,
                        "de": 0
                    }
                )
                lx1 = cx1
                ly1 = cy1
                lvx1 = cvx1
                lvy1 = cvy1

        for row in rows:
            next_x = row["x1"]
            next_y = row["y1"]
            next_vx = row["vx1"]
            next_vy = row["vy1"]
            de = row["de"]

            dx = next_x - last_x
            dy = next_y - last_y
            dvx = next_vx - last_vx
            dvy = next_vy - last_vy
            avg_vx = last_vx + 0.5 * dvx
            avg_vy = last_vy + 0.5 * dvy

            print("x:", last_x, row["x0"])
            print("y:", last_y, row["y0"])
            print("vx:", last_vx, row["vx0"])
            print("vy:", last_vy, row["vy0"])
            print("dx:", dx)
            print("dy:", dy)
            print("dvx:", dvx)
            print("dvy:", dvy)

            dt = row["dt"]
            int_dt = around(dt * acc_step)

            if int_dt == 0:
                int_dt = 1

            print("int_dt:", int_dt)

            int_vx0 = around(last_vx * 2 ** 32 * spm / v_step)
            int_vy0 = around(last_vy * 2 ** 32 * spm / v_step)
            int_vx1 = around(next_vx * 2 ** 32 * spm / v_step)
            int_vy1 = around(next_vy * 2 ** 32 * spm / v_step)
            int_ax = around((int_vx1 - int_vx0) / int_dt * 65536)
            int_ay = around((int_vy1 - int_vy0) / int_dt * 65536)
            print("int_vx1:", int_vx1, "int_vy1:", int_vy1)

            real_dx = int_x(int_dt, int_vx0 * 65536, int_ax, 0, 0) / 65536 * v_mult
            real_dy = int_x(int_dt, int_vy0 * 65536, int_ay, 0, 0) / 65536 * v_mult
            x_error = dx * 2.0 ** 32 * spm - real_dx

            int_jx = around(-12 * x_error / int_dt / int_dt / int_dt * 65536 / v_mult)
            int_ax = around(int_ax - int_jx * int_dt / 2)
            print("x_error:", x_error / 2.0 ** 32 / spm, "int_jx:", int_jx, "int_ax:", int_ax)

            y_error = dy * 2.0 ** 32 * spm - real_dy
            int_jy = around(-12 * y_error / int_dt / int_dt / int_dt * 65536 / v_mult)
            int_ay = around(int_ay - int_jy * int_dt / 2)
            print("y_error:", y_error / 2.0 ** 32 / spm, "int_jy:", int_jy, "int_ay:", int_ay)

            segs = [
                ProfileSegment(
                    apg=apg_x, a=int(int_ax), j=int(int_jx)
                ),
                ProfileSegment(
                    apg=apg_y, a=int(int_ay), j=int(int_jy)
                ),
            ]

            sub_profile = [[int(int_dt), segs]]
            pr_opt += sub_profile

            res = emulate(sub_profile, apg_states=apg_states, accel_step=50000000 / acc_step)
            res["xv"] = res["X_v"] * 65536 / 2 ** 32 / 80 * 50000000
            res["yv"] = res["Y_v"] * 65536 / 2 ** 32 / 80 * 50000000

            print("ApgStates:", apg_states["X"].x / 2 ** 32 / spm, apg_states["Y"].x / 2 ** 32 / spm)
            print("        V:", apg_states["X"].v / 2 ** 32 / spm * v_step, apg_states["Y"].v / 2 ** 32 / spm * v_step)
            print("   max_xv:", res["xv"].max(), res["xv"].min())
            print("   max_yv:", res["yv"].max(), res["yv"].min())

            last_x = apg_states["X"].x / 2 ** 32 / spm
            last_y = apg_states["Y"].x / 2 ** 32 / spm
            last_vx = apg_states["X"].v / 2 ** 32 / spm * v_step
            last_vy = apg_states["Y"].v / 2 ** 32 / spm * v_step

            print("final x_error:", last_x - next_x)
            print("final y_error:", last_y - next_y)
            print("final vx_error:", last_vx - next_vx)
            print("final vy_error:", last_vy - next_vy)

            if 1:
                assert res["xv"].max() < 300
                assert res["xv"].min() > -300
                assert res["yv"].max() < 300
                assert res["yv"].min() > -300

                assert abs(last_x - next_x) < 0.1
                assert abs(last_y - next_y) < 0.1
                assert abs(last_vx - next_vx) < 5
                assert abs(last_vy - next_vy) < 5

            if 0:
                if abs(last_vx) < 0.001:
                    last_vx = 0
                if abs(last_vy) < 0.001:
                    last_vy = 0

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
