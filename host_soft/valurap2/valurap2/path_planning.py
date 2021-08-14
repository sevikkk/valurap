import logging
import math
import os
import pickle
import sys
import time
from math import sqrt, ceil, pow, hypot, copysign

import numpy as np
import pandas as pd
from numpy.linalg import norm

try:
    from scipy.interpolate import interp1d
except ImportError:
    interp1d = None

try:
    from splipy import curve_factory
except ImportError:
    curve_factory = None

from . import gcode
from .profile import ProfileSegment
from .emulate import emulate
import logging

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


class PathPlanner:
    max_xa = 1000
    max_ya = 1000
    max_ea = 1000
    max_za = 30

    max_xv = 1000
    max_yv = 1000
    max_ev = 1000
    max_zv = 20

    min_seg = 0.3
    max_delta = 0.1
    max_delta_e = 0.01
    max_seg = 30.0
    max_seg_num = 5
    min_plato_len = 1
    skip_plato_len = 0.09
    assert min_seg > skip_plato_len * 3
    spm = 80
    spme1 = 837
    spme2 = 837/2
    spmz = 1600
    accel_step = 1000
    step_bit = 48
    max_a_extra = 1.2
    max_a_extra2 = 1.5
    emu_in_loop = True
    espeed_by_de_corner = True
    espeed_by_de_accel = False
    espeed_by_de_plato = False
    espeed_by_de_decel = True

    delta_err = 1.0
    delta_v_err = 1.0
    delta_e_err = 1.0
    delta_ve_err = 1.0

    home_spms = [spm, spm, spm, spm, spmz, spmz, spmz, spmz]
    print_spms = [spm, spm, spm, spmz, spme1, spme2, 1.0, 1.0]
    spms = print_spms

    def __init__(self, mode=None):
        self.apg_states = {}
        self.emu_t = 0
        self.last_x = None
        self.last_y = None
        self.last_z = None
        self.last_extruder = None
        self.mode = None
        if mode:
            self.set_mode(mode)
        self.max_deltas = {}
        self.msg_buf = []
        self.msg_print = False

    def set_mode(self, mode):
        if mode == "print":
            self.spms = self.print_spms
        elif mode == "home":
            self.spms = self.home_spms
        else:
            raise RuntimeError("Wrong mode: {}".format(mode))
        self.mode = mode
        self.init_apgs()

    def init_apgs(self, reset=False):
        if reset or not self.apg_states:
            self.apg_states = {}
            emulate(
                [],
                apg_states=self.apg_states,
                accel_step=self.accel_step,
                spms=self.spms,
                step_bit=self.step_bit
            )

    def make_path(self, gcode_path, speed_k=1.0):
        filtered_path = self.filter_path(gcode_path)
        if filtered_path is None:
            return None, None
        path = self.path_from_gcode(filtered_path, speed_k)
        path = self.generate_computed_fields(path)
        slowdowns = self.generate_initial_slowdowns(path)
        return path, slowdowns

    def generate_initial_slowdowns(self, path):
        slowdowns = pd.DataFrame()
        slowdowns["corner"] = path["v"] * 0.0 + 1.0
        slowdowns["plato"] = path["v"] * 0.0 + 1.0
        return slowdowns

    def generate_computed_fields(self, path):
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
        path["dt"] = (path["l"] / path["v"]).fillna(0)
        path["t"] = path["dt"].cumsum().shift(1).fillna(0)
        path = path[1:].copy()
        path["idx"] = range(len(path))
        path = path.set_index("idx")
        return path

    def filter_path(self, path):
        #print("input path:", path)
        last_x, last_y, last_v, last_e, last_line = path[0]
        total_l = 0
        total_dt = 0
        new_path = [path[0]]
        t_l = 0

        sn = len(path)
        for i in range(1, sn - 1):
            (px, py, pv, pe, pline) = path[i - 1]
            (x, y, v, e, line) = path[i]
            (nx, ny, nv, ne, nline) = path[i + 1]

            dx = x - px
            dy = y - py
            l = hypot(dx, dy)

            if v > 0:
                dt = l / v
            else:
                dt = 0

            total_l += l
            total_dt += dt

            t_dx = x - last_x
            t_dy = y - last_y
            t_de = e - last_e
            t_l = hypot(t_dx, t_dy)

            if t_l < self.min_seg:
                continue

            ndx = nx - x
            ndy = ny - y
            nl = hypot(ndx, ndy)

            if (i !=  sn - 2) and nl < self.min_seg:
                continue

            t_v = total_l / total_dt

            if t_l > self.max_seg:
                splits = min(self.max_seg_num, ceil(t_l / self.max_seg))
                for i in range(1, splits):
                    new_path.append(
                        (
                            last_x + t_dx * i / splits,
                            last_y + t_dy * i / splits,
                            t_v,
                            last_e + t_de * i / splits,
                            line,
                        )
                    )

            new_path.append((x, y, t_v, e, line))
            last_x, last_y, last_v, last_e, last_line = new_path[-1]
            total_l = 0
            total_dt = 0

        if total_l == 0:
            new_path.append((last_x, last_y, 0, last_e, last_line))
            #print("new path:", new_path)
            return new_path

        if len(new_path) > 1:
            print("last sub-segment final len is to small:", t_l, total_l)
            assert t_l < self.min_seg
            assert total_l < self.min_seg * 10

            prev_last_seg = new_path[-1]
            new_path = new_path[:-1]

            new_path.append((last_x, last_y, prev_last_seg[2], last_e, last_line))
            new_path.append((last_x, last_y, 0, last_e, last_line))
            print("new path:", new_path)
            return new_path

        print("segment len to small:", t_l, total_l, new_path)
        assert t_l < self.min_seg
        assert total_l < self.min_seg * 10

        return None

    def path_from_gcode(self, gcode_path, speed_k):
        seg = np.array(gcode_path)
        path = pd.DataFrame(
            {
                "x": seg[:, 0],
                "y": seg[:, 1],
                "v": seg[:, 2],
                "e": seg[:, 3] - seg[0, 3],
                "line": np.int32(seg[:, 4]),
            }
        )
        path["v"] *= speed_k
        return path

    def gen_speeds(self, path, slowdowns):
        speeds = pd.DataFrame()
        speeds["path"] = path["v"]
        speeds["v_to_ve"] = (path["de"] / path["dt"] / path["v"]).fillna(0)

        speeds["entry"] = path["v"] * slowdowns["corner"]
        speeds["exit"] = path["v"] * (slowdowns["corner"].shift(-1).fillna(0))

        speeds["plato_base"] = np.minimum(speeds["entry"], speeds["exit"])
        speeds["plato_delta"] = speeds["path"] - speeds["plato_base"]
        speeds["plato"] = speeds["plato_base"] + speeds["plato_delta"] * slowdowns["plato"]

        speeds["unit_x"] = (path["dx"] / path["l"]).fillna(1.0)
        speeds["unit_y"] = (path["dy"] / path["l"]).fillna(0.0)
        speeds["unit_e"] = (path["de"] / path["l"]).fillna(0.0)

        for k in ["entry", "exit", "plato", "path"]:
            speeds[k + "_x"] = speeds[k] * speeds["unit_x"]
            speeds[k + "_y"] = speeds[k] * speeds["unit_y"]

        max_a_x = np.abs(self.max_xa / speeds["unit_x"].fillna(np.inf))
        max_a_y = np.abs(self.max_ya / speeds["unit_y"].fillna(np.inf))
        max_a = np.minimum(max_a_x, max_a_y)
        speeds["max_a"] = max_a  # max accell for not componentized move

        speeds["p_unit_x"] = speeds["unit_x"].shift(1).fillna(1.0)
        speeds["p_unit_y"] = speeds["unit_y"].shift(1).fillna(1.0)

        speeds["p_exit"] = speeds["exit"].shift(1).fillna(0)
        speeds["p_exit_x"] = speeds["exit_x"].shift(1).fillna(0)
        speeds["p_exit_y"] = speeds["exit_y"].shift(1).fillna(0)

        return speeds

    def process_corner_errors(self, path, slowdowns):
        speeds = self.gen_speeds(path, slowdowns)

        cc = pd.DataFrame()
        cc["dvx"] = speeds["entry_x"] - speeds["p_exit_x"]
        cc["dvy"] = speeds["entry_y"] - speeds["p_exit_y"]

        cc["dtx"] = np.abs(cc["dvx"] / self.max_xa)
        cc["dty"] = np.abs(cc["dvy"] / self.max_ya)
        cc["dt"] = np.maximum(cc["dtx"], cc["dty"])

        cc["entry_dt"] = cc["dt"] / 2
        cc["entry_dt"][0] = cc["dt"][0]

        last_i = len(cc["dvx"]) - 1

        cc["exit_dt"] = cc["entry_dt"].shift(-1).fillna(0)
        cc["exit_dt"][last_i - 1] += cc["entry_dt"][last_i]
        cc["entry_dt"][last_i] = 0

        cc["l_entry"] = cc["entry_dt"] * speeds["entry"]
        cc["l_entry"][0] = cc["entry_dt"][0] * speeds["entry"][0] / 2
        cc["l_exit"] = cc["exit_dt"] * speeds["exit"]
        cc["l_exit"][last_i - 1] = cc["exit_dt"][last_i - 1] * speeds["exit"][last_i - 1] / 2
        cc["l_free"] = path["l"] - cc["l_entry"] - cc["l_exit"]

        cc["entry_ax"] = (cc["dvx"] / cc["dt"]).fillna(0)
        cc["entry_ay"] = (cc["dvy"] / cc["dt"]).fillna(0)
        cc["exit_ax"] = cc["entry_ax"].shift(-1).fillna(0)
        cc["exit_ay"] = cc["entry_ay"].shift(-1).fillna(0)

        cc["mdx"] = cc["entry_ax"] * np.square(cc["entry_dt"]) / 2
        cc["mdy"] = cc["entry_ay"] * np.square(cc["entry_dt"]) / 2
        cc["mdx"][0] = 0
        cc["mdy"][0] = 0
        cc["mvx"] = speeds["entry_x"] - cc["entry_ax"] * cc["entry_dt"]
        cc["mvy"] = speeds["entry_y"] - cc["entry_ay"] * cc["entry_dt"]
        cc["md"] = norm(cc[["mdx", "mdy"]].values, axis=1)

        cc["error_slowdown"] = 1.0 / np.sqrt(np.maximum(cc["md"] / self.max_delta, 1.0))
        cc["error_slowdown"][0] = 1.0
        cc["error_slowdown"][last_i] = 1.0

        cc["entry_slowdown"] = 1.0 / np.sqrt(
            np.maximum(1.0, cc["l_entry"] / (path["l"] - self.skip_plato_len * 3) * 2.0)
        ).fillna(1.0)
        cc["prev_exit_slowdown"] = 1.0 / np.sqrt(
            np.maximum(1.0, cc["l_exit"] / (path["l"] - self.skip_plato_len * 3) * 2.0)
        ).shift(1).fillna(1.0)
        cc["slowdown"] = np.minimum(
            np.minimum(cc["entry_slowdown"], cc["prev_exit_slowdown"]), cc["error_slowdown"]
        )

        updated = np.sum(cc["slowdown"] < 0.9999)
        if updated > 0:
            print("cc updated", updated)

        new_slowdowns = slowdowns.copy()
        new_slowdowns["corner"] = slowdowns["corner"] * cc["slowdown"]
        return new_slowdowns, updated, cc

    def reverse_pass(self, path, slowdowns):
        speeds = self.gen_speeds(path, slowdowns)
        _, _, cc = self.process_corner_errors(path, slowdowns)

        new_slowdowns = slowdowns.copy()
        last_i = len(path) - 2  # skip the very last segment as it is a noop

        s_speeds = speeds.iloc[last_i]
        s_cc = cc.iloc[last_i]

        corrected_exit_speed = s_speeds["exit"]  # preload with unmodified exit values
        corrected_l_exit = s_cc["l_exit"]

        updated = 0
        for i in range(last_i, -1, -1):
            s_speeds = speeds.iloc[i]
            s_cc = cc.iloc[i]
            s_path = path.iloc[i]
            if i > 0:
                ns_speeds = speeds.iloc[i - 1]
                ns_cc = cc.iloc[i - 1]
                next_exit_speed = ns_speeds["exit"]
                next_l_exit = ns_cc["l_exit"]
            else:
                next_exit_speed = np.nan
                next_l_exit = np.nan

            entry_speed = s_speeds["entry"]
            max_a = s_speeds["max_a"]
            l_entry = s_cc["l_entry"]
            l_total = s_path["l"]
            l_free = l_total - l_entry - corrected_l_exit
            cur_dt = abs((corrected_exit_speed - entry_speed) / max_a)
            cur_plato_min = (corrected_exit_speed + entry_speed) / 2 * cur_dt

            skip = False

            if l_free * 0.99 - cur_plato_min > self.skip_plato_len * 2:
                #print("no correction needed", i, cur_plato_min, l_free)
                skip = True
            elif entry_speed < corrected_exit_speed:
                #print("accelerating segment, skipping", i, entry_speed, corrected_exit_speed)
                skip = True

            if skip:
                corrected_exit_speed = next_exit_speed
                corrected_l_exit = next_l_exit
                continue

            l_target = l_total - corrected_l_exit - self.skip_plato_len * 3
            assert l_target > 0

            # Solved by Maxima:
            # eq: [
            #     t = -(v_exit - v_enter * k) / a_max,
            #     l_plato = t * (v_exit + v_enter * k) / 2,
            #     l_new = l_orig * k * k,
            #     l = l_new + l_plato
            # ];
            # solve(eq,[t, l_new, l_plato, k]);
            #
            # k=sqrt((v_enter^2+2*a_max*l_orig)*v_exit^2+2*a_max*l*v_enter^2+4*a_max^2*l*l_orig)/(v_enter^2+2*a_max*l_orig)]]

            kk = (
                (entry_speed ** 2 + 2 * max_a * l_entry) * corrected_exit_speed ** 2
                + 2 * max_a * l_target * entry_speed ** 2
                + 4 * max_a ** 2 * l_target * l_entry
            )
            assert kk > 0
            k = sqrt(kk) / (entry_speed ** 2 + 2 * max_a * l_entry)

            #print("Calculated k:", k)

            if k < 0.999999:
                updated += 1
                k *= 0.98
            else:
                k = 1.0

            if entry_speed * k < corrected_exit_speed:
                k = corrected_exit_speed / entry_speed
                #print("segment tries to reverse, capping", k)

            corr_dt = abs((corrected_exit_speed - entry_speed * k) / max_a)
            corr_plato_min = (corrected_exit_speed + entry_speed * k) / 2 * corr_dt
            corr_free = l_total - l_entry * k * k  - corrected_l_exit - corr_plato_min

            #print("{}: correction results: total: {} free: {}: new free: {} target: {} final: {}".format(i, l_total, l_free, corr_free, l_target, corr_plato_min + l_entry * k * k))

            corrected_exit_speed = next_exit_speed * k
            corrected_l_exit = next_l_exit * k * k
            new_slowdowns["corner"].iloc[i] = slowdowns["corner"].iloc[i] * k

        if updated > 0:
            print("rp updated:", updated)

        return new_slowdowns, updated

    def forward_pass(self, path, slowdowns):
        speeds = self.gen_speeds(path, slowdowns)
        _, _, cc = self.process_corner_errors(path, slowdowns)

        new_slowdowns = slowdowns.copy()

        s_speeds = speeds.iloc[0]
        s_cc = cc.iloc[0]

        corrected_entry_speed = s_speeds["entry"]  # preload with unmodified exit values
        corrected_l_entry = s_cc["l_entry"]
        last_i = len(path) - 1

        updated = 0
        for i in range(0, last_i):
            s_speeds = speeds.iloc[i]
            s_cc = cc.iloc[i]
            s_path = path.iloc[i]
            if i < last_i:
                ns_speeds = speeds.iloc[i + 1]
                ns_cc = cc.iloc[i + 1]
                ns_path = path.iloc[i + 1]
                next_entry_speed = ns_speeds["entry"]
                next_l_entry = ns_cc["l_entry"]
                next_l_total = ns_path["l"]
                if next_l_total < next_l_entry:
                    print("next_l_total: ", next_l_total, next_l_entry, i, ns_path.line)
                    print(path[["line", "px", "py", "x", "y", "v", "de", "l"]])
                    print(slowdowns)
                    print(speeds[["path", "entry", "exit", "plato", "p_exit"]])
                    print(cc[["dvx", "dvy", "entry_dt", "exit_dt", "l_entry", "l_exit", "l_free", "entry_slowdown", "prev_exit_slowdown"]])
                assert next_l_total >= next_l_entry
            else:
                next_entry_speed = np.nan
                next_l_entry = np.nan

            exit_speed = s_speeds["exit"]
            max_a = s_speeds["max_a"]
            l_exit = s_cc["l_exit"]
            l_total = s_path["l"]
            l_free = l_total - l_exit - corrected_l_entry
            cur_dt = abs((corrected_entry_speed - exit_speed) / max_a)
            cur_plato_min = (corrected_entry_speed + exit_speed) / 2 * cur_dt

            skip = False

            if l_free * 0.99 - cur_plato_min > self.skip_plato_len * 2:
                #print("no correction needed", i, cur_plato_min, l_free)
                skip = True
            elif exit_speed < corrected_entry_speed:
                #print("decelerating segment, skipping", i, corrected_entry_speed, exit_speed)
                skip = True

            if skip:
                corrected_entry_speed = next_entry_speed
                corrected_l_entry = next_l_entry
                continue

            l_target = l_total - corrected_l_entry - self.skip_plato_len * 3
            assert l_target > 0

            # Solved by Maxima:
            # eq: [
            #     t = (v_exit * k  - v_enter) / a_max,
            #     l_plato = t * (v_exit * k + v_enter) / 2,
            #     l_new = l_orig * k * k,
            #     l = l_new + l_plato
            # ];
            # solve(eq,[t, l_new, l_plato, k]);
            #
            # k=sqrt((v_enter^2+2*a_max*l)*v_exit^2+2*a_max*l_orig*v_enter^2+4*a_max^2*l*l_orig)/(v_exit^2+2*a_max*l_orig)

            kk = (
                (corrected_entry_speed ** 2 + 2 * max_a * l_target) * exit_speed ** 2
                + 2 * max_a * l_exit * corrected_entry_speed ** 2
                + 4 * max_a ** 2 * l_target * l_exit
            )
            assert kk > 0
            k = sqrt(kk) / (exit_speed ** 2 + 2 * max_a * l_exit)

            #print("Calculated k:", k)

            if k < 0.999999:
                updated += 1
                k *= 0.98
            else:
                k = 1.0

            if exit_speed * k < corrected_entry_speed:
                k = corrected_entry_speed / exit_speed
                #print("segment tries to reverse, capping", k)

            corr_dt = abs((corrected_entry_speed - exit_speed * k) / max_a)
            corr_plato_min = (corrected_entry_speed + exit_speed * k) / 2 * corr_dt
            corr_free = l_total - l_exit * k * k  - corrected_l_entry - corr_plato_min

            #print("{}: correction results: total: {} free: {}: new free: {} target: {} final: {}".format(i, l_total, l_free, corr_free, l_target, corr_plato_min + l_exit * k * k))

            corrected_entry_speed = next_entry_speed * k
            corrected_l_entry = next_l_entry * k * k
            new_slowdowns["corner"].iloc[i + 1] = slowdowns["corner"].iloc[i + 1] * k

        if updated > 0:
            print("fp updated:", updated)

        return new_slowdowns, updated


    def dp(self, *args):
        self.msg_buf.append(args)

    def dp_force(self, *args):
        self.msg_buf.append(args)
        self.msg_print = True

    def print_msg_buf(self):
        if self.msg_print:
            for k in self.msg_buf:
                print(*k)

        self.msg_buf = []
        self.msg_print = False

    def gen_segments_float(self, path, slowdowns, extruder=1, do_reset=True):
        self.init_apgs()
        if extruder == 1:
            apg_map = {
                "X": 0,
                "Y": 2,
                "Z": 3,
                "E": 4
            }
        else:
            apg_map = {
                "X": 1,
                "Y": 2,
                "Z": 3,
                "E": 5
            }

        self.max_deltas = {
            "dx": 0,
            "dy": 0,
            "de": 0,
            "dvx": 0,
            "dvy": 0,
            "dve": 0,
            "ax": 0,
            "ay": 0,
            "ae": 0,
        }

        self.apg_x = apg_map["X"]
        self.apg_x_s = self.apg_states[self.apg_x]
        self.apg_y = apg_map["Y"]
        self.apg_y_s = self.apg_states[self.apg_y]
        self.apg_e = apg_map["E"]
        self.apg_e_s = self.apg_states[self.apg_e]

        speeds = self.gen_speeds(path, slowdowns)
        _, _, cc = self.process_corner_errors(path, slowdowns)

        plato = pd.DataFrame()
        plato["start_x"] = path["px"] + speeds["unit_x"] * cc["l_entry"]
        plato["start_y"] = path["py"] + speeds["unit_y"] * cc["l_entry"]
        plato["start_e"] = path["pe"] + speeds["unit_e"] * cc["l_entry"]
        plato["start_vx"] = speeds["entry_x"]
        plato["start_vy"] = speeds["entry_y"]
        plato["start_v"] = speeds["entry"]
        plato["top_vx"] = speeds["plato_x"]
        plato["top_vy"] = speeds["plato_y"]
        plato["top_v"] = speeds["plato"]
        plato["end_x"] = path["x"] - speeds["unit_x"] * cc["l_exit"]
        plato["end_y"] = path["y"] - speeds["unit_y"] * cc["l_exit"]
        plato["end_e"] = path["e"] - speeds["unit_e"] * cc["l_exit"]
        plato["end_vx"] = speeds["exit_x"]
        plato["end_vy"] = speeds["exit_y"]
        plato["end_v"] = speeds["exit"]

        emu_in_loop = self.emu_in_loop

        segments = []
        profile = []

        first_seg = path.iloc[0]

        last_vx = 0
        last_vy = 0
        last_v = 0.0
        last_ve = 0.0

        last_x = first_seg["px"]
        last_y = first_seg["py"]
        last_e = first_seg["pe"]

        if emu_in_loop:
            segs = []
            if do_reset:
                segs.extend([
                    ProfileSegment(apg=self.apg_x, x=int(last_x / self.apg_x_s.x_k), v=0, a=0),
                    ProfileSegment(apg=self.apg_y, x=int(last_y / self.apg_y_s.x_k), v=0, a=0),
                ])
            segs.append(ProfileSegment(apg=self.apg_e, x=int(last_e / self.apg_e_s.x_k), v=0, a=0))
            sub_profile = [[5, segs]]
            emulate(
                sub_profile,
                apg_states=self.apg_states,
                accel_step=self.accel_step,
                no_tracking=True,
            )
            profile.extend(sub_profile)
            self.emu_t += 5

            last_x_n = self.apg_x_s.to_floats()["x"]
            last_y_n = self.apg_y_s.to_floats()["x"]

            print("Restarting, deltas:", last_x - last_x_n, last_y - last_y_n)
            print("            Speeds:", self.apg_x_s.v_eff, self.apg_y_s.v_eff)
            last_x = last_x_n
            last_y = last_y_n

        last_i = len(path) - 1
        for i in range(0, last_i + 1):
            s_speeds = speeds.iloc[i]
            s_plato = plato.iloc[i]
            s_path = path.iloc[i]

            self.msg_buf = []
            self.msg_print = False
            self.dp("======== {} L{} T{:.4f} =========".format(i, s_path["line"], self.emu_t * self.apg_x_s.t_k))

            unit_x = s_speeds["unit_x"]
            unit_y = s_speeds["unit_y"]
            unit_e = s_speeds["unit_e"]
            target_x = s_plato["start_x"]
            target_y = s_plato["start_y"]
            target_e = s_plato["start_e"]
            target_vx = s_plato["start_vx"]
            target_vy = s_plato["start_vy"]
            max_a = s_speeds["max_a"]
            if 1:
                self.dp("e: {} -> {} v_to_ve: {}".format(last_e, target_e, s_speeds["v_to_ve"]))

                self.dp(
                    "corner: x: ({}, {}) -> ({}, {}) v: ({}, {}) -> ({}, {})".format(
                        last_x, last_y, target_x, target_y, last_vx, last_vy, target_vx, target_vy,
                    )
                )

            dvx = target_vx - last_vx
            dvy = target_vy - last_vy

            dtx = abs(dvx / self.max_xa)
            dty = abs(dvy / self.max_ya)
            dt = max(dtx, dty)
            ax = dvx / dt
            ay = dvy / dt

            if self.espeed_by_de_corner:
                # eq: [
                #     v_1 = v_0 + a *  dt,
                #     v_avg = (v_0 + v_1)/2,
                #     dt = (x_1 - x_0)/v_avg
                # ];
                # solve(eq, [v_1, v_avg, a]);
                #
                # v_1=-(-2*x_1+2*x_0+dt*v_0)/dt
                target_ve = (target_e - last_e) * 2 / dt - last_ve
            else:
                target_ve = s_plato["start_v"] * s_speeds["v_to_ve"]

            dve = target_ve - last_ve
            ae = dve / dt

            if dt > 0:
                split_points = [dt]

                if last_vx * target_vx < 0:
                    dtx = abs(last_vx / ax)
                    split_points.append(dtx)

                if last_vy * target_vy < 0:
                    dty = abs(last_vy / ay)
                    split_points.append(dty)

                split_points.sort()
                st_x = last_x
                st_y = last_y
                st_e = last_e
                st_vx = last_vx
                st_vy = last_vy
                st_ve = last_ve
                pdt = 0.0
                last_sn = len(split_points) - 1
                for sn, dts in enumerate(split_points):
                    if sn == last_sn:
                        sp_x = target_x
                        sp_y = target_y
                        sp_e = target_e
                        sp_vx = target_vx
                        sp_vy = target_vy
                        sp_ve = target_ve
                    else:
                        sp_x = st_x + st_vx * dts + ax * pow(dts, 2) / 2
                        sp_y = st_y + st_vy * dts + ay * pow(dts, 2) / 2
                        sp_e = st_e + st_ve * dts + ae * pow(dts, 2) / 2
                        sp_vx = st_vx + ax * dts
                        sp_vy = st_vy + ay * dts
                        sp_ve = st_ve + ae * dts
                    if 1:
                        self.dp(
                            "corner_{} ({} {}): x: ({}, {}) -> ({}, {}) v: ({}, {}) -> ({}, {})".format(
                                sn, dts, dt, last_x, last_y, sp_x, sp_y, last_vx, last_vy, sp_vx, sp_vy,
                            )
                        )
                    segments.append(
                        (
                            1.0 * i,
                            1.0 + sn,
                            dts - pdt,
                            ax,
                            ay,
                            last_x,
                            last_y,
                            sp_x,
                            sp_y,
                            last_vx,
                            last_vy,
                            sp_vx,
                            sp_vy,
                            last_e,
                            sp_e,
                            last_ve,
                            sp_ve
                        )
                    )

                    if emu_in_loop:
                        sub_profile = self.calculate_single_segment2(*segments[-1])
                        profile.extend(sub_profile)
                        last_x = self.last_x
                        last_y = self.last_y
                        last_e = self.last_e
                        last_vx = self.last_vx
                        last_vy = self.last_vy
                        last_ve = self.last_ve
                    else:
                        last_x = sp_x
                        last_y = sp_y
                        last_e = sp_e
                        last_vx = sp_vx
                        last_vy = sp_vy
                        last_ve = sp_ve
                    last_v = hypot(last_vx, last_vy)
                    pdt = dts

            target_x = s_plato["end_x"]
            target_y = s_plato["end_y"]
            target_e = s_plato["end_e"]
            target_vx = s_plato["end_vx"]
            target_vy = s_plato["end_vy"]
            target_v = s_plato["end_v"]

            top_vx = s_plato["top_vx"]
            top_vy = s_plato["top_vy"]
            top_v = s_plato["top_v"]

            if i == last_i:
                assert target_v == 0
                break

            if 1:
                self.dp(
                    "plato: x: ({}, {}) -> ({}, {}) v: ({}, {}) -> ({}, {}) -> ({}, {})".format(
                        last_x,
                        last_y,
                        target_x,
                        target_y,
                        last_vx,
                        last_vy,
                        top_vx,
                        top_vy,
                        target_vx,
                        target_vy,
                    )
                )

            l = hypot(target_x - last_x, target_y - last_y)
            if l < self.skip_plato_len:
                self.dp("plato is too short, skipped", l, self.skip_plato_len)
            else:
                dvx1 = top_vx - last_vx
                dvy1 = top_vy - last_vy

                dtx1 = abs(dvx1 / self.max_xa)
                dty1 = abs(dvy1 / self.max_ya)
                dt1 = max(dtx1, dty1)
                if dt1 > 0:
                    ax1 = dvx1 / dt1
                    ay1 = dvy1 / dt1
                    dx1 = dt1 * last_vx + dt1 * dt1 * ax1 / 2
                    dy1 = dt1 * last_vy + dt1 * dt1 * ay1 / 2
                    l1 = hypot(dx1, dy1)
                else:
                    l1 = 0

                dvx2 = target_vx - top_vx
                dvy2 = target_vy - top_vy

                dtx2 = abs(dvx2 / self.max_xa)
                dty2 = abs(dvy2 / self.max_ya)
                dt2 = max(dtx2, dty2)
                if dt2 > 0:
                    ax2 = dvx2 / dt2
                    ay2 = dvy2 / dt2
                    dx2 = dt2 * top_vx + pow(dt2, 2) * ax2 / 2
                    dy2 = dt2 * top_vy + pow(dt2, 2) * ay2 / 2
                    l2 = hypot(dx2, dy2)
                else:
                    l2 = 0

                if 1:
                    self.dp("l1, l2, l, fl", l1, l2, l, l - l1 - l2)
                    self.dp("dt1, dt2", dt1, dt2)
                if (l >= self.min_plato_len) and (l1 + l2 < l * 0.8):
                    self.dp("long plato")
                    pass
                else:
                    max_a_k = max_a * self.max_a_extra
                    max_top_v = sqrt(2 * max_a_k * l + pow(last_v, 2) + pow(target_v, 2)) / sqrt(2)

                    if (max_top_v < last_v) or (max_top_v < target_v) or (l < self.min_plato_len):
                        if last_v > target_v:
                            self.dp("single segment plato (top = last)")
                            top_v = last_v
                            top_vx = last_vx
                            top_vy = last_vy
                        else:
                            self.dp("single segment plato (top = target)")
                            top_v = target_v
                            top_vx = target_vx
                            top_vy = target_vy
                    else:
                        self.dp("short plato", top_v, max_top_v)

                        k = min(1.0, max_top_v / top_v)

                        top_vx *= k
                        top_vy *= k
                        top_v *= k

                dvx1 = top_vx - last_vx
                dvy1 = top_vy - last_vy

                dtx1 = abs(dvx1 / self.max_xa) / self.max_a_extra2 # 10% extra for accelleration to fix errors from previous steps
                dty1 = abs(dvy1 / self.max_ya) / self.max_a_extra2
                dt1 = max(dtx1, dty1)
                if dt1 > 0:
                    ax1 = dvx1 / dt1
                    ay1 = dvy1 / dt1
                    dx1 = dt1 * last_vx + dt1 * dt1 * ax1 / 2
                    dy1 = dt1 * last_vy + dt1 * dt1 * ay1 / 2
                    l1 = hypot(dx1, dy1)
                else:
                    l1 = 0
                    ax1 = 0
                    ay1 = 0

                dvx2 = target_vx - top_vx
                dvy2 = target_vy - top_vy

                dtx2 = abs(dvx2 / self.max_xa) / self.max_a_extra2
                dty2 = abs(dvy2 / self.max_ya) / self.max_a_extra2
                dt2 = max(dtx2, dty2)
                if dt2 > 0:
                    ax2 = dvx2 / dt2
                    ay2 = dvy2 / dt2
                    dx2 = dt2 * top_vx + pow(dt2, 2) * ax2 / 2
                    dy2 = dt2 * top_vy + pow(dt2, 2) * ay2 / 2
                    l2 = hypot(dx2, dy2)
                else:
                    l2 = 0
                    ax2 = 0
                    ay2 = 0

                if 1:
                    self.dp("l1, l2, l, fl", l1, l2, l, l - l1 - l2)
                    self.dp("dt1, dt2", dt1, dt2)
                if l - (l1 + l2) < -0.001:
                    raise RuntimeError("extra extra short plato: l: {} l1: {} l2: {} d: {}".format(l, l1, l2, l - l1 - l2))

                accel_x = s_plato["start_x"] + unit_x * l1
                accel_y = s_plato["start_y"] + unit_y * l1
                accel_e = s_plato["start_e"] + unit_e * l1
                if self.espeed_by_de_accel:
                    if dt1 > 0:
                        accel_ve = (accel_e - last_e) * 2 / dt1 - last_ve
                    else:
                        accel_ve = last_ve
                else:
                    accel_ve = s_plato["top_v"] * s_speeds["v_to_ve"]

                if dt1 > 0:
                    if 1:
                        self.dp(
                            "plato accel: x: ({}, {}) -> ({}, {}) v: ({}, {}) -> ({}, {})\ne: {} -> {} ({})".format(
                                last_x, last_y, accel_x, accel_y, last_vx, last_vy, top_vx, top_vy, last_e, accel_e, accel_ve
                            )
                        )

                    segments.append(
                        (
                            1.0 * i,
                            10.0,
                            dt1,
                            ax1,
                            ay1,
                            last_x,
                            last_y,
                            accel_x,
                            accel_y,
                            last_vx,
                            last_vy,
                            top_vx,
                            top_vy,
                            last_e,
                            accel_e,
                            last_ve,
                            accel_ve
                        )
                    )

                    if emu_in_loop:
                        sub_profile = self.calculate_single_segment2(*segments[-1])
                        profile.extend(sub_profile)
                        last_x = self.last_x
                        last_y = self.last_y
                        last_e = self.last_e
                        last_vx = self.last_vx
                        last_vy = self.last_vy
                        last_ve = self.last_ve
                    else:
                        last_x = accel_x
                        last_y = accel_y
                        last_e = accel_e
                        last_vx = top_vx
                        last_vy = top_vy
                        last_ve = accel_ve
                    last_v = hypot(last_vx, last_vy)

                plato_l = l - l1 - l2
                dtl = plato_l / top_v

                decel_x = s_plato["end_x"] - unit_x * l2
                decel_y = s_plato["end_y"] - unit_y * l2
                decel_e = s_plato["end_e"] - unit_e * l2
                if self.espeed_by_de_plato:
                    if dtl > 0:
                        decel_ve = (decel_e - last_e) * 2 / dtl - last_ve
                    else:
                        decel_ve = last_ve
                else:
                    decel_ve = s_plato["top_v"] * s_speeds["v_to_ve"]

                if dtl > 0:
                    if 1:
                        self.dp(
                            "plato feed: x: ({}, {}) -> ({}, {}) v: ({}, {}) -> ({}, {})\ne: {} -> {} ({})".format(
                                last_x, last_y, decel_x, decel_y, last_vx, last_vy, top_vx, top_vy, last_e, decel_e, decel_ve
                            )
                        )

                    segments.append(
                        (
                            1.0 * i,
                            20.0,
                            dtl,
                            0,
                            0,
                            last_x,
                            last_y,
                            decel_x,
                            decel_y,
                            last_vx,
                            last_vy,
                            top_vx,
                            top_vy,
                            last_e,
                            decel_e,
                            last_ve,
                            decel_ve
                        )
                    )

                    if emu_in_loop:
                        sub_profile = self.calculate_single_segment2(*segments[-1])
                        profile.extend(sub_profile)
                        last_x = self.last_x
                        last_y = self.last_y
                        last_e = self.last_e
                        last_vx = self.last_vx
                        last_vy = self.last_vy
                        last_ve = self.last_ve
                    else:
                        last_x = decel_x
                        last_y = decel_y
                        last_e = decel_e
                        last_vx = top_vx
                        last_vy = top_vy
                        last_ve = decel_ve
                    last_v = hypot(last_vx, last_vy)

                if dt2 > 0:
                    if self.espeed_by_de_decel:
                        target_ve = (target_e - last_e) * 2 / dt2 - last_ve
                    else:
                        target_ve = s_plato["end_v"] * s_speeds["v_to_ve"]
                    if 1:
                        self.dp(
                            "plato decel: x: ({}, {}) -> ({}, {}) v: ({}, {}) -> ({}, {})\ne: {} -> {} ({})".format(
                                last_x,
                                last_y,
                                target_x,
                                target_y,
                                last_vx,
                                last_vy,
                                target_vx,
                                target_vy,
                                last_e, target_e, target_ve
                            )
                        )

                    segments.append(
                        (
                            1.0 * i,
                            30.0,
                            dt2,
                            ax2,
                            ay2,
                            last_x,
                            last_y,
                            target_x,
                            target_y,
                            last_vx,
                            last_vy,
                            target_vx,
                            target_vy,
                            last_e,
                            target_e,
                            last_ve,
                            target_ve
                        )
                    )

                    if emu_in_loop:
                        sub_profile = self.calculate_single_segment2(*segments[-1])
                        profile.extend(sub_profile)
                        last_x = self.last_x
                        last_y = self.last_y
                        last_e = self.last_e
                        last_vx = self.last_vx
                        last_vy = self.last_vy
                        last_ve = self.last_ve
                    else:
                        last_x = target_x
                        last_y = target_y
                        last_e = target_e
                        last_vx = target_vx
                        last_vy = target_vy
                        last_ve = target_ve
                    last_v = hypot(last_vx, last_vy)

            self.print_msg_buf()

        if emu_in_loop:
            segs = [
                ProfileSegment(apg=self.apg_x, v=0, a=0),
                ProfileSegment(apg=self.apg_y, v=0, a=0),
                ProfileSegment(apg=self.apg_e, v=0, a=0),
            ]
            sub_profile = [[5, segs]]
            emulate(
                sub_profile,
                apg_states=self.apg_states,
                accel_step=self.accel_step,
                no_tracking=True,
            )
            profile.extend(sub_profile)
            self.emu_t += 5

        segments = np.array(segments)
        df = pd.DataFrame()
        df["i"] = segments[:, 0]
        df["st"] = segments[:, 1]
        df["dt"] = segments[:, 2]
        df["t"] = np.cumsum(df["dt"]).shift(1, fill_value=0.0)
        df["ax"] = segments[:, 3]
        df["ay"] = segments[:, 4]
        df["x0"] = segments[:, 5]
        df["y0"] = segments[:, 6]
        df["x1"] = segments[:, 7]
        df["y1"] = segments[:, 8]
        df["vx0"] = segments[:, 9]
        df["vy0"] = segments[:, 10]
        df["vx1"] = segments[:, 11]
        df["vy1"] = segments[:, 12]
        df["e0"] = segments[:, 13]
        df["e1"] = segments[:, 14]
        df["ve0"] = segments[:, 15]
        df["ve1"] = segments[:, 16]

        return df, profile

    def calculate_single_segment2(
        self,
        i_in,
        sn_in,
        dt,
        ax_in,
        ay_in,
        last_x,
        last_y,
        target_x,
        target_y,
        last_vx,
        last_vy,
        target_vx,
        target_vy,
        last_e,
        target_e,
        last_ve,
        target_ve
    ):
        int_dt = int(ceil(dt / self.apg_states[0].t_k))
        orig_dt = dt
        if int_dt < 3:
            return []

        dt = int_dt * self.apg_states[0].t_k

        retest = 0

        ax = (target_vx - last_vx) / dt
        ay = (target_vy - last_vy) / dt
        ae = (target_ve - last_ve) / dt
        if abs(ae) > self.max_ea:
            ae = copysign(self.max_ea, ae)
        jx = 0
        jy = 0
        je = 0
        int_last_vx = self.apg_x_s.v_out
        int_last_vy = self.apg_y_s.v_out
        int_last_ve = self.apg_e_s.v_out
        int_ax = round(ax / self.apg_x_s.a_k)
        int_ay = round(ay / self.apg_y_s.a_k)
        int_ae = round(ae / self.apg_e_s.a_k)
        int_tvx = round(target_vx / self.apg_x_s.v_k)
        int_tvy = round(target_vy / self.apg_y_s.v_k)
        int_tve = round(target_ve / self.apg_e_s.v_k)
        int_jx = 0
        int_jy = 0
        int_je = 0
        if 1:
            self.dp("dt:", orig_dt, int_dt, dt)
            self.dp("ax:", ax)
            self.dp("ay:", ay)
            self.dp("ae:", ae)

        test_x, test_y, test_e, test_vx, test_vy, test_ve = self.emu_profile(int_dt, int_ax, int_ay, int_ae, int_jx, int_jy, int_je, int_tvx, int_tvy, int_tve)

        if not ((abs(test_x - target_x) < self.max_delta / 2) and (abs(test_vx - target_vx) < 1)):
            self.dp("delta_x", test_x, target_x, test_vx, target_vx)
            retest = 1
            jx = 12 * (last_x - target_x) / pow(dt, 3) + 6 * (last_vx + target_vx) / pow(dt, 2)
            ax = (target_vx - last_vx) / dt - jx * dt / 2
            ax2 = ax + jx * dt
            max_ax = max(abs(ax), abs(ax2))
            if max_ax > self.max_xa * self.max_a_extra2:
                self.dp("CAP FOR MAX_XA", max_ax, self.max_xa)
                jx *= (self.max_xa / max_ax) * 0.7
                ax = (target_vx - last_vx) / dt - jx * dt / 2
                if abs(ax) > self.max_xa * self.max_a_extra2:
                    self.dp_force("EXTRA CAP FOR MAX_XA", max_ax, self.max_xa * self.max_a_extra2)
                    ax = copysign(self.max_xa * self.max_a_extra2, (target_vx - last_vx))
                    jx = 0

        if not ((abs(test_y - target_y) < self.max_delta / 2) and (abs(test_vy - target_vy) < 1)):
            self.dp("delta_y", test_y, target_y, test_vy, target_vy)
            retest = 1
            jy = 12 * (last_y - target_y) / pow(dt, 3) + 6 * (last_vy + target_vy) / pow(dt, 2)
            ay = (target_vy - last_vy) / dt - jy * dt / 2
            ay2 = ay + jy * dt
            max_ay = max(abs(ay), abs(ay2))
            if max_ay > self.max_ya * self.max_a_extra2:
                self.dp("CAP FOR MAX_YA", max_ay, self.max_ya)
                jy *= (self.max_ya / max_ay) * 0.7
                ay = (target_vy - last_vy) / dt - jy * dt / 2
                if abs(ay) > self.max_ya * self.max_a_extra2:
                    self.dp_force("EXTRA CAP FOR MAX_YA", max_ay, self.max_ya * self.max_a_extra2)
                    ay = copysign(self.max_ya * self.max_a_extra2, (target_vy - last_vy))
                    jy = 0

        if not ((abs(test_e - target_e) < self.max_delta_e / 2) and (abs(test_ve - target_ve) < 1)):
            self.dp("delta_e", test_e, target_e, test_ve, target_ve)
            retest = 1
            je = 12 * (last_e - target_e) / pow(dt, 3) + 6 * (last_ve + target_ve) / pow(dt, 2)
            ae = (target_ve - last_ve) / dt - je * dt / 2
            ae2 = ae + je * dt
            max_ae = max(abs(ae), abs(ae2))
            if max_ae > self.max_ea * self.max_a_extra2:
                self.dp("CAP FOR MAX_EA", max_ae, self.max_ea)
                je *= (self.max_ea / max_ae) * 0.7
                ae = (target_ve - last_ve) / dt - je * dt / 2
                if abs(ae) > self.max_ea * self.max_a_extra2:
                    self.dp("EXTRA CAP FOR MAX_EA", max_ae, self.max_ea * self.max_a_extra2)
                    ae = copysign(self.max_ea * self.max_a_extra2, (target_ve - last_ve))
                    je = 0

        if retest:
            int_last_vx = self.apg_x_s.v_out
            int_last_vy = self.apg_y_s.v_out
            int_last_ve = self.apg_e_s.v_out
            int_tvx = round(target_vx / self.apg_x_s.v_k)
            int_tvy = round(target_vy / self.apg_y_s.v_k)
            int_tve = round(target_ve / self.apg_e_s.v_k)
            int_ax = round(ax / self.apg_x_s.a_k)
            int_ay = round(ay / self.apg_y_s.a_k)
            int_ae = round(ae / self.apg_e_s.a_k)
            int_jx = round(jx / self.apg_x_s.j_k)
            int_jy = round(jy / self.apg_y_s.j_k)
            int_je = round(je / self.apg_e_s.j_k)

            test_x, test_y, test_e, test_vx, test_vy, test_ve = self.emu_profile(int_dt, int_ax, int_ay, int_ae, int_jx, int_jy, int_je, int_tvx, int_tvy, int_tve)
            tests = (
                (abs(test_x - target_x) < self.max_delta * 2 * self.delta_err),
                (abs(test_y - target_y) < self.max_delta * 2 * self.delta_err),
                (abs(test_e - target_e) < self.max_delta_e * 10 * self.delta_e_err),
                (abs(test_vx - target_vx) < 2 * self.delta_v_err),
                (abs(test_vy - target_vy) < 2 * self.delta_v_err),
                (abs(test_ve - target_ve) < 2 * self.delta_ve_err)
            )
            if not all(tests):
                self.dp_force("Target precision not reached dx: {} dy: {} de: {} dvx: {} dvy: {} dve: {} tests: {}".format(
                    abs(test_x - target_x),
                    abs(test_y - target_y),
                    abs(test_e - target_e),
                    abs(test_vx - target_vx),
                    abs(test_vy - target_vy),
                    abs(test_ve - target_ve),
                    tests
                ))
                self.print_msg_buf()
                raise RuntimeError("target prcision: {}".format(tests))

        if 1:
            self.dp("int_v:", int_last_vx, int_tvx, int_last_vy, int_tvy, int_last_ve, int_tve)
            self.dp("int_j:", int_jx, int_jy, int_je)

        ax0 = int_ax * self.apg_x_s.a_k
        ax1 = (int_ax + int_jx * (int_dt - 1)) * self.apg_x_s.a_k

        vxm = 0
        if (jx != 0) and (ax0 * ax1 < 0):
            vxm = -pow(ax, 2) / 2 / jx

        ay0 = int_ay * self.apg_y_s.a_k
        ay1 = (int_ay + int_jy * (int_dt - 1)) * self.apg_y_s.a_k

        vym = 0
        if (jy != 0) and (ay0 * ay1 < 0):
            vym = -pow(ay0, 2) / 2 / jy

        ae0 = int_ae * self.apg_e_s.a_k
        ae1 = (int_ae + int_je * (int_dt - 1)) * self.apg_e_s.a_k

        vem = 0
        if (je != 0) and (ae0 * ae1 < 0):
            vem = -pow(ae0, 2) / 2 / je

        try:
            assert abs(ax0) < self.max_xa * 2.5
            assert abs(ax1) < self.max_xa * 2.5
            assert abs(vxm) < self.max_xv * 1.5
            assert abs(ay0) < self.max_ya * 2.5
            assert abs(ay1) < self.max_ya * 2.5
            assert abs(vym) < self.max_yv * 1.5
            #assert abs(ae0) < self.max_ea * 2.5
            #assert abs(ae1) < self.max_ea * 2.5
            #assert abs(vem) < self.max_ev * 1.5
        except AssertionError:
            self.dp_force("==== Assertion error ====")
            self.dp("dt, int_dt, dx, dy, de", dt, int_dt, target_x - last_x, target_y - last_y, target_e - last_e)
            self.dp("ax, jx, ax0, ax1, vxm", ax, jx, ax0, ax1, vxm)
            self.dp("ay, jy, ay0, ay1, vym", ay, jy, ay0, ay1, vym)
            self.dp("ae, je, ae0, ae1, vem", ae, je, ae0, ae1, vem)
            raise

        for k, v in [
            ("ax", ax0),
            ("ax", ax1),
            ("ay", ay0),
            ("ay", ay1),
            ("ae", ae0),
            ("ae", ae1),
        ]:
            self.max_deltas[k] = max(self.max_deltas[k], abs(v))

        sub_profile = []
        if int_dt > 0:
            segs = [
                ProfileSegment(apg=self.apg_x, a=int(int_ax), j=int(int_jx), target_v=int(int_tvx)),
                ProfileSegment(apg=self.apg_y, a=int(int_ay), j=int(int_jy), target_v=int(int_tvy)),
                ProfileSegment(apg=self.apg_e, a=int(int_ae), j=int(int_je), target_v=int(int_tve)),
            ]

            sub_profile = [[int_dt, segs]]

        if 0:
            print(sub_profile)

        emulate(
            sub_profile, apg_states=self.apg_states, accel_step=self.accel_step, no_tracking=True
        )

        self.emu_t += int_dt
        self.last_x = self.apg_x_s.to_floats()["x"]
        self.last_y = self.apg_y_s.to_floats()["x"]
        self.last_e = self.apg_e_s.to_floats()["x"]
        self.last_vx = self.apg_x_s.to_floats()["v_out"]
        self.last_vy = self.apg_y_s.to_floats()["v_out"]
        self.last_ve = self.apg_e_s.to_floats()["v_out"]
        self.last_v = hypot(self.last_vx, self.last_vy)
        if 1:
            self.dp(
                "last_x",
                self.last_x,
                "last_y",
                self.last_y,
                "last_e",
                self.last_e,
                "last_vx",
                self.last_vx,
                "last_vy",
                self.last_vy,
                "last_ve",
                self.last_ve,
            )
            self.dp(
                "d_x",
                self.last_x - target_x,
                "d_y",
                self.last_y - target_y,
                "d_e",
                self.last_e - target_e,
                "d_vx",
                self.last_vx - target_vx,
                "d_vy",
                self.last_vy - target_vy,
                "d_ve",
                self.last_ve - target_ve,
            )

        for k, v in [
            ("dx", self.last_x - target_x),
            ("dy", self.last_y - target_y),
            ("de", self.last_e - target_e),
            ("dvx", self.last_vx - target_vx),
            ("dvy", self.last_vy - target_vy),
            ("dve", self.last_ve - target_ve),
        ]:
            self.max_deltas[k] = max(self.max_deltas[k], abs(v))

        return sub_profile

    def gen_all_segments_pandas(self, path, slowdowns):

        speeds = self.gen_speeds(path, slowdowns)
        _, _, cc = self.process_corner_errors(path, slowdowns)

        plato = pd.DataFrame()
        plato["middle_x"] = path["px"] + cc["mdx"]
        plato["middle_y"] = path["py"] + cc["mdy"]
        plato["middle_e"] = path["pe"]
        plato["middle_vx"] = cc["mvx"]
        plato["middle_vy"] = cc["mvy"]
        plato["middle_v"] = np.linalg.norm(cc[["mvx", "mvy"]], axis=1)

        plato["start_x"] = path["px"] + speeds["unit_x"] * cc["l_entry"]
        plato["start_y"] = path["py"] + speeds["unit_y"] * cc["l_entry"]
        plato["start_e"] = path["pe"] + speeds["unit_e"] * cc["l_entry"]
        plato["start_vx"] = speeds["entry_x"]
        plato["start_vy"] = speeds["entry_y"]
        plato["start_v"] = speeds["entry"]
        plato["top_vx"] = speeds["plato_x"]
        plato["top_vy"] = speeds["plato_y"]
        plato["top_v"] = speeds["plato"]
        plato["end_x"] = path["x"] - speeds["unit_x"] * cc["l_exit"]
        plato["end_y"] = path["y"] - speeds["unit_y"] * cc["l_exit"]
        plato["end_e"] = path["e"] - speeds["unit_e"] * cc["l_exit"]
        plato["end_vx"] = speeds["exit_x"]
        plato["end_vy"] = speeds["exit_y"]
        plato["end_v"] = speeds["exit"]
        plato["v_to_ve"] = speeds["v_to_ve"]

        plato["pre_x"] = plato["end_x"].shift(1).fillna(path["px"][0])
        plato["pre_y"] = plato["end_y"].shift(1).fillna(path["py"][0])
        plato["pre_e"] = plato["end_e"].shift(1).fillna(0)
        plato["pre_vx"] = plato["end_vx"].shift(1).fillna(0)
        plato["pre_vy"] = plato["end_vy"].shift(1).fillna(0)
        plato["pre_v"] = plato["end_v"].shift(1).fillna(0)
        plato["pre_v_to_ve"] = plato["v_to_ve"].shift(1).fillna(0)
        plato["corner_dt"] = cc["dt"]

        plato["plato_l"] = cc["l_free"]
        s1 =  (2 * speeds["max_a"] * 0.9 * plato["plato_l"]
            + plato["start_v"] * plato["start_v"]
            + plato["end_v"] * plato["end_v"]
               ) / 2

        max_top_v = np.sqrt(s1)
        plato["max_top_v"] = np.max([plato["start_v"], max_top_v, plato["end_v"]], axis=0)

        try:
            assert all(plato["max_top_v"] >= plato["start_v"])
        except:
            d1 = plato["max_top_v"] - plato["start_v"]
            print(plato[["max_top_v", "start_v"]][d1 < 0])
            raise
        try:
            assert all(plato["max_top_v"] >= plato["end_v"])
        except:
            d2 = plato["max_top_v"] -plato["end_v"]
            print(plato[["max_top_v", "end_v"]][d2 < 0])
            raise

        plato["real_top_v"] = np.min(plato[["top_v", "max_top_v"]], axis=1)
        plato["real_top_vx"] = plato["real_top_v"] * speeds["unit_x"]
        plato["real_top_vy"] = plato["real_top_v"] * speeds["unit_y"]
        plato["accel_dt"] = (plato["real_top_v"] - plato["start_v"]) / speeds["max_a"]
        plato["decel_dt"] = (plato["real_top_v"] - plato["end_v"]) / speeds["max_a"]
        plato["accel_l"] = (plato["real_top_v"] + plato["start_v"]) * plato["accel_dt"] / 2
        plato["decel_l"] = (plato["real_top_v"] + plato["end_v"]) * plato["decel_dt"] / 2
        plato["top_l"] = plato["plato_l"] - plato["accel_l"] - plato["decel_l"]
        plato["top_dt"] = (plato["top_l"] / plato["real_top_v"]).fillna(0)
        plato["dt"] = plato["corner_dt"] + plato["accel_dt"] + plato["top_dt"] + plato["decel_dt"]
        plato["t"] = np.cumsum(plato["dt"]).shift(1).fillna(0)
        # display(plato)
        # display(plato.iloc[0])
        # display(plato.iloc[1])
        # display(plato.iloc[-2])
        # display(plato.iloc[-1])

        pre_corner_segs = pd.DataFrame()
        pre_corner_segs["idx"] = plato.index.values * 5
        pre_corner_segs["tp"] = 0
        pre_corner_segs["line"] = path["line"]
        pre_corner_segs["t"] = plato["t"]

        dt = plato["corner_dt"] / 2
        dt[0] = 0
        dt[len(dt) - 1] *= 2
        pre_corner_segs["dt"] = dt

        pre_corner_segs["start_x"] = plato["pre_x"]
        pre_corner_segs["start_y"] = plato["pre_y"]
        pre_corner_segs["start_e"] = plato["pre_e"]
        pre_corner_segs["start_vx"] = plato["pre_vx"]
        pre_corner_segs["start_vy"] = plato["pre_vy"]
        pre_corner_segs["end_x"] = plato["middle_x"]
        pre_corner_segs["end_y"] = plato["middle_y"]
        pre_corner_segs["end_e"] = plato["middle_e"]
        pre_corner_segs["end_vx"] = plato["middle_vx"]
        pre_corner_segs["end_vy"] = plato["middle_vy"]
        pre_corner_segs["v_to_ve"] = plato["pre_v_to_ve"]

        corner_segs = pd.DataFrame()
        corner_segs["idx"] = pre_corner_segs["idx"] + 1
        corner_segs["tp"] = 1
        corner_segs["line"] = path["line"]
        corner_segs["t"] = pre_corner_segs["t"] + pre_corner_segs["dt"]

        dt = plato["corner_dt"] / 2
        dt[0] *= 2
        dt[len(dt) - 1] = 0
        corner_segs["dt"] = dt

        corner_segs["start_x"] = pre_corner_segs["end_x"]
        corner_segs["start_y"] = pre_corner_segs["end_y"]
        corner_segs["start_e"] = pre_corner_segs["end_e"]
        corner_segs["start_vx"] = pre_corner_segs["end_vx"]
        corner_segs["start_vy"] = pre_corner_segs["end_vy"]
        corner_segs["end_x"] = plato["start_x"]
        corner_segs["end_y"] = plato["start_y"]
        corner_segs["end_e"] = plato["start_e"]
        corner_segs["end_vx"] = plato["start_vx"]
        corner_segs["end_vy"] = plato["start_vy"]
        corner_segs["v_to_ve"] = plato["v_to_ve"]

        accel_segs = pd.DataFrame()
        accel_segs["idx"] = corner_segs["idx"] + 1
        accel_segs["tp"] = 2
        accel_segs["line"] = path["line"]
        accel_segs["t"] = corner_segs["t"] + corner_segs["dt"]
        accel_segs["dt"] = plato["accel_dt"]
        accel_segs["start_x"] = corner_segs["end_x"]
        accel_segs["start_y"] = corner_segs["end_y"]
        accel_segs["start_e"] = corner_segs["end_e"]
        accel_segs["start_vx"] = corner_segs["end_vx"]
        accel_segs["start_vy"] = corner_segs["end_vy"]
        accel_segs["end_x"] = accel_segs["start_x"] + speeds["unit_x"] * plato["accel_l"]
        accel_segs["end_y"] = accel_segs["start_y"] + speeds["unit_y"] * plato["accel_l"]
        accel_segs["end_e"] = accel_segs["start_e"] + speeds["unit_e"] * plato["accel_l"]
        accel_segs["end_vx"] = plato["real_top_vx"]
        accel_segs["end_vy"] = plato["real_top_vy"]
        accel_segs["v_to_ve"] = plato["v_to_ve"]

        top_segs = pd.DataFrame()
        top_segs["idx"] = accel_segs["idx"] + 1
        top_segs["tp"] = 3
        top_segs["line"] = path["line"]
        top_segs["t"] = accel_segs["t"] + accel_segs["dt"]
        top_segs["dt"] = plato["top_dt"]
        top_segs["start_x"] = accel_segs["end_x"]
        top_segs["start_y"] = accel_segs["end_y"]
        top_segs["start_e"] = accel_segs["end_e"]
        top_segs["start_vx"] = accel_segs["end_vx"]
        top_segs["start_vy"] = accel_segs["end_vy"]
        top_segs["end_x"] = top_segs["start_x"] + speeds["unit_x"] * plato["top_l"]
        top_segs["end_y"] = top_segs["start_y"] + speeds["unit_y"] * plato["top_l"]
        top_segs["end_e"] = top_segs["start_e"] + speeds["unit_e"] * plato["top_l"]
        top_segs["end_vx"] = top_segs["start_vx"]
        top_segs["end_vy"] = top_segs["start_vy"]
        top_segs["v_to_ve"] = plato["v_to_ve"]

        decel_segs = pd.DataFrame()
        decel_segs["idx"] = top_segs["idx"] + 1
        decel_segs["tp"] = 4
        decel_segs["line"] = path["line"]
        decel_segs["t"] = top_segs["t"] + top_segs["dt"]
        decel_segs["dt"] = plato["decel_dt"]
        decel_segs["start_x"] = top_segs["end_x"]
        decel_segs["start_y"] = top_segs["end_y"]
        decel_segs["start_e"] = top_segs["end_e"]
        decel_segs["start_vx"] = top_segs["end_vx"]
        decel_segs["start_vy"] = top_segs["end_vy"]
        decel_segs["end_x"] = plato["end_x"]
        decel_segs["end_y"] = plato["end_y"]
        decel_segs["end_e"] = plato["end_e"]
        decel_segs["end_vx"] = plato["end_vx"]
        decel_segs["end_vy"] = plato["end_vy"]
        decel_segs["v_to_ve"] = plato["v_to_ve"]

        pre_corner_segs = pre_corner_segs.set_index("idx")
        corner_segs = corner_segs.set_index("idx")
        accel_segs = accel_segs.set_index("idx")
        top_segs = top_segs.set_index("idx")
        decel_segs = decel_segs.set_index("idx")

        all_segs_raw = pd.concat([pre_corner_segs, corner_segs, accel_segs, top_segs, decel_segs]).sort_index()
        all_segs_filter = (all_segs_raw["dt"] > 1e-5).values
        all_segs_filter[0] = True
        all_segs_filter[-1] = True
        all_segs = all_segs_raw[all_segs_filter][[
            "tp", "line", "t", "v_to_ve", "start_x", "start_y", "start_e", "start_vx", "start_vy",
        ]].copy().sort_index()

        all_segs["start_v"] = np.linalg.norm(all_segs[["start_vx", "start_vy"]], axis=1)
        all_segs["end_x"] = all_segs["start_x"].shift(-1)
        all_segs["end_y"] = all_segs["start_y"].shift(-1)
        all_segs["end_e"] = all_segs["start_e"].shift(-1)
        all_segs["end_vx"] = all_segs["start_vx"].shift(-1)
        all_segs["end_vy"] = all_segs["start_vy"].shift(-1)
        all_segs["end_v"] = all_segs["start_v"].shift(-1)
        all_segs["dt"] = all_segs["t"].shift(-1) - all_segs["t"]

        all_segs = all_segs.iloc[1:-1, :]

        all_segs["avg_v"] = (all_segs["start_v"] + all_segs["end_v"]) / 2

        de = all_segs["end_e"] - all_segs["start_e"]
        de[np.abs(de) < 1e-5] = 0
        avg_ve = de / all_segs["dt"]

        all_segs["dx"] = np.abs(80 * (all_segs["end_x"] - all_segs["start_x"]))
        all_segs["dy"] = np.abs(80 * (all_segs["end_y"] - all_segs["start_y"]))
        all_segs["de"] = np.abs(837 * de)
        all_segs["dx_dt"] = all_segs["dt"] / all_segs["dx"] * 1000000
        all_segs["dy_dt"] = all_segs["dt"] / all_segs["dy"] * 1000000
        all_segs["de_dt"] = all_segs["dt"] / all_segs["de"] * 1000000
        all_segs["avg_ve"] = avg_ve
        all_segs["v_to_ve2"] = (all_segs["avg_ve"] / all_segs["avg_v"]).fillna(0)

        return all_segs

    borders = 100
    delta_t = 0.001

    def sample_all_segments(self, all_segs):
        track_t = []
        track_x = []
        track_y = []
        track_e = []
        track_e_exp = []
        track_vx = []
        track_vy = []
        track_ve = []

        last_e = 0
        last_ve = 0

        borders = self.borders
        delta_t = self.delta_t

        # first and last segments require patching, as j-only move takes 1.5x time
        dt_first = all_segs["dt"].iloc[0]
        extra_start = int(ceil(dt_first / delta_t)) + borders
        last_t = -extra_start * delta_t

        t_last = all_segs["t"].iloc[-1]
        dt_last = all_segs["dt"].iloc[-1]
        extra_end = int(ceil(dt_last / delta_t)) + borders
        final_t = t_last + extra_end * delta_t

        last_i = len(all_segs) - 1

        for i, seg in enumerate(all_segs.itertuples()):
            t = seg.t
            dt = seg.dt
            end_t = t + dt

            st_x = seg.start_x
            st_vx = seg.start_vx
            tg_x = seg.end_x
            tg_vx = seg.end_vx

            dvx = tg_vx - st_vx
            ax = dvx / dt
            jx = 0

            st_y = seg.start_y
            st_vy = seg.start_vy
            tg_y = seg.end_y
            tg_vy = seg.end_vy

            dvy = tg_vy - st_vy
            ay = dvy / dt
            jy = 0

            st_e = seg.start_e
            tg_e = seg.end_e

            st_v = sqrt(st_vx * st_vx + st_vy * st_vy)
            tg_v = sqrt(tg_vx * tg_vx + tg_vy * tg_vy)
            st_ve = st_v * seg.v_to_ve
            tg_ve = tg_v * seg.v_to_ve

            if seg.tp in (0, 1):
                st_ve = tg_ve = (tg_e - st_e) / dt

            dve = tg_ve - st_ve
            ae = dve / dt
            je = 0

            calc_j = False
            if i == 0:
                dt *= 1.5
                t = end_t - dt

                tg_ve += st_ve
                st_ve = 0
                calc_j = True
            elif i == last_i:
                dt *= 1.5
                end_t = t + dt

                st_ve += tg_ve
                tg_ve = 0
                calc_j = True

            if calc_j:
                dx = tg_x - st_x
                dy = tg_y - st_y
                de = tg_e - st_e

                jx = -(12 * dx - 6 * dt * tg_vx - 6 * dt * st_vx) / dt / dt / dt
                ax = (6 * dx - 2 * dt * tg_vx - 4 * dt * st_vx) / dt / dt

                jy = -(12 * dy - 6 * dt * tg_vy - 6 * dt * st_vy) / dt / dt / dt
                ay = (6 * dy - 2 * dt * tg_vy - 4 * dt * st_vy) / dt / dt

                je = -(12 * de - 6 * dt * tg_ve - 6 * dt * st_ve) / dt / dt / dt
                ae = (6 * de - 2 * dt * tg_ve - 4 * dt * st_ve) / dt / dt

                print(ax, jx, ay, jy, ae, je)

            dx = st_vx * dt + ax * dt * dt / 2 + jx * dt * dt * dt / 6
            dx_err = dx - (tg_x - st_x)

            dy = st_vy * dt + ay * dt * dt / 2 + jy * dt * dt * dt / 6
            dy_err = dy - (tg_y - st_y)

            de = st_ve * dt + ae * dt * dt / 2 + je * dt * dt * dt / 6
            de_err = de - (tg_e - st_e)

            try:
                assert abs(dx_err) < 0.01
                assert abs(dy_err) < 0.01
                assert abs(de_err) < 0.01
            except:
                print(t, seg.tp, seg.line, dx_err, dy_err, de_err)
                raise

            if i == 0:
                while last_t < t:
                    track_t.append(last_t)
                    track_x.append(st_x)
                    track_y.append(st_y)
                    track_vx.append(st_vx)
                    track_vy.append(st_vy)
                    track_e.append(st_e)
                    track_ve.append(st_ve)

                    last_t += delta_t

            while last_t < end_t:
                ct = last_t - t
                dx = st_vx * ct + ax * ct * ct / 2 + jx * ct * ct * ct / 6
                dy = st_vy * ct + ay * ct * ct / 2 + jy * ct * ct * ct / 6
                de = st_ve * ct + ae * ct * ct / 2 + je * ct * ct * ct / 6
                x = st_x + dx
                y = st_y + dy
                e = st_e + de
                vx = st_vx + ax * ct + jx * ct * ct / 2
                vy = st_vy + ay * ct + jy * ct * ct / 2
                ve = st_ve + ae * ct + je * ct * ct / 2

                track_t.append(last_t)
                track_x.append(x)
                track_y.append(y)
                track_vx.append(vx)
                track_vy.append(vy)
                track_e.append(e)
                track_ve.append(ve)

                last_t += delta_t

        while last_t < final_t:
            track_t.append(last_t)
            track_x.append(tg_x)
            track_y.append(tg_y)
            track_e.append(tg_e)
            track_vx.append(tg_vx)
            track_vy.append(tg_vy)
            track_ve.append(tg_ve)
            last_t += delta_t

        df = pd.DataFrame()
        df["t"] = track_t
        df["x"] = track_x
        df["y"] = track_y
        df["e"] = track_e
        df["vx"] = track_vx
        df["vy"] = track_vy
        df["ve"] = track_ve

        df["v"] = np.linalg.norm(df[["vx", "vy"]], axis=1)
        df["dx"] = (df["x"] - df["x"].shift(1))
        df["dy"] = (df["y"] - df["y"].shift(1))
        df["d"] = np.linalg.norm(df[["dx", "dy"]], axis=1)
        df["de"] = (df["e"] - df["e"].shift(1))

        return df

    lin_k = 5
    def smooth_and_lin_advance(self, df):
        df["de_smooth"] = df["de"].rolling(20, center=True, win_type="hamming").mean()
        df["e_smooth"] = df["de_smooth"].cumsum()

        df["de_adv"] = df["de_smooth"] * self.lin_k

        df["e_adv"] = df["e_smooth"] + df["de_adv"]

        df["dx_smooth"] = df["dx"].rolling(5, center=True, win_type="hamming").mean()
        df["dy_smooth"] = df["dy"].rolling(5, center=True, win_type="hamming").mean()
        df["x_smooth"] = df["dx_smooth"].cumsum() + df["x"].iloc[0]
        df["y_smooth"] = df["dy_smooth"].cumsum() + df["y"].iloc[0]

    cf_rtol = 1e-4
    cf_atol = 0.01

    def curve_fit(self, df, all_segs):
        borders = self.borders
        t0 = df["t"].iloc[int(borders / 2)]
        t1 = df["t"].iloc[int(-borders / 2)]
        length = np.sum(df["d"].iloc[int(borders / 2):int(-borders / 2)])

        xf = interp1d(df["t"], df[["x_smooth", "y_smooth", "e_smooth"]].T)
        xxf = lambda x: xf(x).T

        c = curve_factory.fit(xxf, t0, t1, rtol=self.cf_rtol, atol=self.cf_atol)

        print("first_curve:", len(c), c)
        err = c.error(xxf)
        print("first_err:", err[1])

        knots = c.knots()[0]
        n_knots = []

        # add first oversample
        accel_t = all_segs.iloc[1]["t"]

        idx = np.searchsorted(knots, accel_t)
        print(accel_t)
        kn_0 = knots[0]
        kn_1 = knots[idx] + 0.010

        rdt = kn_1 - kn_0
        rn = int(ceil(rdt / 0.005))
        rsdt = rdt / rn

        idx2 = np.searchsorted(knots, kn_1) + 3

        for i in range(rn + 1):
            n_kn = kn_0 + rsdt * i
            ok = True
            for kn in knots[:idx2]:
                if abs(kn - n_kn) < 0.001:
                    print("{} too close to {}".format(kn, n_kn))
                    ok = False
                    break
            if ok:
                n_knots.append(n_kn)

        # add last oversample
        decel_t = all_segs.iloc[-1]["t"]

        idx = np.searchsorted(knots, decel_t) - 1
        print(decel_t)
        print(knots[idx - 1])
        print(knots[idx])
        print(knots[idx + 1])
        kn_0 = knots[idx] - 0.010
        kn_1 = knots[-1]

        rdt = kn_1 - kn_0
        rn = int(ceil(rdt / 0.005))
        rsdt = rdt / rn

        idx2 = np.searchsorted(knots, kn_0) - 3

        for i in range(rn + 1):
            n_kn = kn_1 - rsdt * i
            ok = True
            for kn in knots[idx2:]:
                if abs(kn - n_kn) < 0.002:
                    print("{} too close to {}".format(kn, n_kn))
                    ok = False
                    break
            if ok:
                n_knots.append(n_kn)

        print(n_knots)
        knots.extend(n_knots)
        knots.sort()
        knots = [knots[0]] * 3 + knots + [knots[-1]] * 3

        b = curve_factory.BSplineBasis(4, knots)
        # do interpolation and return result
        t = np.array(b.greville())
        crv = curve_factory.interpolate(xxf(t), b, t)
        print(len(crv), crv)
        (err2, max_err) = crv.error(xxf)
        print(max_err)
        return crv, max_err

    def format_curve_to_code(self, c, apg_x=0, apg_y=2, apg_e=4, do_reset=True):
        apg_x_s = self.apg_states[apg_x]
        apg_y_s = self.apg_states[apg_y]
        apg_e_s = self.apg_states[apg_e]
        t_k = apg_x_s.t_k

        knots = c.knots()[0]

        new_knots = []

        for i, t in enumerate(knots):
            int_t = int(round(t / t_k))

            if i == 0:
                print(t)
                last_int_t = int_t
                new_knots.append(t)
                continue

            int_dt = int_t - last_int_t
            if int_dt < 10:
                continue

            new_knots.append(t)
            last_int_t = int_t

        knots = new_knots
        x_vals = c(knots)
        v_vals = c.derivative(knots, d=1)
        a_vals = c.derivative(knots, d=2)
        j_vals = c.derivative(knots, d=3)

        tg_x, tg_y, tg_e = x_vals[0]

        segs = []

        if do_reset:
            segs += [
                ProfileSegment(apg=apg_x, x=int(tg_x / apg_x_s.x_k), v=0, a=0),
                ProfileSegment(apg=apg_y, x=int(tg_y / apg_y_s.x_k), v=0, a=0),
            ]
        segs += [
            ProfileSegment(apg=apg_e, x=int(tg_e / apg_e_s.x_k), v=0, a=0)
        ]

        segments = []
        sub_profile = [[5, segs]]
        emulate(
                sub_profile,
                apg_states=self.apg_states,
                accel_step=self.accel_step,
                step_bit=self.step_bit,
                no_tracking=True,
        )

        segments.extend(sub_profile)
        self.emu_t += 5

        last_x = apg_x_s.x_float()
        last_vx = apg_x_s.v_float()
        last_y = apg_y_s.x_float()
        last_vy = apg_y_s.v_float()
        last_e = apg_e_s.x_float()
        last_ve = apg_e_s.v_float()
        last_ax = apg_x_s.a_float()
        last_ay = apg_y_s.a_float()
        last_ae = apg_e_s.a_float()

        last_int_t = None

        for i, t in enumerate(knots):
            int_t = int(round(t / t_k))

            if i == 0:
                print(t)
                last_int_t = int_t
                continue

            int_dt = int_t - last_int_t
            dt = int_dt * t_k

            tg_x, tg_y, tg_e = x_vals[i]
            tg_vx, tg_vy, tg_ve = v_vals[i]
            exp_ax, exp_ay, exp_ae = a_vals[i - 1]
            exp_jx, exp_jy, exp_je = j_vals[i - 1]

            def calc_aj(dt, x, last_x, v, last_v, a_k, j_k):
                dx = x - last_x

                ax = (6 * dx - 2 * dt * v - 4 * dt * last_v) / dt / dt
                int_ax = round(ax / a_k)

                ax = int_ax * a_k
                jx = (6 * dx - 6 * dt * last_v - 3 * ax * dt * dt) / dt / dt / dt

                int_jx = round(jx / j_k)
                jx = int_jx * j_k

                return ax, int_ax, jx, int_jx

            ax, int_ax, jx, int_jx = calc_aj(dt, tg_x, last_x, tg_vx, last_vx, apg_x_s.a_k, apg_x_s.j_k)
            ay, int_ay, jy, int_jy = calc_aj(dt, tg_y, last_y, tg_vy, last_vy, apg_y_s.a_k, apg_y_s.j_k)
            ae, int_ae, je, int_je = calc_aj(dt, tg_e, last_e, tg_ve, last_ve, apg_e_s.a_k, apg_e_s.j_k)

            profile = [
                [
                    int_dt,
                    [
                        ProfileSegment(apg=apg_x, a=int(int_ax), j=int(int_jx)),
                        ProfileSegment(apg=apg_y, a=int(int_ay), j=int(int_jy)),
                        ProfileSegment(apg=apg_e, a=int(int_ae), j=int(int_je)),
                    ],
                ]
            ]
            emulate(profile, apg_states=self.apg_states, accel_step=self.accel_step, no_tracking=True)
            segments.extend(profile)
            self.emu_t += int_dt

            last_x = apg_x_s.x_float()
            last_vx = apg_x_s.v_float()
            last_y = apg_y_s.x_float()
            last_vy = apg_y_s.v_float()
            last_e = apg_e_s.x_float()
            last_ve = apg_e_s.v_float()
            last_int_t += int_dt

            print(
                "{:7.3f} {:4d} x: {:5.2f}/{:5.2f} y: {:5.2f}/{:5.2f} e: {:5.2f}/{:5.2f} a: {:9d} {:9d} {:9d} j: {:6d} {:6d} {:6d}".format(
                    t, int_dt,
                    (last_x - tg_x) * apg_x_s.spm, last_vx - tg_vx,
                    (last_y - tg_y) * apg_y_s.spm, last_vy - tg_vy,
                    (last_e - tg_e) * apg_e_s.spm, last_ve - tg_ve,
                    int(int_ax),
                    int(int_ay),
                    int(int_ae),
                    int(int_jx),
                    int(int_jy),
                    int(int_je),
                ))

            last_ax = apg_x_s.a_float()
            last_ay = apg_y_s.a_float()
            last_ae = apg_e_s.a_float()

        segs = [
            ProfileSegment(apg=apg_x, v=0, a=0),
            ProfileSegment(apg=apg_y, v=0, a=0),
            ProfileSegment(apg=apg_e, v=0, a=0)
        ]

        profile = [[5, segs]]
        emulate(profile, apg_states=self.apg_states, accel_step=self.accel_step, no_tracking=True)
        segments.extend(profile)
        self.emu_t += 5

        last_vx = apg_x_s.v_float()
        last_vy = apg_y_s.v_float()
        last_ve = apg_e_s.v_float()
        last_ax = apg_x_s.a_float()
        last_ay = apg_y_s.a_float()
        last_ae = apg_e_s.a_float()

        print(last_vx, last_vy, last_ve, last_ax, last_ay, last_ae)
        print(len(segments))

        self.last_x = apg_x_s.to_floats()["x"]
        self.last_y = apg_y_s.to_floats()["x"]
        self.last_e = apg_e_s.to_floats()["x"]
        self.last_vx = apg_x_s.to_floats()["v_out"]
        self.last_vy = apg_y_s.to_floats()["v_out"]
        self.last_ve = apg_e_s.to_floats()["v_out"]
        self.last_v = hypot(self.last_vx, self.last_vy)

        return segments

    def emu_profile(self, int_dt, int_ax, int_ay, int_ae, int_jx, int_jy, int_je, int_tvx, int_tvy, int_tve):
        test_states = { k: v.copy() for k, v in self.apg_states.items() }

        test_profile = [
            [
                int_dt,
                [
                    ProfileSegment(apg=self.apg_x, a=int_ax, j=int_jx, target_v=int_tvx),
                    ProfileSegment(apg=self.apg_y, a=int_ay, j=int_jy, target_v=int_tvy),
                    ProfileSegment(apg=self.apg_e, a=int_ae, j=int_je, target_v=int_tve),
                ],
            ]
        ]
        #print("testing: ", test_profile)

        if int_ae < - 2**32 or int_ae > 2**32 - 1:
            raise RuntimeError("INT_AE is too big: {}".format(int_ae))

        emulate(test_profile, apg_states=test_states, accel_step=self.accel_step, no_tracking=True)
        test_x = test_states[self.apg_x].to_floats()["x"]
        test_y = test_states[self.apg_y].to_floats()["x"]
        test_e = test_states[self.apg_e].to_floats()["x"]
        test_vx = test_states[self.apg_x].to_floats()["v_out"]
        test_vy = test_states[self.apg_y].to_floats()["v_out"]
        test_ve = test_states[self.apg_e].to_floats()["v_out"]
        return test_x, test_y, test_e, test_vx, test_vy, test_ve

    def ext_to_code(self, dx, speed=None, axe=None, axes=None):
        if axes is None:
            axes = []

        if axe:
            axes = [axe] + axes

        if type(dx) not in (list, tuple):
            dxes = [dx] * len(axes)
        else:
            dxes = list(dx)

        assert len(dxes) == len(axes)

        if type(speed) not in (list, tuple):
            speeds = [speed] * len(axes)
        else:
            speeds = list(speed)

        assert len(speeds) == len(axes)

        max_plato_dt = 0
        max_acc_dt = 0
        no_work = True
        for i in range(len(axes)):
            axe = axes[i]
            dx = dxes[i]
            speed = speeds[i]

            if axe[0] == "-":
                axe = axe[1:]
                dx = -dx
                dxes[i] = dx
                axes[i] =  axe

            apg, speed, max_a = self.axe_params(axe, speed)
            apg_s = self.apg_states[apg]
            delta = 1 / apg_s.spm

            dx = abs(dx)
            if dx < delta:
                continue

            no_work = False

            acc_dt = speed / max_a
            full_dx = max_a * acc_dt * acc_dt  # / 2 * 2

            if dx < full_dx:
                acc_dt = sqrt(dx / max_a)
                speed = max_a * acc_dt * 0.9

                acc_dt = speed / max_a
                full_dx = max_a * acc_dt * acc_dt  # / 2 * 2

            plato_de = dx - full_dx
            plato_dt = plato_de / speed

            max_plato_dt = max(max_plato_dt, plato_dt)
            max_acc_dt = max(max_acc_dt, acc_dt)

        if no_work:
            return []

        apg_s = self.apg_states[0]
        int_acc_dt = max(5, apg_s.dt_int(max_acc_dt))
        int_plato_dt = max(5, apg_s.dt_int(max_plato_dt))
        acc_dt = apg_s.dt_float(int_acc_dt)
        plato_dt = apg_s.dt_float(int_plato_dt)

        segs = []
        segs_acc = []
        segs_dec = []
        segs_stop = []

        for i in range(len(axes)):
            axe = axes[i]
            dx = dxes[i]
            speed = speeds[i]

            apg, speed, max_a = self.axe_params(axe, speed)
            apg_s = self.apg_states[apg]

            plato_v = dx / (acc_dt + plato_dt)

            int_v = apg_s.v_int(plato_v)
            int_a = int(int_v/int_acc_dt)
            segs_acc.append(ProfileSegment(apg=apg, v=0, a=int_a, target_v=int_v))
            segs_dec.append(ProfileSegment(apg=apg, a=-int_a, target_v=0))
            segs_stop.append(ProfileSegment(apg=apg, v=0, a=0))

        segs.append([int_acc_dt + int_plato_dt, segs_acc])
        segs.append([int_acc_dt, segs_dec])
        segs.append([5, segs_stop])
        self.emu_t += int_acc_dt + int_plato_dt + int_acc_dt + 5

        print(segs)

        test_states = {k: v.copy(zero=True) for k, v in self.apg_states.items()}
        emulate(segs, apg_states=test_states)

        for i in range(len(axes)):
            axe = axes[i]
            dx = dxes[i]
            apg, speed, max_a = self.axe_params(axe, speed)

            delta = 1 / test_states[apg].spm
            test_x = test_states[apg].x_float()

            exp_int_x = int(test_states[apg].x_int(dx))
            exp_x = test_states[apg].x_float(exp_int_x)

            log.error("delta_x: %s %s %s %s %s %s", apg, test_x - exp_x, delta, test_x, exp_x, dx)
            assert abs(test_x - exp_x) < delta

        return segs

    def axe_params(self, axe, speed=None):
        if axe in ("E", 'E1'):
            assert self.spms == self.print_spms
            apg = 4
            max_a = self.max_ea
            default_speed = 6
        elif axe in ('E2'):
            assert self.spms == self.print_spms
            apg = 5
            max_a = self.max_ea
            default_speed = 2
        elif axe in ('X', "X1"):
            apg = 0
            max_a = self.max_xa
            default_speed = 150
        elif axe in ("X2"):
            apg = 1
            max_a = self.max_xa
            default_speed = 150
        elif axe in ('Y'):
            assert self.spms == self.print_spms
            apg = 2
            max_a = self.max_ya
            default_speed = 150
        elif axe in ('Z'):
            assert self.spms == self.print_spms
            apg = 3
            max_a = self.max_za
            default_speed = 5
        elif axe in ('YL'):
            assert self.spms == self.home_spms
            apg = 2
            max_a = self.max_ya
            default_speed = 150
        elif axe in ('YR'):
            assert self.spms == self.home_spms
            apg = 3
            max_a = self.max_ya
            default_speed = 150
        elif axe in ('ZFL'):
            assert self.spms == self.home_spms
            apg = 4
            max_a = self.max_za
            default_speed = 5
        elif axe in ('ZFR'):
            assert self.spms == self.home_spms
            apg = 5
            max_a = self.max_za
            default_speed = 5
        elif axe in ('ZBL'):
            assert self.spms == self.home_spms
            apg = 6
            max_a = self.max_za
            default_speed = 5
        elif axe in ('ZBR'):
            assert self.spms == self.home_spms
            apg = 7
            max_a = self.max_za
            default_speed = 5
        else:
            raise RuntimeError("Unknown axe: {}".format(axe))

        if speed is None:
            speed = default_speed

        return apg, speed, max_a

    def segment_to_code_old(self, seg, speed_k=1.0, restart=False, extruder="E1"):
        if restart:
            return []

        t0 = time.time()
        path, slowdowns = self.make_path(seg, speed_k)
        if path is None:
            return []
        slowdowns, updated, cc = self.process_corner_errors(path, slowdowns)
        slowdowns, updated = self.reverse_pass(path, slowdowns)
        slowdowns, updated = self.forward_pass(path, slowdowns)
        t1 = time.time()

        do_reset = self.last_x is None
        segments, profile = self.gen_segments_float(path, slowdowns, do_reset=do_reset, extruder=int(extruder[1]))
        t2 = time.time()
        print("Planning time:", t1 - t0)
        print("Format time:", t2 - t1)
        return profile

    def segment_to_code(self, seg, speed_k=1.0, restart=False, extruder="E1"):
        if restart:
            return []

        if extruder == "E1":
            apg_x = 0
            apg_y = 2
            apg_e = 4
            apg_z = 3
        else:
            apg_x = 1
            apg_y = 2
            apg_e = 5
            apg_z = 3

        t0 = time.time()
        path, slowdowns = self.make_path(seg, speed_k)
        if path is None:
            return []
        slowdowns, updated, cc = self.process_corner_errors(path, slowdowns)
        slowdowns, updated = self.reverse_pass(path, slowdowns)
        slowdowns, updated = self.forward_pass(path, slowdowns)

        t1 = time.time()

        all_segments = self.gen_all_segments_pandas(path, slowdowns)
        sampled = self.sample_all_segments(all_segments)
        self.smooth_and_lin_advance(sampled)
        crv, max_err = self.curve_fit(sampled, all_segments)

        do_reset = self.last_x is None

        profile = self.format_curve_to_code(
            crv, apg_x=apg_x, apg_y=apg_y, apg_e=apg_e, do_reset=do_reset)

        t2 = time.time()
        print("Planning time:", t1 - t0)
        print("Format time:", t2 - t1)
        return profile


    def gen_layers(self, input_fn, output_prefix=None, speed_k=1.0, max_layers=None):
        self.init_apgs()
        if output_prefix is None:
            output_prefix = os.path.splitext(input_fn)[0]

        lines = gcode.reader(input_fn)
        pg = gcode.path_gen(lines)
        sg = gcode.gen_segments(pg)
        layer_num = 0
        layer_data = []
        current_segment = []
        restart = False
        extruder_changed = False
        self.last_x = None
        self.last_y = None
        self.last_z = None
        self.last_extruder = "E1"

        fn_tpl = "{}_{:05d}.layer"
        for i, s in enumerate(sg):
            # print(str(s)[:100])
            if isinstance(s, gcode.do_move):
                print(i, s)
                dx = s.deltas.get("X", 0)
                dy = s.deltas.get("Y", 0)
                dz = s.deltas.get("Z", 0)

                if abs(dz) > 0 or extruder_changed:
                    if self.save_layer(current_segment, fn_tpl, layer_data, output_prefix, layer_num, restart, self.last_extruder):
                        layer_num += 1
                        print("current time:", self.emu_t, self.emu_t * self.accel_step / 50000000 / 60)

                    current_segment = []
                    ok = True

                    if extruder_changed:
                        ok = False

                    if abs(dz) > 0:
                        if self.last_z is None:
                            ok = False
                        else:
                            dz = s.target["Z"] - self.last_z
                            if abs(dz) > 1:
                                print("dz:", dz)
                                assert abs(dz) < 1

                    if (abs(dx) > 0) or (abs(dy) > 0):
                        if self.last_x is None or self.last_y is None:
                            ok = False
                        else:
                            dx = s.target["X"] - self.last_x
                            dy = s.target["Y"] - self.last_y

                    if ok:
                        if self.last_extruder == "E1":
                            x_axe = "X1"
                            x_apg = 0
                        else:
                            x_axe = "X2"
                            x_apg = 1

                        if (abs(dz) > 0):
                            cur_z = self.apg_states[3].to_floats()["x"]
                            assert abs(self.last_z - cur_z) < 0.01
                            print("generating dz={} movement".format(dz))
                            current_segment.extend(
                                self.ext_to_code(dx=dz, axe="Z")
                            )

                        if (abs(dx) > 0) or (abs(dy) > 0):
                            cur_x = self.apg_states[x_apg].to_floats()["x"]
                            cur_y = self.apg_states[2].to_floats()["x"]
                            assert abs(self.last_x - cur_x) < 0.01
                            assert abs(self.last_y - cur_y) < 0.01
                            print("generating dx={}, dy={} movement".format(dx, dy))
                            current_segment.extend(
                                self.ext_to_code(
                                    dx=[dx, dy],
                                    axes=[x_axe, "Y"]
                                )
                            )
                        emulate(
                            current_segment,
                            apg_states=self.apg_states,
                            accel_step=self.accel_step,
                            no_tracking=True,
                        )

                        tdt = 0
                        tupled_segment = []
                        for dt, segs in current_segment:
                            tupled_segment.append((dt, tuple([s.to_tuple() for s in segs])))
                            self.emu_t += dt

                        move_data = {
                            "accel_step": self.accel_step,
                            "start_state": (self.last_x, self.last_y, self.last_z),
                            "segment": tupled_segment,
                        }

                        if (abs(dx) > 0) or (abs(dy) > 0):
                            self.last_x = self.apg_states[x_apg].to_floats()["x"]
                            self.last_y = self.apg_states[2].to_floats()["x"]

                        if (abs(dz) > 0):
                            self.last_z = self.apg_states[3].to_floats()["x"]
                    else:
                        self.last_x = None
                        self.last_y = None
                        self.last_z = None
                        move_data = None

                    extruder_changed = False

                    restart = self.check_layer(fn_tpl, output_prefix, layer_num)

                    layer_data = [
                        ("start", s.target, s.deltas, (self.last_x, self.last_y, self.last_z, self.emu_t), self.last_extruder, move_data)
                    ]
                    current_segment = []

                    if self.last_z is None:
                        self.last_z = s.target["Z"]
                        self.apg_states[3].x = self.apg_states[3].x_int(self.last_z)

                    if max_layers and layer_num > max_layers:
                        print("max_layers reached")
                        return
                else:
                    assert (False)
            elif isinstance(s, gcode.do_ext):
                print(i, s)
                current_segment.extend(self.ext_to_code(dx=s.deltas["E"], speed=s.deltas["F"] / 60.0, axe=self.last_extruder))
            elif isinstance(s, gcode.do_home) or isinstance(s, gcode.do_extruder):
                print(i, s)
                if self.save_layer(current_segment, fn_tpl, layer_data, output_prefix, layer_num, restart, self.last_extruder):
                    layer_num += 1
                    print("current time:", self.emu_t, self.emu_t * self.accel_step / 50000000 / 60)
                restart = False
                current_segment = []
                if isinstance(s, gcode.do_extruder):
                    self.last_extruder = "E{}".format(s.ext + 1)
                    extruder_changed = True
                    layer_data = [("extruder_switch", s.ext)]
                else:
                    layer_data = [("do_home", s.cur_pos)]

                self.last_x = None
                self.last_y = None
                self.last_z = None

            elif isinstance(s, gcode.do_segment):
                current_segment.extend(self.segment_to_code(s.path, speed_k, restart, self.last_extruder))

                print("segment", i, len(s.path))
            else:
                assert (False)

        self.save_layer(current_segment, fn_tpl, layer_data, output_prefix, layer_num, restart, self.last_extruder)
        print("Total time:", self.emu_t,  self.emu_t * self.accel_step / 50000000 / 60)


    def save_layer(self, current_segment, fn_tpl, layer_data, output_prefix, layer_num, restart, current_extruder):
        if restart:
            return True

        if current_segment:
            tupled_segment = []
            for dt, segs in current_segment:
                tupled_segment.append((dt, tuple([s.to_tuple() for s in segs])))

            layer_data.append(("segment", {
                "accel_step": self.accel_step,
                "extruder": current_extruder,
            }, tupled_segment))
        if layer_data:
            layer_data.append(("end_state", (self.last_x, self.last_y, self.last_z, self.emu_t)))
            with open(fn_tpl.format(output_prefix, layer_num) + ".tmp", "wb") as f:
                pickle.dump(layer_data, f)
            os.rename(fn_tpl.format(output_prefix, layer_num) + ".tmp", fn_tpl.format(output_prefix, layer_num))
            return True
        return False

    def check_layer(self, fn_tpl, output_prefix, layer_num):
        fn = fn_tpl.format(output_prefix, layer_num)
        if not os.path.exists(fn):
            return False

        try:
            with open(fn_tpl.format(output_prefix, layer_num), "rb") as f:
                layer_data = pickle.load(f)
                print("first cmd:", layer_data[0])
                print("last_cmd", layer_data[-1])
        except Exception as e:
            import traceback
            import sys
            print("old layer load error:")
            traceback.print_exc(file=sys.stdout)
            return False

        if layer_data[0][0] != "start" or len(layer_data[0]) < 4:
            print("start record do not have apg_state")
            return False

        if layer_data[-1][0] != "end_state":
            print("end_state record missing")
            return False

        last_x, last_y, last_z, emu_t = layer_data[0][3]
        current_extruder = layer_data[0][4]
        n_last_x, n_last_y, n_last_z, n_emu_t = layer_data[-1][1]

        if self.last_x is not None:
            print("reusing old layer", layer_num,
                  self.last_x - last_x,
                  self.last_y - last_y,
                  self.last_z - last_z,
                  self.emu_t - emu_t)
            assert abs(self.last_x - last_x) < 0.01
            assert abs(self.last_y - last_y) < 0.01
            assert abs(self.last_z - last_z) < 0.01
            assert self.last_extruder == current_extruder
        else:
            print("reusing old first layer", layer_num)

        self.last_x = n_last_x
        self.last_y = n_last_y
        self.last_z = n_last_z
        print("current_extruder:", current_extruder)
        if current_extruder ==  "E1":
            self.apg_states[0].x = self.apg_states[0].x_int(self.last_x)
        else:
            self.apg_states[1].x = self.apg_states[1].x_int(self.last_x)
        self.apg_states[2].x = self.apg_states[2].x_int(self.last_y)
        self.apg_states[3].x = self.apg_states[3].x_int(self.last_z)
        self.emu_t = n_emu_t

        return True

