import math
import sys
import time
import pickle
import os.path
from copy import deepcopy
from random import randint
import numpy as np

import cv2
from sklearn.linear_model import LinearRegression

from valurap import rest_client
from valurap.asg import ProfileSegment
from valurap.printer import Valurap
from valurap import path_planning2 as pp2

fn_tpl = '{}_{:05d}.layer'

base = sys.argv[1]
if base.endswith(".gcode"):
    base = base[:-6]

assert os.path.exists(fn_tpl.format(base, 0))

c = rest_client.Client()

while True:
    try:
        c.abort()
    except Exception as e:
        print("connection Failed", e)
        time.sleep(1)
    else:
        break


print("prime_extruders")

axes = ["E1", "E2"]
c.enable(axes=",".join(axes))
c.move(E1=-50000, E2=-16000)
r = c.wait_idle()
print("all done")


class Prn():
    base_offsets = {
        "E1": {
            "X": 0,
            "Y": 0,
            "Z": 5040 - 1600 * (0.8 - 0.149)  # + 50000
        },
        "E2": {
            "X": (7 - 0.11 + 0.4) * 80,
            "Y": (120 + 2.5 + 0.1) * 80,
            "Z": 9110 + 1600 * 0.066 - 160  # + 50000
        }
    }

    expected_marker_positions = {
        "E1": ("X1", -3796, -9430),
        "E2": ("X2",  1471, -1902)
    }

    def __init__(self, c):
        self.c = c
        self.current_X1 = None
        self.current_X2 = None
        self.current_Y = None
        self.current_Z = None
        self.current_extruder = None
        self.planner = pp2.PathPlanner()
        self.accumulated_layers = []
        self.first_send = True
        self.offsets = deepcopy(self.base_offsets)
        self.prn = Valurap()
        self.prn.axe_z.enabled = True
        self.prn.axe_x1.enabled = True
        self.prn.axe_x2.enabled = True
        self.prn.axe_e1.enabled = True
        self.prn.axe_e2.enabled = True
        self.prn.axe_y.enabled = True

    def wait(self, axe="X1"):
        r = self.c.wait_idle()
        x = None
        y = None
        for s in r["state"]["apg_states"]:
            if s["name"] == axe:
                x = s["x"]
            if s["name"] == "Y":
                y = s["x"]

        return x, y

    def get_circles(self, attempts=4, axe="X1"):
        if axe == "X1":
            cap = cv2.VideoCapture('http://orange:8081/')
        elif axe == "X2":
            cap = cv2.VideoCapture('http://orange:8082/')
        else:
            raise RuntimeError("Unknown axe", axe)

        ret, img = cap.read()
        # ret, img = cap.read()
        # ret, img = cap.read()
        cap.release()
        assert img.shape == (480, 640, 3)

        ret, circles = cv2.findCirclesGrid(img, (6, 6))
        if ret:
            cv2.drawChessboardCorners(img, (6, 6), circles, ret)
            # display(circles)
            x = circles[:, 0][:, 0]
            y = circles[:, 0][:, 1]
            x0 = np.average(x)
            y0 = np.average(y)
            return x0, y0, img
        else:
            if attempts > 0:
                return self.get_circles(attempts - 1, axe)
        return (None, None, img)

    def optozero(self, axe="X1", delta=500):
        c = self.c

        a = []
        b = []
        cur_x = 0
        cur_y = 0
        dd = 1
        for i in range(45):
            if i == 20:
                print("optozero: set to 2.5x step")
                dd = 2.5
            elif i == 30:
                print("optozero: set to 5x step")
                dd = 5

            tx = randint(-delta * dd, delta * dd)
            ty = randint(-delta * dd, delta * dd)
            dx = tx - cur_x
            dy = ty - cur_y
            cur_x = tx
            cur_y = ty

            c.move(**{axe: dx, "Y": dy})
            r = self.wait(axe)

            cx, cy, img = self.get_circles(axe=axe)
            if cx is not None:
                a.append([cx, cy])
                b.append(r)
                if len(a) >= 8:
                    break

        if len(a) < 4:
            print("Failed to find target pattern", len(a))
            return (None, None)

        a = np.array(a)
        b = np.array(b)

        x = b[:, 0]
        y = b[:, 1]

        reg_x = LinearRegression().fit(a, x)
        reg_y = LinearRegression().fit(a, y)
        tx = reg_x.predict([[320, 240]])[0]
        ty = reg_y.predict([[320, 240]])[0]

        c.moveto(**{axe: int(round(tx)), "Y": int(round(ty))})
        rf = self.wait(axe)
        att = 20
        while True:
            cx, cy, img = self.get_circles(axe=axe)

            ctx = reg_x.predict([[cx, cy]])[0]
            cty = reg_y.predict([[cx, cy]])[0]

            dx = tx - ctx
            dy = ty - cty
            print("suggested move:", dx, dy, cx, cy)
            if abs(dx) < 2 and abs(dy) < 2:
                break
            c.move(**{axe: int(round(dx)), "Y": int(round(dy))})
            rf = self.wait(axe)
            att -= 1
            if att <= 0:
                print("Failed to get final adjust")
                return (None, None)

        return rf

    def adjust_offsets(self):
        c = self.c
        c.moveto(Z=100000)
        c.wait_idle()
        for axe in ("E1", "E2"):
            x_axe, exp_x, exp_y = self.expected_marker_positions[axe]
            c.moveto(**{x_axe: exp_x, "Y": exp_y})
            c.wait_idle()
            real_x, real_y = self.optozero(axe=x_axe)
            if real_x is None:
                raise RuntimeError("Unable to find marker for extruder {}".format(axe))

            real_x = int(real_x)
            real_y = int(real_y)

            dx = real_x - exp_x
            dy = real_y - exp_y
            print("Adjustment: {}\n  X: {} ({} -> {})\n  Y: {} ({} -> {})".format(
                math.hypot(dx, dy),
                dx, exp_x, real_x,
                dy, exp_y, real_y,
            ))
            self.offsets[axe]["X"] += dx
            self.offsets[axe]["Y"] += dy

            assert math.hypot(dx, dy) < 200

    def process_job_end(self):
        sub_chunks = []
        acc_len = 0
        exp_len = 500
        for layer in self.accumulated_layers:
            sub_chunks.append(layer)
            if layer[0] == "segment":
                acc_len += len(layer[2])

            if acc_len > exp_len:
                self.first_send = False
                exp_len = 500
                if 0:
                    self.c.exec_code(sub_chunks)
                else:
                    codes = self.format_layer(sub_chunks)
                    self.c.exec_binary(codes)
                sub_chunks = []
                acc_len = 0

        if sub_chunks:
            if 0:
                self.c.exec_code(sub_chunks)
            else:
                codes = self.format_layer(sub_chunks)
                self.c.exec_binary(codes)

        print("[PRN] DONE")

    def process_home(self):
        assert not self.accumulated_layers
        print("[PRN] HOME")
        c = self.c
        c.abort()
        time.sleep(2)
        c.home()
        r = c.wait_idle()
        print(r)

        if 0:
            self.adjust_offsets()

        c.moveto(X1=-190 * self.planner.spm, X2=170 * self.planner.spm)
        rr1 = c.wait_idle()
        print(rr1)

        c.moveto(Y=0)
        rr2 = c.wait_idle()
        print(rr2)

        c.moveto(Z=20000)
        rr3 = c.wait_idle()
        print(rr3)

        prn.set_state(rr1)
        prn.set_state(rr2)
        prn.set_state(rr3)

        c.enable(axes="E1,E2")
        c.move(E1=-50000, E2=-16000)
        c.wait_idle()

    def process_move(self, x=None, y=None, z=None, e=None):
        c_e = self.current_extruder
        mapping = {"Y": "Y"}
        segs = []

        axe_x = "X1"
        if x is not None:
            real_x = x * self.planner.spm + self.offsets[c_e]["X"]
            if self.current_extruder == "E1":
                dx = real_x - self.current_X1
                self.current_X1 = real_x
            else:
                axe_x = "X2"
                dx = real_x - self.current_X2
                self.current_X2 = real_x

            print("[PRN] MOVE {} TO {} ({})".format(axe_x, real_x, dx))

            segs += self.planner.ext_to_code(dx / self.planner.spm, 100, axe=axe_x)

        mapping[axe_x] = "X"

        if y is not None:
            real_y = y * self.planner.spm + self.offsets[c_e]["Y"]
            dy = real_y - self.current_Y
            segs += self.planner.ext_to_code(dy / self.planner.spm, 100, axe="Y")
            print("[PRN] MOVE Y TO {} ({})".format(real_y, dy))
            self.current_Y = real_y

        axe_z = "Z"
        if z is not None:
            real_z = z * self.planner.spmz + self.offsets[c_e]["Z"]
            dz = real_z - self.current_Z
            print("[PRN] MOVE Z TO {} ({}) ()mm".format(real_z, dz, z))

            segs += self.planner.ext_to_code(dz / self.planner.spmz, 3, axe="Z")
            self.current_Z = real_z
            assert e is None
        elif e is not None:
            axe_z = c_e
            segs += self.planner.ext_to_code(e, 10, axe=c_e)
            print("[PRN] MOVE {} for {}mm".format(c_e, e))

        mapping[axe_z] = "Z"

        tupled_segment = []
        for dt, segs in segs:
            tupled_segment.append((dt, tuple([s.to_tuple() for s in segs])))

        self.accumulated_layers.append(("segment", {
            "map": mapping,
            "acc_step": self.planner.acc_step,
            "extruder": self.current_extruder
        }, tupled_segment))

    def format_layer(self, layer):
        codes = []
        prn = self.prn
        for pp in layer:
            if pp[0] != "segment":
                continue

            cmd, meta, segments = pp
            if "map" in meta:
                if meta["map"]:
                    codes.append(prn.asg.gen_map_code(meta["map"]))

            pr_opt = []

            apgs = {
                "X": prn.apg_x,
                "Y": prn.apg_y,
                "Z": prn.apg_z,
            }

            for dt, segs in segments:
                pr_opt.append([
                    dt, [ProfileSegment.from_tuple(s, apgs) for s in segs]
                ])

            path_code = prn.asg.gen_path_code(pr_opt,
                                              accel_step=50000000/meta["acc_step"],
                                              real_apgs=apgs)
            print(len(path_code))
            codes.append(path_code)

        full_code = []
        for code in codes:
            full_code.extend(code[:-1])

        return full_code


    def process_segment(self, segment, start, end, e):
        assert e == self.current_extruder
        if self.current_extruder == "E1":
            current_x = self.current_X1
        else:
            current_x = self.current_X2

        if start:
            print("Expected start", start)
            real_x = start[0] * self.planner.spm + self.offsets[e]["X"]
            real_y = start[1] * self.planner.spm + self.offsets[e]["Y"]
            assert abs(current_x - real_x) < 0.001
            assert abs(self.current_Y - real_y) < 0.001
        print("[PRN] DO SEGMENT", segment[1], len(segment[2]), len(layer_data))
        if end[1][0] is not None:
            real_x = end[1][0] * self.planner.spm + self.offsets[e]["X"]
            real_y = end[1][1] * self.planner.spm + self.offsets[e]["Y"]
            if self.current_extruder == "E1":
                self.current_X1 = real_x
            else:
                self.current_X2 = real_x
            self.current_Y = real_y

            cmd, meta, tup_seg = segment
            seg_len = len(tup_seg)
            print("SEGMENT LENGTH:", seg_len)
            if 1:
                cur_chunk = []
                for step in tup_seg:
                    cur_chunk.append(step)
                    if step == (5, (('X', None, 0), ('Y', None, 0), ('Z', None, 0))):
                        print("  chunk:", len(cur_chunk))
                        self.accumulated_layers.append((cmd, meta, cur_chunk))
                        cur_chunk = []
                if cur_chunk:
                    print("  chunk:", len(cur_chunk))
                    self.accumulated_layers.append((cmd, meta, cur_chunk))
            else:
                self.accumulated_layers.append(segment)

            while True:
                if self.c.emu:
                    break
                r = self.c.state()
                # print(r)
                if r["state"]["code_len"] < 1000000:
                    print("submit code")
                    break
                # print("code_len is too big: {}, sleeping".format(r["state"]["code_len"]))
                time.sleep(1)

            sub_chunks = []
            acc_len = 0

            if self.first_send:
                exp_len = 10000
            else:
                exp_len = 500

            for layer in self.accumulated_layers:
                sub_chunks.append(layer)
                if layer[0] == "segment":
                    acc_len += len(layer[2])

                if acc_len > exp_len:
                    self.first_send = False
                    exp_len = 500
                    if 0:
                        self.c.exec_code(sub_chunks)
                    else:
                        codes = self.format_layer(sub_chunks)
                        self.c.exec_binary(codes)
                    sub_chunks = []
                    acc_len = 0

            self.accumulated_layers = sub_chunks
        else:
            self.accumulated_layers.append(segment)
            print("extruder only segment, just spooling")

    def set_state(self, r):
        if self.c.emu:
            self.current_X1, self.current_X2, self.current_Y, self.current_Z = (
                -15200.4140625, 13598.58984375, -0.41015625, 19951.015625
            )
            return

        for st in r["state"]["apg_states"]:
            if st["name"] == "X1":
                self.current_X1 = st["x"]
            if st["name"] == "X2":
                self.current_X2 = st["x"]
            if st["name"] == "Y":
                self.current_Y = st["x"]
            if st["name"] == "Z":
                self.current_Z = st["x"]

        # print(self.current_X1, self.current_X2, self.current_Y, self.current_Z)


