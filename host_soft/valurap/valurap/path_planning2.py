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
    max_ea = 100
    max_za = 100

    max_xv = 1000
    max_yv = 1000
    max_ev = 1000

    min_seg = 0.1
    max_delta = 0.1
    max_seg = 10.0
    spm = 80
    spme = 837
    spmz = 1600
    acc_step = 10000
    v_step = 50000000

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
        path["dt"] = path["l"] / path["v"]
        path["t"] = path["dt"].cumsum().shift(1).fillna(0)
        path = path[1:].copy()
        path["idx"] = range(len(path))
        path = path.set_index("idx")
        return path

    def filter_path(self, path):
        new_path = [path[0]]
        last_x, last_y, last_v, last_e, last_line = path[0]
        for x, y, v, e, line in path:

            dx = x - last_x
            dy = y - last_y
            de = e - last_e
            l = hypot(dx, dy)
            if l < self.min_seg:
                continue

            if l > self.max_seg:
                splits = min(5, ceil(l / self.max_seg))
                for i in range(1, splits):
                    new_path.append((
                        last_x + dx * i / splits,
                        last_y + dy * i / splits,
                        v,
                        last_e + de * i / splits,
                        line
                    ))

            new_path.append((x, y, v, e, line))
            last_x, last_y, last_v, last_e, last_line = new_path[-1]

        return new_path

    def path_from_gcode(self, gcode_path, speed_k):
        seg = np.array(gcode_path)
        path = pd.DataFrame({
            "x": seg[:, 0],
            "y": seg[:, 1],
            "v": seg[:, 2],
            "e": seg[:, 3],
            "line": np.int32(seg[:, 4]),
        })
        path["v"] *= speed_k
        return path

    def gen_speeds(self, path, slowdowns):
        speeds = pd.DataFrame()
        speeds["path"] = path["v"]
        speeds["c_in"] = path["pv"] * slowdowns["corner"]  # this corner, prev segment
        speeds["c_out"] = path["v"] * slowdowns["corner"]  # this corner, this segment
        speeds["out"] = path["v"] * (slowdowns["corner"].shift(-1).fillna(0))  # next corner c_in
        speeds["plato_base"] = np.minimum(speeds["c_out"], speeds["out"])
        speeds["plato_delta"] = path["v"] - speeds["plato_base"]
        speeds["plato"] = speeds["plato_base"] + speeds["plato_delta"] * slowdowns["plato"]
        for k in ["c_in", "c_out", "plato", "out", "plato_base"]:
            if k == "c_in":
                xp = "p"
            else:
                xp = ""
            speeds[k + "_x"] = speeds[k] * path[xp + "dx"] / path[xp + "l"]
            speeds[k + "_y"] = speeds[k] * path[xp + "dy"] / path[xp + "l"]
            speeds[k + "_x"][speeds[k] == 0] = 0
            speeds[k + "_y"][speeds[k] == 0] = 0

        speeds["unit_x"] = (path["dx"] / path["l"]).fillna(1.0)
        speeds["unit_y"] = (path["dy"] / path["l"]).fillna(0.0)
        max_a_x = np.abs(speeds["plato"] * self.max_xa / speeds["plato_x"].fillna(np.inf))
        max_a_y = np.abs(speeds["plato"] * self.max_ya / speeds["plato_y"].fillna(np.inf))
        max_a = np.minimum(max_a_x, max_a_y)
        speeds["max_a"] = max_a

        return speeds

    def process_corner_errors(self, path, slowdowns):
        speeds = self.gen_speeds(path, slowdowns)

        cc = pd.DataFrame()
        cc["dvx"] = speeds["c_out_x"] - speeds["c_in_x"]
        cc["dvy"] = speeds["c_out_y"] - speeds["c_in_y"]
        cc["dtx"] = np.abs(cc["dvx"] / self.max_xa)
        cc["dty"] = np.abs(cc["dvy"] / self.max_ya)
        cc["dt"] = np.maximum(cc["dtx"], cc["dty"])
        cc["cdt"] = cc["dt"] / 2
        cc["cdt"][0] = cc["dt"][0]

        cc["l_in"] = (cc["cdt"] * speeds["c_in"]).shift(-1).fillna(0)
        cc["l_out"] = cc["cdt"] * speeds["c_out"]
        cc["l_out"][0] = cc["dt"][0] * speeds["c_out"][0] / 2
        cc["l_free"] = path["l"] - cc["l_in"] - cc["l_out"]

        cc["ax"] = (cc["dvx"] / cc["dt"]).fillna(0)
        cc["ay"] = (cc["dvy"] / cc["dt"]).fillna(0)
        cc["mdx"] = cc["ax"] * np.square(cc["dt"] / 2) / 2
        cc["mdy"] = cc["ay"] * np.square(cc["dt"] / 2) / 2
        cc["mvx"] = (speeds["c_out_x"] + speeds["c_in_x"]) / 2
        cc["mvy"] = (speeds["c_out_y"] + speeds["c_in_y"]) / 2
        cc["md"] = norm(cc[['mdx', 'mdy']].values, axis=1)
        cc["md"][0] = 0

        cc["error_slowdown"] = 1.0 / np.sqrt(np.maximum(cc["md"] / self.max_delta, 1.0))
        cc["in_slowdown"] = 1.0 / np.sqrt(np.maximum(1.0, cc["l_in"] / path["l"] * 2.0)).shift(1).fillna(1.0)
        cc["out_slowdown"] = 1.0 / np.sqrt(np.maximum(1.0, cc["l_out"] / path["l"] * 2.0))
        cc["slowdown"] = np.minimum(np.minimum(cc["out_slowdown"], cc["in_slowdown"]), cc["error_slowdown"])

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
        next_speed = 0
        updated = 0
        for i in range(len(path) - 1, -1, -1):
            s_speeds = speeds.iloc[i]
            s_cc = cc.iloc[i]
            max_in_speed = sqrt(
                pow(next_speed, 2)
                + 2 * s_cc["l_free"] * 0.9 * s_speeds["max_a"]
            )
            k = min(1.0, max_in_speed / s_speeds["c_out"])
            if k < 0.999:
                new_slowdowns["corner"].iloc[i] = slowdowns["corner"].iloc[i] * k
                updated += 1

            next_speed = s_speeds["c_in"] * k

        if updated > 0:
            print("rp updated:", updated)

        return new_slowdowns, updated

    def forward_pass(self, path, slowdowns):
        speeds = self.gen_speeds(path, slowdowns)
        _, _, cc = self.process_corner_errors(path, slowdowns)
        new_slowdowns = slowdowns.copy()
        updated = 0
        start_speed = 0
        for i in range(0, len(path)):
            s_speeds = speeds.iloc[i]
            s_cc = cc.iloc[i]
            if i > 0:
                p_speeds = speeds.iloc[i - 1]
                max_out_speed = sqrt(
                    pow(start_speed, 2)
                    + 2 * s_cc["l_free"] * 0.9 * p_speeds["max_a"]
                )
                k = min(1.0, max_out_speed / s_speeds["c_in"])
            else:
                k = 1.0

            if k < 0.999:
                new_slowdowns["corner"].iloc[i] = slowdowns["corner"].iloc[i] * k
                updated += 1

            start_speed = s_speeds["c_out"] * k

        if updated > 0:
            print("fp updated:", updated)

        return new_slowdowns, updated


    def gen_segments_float(self, path, slowdowns):
        self.init_coefs()

        speeds = self.gen_speeds(path, slowdowns)
        _, _, cc = self.process_corner_errors(path, slowdowns)

        plato = pd.DataFrame()
        plato["start_x"] = path["px"] + speeds["unit_x"] * cc["l_out"]
        plato["start_y"] = path["py"] + speeds["unit_y"] * cc["l_out"]
        plato["start_vx"] = speeds["c_out_x"]
        plato["start_vy"] = speeds["c_out_y"]
        plato["start_v"] = speeds["c_out"]
        plato["top_vx"] = speeds["plato_x"]
        plato["top_vy"] = speeds["plato_y"]
        plato["top_v"] = speeds["plato"]
        plato["end_x"] = path["x"] - speeds["unit_x"] * cc["l_in"]
        plato["end_y"] = path["y"] - speeds["unit_y"] * cc["l_in"]
        plato["end_vx"] = speeds["out_x"]
        plato["end_vy"] = speeds["out_y"]
        plato["end_v"] = speeds["out"]

        segments = []

        first_seg = path.iloc[0]

        last_x = first_seg["px"]
        last_y = first_seg["py"]
        last_vx = 0
        last_vy = 0
        last_v = 0.0
        last_e = first_seg["pe"]
        next_e = last_e
        last_ve = 0.0

        for i in range(0, len(path)):
            print("======== {} =========".format(i))
            s_speeds = speeds.iloc[i]
            s_plato = plato.iloc[i]
            s_path = path.iloc[i]

            unit_x = s_speeds["unit_x"]
            unit_y = s_speeds["unit_y"]
            target_x = s_plato["start_x"]
            target_y = s_plato["start_y"]
            target_vx = s_plato["start_vx"]
            target_vy = s_plato["start_vy"]
            max_a = s_speeds["max_a"]

            print("corner: x: ({}, {}) -> ({}, {}) v: ({}, {}) -> ({}, {})".format(
                last_x, last_y, target_x, target_y,
                last_vx, last_vy, target_vx, target_vy,
            ))

            dvx = target_vx - last_vx
            dvy = target_vy - last_vy

            dtx = abs(dvx / self.max_xa)
            dty = abs(dvy / self.max_ya)
            dt = max(dtx, dty)
            ax = dvx / dt
            ay = dvy / dt

            if dt > 0:
                split_points = [dt]

                if (last_vx * target_vx < 0):
                    dtx = abs(last_vx/ax)
                    split_points.append(dtx)

                if (last_vy * target_vy < 0):
                    dty = abs(last_vy/ay)
                    split_points.append(dty)

                split_points.sort()
                st_x = last_x
                st_y = last_y
                st_vx =last_vx
                st_vy =last_vy
                pdt = 0.0
                for sn, dts in enumerate(split_points):
                    sp_x = st_x + st_vx * dts + ax * pow(dts, 2)/2
                    sp_y = st_y + st_vy * dts + ay * pow(dts, 2)/2
                    sp_vx = st_vx + ax * dts
                    sp_vy = st_vy + ay * dts
                    print("corner_{} ({} {}): x: ({}, {}) -> ({}, {}) v: ({}, {}) -> ({}, {})".format(
                        sn, dts, dt,
                        last_x, last_y, sp_x, sp_y,
                        last_vx, last_vy, sp_vx, sp_vy,
                    ))
                    segments.append((
                        1.0 * i, 1.0 + sn,
                        dts - pdt, ax, ay,
                        last_x, last_y,
                        sp_x, sp_y,
                        last_vx, last_vy,
                        sp_vx, sp_vy,
                    ))

                    last_x = sp_x
                    last_y = sp_y
                    last_vx = sp_vx
                    last_vy = sp_vy
                    last_v = hypot(last_vx, last_vy)
                    pdt = dts

            target_x = s_plato["end_x"]
            target_y = s_plato["end_y"]
            target_vx = s_plato["end_vx"]
            target_vy = s_plato["end_vy"]
            target_v = s_plato["end_v"]

            top_vx = s_plato["top_vx"]
            top_vy = s_plato["top_vy"]
            top_v = s_plato["top_v"]

            print("plato: x: ({}, {}) -> ({}, {}) v: ({}, {}) -> ({}, {}) -> ({}, {})".format(
                last_x, last_y, target_x, target_y,
                last_vx, last_vy, top_vx, top_vy, target_vx, target_vy,
            ))

            l = hypot(target_x - last_x, target_y - last_y)
            if l > 0:
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
                if l1 + l2 < l * 0.8:
                    print("long plato")
                else:
                    max_top_v = sqrt(2 * max_a * l + pow(last_v, 2) + pow(target_v, 2)) / sqrt(2)
                    if (max_top_v < last_v) or (max_top_v < target_v):
                        print("extra short plato", top_v, max_top_v, last_v, target_v)
                        raise RuntimeError
                    else:
                        print("short plato", top_v, max_top_v)

                    k = min(1.0, max_top_v / top_v)

                    top_vx *= k
                    top_vy *= k
                    top_v *= k

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
                    ax1 = 0
                    ay1 = 0

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
                    ax2 = 0
                    ay2 = 0

                print("l1, l2, l, fl", l1, l2, l, l - l1 - l2)
                print("dt1, dt2", dt1, dt2)
                if l - (l1 + l2) < -0.001:
                    raise RuntimeError("extra extra short plato")

                accel_x = s_plato["start_x"] + unit_x * l1
                accel_y = s_plato["start_y"] + unit_y * l1
                decel_x = s_plato["end_x"] - unit_x * l2
                decel_y = s_plato["end_y"] - unit_y * l2

                if dt1 > 0:
                    print("plato accel: x: ({}, {}) -> ({}, {}) v: ({}, {}) -> ({}, {})".format(
                        last_x, last_y, accel_x, accel_y,
                        last_vx, last_vy, top_vx, top_vy,
                    ))

                    segments.append((
                        1.0 * i, 10.0,
                        dt1, ax1, ay1,
                        last_x, last_y,
                        accel_x, accel_y,
                        last_vx, last_vy,
                        top_vx, top_vy,
                    ))

                    last_x = accel_x
                    last_y = accel_y
                    last_vx = top_vx
                    last_vy = top_vy
                    last_v = hypot(last_vx, last_vy)

                plato_l = l - l1 - l2
                dtl = plato_l / top_v

                if dtl > 0:
                    print("plato feed: x: ({}, {}) -> ({}, {}) v: ({}, {}) -> ({}, {})".format(
                        last_x, last_y, decel_x, decel_y,
                        last_vx, last_vy, top_vx, top_vy,
                    ))

                    segments.append((
                        1.0 * i, 20.0,
                        dtl, 0, 0,
                        last_x, last_y,
                        decel_x, decel_y,
                        last_vx, last_vy,
                        top_vx, top_vy,
                    ))

                    last_x = decel_x
                    last_y = decel_y
                    last_vx = top_vx
                    last_vy = top_vy
                    last_v = hypot(last_vx, last_vy)

                if dt2 > 0:
                    print("plato decel: x: ({}, {}) -> ({}, {}) v: ({}, {}) -> ({}, {})".format(
                        last_x, last_y, target_x, target_y,
                        last_vx, last_vy, target_vx, target_vy,
                    ))

                    segments.append((
                        1.0 * i, 30.0,
                        dt2, ax2, ay2,
                        last_x, last_y,
                        target_x, target_y,
                        last_vx, last_vy,
                        target_vx, target_vy,
                    ))

                    last_x = target_x
                    last_y = target_y
                    last_vx = target_vx
                    last_vy = target_vy
                    last_v = hypot(last_vx, last_vy)

        segments = np.array(segments)
        df = pd.DataFrame()
        df["i"] = segments[:, 0]
        df["st"] = segments[:, 1]
        df["dt"] = segments[:, 2]
        df["t"] = np.cumsum(df["dt"]).shift(1,fill_value=0.0)
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

        return df


    def gen_segments(self, path, slowdowns, add_reset=True):
        self.init_coefs()

        speeds = self.gen_speeds(path, slowdowns)
        _, _, cc = self.process_corner_errors(path, slowdowns)

        plato = pd.DataFrame()
        plato["start_x"] = path["px"] + speeds["unit_x"] * cc["l_out"]
        plato["start_y"] = path["py"] + speeds["unit_y"] * cc["l_out"]
        plato["start_vx"] = speeds["c_out_x"]
        plato["start_vy"] = speeds["c_out_y"]
        plato["top_vx"] = speeds["plato_x"]
        plato["top_vy"] = speeds["plato_y"]
        plato["top_v"] = speeds["plato"]
        plato["end_x"] = path["x"] - speeds["unit_x"] * cc["l_in"]
        plato["end_y"] = path["y"] - speeds["unit_y"] * cc["l_in"]
        plato["end_vx"] = speeds["out_x"]
        plato["end_vy"] = speeds["out_y"]
        plato["end_v"] = speeds["out"]


        pr_opt = []

        first_seg = path.iloc[0]

        self.last_x = first_seg["px"]
        self.last_y = first_seg["py"]
        self.last_vx = 0
        self.last_vy = 0
        self.last_v = 0.0
        self.last_e = 0.0
        self.next_e = self.last_e
        self.last_ve = 0.0

        if add_reset or not self.apg_states:
            segs = [
                ProfileSegment(
                    apg=self.apg_x, x=self.last_x * self.spm, v=0, a=0
                ),
                ProfileSegment(
                    apg=self.apg_y, x=self.last_y * self.spm, v=0, a=0
                ),
                ProfileSegment(
                    apg=self.apg_z, x=self.last_e * self.spme, v=0, a=0
                ),
            ]
            sub_profile = [[5, segs]]

            if add_reset:
                pr_opt += sub_profile

            emulate(sub_profile, apg_states=self.apg_states, accel_step=self.accel_step, no_tracking=True)
        else:
            last_x_n = self.apg_states["X"].x / self.k_xxy
            last_y_n = self.apg_states["Y"].x / self.k_xxy
            last_e_n = self.apg_states["Z"].x / self.k_xe
            print("Restarting from old state, deltas: {} {} speeds: {} {}".format(
                self.last_x - last_x_n, self.last_y - last_y_n,
                self.apg_states["X"].v, self.apg_states["Y"].v))
            self.last_x = last_x_n
            self.last_y = last_y_n
            self.last_e = last_e_n
            self.next_e = self.last_e

        for i in range(0, len(path)):
            print("======== {} =========".format(i))
            s_speeds = speeds.iloc[i]
            s_plato = plato.iloc[i]

            unit_x = s_speeds["unit_x"]
            unit_y = s_speeds["unit_y"]
            target_x = s_plato["start_x"]
            target_y = s_plato["start_y"]
            target_vx = s_plato["start_vx"]
            target_vy = s_plato["start_vy"]
            max_a = s_speeds["max_a"]

            print("corner: x: ({}, {}) -> ({}, {}) v: ({}, {}) -> ({}, {})".format(
                self.last_x, self.last_y, target_x, target_y,
                self.last_vx, self.last_vy, target_vx, target_vy,
            ))

            if (self.last_vx * target_vx > 0) and (self.last_vy * target_vy > 0):
                print("monotonic corner, do it in single step")

                sub_profile = self.calculate_single_segment(
                    self.last_vx, self.last_vy, self.last_x, self.last_y,
                    target_vx, target_vy, target_x, target_y
                )

                pr_opt += sub_profile
            else:
                print("non monotonic corner, spliting up")

                dvx = target_vx - self.last_vx
                dvy = target_vy - self.last_vy

                dtx = abs(dvx / self.max_xa)
                dty = abs(dvy / self.max_ya)
                dt = max(dtx, dty)
                ax = dvx / dt
                ay = dvy / dt

                split_points = [dt]

                if (self.last_vx * target_vx < 0):
                    dtx = abs(self.last_vx/ax)
                    split_points.append(dtx)

                if (self.last_vy * target_vy < 0):
                    dty = abs(self.last_vy/ay)
                    split_points.append(dty)

                split_points.sort()
                st_x = self.last_x
                st_y = self.last_y
                st_vx = self.last_vx
                st_vy = self.last_vy
                for sn, dts in enumerate(split_points):
                    sp_x = st_x + st_vx * dts + ax * pow(dts, 2)/2
                    sp_y = st_y + st_vy * dts + ay * pow(dts, 2)/2
                    sp_vx = st_vx + ax * dts
                    sp_vy = st_vy + ay * dts
                    print("corner_{} ({} {}): x: ({}, {}) -> ({}, {}) v: ({}, {}) -> ({}, {})".format(
                        sn, dts, dt,
                        self.last_x, self.last_y, sp_x, sp_y,
                        self.last_vx, self.last_vy, sp_vx, sp_vy,
                    ))
                    sub_profile = self.calculate_single_segment(
                        self.last_vx, self.last_vy, self.last_x, self.last_y,
                        sp_vx, sp_vy, sp_x, sp_y
                    )

                    pr_opt += sub_profile

            target_x = s_plato["end_x"]
            target_y = s_plato["end_y"]
            target_vx = s_plato["end_vx"]
            target_vy = s_plato["end_vy"]
            target_v = s_plato["end_v"]

            top_vx = s_plato["top_vx"]
            top_vy = s_plato["top_vy"]
            top_v = s_plato["top_v"]

            print("plato: x: ({}, {}) -> ({}, {}) v: ({}, {}) -> ({}, {}) -> ({}, {})".format(
                self.last_x, self.last_y, target_x, target_y,
                self.last_vx, self.last_vy, top_vx, top_vy, target_vx, target_vy,
            ))

            l = hypot(target_x - self.last_x, target_y - self.last_y)

            dvx1 = top_vx - self.last_vx
            dvy1 = top_vy - self.last_vy

            dtx1 = abs(dvx1 / self.max_xa)
            dty1 = abs(dvy1 / self.max_ya)
            dt1 = max(dtx1, dty1)
            if dt1 > 0:
                ax1 = dvx1 / dt1
                ay1 = dvy1 / dt1
                dx1 = dt1 * self.last_vx + dt1 * dt1 * ax1 / 2
                dy1 = dt1 * self.last_vy + dt1 * dt1 * ay1 / 2
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
            if l1 + l2 < l * 0.8:
                print("long plato")
            else:
                max_top_v = sqrt(2 * max_a * l + pow(self.last_v, 2) + pow(target_v, 2)) / sqrt(2)
                if (max_top_v < self.last_v) or (max_top_v < target_v):
                    print("extra short plato", top_v, max_top_v, self.last_v, target_v)
                    raise RuntimeError
                else:
                    print("short plato", top_v, max_top_v)

                k = min(1.0, max_top_v / top_v)

                top_vx *= k
                top_vy *= k

                dvx1 = top_vx - self.last_vx
                dvy1 = top_vy - self.last_vy

                dtx1 = abs(dvx1 / self.max_xa / 1.1)
                dty1 = abs(dvy1 / self.max_ya / 1.1)
                dt1 = max(dtx1, dty1)
                if dt1 > 0:
                    ax1 = dvx1 / dt1
                    ay1 = dvy1 / dt1
                    dx1 = dt1 * self.last_vx + dt1 * dt1 * ax1 / 2
                    dy1 = dt1 * self.last_vy + dt1 * dt1 * ay1 / 2
                    l1 = hypot(dx1, dy1)
                else:
                    l1 = 0

                dvx2 = target_vx - top_vx
                dvy2 = target_vy - top_vy

                dtx2 = abs(dvx2 / self.max_xa / 1.1)
                dty2 = abs(dvy2 / self.max_ya / 1.1)
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
                if l1 + l2 > l:
                    raise RuntimeError("extra extra short plato")

            accel_x = s_plato["start_x"] + unit_x * l1
            accel_y = s_plato["start_y"] + unit_y * l1
            decel_x = s_plato["end_x"] - unit_x * l2
            decel_y = s_plato["end_y"] - unit_y * l2

            print("plato accel: x: ({}, {}) -> ({}, {}) v: ({}, {}) -> ({}, {})".format(
                self.last_x, self.last_y, accel_x, accel_y,
                self.last_vx, self.last_vy, top_vx, top_vy,
            ))

            sub_profile = self.calculate_single_segment(
                self.last_vx, self.last_vy, self.last_x, self.last_y,
                top_vx, top_vy, accel_x, accel_y
            )

            print(sub_profile)
            pr_opt += sub_profile

            print("plato feed: x: ({}, {}) -> ({}, {}) v: ({}, {}) -> ({}, {})".format(
                self.last_x, self.last_y, decel_x, decel_y,
                self.last_vx, self.last_vy, top_vx, top_vy,
            ))

            sub_profile = self.calculate_single_segment(
                self.last_vx, self.last_vy, self.last_x, self.last_y,
                top_vx, top_vy, decel_x, decel_y
            )

            pr_opt += sub_profile

            print("plato decel: x: ({}, {}) -> ({}, {}) v: ({}, {}) -> ({}, {})".format(
                self.last_x, self.last_y, target_x, target_y,
                self.last_vx, self.last_vy, target_vx, target_vy,
            ))

            sub_profile = self.calculate_single_segment(
                self.last_vx, self.last_vy, self.last_x, self.last_y,
                target_vx, target_vy, target_x, target_y
            )

            pr_opt += sub_profile


        segs = [
            ProfileSegment(
                apg=self.apg_x, v=0, a=0
            ),
            ProfileSegment(
                apg=self.apg_y, v=0, a=0
            ),
            ProfileSegment(
                apg=self.apg_z, v=0, a=0
            ),
        ]
        sub_profile = [[5, segs]]
        pr_opt += sub_profile

        return pr_opt

    def calculate_single_segment(self, last_vx, last_vy, last_x, last_y, target_vx, target_vy, target_x, target_y):
        def calc_int_x(t, v=0, a=0, j=0, jj=0):
            ix = (
                v * 65536 * t
                + a * t * (t - 1) / 2
                + j * t * (t - 1) * (t - 2) / 6
                + jj * t * (t - 1) * (t - 2) * (t - 3) / 24
            )
            return ix / self.k_xxy

        def calc_int_v(t, v=0, a=0, j=0, jj=0):
            iv = (v * 65536 + a * t + j * t * (t - 1) / 2 + jj * t * (t - 1) * (t - 2) / 6)
            return iv / self.k_vxy / 65536

        def calc_int_a(t, v=0, a=0, j=0, jj=0):
            return (a + j * t + jj * t * (t - 1) / 2) / self.k_axy

        dts = []

        dx = abs(target_x - last_x)
        dy = abs(target_y - last_y)
        l = hypot(dx, dy)
        v = max(
            hypot(last_vx, last_vy),
            hypot(target_vx, target_vy)
        )

        if (dx > self.min_seg/2) and (dx / l > 0.01) and ((abs(target_vx/v) > 0.01) or (abs(last_vx / v) >  0.01)):
            dtx = 2 * (target_x - last_x) / (target_vx + last_vx)
            print("dtx", dtx)
            dts.append((dx, dtx))

        if (dy > self.min_seg/2) and (dy / l > 0.01) and ((abs(target_vy/v) > 0.01) or (abs(last_vy / v) >  0.01)):
            dty = 2 * (target_y - last_y) / (target_vy + last_vy)
            print("dty", dty)
            dts.append((dy, dty))

        if not dts:
            return []

        if 1:
            sum_dx = 0
            sum_dt = 0
            for sdx, sdt in dts:
                sum_dt += sdt * sdx
                sum_dx += sdx

            dt = sum_dt / sum_dx
        else:
            dts.sort(reverse=True)
            dt = dts[0][1]

        int_dt = int(ceil(dt * self.acc_step))
        dt = 1.0 / self.acc_step * int_dt

        retest = 0

        ax = (target_vx - last_vx) / dt
        ay = (target_vy - last_vy) / dt
        jx = 0
        jy = 0
        test_x, test_y, test_vx, test_vy = self.emu_profile(int_dt, ax, ay, jx, jy)

        if not (
                (abs(test_x - target_x) < self.max_delta / 2)
                and (abs(test_vx - target_vx) < 3)
        ):
            retest = 1
            jx = 12 * (last_x - target_x) / pow(dt, 3) + 6 * (last_vx + target_vx) / pow(dt, 2)
            ax = (target_vx - last_vx) / dt - jx * dt / 2
            ax2 = ax + jx * dt
            max_ax = max(abs(ax), abs(ax2))
            if max_ax > self.max_xa:
                jx *= (self.max_xa / max_ax) * 0.7
                ax = (target_vx - last_vx) / dt - jx * dt / 2

        if not (
                (abs(test_y - target_y) < self.max_delta / 2)
                and (abs(test_vy - target_vy) < 3)
        ):
            retest = 1
            jy = 12 * (last_y - target_y) / pow(dt, 3) + 6 * (last_vy + target_vy) / pow(dt, 2)
            ay = (target_vy - last_vy) / dt - jy * dt / 2
            ay2 = ay + jy * dt
            max_ay = max(abs(ay), abs(ay2))
            if max_ay > self.max_ya:
                jy *= (self.max_ya / max_ay) * 0.7
                ay = (target_vy - last_vy) / dt - jy * dt / 2


        if retest:
            test_x, test_y, test_vx, test_vy = self.emu_profile(int_dt, ax, ay, jx, jy)
            if not (
                    (abs(test_x - target_x) < self.max_delta * 2)
                    and (abs(test_y - target_y) < self.max_delta * 2)
                    and (abs(test_vx - target_vx) < 3)
                    and (abs(test_vy - target_vy) < 3)
            ):
                print(abs(test_x - target_x), abs(test_y - target_y), abs(test_vx - target_vx), abs(test_vy - target_vy))
                raise RuntimeError("Target precision not reached")

        int_ax = round(ax * self.k_axy)
        int_jx = round(jx * self.k_jxy)
        int_ay = round(ay * self.k_axy)
        int_jy = round(jy * self.k_jxy)
        int_tvx = round(target_vx * self.k_vxy)
        int_tvy = round(target_vy * self.k_vxy)

        ax0 = int_ax / self.k_axy
        ax1 = (int_ax + int_jx * (int_dt - 1)) / self.k_axy

        vxm = 0
        if ax0 * ax1 < 0:
            vxm = -pow(ax, 2) / 2 / jx

        ay0 = int_ay / self.k_axy
        ay1 = (int_ay + int_jy * (int_dt - 1)) / self.k_axy

        vym = 0
        if ay0 * ay1 < 0:
            vym = -pow(ay0, 2) / 2 / jy

        try:
            assert (abs(ax0) < self.max_xa * 1.5)
            assert (abs(ax1) < self.max_xa * 1.5)
            assert (abs(vxm) < self.max_xv * 1.5)
            assert (abs(ay0) < self.max_ya * 1.5)
            assert (abs(ay1) < self.max_ya * 1.5)
            assert (abs(vym) < self.max_yv * 1.5)
        except AssertionError:
            print("==== Assertion error ====")
            print("dt, int_dt, dx, dy", dt, int_dt, dx, dy)
            print("ax, jx, ax0, ax1, vxm", ax, jx, ax0, ax1, vxm)
            print("ay, jy, ay0, ay1, vym", ay, jy, ay0, ay1, vym)
            raise

        sub_profile = []
        if int_dt > 0:
            segs = [
                ProfileSegment(
                    apg=self.apg_x, a=int(int_ax), j=int(int_jx), target_v=int_tvx
                ),
                ProfileSegment(
                    apg=self.apg_y, a=int(int_ay), j=int(int_jy), target_v=int_tvy
                ),
                ProfileSegment(
                    apg=self.apg_z, a=0, j=0
                ),
            ]

            sub_profile = [[int_dt, segs]]

        print(sub_profile)

        emulate(sub_profile, apg_states=self.apg_states, accel_step=self.accel_step, no_tracking=True)

        self.last_x = self.apg_states["X"].x / self.k_xxy
        self.last_y = self.apg_states["Y"].x / self.k_xxy
        self.last_e = self.apg_states["Z"].x / self.k_xe
        self.last_vx = self.apg_states["X"].v / self.k_vxy
        self.last_vy = self.apg_states["Y"].v / self.k_vxy
        self.last_ve = self.apg_states["Z"].v / self.k_ve
        self.last_v = hypot(self.last_vx, self.last_vy)
        print("last_x", self.last_x, "last_y", self.last_y, "last_vx", self.last_vx, "last_vy", self.last_vy)
        print("d_x", self.last_x - target_x, "d_y", self.last_y - target_y, "d_vx", self.last_vx -target_vx, "d_vy", self.last_vy - target_vy)

        return sub_profile

    def emu_profile(self, int_dt, ax, ay, jx, jy):
        int_ax = round(ax * self.k_axy)
        int_ay = round(ay * self.k_axy)
        int_jx = round(jx * self.k_jxy)
        int_jy = round(jy * self.k_jxy)
        test_states = {
            "X": self.apg_states["X"].copy(),
            "Y": self.apg_states["Y"].copy(),
            "Z": self.apg_states["Z"].copy(),
        }
        test_profile = [[
            int_dt,
            [
                ProfileSegment(
                    apg=self.apg_x, a=int(int_ax), j=int(int_jx)
                ),
                ProfileSegment(
                    apg=self.apg_y, a=int(int_ay), j=int(int_jy)
                ),
                ProfileSegment(
                    apg=self.apg_z, a=0, j=0
                ),
            ]
        ]]
        emulate(test_profile, apg_states=test_states, accel_step=self.accel_step, no_tracking=True)
        test_x = test_states["X"].x / self.k_xxy
        test_y = test_states["Y"].x / self.k_xxy
        test_vx = test_states["X"].v / self.k_vxy
        test_vy = test_states["Y"].v / self.k_vxy
        return test_x, test_y, test_vx, test_vy

