from math import sqrt, ceil, pow, hypot

import numpy as np
import pandas as pd
from numpy.linalg import norm

from valurap.asg import ProfileSegment
from valurap.emulate import emulate


class FakeApg:
    def __init__(self, name):
        self.name = name


class PathPlanner:
    max_xa = 1000
    max_ya = 1000
    max_ea = 5000
    max_za = 100

    max_xv = 1000
    max_yv = 1000
    max_ev = 1000

    min_seg = 0.1
    max_delta = 0.1
    max_delta_e = 0.1
    max_seg = 30.0
    max_seg_num = 5
    min_plato_len = 1
    skip_plato_len = 0.01
    assert skip_plato_len * 3 < min_seg
    j_by_speed = False
    spm = 80
    spme = 837
    spmz = 1600
    acc_step = 10000
    v_step = 50000000

    max_a_extra = 1.2
    max_a_extra2 = 1.5
    emu_in_loop = False
    espeed_by_de = False

    delta_e_err = 1.0
    delta_ve_err = 1.0

    def init_coefs(self):
        self.v_mult = self.v_step / self.acc_step
        self.k_xxy = 2.0 ** 32 * self.spm
        self.k_vxy = 2.0 ** 32 * self.spm / self.v_step
        self.k_axy = self.k_vxy * 65536 / self.acc_step
        self.k_jxy = self.k_axy / self.acc_step
        self.k_xe = 2.0 ** 32 * self.spme
        self.k_ve = 2.0 ** 32 * self.spme / self.v_step
        self.k_ae = self.k_ve * 65536 / self.acc_step
        self.k_je = self.k_ae / self.acc_step
        self.k_xz = 2.0 ** 32 * self.spmz
        self.k_vz = 2.0 ** 32 * self.spmz / self.v_step
        self.k_az = self.k_vz * 65536 / self.acc_step
        self.k_jz = self.k_az / self.acc_step

        self.int_max_ax = self.max_xa * self.k_axy * 1.2
        self.int_max_ay = self.max_ya * self.k_axy * 1.2
        self.int_max_ae = self.max_ea * self.k_ae * 1.2
        self.int_max_az = self.max_za * self.k_az * 1.2
        self.accel_step = self.v_step / self.acc_step

    def __init__(self, apgs=None):
        if apgs is None:
            apgs = {}

        self.apgs = apgs
        for l in ["X", "Y", "Z"]:
            apgs.setdefault(l, FakeApg(l))

        self.apg_states = {}
        self.init_coefs()

    @property
    def apg_x(self):
        return self.apgs["X"]

    @property
    def apg_y(self):
        return self.apgs["Y"]

    @property
    def apg_z(self):
        return self.apgs["Z"]

    def make_path(self, gcode_path, speed_k=1.0):
        filtered_path = self.filter_path(gcode_path)
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
        new_path = []
        last_x, last_y, last_v, last_e, last_line = path[0]
        last_sn = len(path) - 1
        for s_n, (x, y, v, e, line) in enumerate(path):

            dx = x - last_x
            dy = y - last_y
            de = e - last_e
            l = hypot(dx, dy)

            if l > self.max_seg:
                splits = min(self.max_seg_num, ceil(l / self.max_seg))
                for i in range(1, splits):
                    new_path.append(
                        (
                            last_x + dx * i / splits,
                            last_y + dy * i / splits,
                            v,
                            last_e + de * i / splits,
                            line,
                        )
                    )
            elif s_n > 0 and s_n < last_sn and l < self.min_seg:
                continue

            new_path.append((x, y, v, e, line))
            last_x, last_y, last_v, last_e, last_line = new_path[-1]

        return new_path

    def path_from_gcode(self, gcode_path, speed_k):
        seg = np.array(gcode_path)
        path = pd.DataFrame(
            {
                "x": seg[:, 0],
                "y": seg[:, 1],
                "v": seg[:, 2],
                "e": seg[:, 3],
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

        for k in ["entry", "exit", "plato", "path"]:
            speeds[k + "_x"] = speeds[k] * speeds["unit_x"]
            speeds[k + "_y"] = speeds[k] * speeds["unit_y"]

        max_a_x = np.abs(self.max_xa / speeds["unit_x"].fillna(np.inf))
        max_a_y = np.abs(self.max_ya / speeds["unit_y"].fillna(np.inf))
        max_a = np.minimum(max_a_x, max_a_y)
        speeds["max_a"] = max_a  # max accell for not componentized move

        speeds["p_unit_x"] = speeds["unit_x"].shift(1).fillna(1.0)
        speeds["p_unit_y"] = speeds["unit_x"].shift(1).fillna(1.0)

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
                print("no correction needed", i, cur_plato_min, l_free)
                skip = True
            elif entry_speed < corrected_exit_speed:
                print("accelerating segment, skipping", i, entry_speed, corrected_exit_speed)
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

            print("Calculated k:", k)

            if k < 0.999999:
                updated += 1
                k *= 0.98
            else:
                k = 1.0

            if entry_speed * k < corrected_exit_speed:
                k = corrected_exit_speed / entry_speed
                print("segment tries to reverse, capping", k)

            corr_dt = abs((corrected_exit_speed - entry_speed * k) / max_a)
            corr_plato_min = (corrected_exit_speed + entry_speed * k) / 2 * corr_dt
            corr_free = l_total - l_entry * k * k  - corrected_l_exit - corr_plato_min

            print("{}: correction results: total: {} free: {}: new free: {} target: {} final: {}".format(i, l_total, l_free, corr_free, l_target, corr_plato_min + l_entry * k * k))

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
                next_entry_speed = ns_speeds["entry"]
                next_l_entry = ns_cc["l_entry"]
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
                print("no correction needed", i, cur_plato_min, l_free)
                skip = True
            elif exit_speed < corrected_entry_speed:
                print("decelerating segment, skipping", i, corrected_entry_speed, exit_speed)
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

            print("Calculated k:", k)

            if k < 0.999999:
                updated += 1
                k *= 0.98
            else:
                k = 1.0

            if exit_speed * k < corrected_entry_speed:
                k = corrected_entry_speed / exit_speed
                print("segment tries to reverse, capping", k)

            corr_dt = abs((corrected_entry_speed - exit_speed * k) / max_a)
            corr_plato_min = (corrected_entry_speed + exit_speed * k) / 2 * corr_dt
            corr_free = l_total - l_exit * k * k  - corrected_l_entry - corr_plato_min

            print("{}: correction results: total: {} free: {}: new free: {} target: {} final: {}".format(i, l_total, l_free, corr_free, l_target, corr_plato_min + l_exit * k * k))

            corrected_entry_speed = next_entry_speed * k
            corrected_l_entry = next_l_entry * k * k
            new_slowdowns["corner"].iloc[i + 1] = slowdowns["corner"].iloc[i + 1] * k

        if updated > 0:
            print("fp updated:", updated)

        return new_slowdowns, updated

    def gen_segments_float(self, path, slowdowns):
        self.init_coefs()

        speeds = self.gen_speeds(path, slowdowns)
        _, _, cc = self.process_corner_errors(path, slowdowns)

        plato = pd.DataFrame()
        plato["start_x"] = path["px"] + speeds["unit_x"] * cc["l_entry"]
        plato["start_y"] = path["py"] + speeds["unit_y"] * cc["l_entry"]
        plato["start_vx"] = speeds["entry_x"]
        plato["start_vy"] = speeds["entry_y"]
        plato["start_v"] = speeds["entry"]
        plato["top_vx"] = speeds["plato_x"]
        plato["top_vy"] = speeds["plato_y"]
        plato["top_v"] = speeds["plato"]
        plato["end_x"] = path["x"] - speeds["unit_x"] * cc["l_exit"]
        plato["end_y"] = path["y"] - speeds["unit_y"] * cc["l_exit"]
        plato["end_vx"] = speeds["exit_x"]
        plato["end_vy"] = speeds["exit_y"]
        plato["end_v"] = speeds["exit"]
        plato["unit_e"] = (path["de"] / path["l"]).fillna(0)
        plato["start_e"] = path["pe"] + plato["unit_e"] * cc["l_entry"]
        plato["end_e"] = path["pe"] + plato["unit_e"] * (path["l"] - cc["l_exit"])

        emu_in_loop = self.emu_in_loop

        segments = []
        profile = []

        first_seg = path.iloc[0]

        last_x = first_seg["px"]
        last_y = first_seg["py"]
        last_vx = 0
        last_vy = 0
        last_v = 0.0
        last_e = first_seg["pe"]
        next_e = last_e
        last_ve = 0.0

        if emu_in_loop:
            segs = [
                ProfileSegment(apg=self.apg_x, x=last_x * self.spm, v=0, a=0),
                ProfileSegment(apg=self.apg_y, x=last_y * self.spm, v=0, a=0),
                ProfileSegment(apg=self.apg_z, x=last_e * self.spme, v=0, a=0),
            ]
            sub_profile = [[5, segs]]
            emulate(
                sub_profile,
                apg_states=self.apg_states,
                accel_step=self.accel_step,
                no_tracking=True,
            )
            profile.extend(sub_profile)

        last_i = len(path) - 1
        for i in range(0, last_i + 1):
            s_speeds = speeds.iloc[i]
            s_plato = plato.iloc[i]
            s_path = path.iloc[i]
            print("======== {} L{} =========".format(i, s_path["line"]))

            unit_x = s_speeds["unit_x"]
            unit_y = s_speeds["unit_y"]
            unit_e = s_plato["unit_e"]
            target_x = s_plato["start_x"]
            target_y = s_plato["start_y"]
            target_e = s_plato["start_e"]
            target_vx = s_plato["start_vx"]
            target_vy = s_plato["start_vy"]
            max_a = s_speeds["max_a"]

            print(
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

            if self.espeed_by_de:
                # eq: [
                #     v_1 = v_0 + a * dt,
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
                for sn, dts in enumerate(split_points):
                    sp_x = st_x + st_vx * dts + ax * pow(dts, 2) / 2
                    sp_y = st_y + st_vy * dts + ay * pow(dts, 2) / 2
                    sp_e = st_e + st_ve * dts + ae * pow(dts, 2) / 2
                    sp_vx = st_vx + ax * dts
                    sp_vy = st_vy + ay * dts
                    sp_ve = st_ve + ae * dts
                    print(
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

            print(
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
                print("plato is too short, skipped", l, self.skip_plato_len)
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

                print("l1, l2, l, fl", l1, l2, l, l - l1 - l2)
                print("dt1, dt2", dt1, dt2)
                if (l >= self.min_plato_len) and (l1 + l2 < l * 0.8):
                    print("long plato")
                else:
                    max_a_k = max_a * self.max_a_extra
                    max_top_v = sqrt(2 * max_a_k * l + pow(last_v, 2) + pow(target_v, 2)) / sqrt(2)

                    if (max_top_v < last_v) or (max_top_v < target_v) or (l < self.min_plato_len):
                        if last_v > target_v:
                            print("single segment plato (top = last)")
                            top_v = last_v
                            top_vx = last_vx
                            top_vy = last_vy
                        else:
                            print("single segment plato (top = target)")
                            top_v = target_v
                            top_vx = target_vx
                            top_vy = target_vy
                    else:
                        print("short plato", top_v, max_top_v)

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

                print("l1, l2, l, fl", l1, l2, l, l - l1 - l2)
                print("dt1, dt2", dt1, dt2)
                if l - (l1 + l2) < -0.001:
                    raise RuntimeError("extra extra short plato: l: {} l1: {} l2: {} d: {}".format(l, l1, l2, l - l1 - l2))

                accel_x = s_plato["start_x"] + unit_x * l1
                accel_y = s_plato["start_y"] + unit_y * l1
                accel_e = s_plato["start_e"] + unit_e * l1
                if self.espeed_by_de:
                    accel_ve = (accel_e - last_e) * 2 / dt1 - last_ve
                else:
                    accel_ve = s_plato["top_v"] * s_speeds["v_to_ve"]

                if dt1 > 0:
                    print(
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
                if self.espeed_by_de:
                    decel_ve = (decel_e - last_e) * 2 / dtl - last_ve
                else:
                    decel_ve = s_plato["top_v"] * s_speeds["v_to_ve"]

                if dtl > 0:
                    print(
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
                    if self.espeed_by_de:
                        target_ve = (target_e - last_e) * 2 / dt2 - last_ve
                    else:
                        target_ve = s_plato["end_v"] * s_speeds["v_to_ve"]
                    print(
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

        if emu_in_loop:
            segs = [
                ProfileSegment(apg=self.apg_x, v=0, a=0),
                ProfileSegment(apg=self.apg_y, v=0, a=0),
                ProfileSegment(apg=self.apg_z, v=0, a=0),
            ]
            sub_profile = [[5, segs]]
            emulate(
                sub_profile,
                apg_states=self.apg_states,
                accel_step=self.accel_step,
                no_tracking=True,
            )
            profile.extend(sub_profile)

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
        int_dt = int(ceil(dt * self.acc_step))
        dt = 1.0 / self.acc_step * int_dt

        retest = 0

        ax = (target_vx - last_vx) / dt
        ay = (target_vy - last_vy) / dt
        ae = (target_ve - last_ve) / dt
        jx = 0
        jy = 0
        je = 0
        int_last_vx = self.apg_states["X"].v
        int_last_vy = self.apg_states["Y"].v
        int_last_ve = self.apg_states["Z"].v
        int_ax = round(ax * self.k_axy)
        int_ay = round(ay * self.k_axy)
        int_ae = round(ae * self.k_ae)
        int_tvx = round(target_vx * self.k_vxy)
        int_tvy = round(target_vy * self.k_vxy)
        int_tve = round(target_ve * self.k_ve)
        int_jx = 0
        int_jy = 0
        int_je = 0

        test_x, test_y, test_e, test_vx, test_vy, test_ve = self.emu_profile(int_dt, int_ax, int_ay, int_ae, int_jx, int_jy, int_je, int_tvx, int_tvy, int_tve)

        if not ((abs(test_x - target_x) < self.max_delta / 2) and (abs(test_vx - target_vx) < 1)):
            retest = 1
            jx = 12 * (last_x - target_x) / pow(dt, 3) + 6 * (last_vx + target_vx) / pow(dt, 2)
            ax = (target_vx - last_vx) / dt - jx * dt / 2
            ax2 = ax + jx * dt
            max_ax = max(abs(ax), abs(ax2))
            if max_ax > self.max_xa * self.max_a_extra2:
                print("CAP FOR MAX_XA", max_ax, self.max_xa)
                jx *= (self.max_xa / max_ax) * 0.7
                ax = (target_vx - last_vx) / dt - jx * dt / 2

        if not ((abs(test_y - target_y) < self.max_delta / 2) and (abs(test_vy - target_vy) < 1)):
            retest = 1
            jy = 12 * (last_y - target_y) / pow(dt, 3) + 6 * (last_vy + target_vy) / pow(dt, 2)
            ay = (target_vy - last_vy) / dt - jy * dt / 2
            ay2 = ay + jy * dt
            max_ay = max(abs(ay), abs(ay2))
            if max_ay > self.max_ya * self.max_a_extra2:
                print("CAP FOR MAX_YA", max_ay, self.max_ya)
                jy *= (self.max_ya / max_ay) * 0.7
                ay = (target_vy - last_vy) / dt - jy * dt / 2

        if not ((abs(test_e - target_e) < self.max_delta_e / 2) and (abs(test_ve - target_ve) < 1)):
            retest = 1
            je = 12 * (last_e - target_e) / pow(dt, 3) + 6 * (last_ve + target_ve) / pow(dt, 2)
            ae = (target_ve - last_ve) / dt - je * dt / 2
            ae2 = ae + je * dt
            max_ae = max(abs(ae), abs(ae2))
            if max_ae > self.max_ea * self.max_a_extra2:
                print("CAP FOR MAX_EA", max_ae, self.max_ea)
                je *= (self.max_ea / max_ae) * 0.7
                ae = (target_ve - last_ve) / dt - je * dt / 2

        if retest:
            int_last_vx = self.apg_states["X"].v
            int_last_vy = self.apg_states["Y"].v
            int_last_ve = self.apg_states["Z"].v
            int_tvx = round(target_vx * self.k_vxy)
            int_tvy = round(target_vy * self.k_vxy)
            int_tve = round(target_ve * self.k_ve)
            int_ax = round(ax * self.k_axy)
            int_ay = round(ay * self.k_axy)
            int_ae = round(ae * self.k_ae)
            int_jx = round(jx * self.k_jxy)
            int_jy = round(jy * self.k_jxy)
            int_je = round(je * self.k_je)

            if self.j_by_speed:
                # eq: [
                #     tvx = vx + avg_ax * dt,
                #     avg_ax = (ax + tax) / 2,
                #     tax = ax + j * dt
                # ];
                # solve(eq, [avg_ax, tax, j]);
                #
                # j=-(2*vx-2*tvx+2*ax*dt)/dt^2
                int_jx2 = -round((2 * int_last_vx * 65536 - 2 * int_tvx * 65536 + 2 * int_ax * int_dt) / (int_dt ** 2))
                int_jy2 = -round((2 * int_last_vy * 65536 - 2 * int_tvy * 65536 + 2 * int_ay * int_dt) / (int_dt ** 2))
                int_je2 = -round((2 * int_last_ve * 65536 - 2 * int_tve * 65536 + 2 * int_ae * int_dt) / (int_dt ** 2))
                print("int_j:", int_jx, int_jx2, int_jy, int_jy2, int_je, int_je2)

                int_jx = int_jx2
                int_jy = int_jy2
                int_je = int_je2

            test_x, test_y, test_e, test_vx, test_vy, test_ve = self.emu_profile(int_dt, int_ax, int_ay, int_ae, int_jx, int_jy, int_je, int_tvx, int_tvy, int_tve)
            if not (
                (abs(test_x - target_x) < self.max_delta * 2)
                and (abs(test_y - target_y) < self.max_delta * 2)
                and (abs(test_e - target_e) < self.max_delta_e * 10 * self.delta_e_err)
                and (abs(test_vx - target_vx) < 2)
                and (abs(test_vy - target_vy) < 2)
                and (abs(test_ve - target_ve) < 2 * self.delta_ve_err)
            ):
                raise RuntimeError("Target precision not reached dx: {} dy: {} de: {} dvx: {} dvy: {} dve: {}".format(
                    abs(test_x - target_x),
                    abs(test_y - target_y),
                    abs(test_e - target_e),
                    abs(test_vx - target_vx),
                    abs(test_vy - target_vy),
                    abs(test_ve - target_ve)
                ))

        print("int_v:", int_last_vx, int_tvx, int_last_vy, int_tvy, int_last_ve, int_tve)
        print("int_j:", int_jx, int_jy, int_je)

        ax0 = int_ax / self.k_axy
        ax1 = (int_ax + int_jx * (int_dt - 1)) / self.k_axy

        vxm = 0
        if (jx != 0) and (ax0 * ax1 < 0):
            vxm = -pow(ax, 2) / 2 / jx

        ay0 = int_ay / self.k_axy
        ay1 = (int_ay + int_jy * (int_dt - 1)) / self.k_axy

        vym = 0
        if (jy != 0) and (ay0 * ay1 < 0):
            vym = -pow(ay0, 2) / 2 / jy

        ae0 = int_ae / self.k_ae
        ae1 = (int_ae + int_je * (int_dt - 1)) / self.k_ae

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
            print("==== Assertion error ====")
            print("dt, int_dt, dx, dy, de", dt, int_dt, target_x - last_x, target_y - last_y, target_e - last_e)
            print("ax, jx, ax0, ax1, vxm", ax, jx, ax0, ax1, vxm)
            print("ay, jy, ay0, ay1, vym", ay, jy, ay0, ay1, vym)
            print("ae, je, ae0, ae1, vem", ae, je, ae0, ae1, vem)
            raise

        sub_profile = []
        if int_dt > 0:
            segs = [
                ProfileSegment(apg=self.apg_x, a=int(int_ax), j=int(int_jx), target_v=int_tvx),
                ProfileSegment(apg=self.apg_y, a=int(int_ay), j=int(int_jy), target_v=int_tvy),
                ProfileSegment(apg=self.apg_z, a=int(int_ae), j=int(int_je), target_v=int_tve),
            ]

            sub_profile = [[int_dt, segs]]

        print(sub_profile)

        emulate(
            sub_profile, apg_states=self.apg_states, accel_step=self.accel_step, no_tracking=True
        )

        self.last_x = self.apg_states["X"].x / self.k_xxy
        self.last_y = self.apg_states["Y"].x / self.k_xxy
        self.last_e = self.apg_states["Z"].x / self.k_xe
        self.last_vx = self.apg_states["X"].v / self.k_vxy
        self.last_vy = self.apg_states["Y"].v / self.k_vxy
        self.last_ve = self.apg_states["Z"].v / self.k_ve
        self.last_v = hypot(self.last_vx, self.last_vy)
        print(
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
        print(
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

        return sub_profile

    def emu_profile(self, int_dt, int_ax, int_ay, int_ae, int_jx, int_jy, int_je, int_tvx, int_tvy, int_tve):
        test_states = {
            "X": self.apg_states["X"].copy(),
            "Y": self.apg_states["Y"].copy(),
            "Z": self.apg_states["Z"].copy(),
        }
        test_profile = [
            [
                int_dt,
                [
                    ProfileSegment(apg=self.apg_x, a=int(int_ax), j=int(int_jx), target_v=int_tvx),
                    ProfileSegment(apg=self.apg_y, a=int(int_ay), j=int(int_jy), target_v=int_tvy),
                    ProfileSegment(apg=self.apg_z, a=int(int_ae), j=int(int_je), target_v=int_tve),
                ],
            ]
        ]
        print("testing: ", test_profile)
        emulate(test_profile, apg_states=test_states, accel_step=self.accel_step, no_tracking=True)
        test_x = test_states["X"].x / self.k_xxy
        test_y = test_states["Y"].x / self.k_xxy
        test_e = test_states["Z"].x / self.k_xe
        test_vx = test_states["X"].v / self.k_vxy
        test_vy = test_states["Y"].v / self.k_vxy
        test_ve = test_states["Z"].v / self.k_ve
        return test_x, test_y, test_e, test_vx, test_vy, test_ve