prn = Prn(c)

state = "init"
i = -1
while True:
    i += 1
    fn = fn_tpl.format(base, i)

    while True:
        if os.path.exists(fn):
            break
        print("layer {} is not yet ready".format(fn))
        time.sleep(2)

    layer_data = open(fn, 'rb').read()
    layer = pickle.loads(layer_data)
    print("layer:", fn, len(layer))
    start = None
    end = None
    do_home = False
    switch_extruder = None
    segment = None

    expected_x = None
    expected_y = None
    expected_z = None
    expected_extruder = None

    for l in layer:
        cmd = l[0]
        print(" cmd:", cmd, state)
        if cmd == "do_home":
            do_home = True
            print("  p:", l)
        elif cmd == "start":
            start = l
            print("  p:", l[3], l[4], l[1])
        elif cmd == "end_state":
            end = l
            print("  p:", l[1])
        elif cmd == "segment":
            assert segment is None
            segment = l
            print("  len: ", len(l[2]))
        elif cmd == "extruder_switch":
            assert segment is None
            switch_extruder = l[1]
            print("  ext: ", l[1])

    if state == "init":
        if switch_extruder is not None:
            assert do_home == False and segment is None
            prn.current_extruder = "E{}".format(switch_extruder + 1)
        elif do_home:
            prn.process_home()
            if segment:
                assert end[1][0] is None
                assert end[1][1] is None
                prn.process_segment(segment, None, end, prn.current_extruder)
            state = "homed"
        else:
            assert False
        continue
    elif state == "homed":
        assert start[3] == (None, None, 0)
        assert segment
        expected_x = start[1]["X"]
        expected_y = start[1]["Y"]
        expected_z = start[1]["Z"]
        expected_extruder = start[4]
        state = "working"
        prn.process_move(x=expected_x, y=expected_y, z=expected_z)
        prn.process_segment(segment, None, end, expected_extruder)
    elif state == "working":
        if do_home:
            prn.process_job_end()
            break
        elif switch_extruder is not None:
            print("[PRN] SWITCH TO", switch_extruder)
            if prn.current_extruder == "E1":
                target_x = -180
            else:
                target_x = 165
            prn.process_move(x=target_x)
            prn.current_extruder = "E{}".format(switch_extruder + 1)
            if segment:
                assert end[1][0] is None
                assert end[1][1] is None
                prn.process_segment(segment, None, end, prn.current_extruder)
            state = "switched"
            print("switched segment:", segment)
            print("switched end", end)
        else:
            assert start[3]
            expected_z = start[1]["Z"]
            print("Z:", expected_z)
            expected_extruder = start[4]
            exp_start = (start[3][0], start[3][1], start[3][2])
            prn.process_move(z=expected_z)
            prn.process_segment(segment, exp_start, end, expected_extruder)
    elif state == "switched":
        print(start[3])
        assert start[3][:2] == (None, None)
        assert segment
        expected_x = start[1]["X"]
        expected_y = start[1]["Y"]
        expected_z = start[1]["Z"]
        expected_extruder = start[4]
        prn.process_move(z=expected_z)
        prn.process_move(y=expected_y)
        prn.process_move(x=expected_x)
        prn.process_segment(segment, None, end, expected_extruder)
        state = "working"
    else:
        assert False

while True:
    r = c.state()
    if r["idle"]:
        break
    print(r["state"]["code_len"])
    time.sleep(10)

c.abort()
c.home()
c.wait_idle()
c.abort()
if 0:
    c.spt(ch=1, val=0)
    c.spt(ch=2, val=0)
    c.spt(ch=3, val=0)

