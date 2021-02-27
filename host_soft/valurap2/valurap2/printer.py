"""
Run:
   seva@orange:~/src/sevasoft/valurap/host_soft$ python -m valurap.printer
"""
import pickle

import random
import time
from functools import partial
from math import sqrt

from valurap2 import path_planning
from valurap2.buf_commands import CommandBuffer as CB

from .commands import S3GPort
from .spi import SPIPort
from .oled import OLED


class ExecutionAborted(Exception):
    pass

class Valurap(object):
    home_positions = {
        "X1": 13200,
        "X2": -14000,
        "YL": -22500,
        "YR": -22500,
        "ZFR":  -312  +6.00*1600,
        "ZFL": -4050  +8.35*1600,
        "ZBR": -1645  +5.55*1600,
        "ZBL": -4297  +8.55*1600,
        #"ZBL": -312,
        #"ZBR": -4050,
        #"ZFL": -1645,
        #"ZFR": -4297
    }
    home_target = {
        "X1": 155,
        "X2": -170,
        "YL": -250,
        "YR": -250,
        "ZBL": 30,
        "ZBR": 30,
        "ZFL": 30,
        "ZFR": 30
    }

    axes = {
        "ZFL": 1,
        "ZBR": 2,
        "ZBL": 3,
        "E1": 4,
        "E2": 5,
        "ZFR": 6,
        "X1": 7,
        "X2": 8,
        "M9": 9,
        "M10": 10,
        "YR": 11,
        "YL": 12,
    }

    def __init__(self, oled=None):
        self.s3g = S3GPort()
        self.spi = SPIPort()

        if oled is None:
            oled = OLED()
        self.oled = oled
        self.cb = CB()

        self.abort = False
        self.hw_state = None
        self.long_code = None
        self.last_status_times = []
        self.last_send_times = []
        self.idle = False

    def setup(self):
        self.spi.setup_tmc2130()
        with self.oled.draw() as draw:
            draw.rectangle(self.oled.bounding_box, outline="white", fill="black")
            draw.text((10, 10), "Reset", fill="white")

        s3g = self.s3g

        print("Executing reset code")

        s3g.S3G_STB(CB.STB_BE_ABORT)  # Reset BE and ASG just in case

        cb = self.cb
        cb.reset()
        cb.hw_reset()
        cb.BUF_DONE()

        self.exec_code(cb)

        print("Reset OLED")
        with self.oled.draw() as draw:
            draw.rectangle(self.oled.bounding_box, outline="white", fill="black")
            draw.text((10, 10), "Ready", fill="white")
        print("Setup done")

    def wait_done(self, verbose=True):
        s3g = self.s3g
        while True:
            if self.abort:
                raise ExecutionAborted
            # a = p.S3G_INPUT(cb.IN_APG_STATUS)
            # print("APG_STATUS", a)
            a = s3g.S3G_INPUT(CB.IN_BE_STATUS)
            # print("BE_STATUS", a)
            if CB.extract_field(CB.IN_BE_STATUS_BUSY, a) == 0:
                break

            if verbose:
                hw_state = self.get_hw_state()
                self.report_status("wait done", be_status=a, hw_state=hw_state)
            time.sleep(0.1)

        if verbose:
            hw_state = self.get_hw_state()
            self.report_status("idle", hw_state=hw_state)
        return a

    def wait_stops(self, stops, verbose=True):
        assert len(stops) > 0

        s3g = self.s3g
        apg0 = CB.INT_APG0_ABORT_DONE
        mask = 0
        for stop in stops:
            mask |= apg0 << stop

        last_stops = 0

        while True:
            if self.abort:
                raise ExecutionAborted
            b = s3g.S3G_INPUT(CB.IN_BE_STATUS)
            # print("BE_STATUS", b)
            ints = s3g.S3G_INPUT(CB.IN_PENDING_INTS)
            if CB.extract_field(CB.IN_BE_STATUS_BUSY, b) == 0:
                if verbose:
                    hw_state = self.get_hw_state()
                    self.report_status("idle", hw_state=hw_state)
                print("Stops not reached: {:X} != {:X}".format(ints & mask, mask))
                return False
            if ints & mask != last_stops:
                print("stops done: {:X} expected: {:X}".format(ints & mask, mask))
                last_stops = ints & mask

            if ints & mask == mask:
                if verbose:
                    hw_state = self.get_hw_state()
                    self.report_status("idle", hw_state=hw_state)
                print("All stops done")
                return True
            # print("ints: {:X}".format(ints))
            if verbose:
                hw_state = self.get_hw_state()
                self.report_status("wait stops", be_status=b, stops=ints & mask, expected_stops=mask, hw_state=hw_state)
            time.sleep(0.1)

    def exec_code(self, cb, wait=True, stops=None, verbose=True):
        be_status = self.s3g.S3G_INPUT(CB.IN_BE_STATUS)
        busy = CB.extract_field(CB.IN_BE_STATUS_BUSY, be_status)
        if not busy:
            self.s3g.S3G_WRITE_FIFO(cb, until_free=500)
            self.s3g.S3G_STB(CB.STB_BE_START)  # Start execution

        while cb.len() > 0:
            if self.abort:
                raise ExecutionAborted
            free_space, status = self.s3g.S3G_WRITE_FIFO(cb, until_free=500)  # Send program into FIFO
            if verbose:
                hw_state = None
                if free_space < 1000:
                    hw_state = self.get_hw_state()
                self.report_status("pushing code", fifo_space=free_space, fifo_status=status, hw_state=hw_state)

        if wait:
            if stops is None:
                return self.wait_done(verbose)
            else:
                res = self.wait_stops(stops, verbose)
                self.s3g.S3G_STB(cb.STB_BE_ABORT)
                self.s3g.S3G_STB(cb.STB_ASG_ABORT)
                return res

    def get_hw_state(self):
        motors_x = []
        hw_state = {"motors_x": motors_x}
        for m in range(12):
            motors_x.append(CB.extract_field(CB.IN_MOTOR_X, self.s3g.S3G_INPUT(CB.IN_MOTOR1_X + m)))

        lb = self.s3g.S3G_INPUT(CB.IN_SE_REG_LB)
        hw_state["lb"] = lb

        self.hw_state = hw_state
        return hw_state

    def report_status(self, state, **kw):
        try:
            lines = []
            fs = kw.get("fifo_space", 0)
            ts = kw.get("fifo_status", 0)
            sl = []
            if fs != 0:
                sl.append("f: {}".format(fs))
            if ts != 0:
                sl.append("s: {}".format(ts))
            sl.append(state)
            lines.append(" ".join(sl))

            print("Status: {} {}".format(state, kw))
            if "hw_state" in kw:
                motors = kw["hw_state"]["motors_x"]
                x1 = motors[6] / 80.0
                x2 = motors[7] / 80.0
                e1 = motors[3] / 847.0
                e2 = motors[4] / 847.0 * 2
                y = motors[10] / 80.0
                z = motors[0] / 1600.0
                lines.append("X1: {:6.1f} X2: {:6.2f}".format(x1, x2))
                lines.append("E1: {:6.1f} E2: {:6.2f}".format(e1, e2))
                lines.append("Y: {:7.1f} Z: {:7.2f}".format(y, z))

                with self.oled.draw() as draw:
                    draw.rectangle(self.oled.bounding_box, outline="white", fill="black")
                    draw.multiline_text((5, 3), "\n".join(lines), fill="white")
        except Exception:
            pass


    # noinspection PyUnreachableCode
    def home(self):
        p = self.s3g

        pp = path_planning.PathPlanner(mode="home")

        cb = self.cb

        for i in (1,2,3,6):
            print("c", i, cb.extract_field(cb.IN_MOTOR_X, p.S3G_INPUT(cb.IN_MOTOR1_X + i - 1)))
            print("h", i, cb.extract_field(cb.IN_MOTOR_X, p.S3G_INPUT(cb.IN_MOTOR1_HOLD_X + i - 1)))

        # Move Z down
        cb.reset()
        cb.enable_axes(["home"], pp)
        cb.add_segments_head(pp)
        cb.add_segments(pp.ext_to_code(30, speed=10, axes=["ZFR", "ZFL", "ZBR", "ZBL"]))
        cb.add_segments_tail()
        cb.BUF_DONE()
        self.exec_code(cb)

        p.S3G_STB(cb.STB_ES_UNLOCK)
        time.sleep(0.1)
        p.S3G_STB(cb.STB_ES_UNLOCK)
        es = p.S3G_INPUT(cb.IN_ES_STATUS)
        print("es_status: {:X}".format(es))
        on_stops = []
        if es & 0x1:
            on_stops.append("X2")
        if es & 0x10:
            on_stops.append("-X1")
        if es & 0x1100:
            on_stops.append("YL")
            on_stops.append("YR")

        if on_stops:
            # Move XY from stops
            cb.reset()
            cb.enable_axes(["home"])
            cb.add_segments_head(pp)
            cb.add_segments(pp.ext_to_code(10, axes=on_stops, speed=10))
            cb.add_segments_tail()
            cb.BUF_DONE()
            self.exec_code(cb)

        # First Home XY
        cb.reset()
        cb.enable_axes(["home", "es_xy"])
        cb.add_segments_head(pp)
        cb.add_segments(pp.ext_to_code(-1000, axes=["-X1", "X2", "YL", "YR"], speed=50))
        cb.add_segments_tail()
        cb.BUF_DONE()
        self.exec_code(cb, stops=[0, 1, 2, 3])

        # Move XY from stops
        cb.reset()
        cb.enable_axes(["home"])
        cb.add_segments_head(pp)
        cb.add_segments(pp.ext_to_code(15, axes=["-X1", "X2", "YL", "YR"], speed=20))
        cb.add_segments_tail()
        cb.BUF_DONE()
        self.exec_code(cb)

        # Second Home XY
        cb.reset()
        cb.enable_axes(["home", "es_xy"])
        cb.add_segments_head(pp)
        cb.add_segments(pp.ext_to_code(-300, axes=["-X1", "X2", "YL", "YR"], speed=10))
        cb.add_segments_tail()
        cb.BUF_DONE()
        self.exec_code(cb, stops=[0, 1, 2, 3])

        cb.reset()
        cb.debug = True
        for motor, axe in (
                (7, "X1"),
                (8, "X2"),
                (11, "YR"),
                (12, "YL")
        ):
            x_c = cb.extract_field(cb.IN_MOTOR_X, p.S3G_INPUT(cb.IN_MOTOR1_X + motor - 1))
            x_h = cb.extract_field(cb.IN_MOTOR_X, p.S3G_INPUT(cb.IN_MOTOR1_HOLD_X + motor - 1))
            print("x:", motor, x_h, x_c)

            my_addr = cb.OUT_MSG_CONFIG0 + ((motor - 1) >> 1)
            bit = CB.format_field(CB.OUT_MSG_CONFIG_SET_X, 1)
            if motor & 1 == 0:
                bit = bit << 16

            for addr in range(cb.OUT_MSG_CONFIG0, cb.OUT_MSG_CONFIG5 + 1):
                if addr == my_addr:
                    cb.BUF_OUTPUT(addr, bit | 0x80008000)
                else:
                    cb.BUF_OUTPUT(addr, 0x80008000)

            x_v = x_c - x_h + self.home_positions[axe]
            cb.BUF_OUTPUT(CB.OUT_MSG_X_VAL, x_v)
            cb.BUF_STB(CB.STB_MSG_SET_X)
        cb.BUF_STB(CB.STB_SP_ZERO)

        cb.BUF_DONE()
        cb.debug = False
        self.exec_code(cb)
        for motor, axe in (
                (7, "X1"),
                (8, "X2"),
                (11, "YR"),
                (12, "YL")
        ):
            x_c = cb.extract_field(cb.IN_MOTOR_X, p.S3G_INPUT(cb.IN_MOTOR1_X + motor - 1))
            print("x:", axe, motor, x_c)

        if 0:
            # Move XY from stops
            cb.reset()
            cb.enable_axes(["home"])
            cb.add_segments_head(pp)
            cb.add_segments(pp.ext_to_code(15, axes=["-X1", "X2", "YL", "YR"], speed=20))
            cb.add_segments_tail()
            cb.BUF_DONE()
            self.exec_code(cb)

            # Checking Home XY
            cb.reset()
            cb.enable_axes(["home", "es_xy"])
            cb.add_segments_head(pp)
            cb.add_segments(pp.ext_to_code(-300, axes=["-X1", "X2", "YL", "YR"], speed=10))
            cb.add_segments_tail()
            cb.BUF_DONE()
            self.exec_code(cb, stops=[0, 1, 2, 3])
            for motor, axe in (
                    (7, "X1"),
                    (8, "X2"),
                    (11, "YR"),
                    (12, "YL")
            ):
                x_c = cb.extract_field(cb.IN_MOTOR_X, p.S3G_INPUT(cb.IN_MOTOR1_X + motor - 1))
                x_h = cb.extract_field(cb.IN_MOTOR_X, p.S3G_INPUT(cb.IN_MOTOR1_HOLD_X + motor - 1))
                print("x:", axe, motor, x_h, x_c)

        # Home Z
        cb.reset()
        cb.enable_axes(["home", "es_z"])
        cb.add_segments_head(pp)
        cb.add_segments(pp.ext_to_code(-700, axes=["ZFR", "ZFL", "ZBR", "ZBL"], speed=10))
        cb.add_segments_tail()
        cb.BUF_DONE()
        self.exec_code(cb, stops=[4, 5, 6, 7])

        # Move Z from stops
        cb.reset()
        cb.enable_axes(["home"])
        cb.add_segments_head(pp)
        cb.add_segments(pp.ext_to_code(5, axes=["ZFR", "ZFL", "ZBR", "ZBL"], speed=2))
        cb.add_segments_tail()
        cb.BUF_DONE()
        self.exec_code(cb)

        # Second Home Z
        cb.reset()
        cb.enable_axes(["home", "es_z"])
        cb.add_segments_head(pp)
        cb.add_segments(pp.ext_to_code(-20, axes=["ZFR", "ZFL", "ZBR", "ZBL"], speed=2))
        cb.add_segments_tail()
        cb.BUF_DONE()
        self.exec_code(cb, stops=[4, 5, 6, 7])

        cb.reset()
        cb.debug = True
        for motor, axe in (
                (1, "ZFL"),
                (2, "ZBR"),
                (3, "ZBL"),
                (6, "ZFR")
        ):
            x_c = cb.extract_field(cb.IN_MOTOR_X, p.S3G_INPUT(cb.IN_MOTOR1_X + motor - 1))
            x_h = cb.extract_field(cb.IN_MOTOR_X, p.S3G_INPUT(cb.IN_MOTOR1_HOLD_X + motor - 1))
            print("x:", axe, motor, x_h, x_c)

            my_addr = cb.OUT_MSG_CONFIG0 + ((motor - 1) >> 1)
            bit = CB.format_field(CB.OUT_MSG_CONFIG_SET_X, 1)
            if motor & 1 == 0:
                bit = bit << 16

            for addr in range(cb.OUT_MSG_CONFIG0, cb.OUT_MSG_CONFIG5 + 1):
                if addr == my_addr:
                    cb.BUF_OUTPUT(addr, bit | 0x80008000)
                else:
                    cb.BUF_OUTPUT(addr, 0x80008000)

            x_v = x_c - x_h + int(self.home_positions[axe])
            cb.BUF_OUTPUT(CB.OUT_MSG_X_VAL, x_v)
            cb.BUF_STB(CB.STB_MSG_SET_X)
        cb.BUF_STB(CB.STB_SP_ZERO)

        cb.BUF_DONE()
        cb.debug = False
        self.exec_code(cb)

        for motor, axe in (
                (1, "ZFL"),
                (2, "ZBR"),
                (3, "ZBL"),
                (6, "ZFR")
        ):
            x_c = cb.extract_field(cb.IN_MOTOR_X, p.S3G_INPUT(cb.IN_MOTOR1_X + motor - 1))
            print("x:", axe, motor, x_c)

        d1 = {}
        d2 = {}
        for k, v in self.home_target.items():
            if k.startswith("Z"):
                d1[k] = v
            else:
                d2[k] = v

        self.moveto(targets=d1, pp=pp, modes=["home"])
        self.moveto(targets=d2, pp=pp, modes=["home"])


    def move(self, pp=None, targets=None, absolute=False, speed=None, modes=None, **kw):
        if pp is None:
            if not modes:
                modes = ["print"]

            if "print" in modes:
                mode = "print"
            elif "home" in modes:
                mode = "home"
            else:
                raise ValueError("primary mode is not specified. Modes: {}".format(modes))

            pp = path_planning.PathPlanner(mode=mode)
            pp.init_apgs()

        if targets is None:
            targets = {}
        else:
            targets = targets.copy()

        if kw:
            targets.update(kw)

        if speed is None:
            speed = 1.0

        axes = []
        dxes = []
        speeds = []

        cb = self.cb

        for axe, dx in targets.items():
            apg, default_speed, _ = pp.axe_params(axe)
            speeds.append(default_speed * speed)

            maxe = axe
            if axe == "Y":
                maxe = "YL"
            if axe == "Z":
                maxe = "ZFL"

            motor = self.axes[maxe]

            apgs = pp.apg_states[apg]
            x_c = cb.extract_field(cb.IN_MOTOR_X, self.s3g.S3G_INPUT(cb.IN_MOTOR1_X + motor - 1)) / apgs.spm
            print("xc", x_c, "dx", dx)

            if absolute:
                dx = dx - x_c
                print("absolute dx:", dx)

            axes.append(axe)
            dxes.append(dx)

        cb.reset()
        cb.enable_axes(modes)

        cb.add_segments_head(pp)
        print("segments: dxes: {} axes: {} speed: {}".format(dxes, axes, min(speeds)))
        cb.add_segments(pp.ext_to_code(dx=dxes, axes=axes, speed=min(speeds)))
        cb.BUF_DONE()
        return self.exec_code(cb)


    def moveto(self, **kw):
        kw["absolute"] = True
        return self.move(**kw)


    def enable_axes(self, modes):
        cb = self.cb
        cb.reset()
        cb.enable_axes(modes)
        cb.BUF_DONE()
        return self.exec_code(cb)
