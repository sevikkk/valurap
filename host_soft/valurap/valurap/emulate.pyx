from math import copysign

import pandas as pd
from numpy.linalg import norm

from valurap.asg import ProfileSegment


cdef class ApgState(object):
    cdef public long x
    cdef public long v
    cdef public long a
    cdef public long j
    cdef public long jj
    cdef public long target_v
    cdef public int target_v_set
    cdef public long accel_step

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
            self.x = int(seg.x * 2 ** 32)
        if seg.v is not None:
            self.v = int(seg.v)
        if seg.a is not None:
            self.a = int(seg.a)
        if seg.j is not None:
            self.j = int(seg.j)
        if seg.jj is not None:
            self.jj = int(seg.jj)
        if seg.target_v is not None:
            self.target_v = int(seg.target_v)
            self.target_v_set = True
        else:
            self.target_v_set = False

    def step(self):
        next_x = self.x + self.v * self.accel_step
        next_v = int(self.v + (self.a >> 16))
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


def emulate(profile, verbose=0, apg_states=None, accel_step=50000, no_tracking=False):
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
        axis_segs = {"X": None, "Y": None, "Z": None}

        for seg in segs:
            axis_segs[seg.apg.name] = seg

        for axis_name, seg in axis_segs.items():
            if verbose > 0:
                print("  ", seg)
            state = apg_states[axis_name]
            if seg:
                state.load(seg)
            prefix = axis_name + "_"

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
                if not no_tracking:
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

    if not no_tracking:
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


class FakeApg:
    def __init__(self, name):
        self.name = name


max_xa = 1000
max_ya = 1000
max_ea = 1000
max_delta = 0.1
spm = 80
spme = 837
acc_step = 10000
v_step = 50000000
v_mult = v_step / acc_step


def format_segments(all_segments, apgs=None, acc_step=1000):
    if apgs is None:
        apgs = {}

    apg_states = {}

    apg_x = apgs.get("X", FakeApg("X"))
    apg_y = apgs.get("Y", FakeApg("Y"))
    apg_z = apgs.get("Z", FakeApg("Z"))

    v_step = 50000000
    v_mult = v_step / acc_step

    k_xxy = 2.0 ** 32 * spm
    k_vxy = 2.0 ** 32 * spm / v_step
    k_xe = 2.0 ** 32 * spme
    k_ve = 2.0 ** 32 * spme / v_step
    k2_30 = 2 ** 30

    int_max_ax = max_xa * k_vxy * 65536 / acc_step * 1.2
    int_max_ay = max_ya * k_vxy * 65536 / acc_step * 1.2
    int_max_ae = max_ea * k_ve * 65536 / acc_step * 1.2

    pr_opt = []
    first_row = all_segments.iloc[0]
    last_x = first_row["x0"]
    last_y = first_row["y0"]
    last_vx = first_row["vx0"]
    last_vy = first_row["vy0"]
    last_e = 0.0
    next_e = 0.0
    last_ve = 0.0
    assert last_vx == 0
    assert last_vy == 0
    segs = [
        ProfileSegment(
            apg=apg_x, x=last_x * spm, v=0, a=0
        ),
        ProfileSegment(
            apg=apg_y, x=last_y * spm, v=0, a=0
        ),
        ProfileSegment(
            apg=apg_z, x=last_e * spme, v=0, a=0
        ),
    ]

    sub_profile = [[5, segs]]
    pr_opt += sub_profile

    emulate(sub_profile, apg_states=apg_states, accel_step=50000000 / acc_step, no_tracking=True)
    #print(apg_states["X"], apg_states["Y"])

    for index, up_row in all_segments.iterrows():
        if 0:
            if index > 55:
                print("last_x:", last_x, "last_y:", last_y)
                print("last_vx:", last_vx, "last_vy:", last_vy)
                break

        print("index:", index, up_row["seg_type"])

        tde = up_row["de"]
        if up_row["dt"] < 0.2: # and abs(tde < 0.001):
            rows = [up_row]
        else:
            tx0 = up_row["x0"]
            ty0 = up_row["y0"]
            tx1 = up_row["x1"]
            ty1 = up_row["y1"]
            tl = norm([tx1 - tx0, ty1 - ty0])
            tvx0 = up_row["vx0"]
            tvy0 = up_row["vy0"]
            tvx1 = up_row["vx1"]
            tvy1 = up_row["vy1"]
            lx1 = tx0
            ly1 = ty0
            lvx1 = tvx0
            lvy1 = tvy0

            splits = int(up_row["dt"] / 0.15)
            if 0:
                if abs(tde) > 0:
                    splits = max(splits, 3)

            #print("long segment, split up", splits)

            dvx = (tvx1 - tvx0) / splits
            dvy = (tvy1 - tvy0) / splits
            dt = up_row["dt"] / splits
            rows = []
            for i in range(splits):
                cvx1 = lvx1 + dvx
                cvy1 = lvy1 + dvy
                cx1 = lx1 + (lvx1 + dvx / 2) * dt
                cy1 = ly1 + (lvy1 + dvy / 2) * dt
                cl = norm([cx1 - lx1, cy1 - ly1])
                de = tde / tl * cl
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
                        "de": de
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
            next_e += row["de"]
            dt = row["dt"]

            dx = next_x - last_x
            dy = next_y - last_y
            de = next_e - last_e
            dvx = next_vx - last_vx
            dvy = next_vy - last_vy

            exp_de = row["de"]
            avg_ve = (next_e - last_e) / dt
            exp_ve = exp_de / dt
            next_ve = 2 * avg_ve - last_ve
            if 1:
                if abs(exp_ve) > 0.1:
                    if abs((next_ve - exp_ve) / exp_ve) > 0.05:
                        next_ve = exp_ve + copysign(abs(exp_ve * 0.05), next_ve - exp_ve)

            if next_ve > 0:
                next_ve = 0

            ae = (next_ve - last_ve)/dt
            if abs(ae) > max_ea:
                print("limit ae", ae, next_ve, last_ve)
                ae = copysign(max_ea, ae)
                next_ve = last_ve + ae * dt
                print("  ae:", ae, next_ve, last_ve)

            #print("x:", last_x, row["x0"])
            #print("y:", last_y, row["y0"])
            #print("vx:", last_vx, row["vx0"])
            #print("vy:", last_vy, row["vy0"])
            #print("ve:", last_ve, exp_ve)
            #print("dx:", dx)
            #print("dy:", dy)
            #print("dvx:", dvx)
            #print("dvy:", dvy)
