import math
import sys
import time
import pickle
import os.path
from copy import deepcopy
from random import randint
import numpy as np
from collections import deque

from valurap2 import rest_client, buf_commands
from valurap2.profile import ProfileSegment
from valurap2 import path_planning as pp

fn_tpl = '{}_{:05d}.layer'

base = sys.argv[1].replace(".gcode", "")
assert os.path.exists(fn_tpl.format(base, 0))

c = rest_client.Client(emu=False)

while True:
    try:
        c.abort()
    except Exception as e:
        print("connection Failed", e)
        time.sleep(1)
    else:
        break


if 0:
    print("prime_extruders")
    c.move(E1=-30, E2=-30)
    c.wait_idle()
    print("done")

class Prn():
    base_offsets = {
        "E1": {
            "X": 0,
            "Y": 0,
            "Z": 9.3
        },
        "E2": {
            "X": 7.29 - 0.8 - 1,
            "Y": 122.6 - 0.2,
            "Z": 12.46
        }
    }

    def __init__(self, c):
        self.c = c
        self.current_X1 = None
        self.current_X2 = None
        self.current_Y = None
        self.current_Z = None
        self.current_extruder = "E1"
        self.planner = pp.PathPlanner()
        self.planner.spms = self.planner.print_spms
        self.planner.init_apgs()
        self.accumulated_segments = deque()
        self.first_send = True
        self.offsets = deepcopy(self.base_offsets)

    def process_job_end(self):
        sub_chunks = []
        acc_len = 0
        exp_len = 500
        for segment in self.accumulated_segments:
            sub_chunks.extend(segment)

            if len(sub_chunks) > exp_len:
                codes = self.format_segment(sub_chunks)
                self.c.exec_binary(codes)
                sub_chunks = []
                acc_len = 0

        if sub_chunks:
            codes = self.format_segment(sub_chunks)
            self.c.exec_binary(codes)

        print("[PRN] DONE")

    def process_home(self):
        assert not self.accumulated_segments
        print("[PRN] HOME")
        c = self.c
        c.abort()
        time.sleep(2)
        c.home()
        c.wait_idle()

        c.move(E1=-30, E2=-30)
        c.wait_idle()

        c.moveto(X1=-190, X2=170, mode="print,e1,e2")
        c.wait_idle()

        c.moveto(Y=0, mode="print,e1,e2")
        rr = c.wait_idle()

        prn.set_state(rr)

    def process_move(self, x=None, y=None, z=None, e=None):
        c_e = self.current_extruder
        segs = []

        if y is not None:
            real_y = y + self.offsets[c_e]["Y"]
            dy = real_y - self.current_Y
            segs += self.planner.ext_to_code(dy, 100, axe="Y")

            print("[PRN] MOVE Y TO {} ({})".format(real_y, dy))
            self.current_Y = real_y

        if x is not None:
            axe_x = "X1"
            real_x = x + self.offsets[c_e]["X"]
            if self.current_extruder == "E1":
                dx = real_x - self.current_X1
                self.current_X1 = real_x
            else:
                axe_x = "X2"
                dx = real_x - self.current_X2
                self.current_X2 = real_x

            print("[PRN] MOVE {} TO {} ({})".format(axe_x, real_x, dx))
            segs += self.planner.ext_to_code(dx, 100, axe=axe_x)

        if z is not None:
            real_z = z + self.offsets[c_e]["Z"]
            dz = real_z - self.current_Z
            print("[PRN] MOVE Z TO {} ({}) ()mm".format(real_z, dz, z))

            segs += self.planner.ext_to_code(dz, 3, axe="Z")
            self.current_Z = real_z

        if e is not None:
            segs += self.planner.ext_to_code(e, 10, axe=c_e)
            print("[PRN] MOVE {} for {}mm".format(c_e, e))

        tupled_segment = []
        for dt, segs in segs:
            tupled_segment.append((dt, tuple([s.to_tuple() for s in segs])))

        self.accumulated_segments.append(tupled_segment)

    def format_segment(self, segments):
        pr_opt = []

        for dt, segs in segments:
            pr_opt.append([
                dt, [ProfileSegment.from_tuple(s) for s in segs]
            ])

        cb = buf_commands.CommandBuffer(debug=False)
        cb.add_segments_head()
        cb.add_segments(pr_opt)
        cb.add_segments_tail()

        return cb.buffer


    def process_segment(self, segment, start, end, e):
        assert e == self.current_extruder
        if self.current_extruder == "E1":
            current_x = self.current_X1
        else:
            current_x = self.current_X2

        if start:
            print("Expected start", start)
            real_x = start[0] + self.offsets[e]["X"]
            real_y = start[1] + self.offsets[e]["Y"]
            assert abs(current_x - real_x) < 0.001
            assert abs(self.current_Y - real_y) < 0.001

        print("[PRN] DO SEGMENT", segment[1], len(segment[2]))
        if end[1][0] is not None:
            real_x = end[1][0] + self.offsets[e]["X"]
            real_y = end[1][1] + self.offsets[e]["Y"]
            if self.current_extruder == "E1":
                self.current_X1 = real_x
            else:
                self.current_X2 = real_x
            self.current_Y = real_y

            cmd, meta, tup_seg = segment
            seg_len = len(tup_seg)
            print("SEGMENT LENGTH:", seg_len)
            self.accumulated_segments.append(tup_seg)

            while True:
                r = self.c.state()
                # print(r)
                if r["buf_len"] < 1000000:
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

            for segment in self.accumulated_segments:
                sub_chunks.extend(segment)

                if len(sub_chunks) > exp_len:
                    self.first_send = False
                    exp_len = 500
                    codes = self.format_segment(sub_chunks)
                    self.c.exec_binary(codes)
                    sub_chunks = []
                    acc_len = 0

            self.accumulated_segments = [sub_chunks]
        else:
            self.accumulated_segments.append(segment[2])
            print("extruder only segment, just spooling")

    def set_state(self, r):
        self.current_X1 = r["state"]["motors_x"][7 - 1] / 80.0
        self.current_X2 = r["state"]["motors_x"][8 - 1] / 80.0
        self.current_Y = r["state"]["motors_x"][12 - 1] / 80.0
        self.current_Z = r["state"]["motors_x"][1 - 1] / 1600.0

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
        assert start[3] == (None, None, None, 0)
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
    print(r["buf_len"])
    time.sleep(10)

c.abort()
c.home()
c.wait_idle()
c.abort()
if 0:
    c.spt(ch=1, val=0)
    c.spt(ch=2, val=0)
    c.spt(ch=3, val=0)