#
            int_dt = round(dt * acc_step)

            if int_dt == 0:
                int_dt = 1

            #print("int_dt:", int_dt)

            int_vx0 = round(last_vx * k_vxy)
            int_vy0 = round(last_vy * k_vxy)
            int_ve0 = round(last_ve * k_ve)
            int_vx1 = round(next_vx * k_vxy)
            int_vy1 = round(next_vy * k_vxy)
            int_ve1 = round(next_ve * k_ve)
            int_ax = round((int_vx1 - int_vx0) / int_dt) * 65536
            int_ay = round((int_vy1 - int_vy0) / int_dt) * 65536
            int_ae = round((int_ve1 - int_ve0) / int_dt) * 65536
            #print("int_dx:", dx * 2 ** 32 * spm, "int_dy:", dy * 2**32 * spm)
            #print("int_vx0:", int_vx0, "int_vy0:", int_vy0, "int_ve0:", int_ve0)
            #print("int_vx1:", int_vx1, "int_vy1:", int_vy1, "int_ve1:", int_ve1)
            #print("int_ax:", int_ax, int_ax / 2**32, "int_ay1:", int_ay, int_ay / 2**32, "int_ae1", int_ae, int_ae / 2**32)

            real_dx = int_x(int_dt, int_vx0 * 65536, int_ax, 0, 0) / 65536 * v_mult
            real_dy = int_x(int_dt, int_vy0 * 65536, int_ay, 0, 0) / 65536 * v_mult
            real_de = int_x(int_dt, int_ve0 * 65536, int_ae, 0, 0) / 65536 * v_mult
            x_error = dx * k_xxy - real_dx
            y_error = dy * k_xxy - real_dy
            e_error = de * k_xe - real_de

            if abs(x_error / k_xxy) > 0.001:
                #print("x_error to big", x_error / 2**32/spm)
                while True:
                    #print("x_error:", x_error / 2 ** 32 / spm)
                    int_jx = round(-12 * x_error / int_dt / int_dt / int_dt * 65536 / v_mult)
                    int_ax0 = round(int_ax - int_jx * int_dt / 2)
                    int_ax1 = round(int_ax + int_jx * int_dt / 2)
                    corrected_ax = max(abs(int_ax0), abs(int_ax1))
                    if corrected_ax > int_max_ax:
                        x_error = x_error * 0.8
                        print("max_ax violation, slow down", x_error, corrected_ax, int_max_ax)
                        if abs(x_error / k_xxy) < 0.0001:
                            print("no way to fix, ignoring")
                            int_jx = 0
                            int_ax0 = int_ax
                            break
                    else:
                        break
                int_jx = int(int_jx)
                int_ax = int(int_ax0)
            else:
                int_jx = 0
            #print("x_error:", x_error / 2.0 ** 32 / spm, "int_jx:", int_jx, "int_ax:", int_ax)

            if abs(y_error / k_xxy) > 0.001:
                #print("y_error to big", y_error/2**32/spm)
                retry = True
                while retry:
                    #print("y_error:", y_error / 2 ** 32 / spm)
                    int_jy = round(-12 * y_error / int_dt / int_dt / int_dt * 65536 / v_mult)
                    int_ay0 = round(int_ay - int_jy * int_dt / 2)
                    int_ay1 = round(int_ay + int_jy * int_dt / 2)
                    corrected_ay = max(abs(int_ay0), abs(int_ay1))
                    if corrected_ay > int_max_ay:
                        print("max_ay violation, slow down", y_error, corrected_ay, int_max_ay)
                        y_error = y_error * 0.8
                        if abs(y_error / k_xxy) < 0.0001:
                            print("no way to fix, ignoring")
                            int_jy = 0
                            int_ay0 = int_ay
                            break
                    else:
                        break
                int_jy = int(int_jy)
                int_ay = int(int_ay0)
            else:
                int_jy = 0
            #print("y_error:", y_error / 2.0 ** 32 / spm, "int_jy:", int_jy, "int_ay:", int_ay)

            if abs(e_error / k_xe) > 0.001:
                #print("e_error to big", e_error/2**32/spme)
                retry = True
                while retry:
                    #print("e_error:", e_error / 2 ** 32 / spme)
                    int_je = round(-12 * e_error / int_dt / int_dt / int_dt * 65536 / v_mult)
                    int_ae0 = round(int_ae - int_je * int_dt / 2)
                    int_ae1 = round(int_ae + int_je * int_dt / 2)
                    corrected_ae = max(abs(int_ae0), abs(int_ae1))
                    if corrected_ae > int_max_ae:
                        print("max_ae violation, slow down", e_error, corrected_ae, int_max_ae)
                        e_error = e_error * 0.8
                        if abs(e_error / k_xe) < 0.0001:
                            print("no way to fix, ignoring")
                            int_je = 0
                            int_ae0 = int_ae
                            break
                    else:
                        break
                int_je = int(int_je)
                int_ae = int(int_ae0)
            else:
                int_je = 0
            #print("e_error:", e_error / 2.0 ** 32 / spme, "int_je:", int_je, "int_ae:", int_ae)


            segs = [
                ProfileSegment(
                    #apg=apg_x, v = int(int_vx0), a=int(int_ax), j=int(int_jx)
                    apg = apg_x, a = int(int_ax), j = int(int_jx)
            ),
                ProfileSegment(
                    # apg=apg_y, v = int(int_vy0), a=int(int_ay), j=int(int_jy)
                    apg=apg_y, a=int(int_ay), j=int(int_jy)
                ),
                ProfileSegment(
                    #apg=apg_y, v = int(int_vy0), a=int(int_ay), j=int(int_jy)
                    apg = apg_z, a = int(int_ae), j = int(int_je)
            ),
            ]

            sub_profile = [[int(int_dt), segs]]
            pr_opt += sub_profile

            res = emulate(sub_profile, apg_states=apg_states, accel_step=50000000 / acc_step, no_tracking=True)

            last_x = apg_states["X"].x / k_xxy
            last_y = apg_states["Y"].x / k_xxy
            last_e = apg_states["Z"].x / k_xe
            last_vx = apg_states["X"].v / k_vxy
            last_vy = apg_states["Y"].v / k_vxy
            last_ve = apg_states["Z"].v / k_ve

            if 0:
                print("final x_error:", last_x - next_x)
                print("final y_error:", last_y - next_y)
                print("final e_error:", last_e - next_e)
                print("final vx_error:", last_vx - next_vx)
                print("final vy_error:", last_vy - next_vy)
                print("final ve_error:", last_ve - next_ve)

            if 0:
                res["xv"] = res["X_v"] * 65536 / k_vxy
                res["yv"] = res["Y_v"] * 65536 / k_vxy
                res["ev"] = res["Z_v"] * 65536 / k_ve

                # print("ApgStates:", apg_states["X"].x / 2 ** 32 / spm, apg_states["Y"].x / 2 ** 32 / spm)
                # print("        V:", apg_states["X"].v / 2 ** 32 / spm * v_step, apg_states["Y"].v / 2 ** 32 / spm * v_step)
                # print("   max_xv:", res["xv"].max(), res["xv"].min())
                # print("   max_yv:", res["yv"].max(), res["yv"].min())
                assert res["xv"].max() < 300
                assert res["xv"].min() > -300
                assert res["yv"].max() < 300
                assert res["yv"].min() > -300
                assert res["ev"].max() < 300
                assert res["ev"].min() > -300
                assert res["X_a"].max() < k2_30
                assert res["X_a"].min() > - k2_30
                assert res["Y_a"].max() < k2_30
                assert res["Y_a"].min() > - k2_30
                assert res["Z_a"].max() < k2_30
                assert res["Z_a"].min() > - k2_30
                assert res["X_j"].max() < k2_30
                assert res["X_j"].min() > - k2_30
                assert res["Y_j"].max() < k2_30
                assert res["Y_j"].min() > - k2_30
                assert res["Z_j"].max() < k2_30
                assert res["Z_j"].min() > - k2_30

            if 1:
                assert abs(last_x - next_x) < 0.1
                assert abs(last_y - next_y) < 0.1
                assert abs(last_e - next_e) < 0.1
                assert abs(last_vx - next_vx) < 5
                assert abs(last_vy - next_vy) < 5
                assert abs(last_ve - next_ve) < 5

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