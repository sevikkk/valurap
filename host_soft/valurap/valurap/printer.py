"""
Run:
   seva@orange:~/src/sevasoft/valurap/host_soft$ python -m valurap.printer
"""
import pickle

import random
import time
from math import sqrt

import struct

from .asg import Asg, ProfileSegment, PathSegment
from .apgs import ApgX, ApgY, ApgZ
from .axes import AxeX1, AxeX2, AxeY, AxeY2, AxeE1, AxeE2, AxeM10, AxeY1, AxeE3, \
    AxeZ, AxeBLZ, AxeBRZ, AxeFLZ, AxeFRZ
from .commands import S3GPort

try:
    from .spi import SPIPort
    from .oled import OLED
except ImportError:
    class SPIPort(object):
        def setup_tmc2130(self):
            pass

    class FakeDraw(object):
        def __enter__(self, *args, **kw):
            return self
        def __exit__(self, *args, **kw):
            return
        def rectangle(self, *args, **kw):
            return
        def text(self, *args, **kw):
            return
        def multiline_text(self, *args, **kw):
            return

    class OLED(object):
        def draw(self, *args, **kw):
            return FakeDraw()

        def bounding_box(self, *args, **kw):
            return (64, 96)

    S3GPortOrig = S3GPort
    class FakeSerial:
        def write(self, *args):
            pass

        def flush(self):
            pass

        def read(self):
            return None

    class S3GPort(S3GPortOrig):
        def open_port(self, port, baudrate):
            return FakeSerial()

        def send_and_wait_reply(self, payload, cmd_id, timeout=1, retries=3):
            cmd = payload[0]
            print("cmd: {}".format(cmd))
            if cmd == 61:
                return b'\x81\0\0\0\0'

            return b'\x81'

class ExecutionAborted(Exception):
    pass

class Valurap(object):
    def __init__(self, oled=None):
        self.s3g = S3GPort()
        self.spi = SPIPort()

        if oled is None:
            oled = OLED()
        self.oled = oled

        self.cap = None

        self.asg = Asg(self)

        self.axe_x1 = AxeX1(self)
        self.axe_x2 = AxeX2(self)
        self.axe_y = AxeY(self)
        self.axe_y1 = AxeY1(self)
        self.axe_y2 = AxeY2(self)
        self.axe_e1 = AxeE1(self)
        self.axe_e2 = AxeE2(self)
        self.axe_e3 = AxeE3(self)
        self.axe_m10 = AxeM10(self)
        self.axe_z = AxeZ(self)
        self.axe_blz = AxeBLZ(self)
        self.axe_brz = AxeBRZ(self)
        self.axe_flz = AxeFLZ(self)
        self.axe_frz = AxeFRZ(self)
        self.axes = {
            "X1": self.axe_x1,
            "X2": self.axe_x2,
            "Y": self.axe_y,
            "Y1": self.axe_y1,
            "Y2": self.axe_y2,
            "E1": self.axe_e1,
            "E2": self.axe_e2,
            "E3": self.axe_e3,
            "M10": self.axe_m10,
            "Z": self.axe_z,
            "BLZ": self.axe_blz,
            "BRZ": self.axe_brz,
            "FLZ": self.axe_flz,
            "FRZ": self.axe_frz,
        }

        self.apg_x = ApgX(self)
        self.apg_y = ApgY(self)
        self.apg_z = ApgZ(self)
        self.apgs = {
            "X": self.apg_x,
            "Y": self.apg_y,
            "Z": self.apg_z,
        }
        self.abort = False

    def setup(self):
        self.spi.setup_tmc2130()
        with self.oled.draw() as draw:
            draw.rectangle(self.oled.bounding_box, outline="white", fill="black")
            draw.text((10, 10), "Reset", fill="white")

        s3g = self.s3g

        s3g.S3G_MASK(0)                                 # Disable reporting for any interrupts
        s3g.S3G_STB(s3g.STB_BE_ABORT)                   # Stop buf_executor
        self.s3g.S3G_CLEAR(0xFFFFFFFF)
        s3g.S3G_OUTPUT(s3g.OUT_MSG_CONTROL, 0)          # Disable all motors
        s3g.S3G_OUTPUT(s3g.OUT_MSG_CONTROL2, 0)         # Disable all motors
        s3g.S3G_OUTPUT(s3g.OUT_ENDSTOPS_OPTIONS, 0)     # Disable all endstops

        reset_code = self.asg.gen_reset_code(self.apgs.values())
        print("Executing reset code")
        self.exec_code(reset_code)

        print("Update axes")
        for axe in self.axes.values():
            axe.enabled = False
            axe.apg = None
            axe.endstop_abort = False
        self.update_axes_config()

        print("Reset OLED")
        with self.oled.draw() as draw:
            draw.rectangle(self.oled.bounding_box, outline="white", fill="black")
            draw.text((10, 10), "Ready", fill="white")
        print("Setup done")

    def exec_code(self, code, addr=0, wait=True):
        s3g = self.s3g
        s3g.S3G_OUTPUT(s3g.OUT_LEDS, 0x55)
        s3g.S3G_WRITE_BUFFER(addr, *code)
        s3g.S3G_OUTPUT(s3g.OUT_BE_START_ADDR, addr)
        s3g.S3G_STB(s3g.STB_ENDSTOPS_UNLOCK)
        s3g.S3G_STB(s3g.STB_BE_START)
        while wait:
            busy, pc = self.check_be_busy()

            if not busy:
                break
            time.sleep(0.1)

    def exec_long_code(self, code, splits=1000, verbose=False):
        addr = 0
        s3g = self.s3g
        s3g.S3G_OUTPUT(s3g.OUT_LEDS, 0x55)
        current_code = code[:splits]
        code = code[splits:]
        #s3g.S3G_WRITE_BUFFER(addr, *current_code)
        s3g.S3G_WRITE_BUFFER(addr, *(current_code + [s3g.BUF_STB(s3g.STB_BE_ABORT), s3g.BUF_DONE()]))
        if verbose:
            print("sent {} commands to addr {}, left {}".format(len(current_code), addr, len(code)))
        s3g.S3G_OUTPUT(s3g.OUT_BE_START_ADDR, addr)
        s3g.S3G_STB(s3g.STB_ENDSTOPS_UNLOCK)
        s3g.S3G_STB(s3g.STB_BE_START)
        addr += len(current_code)
        last_free_buf = None
        while True:
            busy, pc = self.check_be_busy(addr, len(code), verbose)
            if not busy:
                break

            if len(code) == 0:
                time.sleep(0.1)
            else:
                free_buf = (pc - addr) % 8192
                if free_buf < 0:
                    free_buf += 8192

                if free_buf < splits + 10:
                    if free_buf != last_free_buf:
                        print("too small free_buf: {}".format(free_buf))
                        last_free_buf = free_buf
                    time.sleep(0.1)
                else:
                    print("free_buf: {}".format(free_buf))
                    last_free_buf = None
                    current_code = code[:splits]
                    code = code[splits:]
                    s3g.S3G_WRITE_BUFFER(addr, *(current_code + [s3g.BUF_STB(s3g.STB_BE_ABORT), s3g.BUF_DONE()]))
                    if verbose:
                        print("sent {} commands to addr {}, left {}".format(len(current_code), addr, len(code)))
                    addr += len(current_code)
                    addr = addr % 8192

        if code:
            raise RuntimeError("Not all code sent, most probably system staled and got exec buffer underflow")

    def check_be_busy(self, cur_addr=-1, cur_len=-1, verbose=False):
        if self.abort:
            raise ExecutionAborted()

        s3g = self.s3g
        status = s3g.S3G_INPUT(s3g.IN_BE_STATUS)
        busy = (status & 0x80000000) >> 31
        waiting = (status & 0x40000000) >> 30
        error = (status & 0x00FF0000) >> 16
        pc = status & 0x0000FFFF
        if verbose:
            print("Busy: {} Wait: {} Error: {} PC: {} Cur addr: {} Cur len: {}".format(busy, waiting, error, pc, cur_addr, cur_len))
        lines = []
        if busy:
            lines.append("B {} P {} A {} L {}".format(busy, pc, cur_addr, cur_len))
        else:
            lines.append("Idle")

        for sl in self.get_state():
            lines.append("{:2s}{:9.1f} {:8d}".format(sl["name"], sl["x"], sl["v"]))

        with self.oled.draw() as draw:
            draw.rectangle(self.oled.bounding_box, outline="white", fill="black")
            draw.multiline_text((5, 3), "\n".join(lines), fill="white")
        return busy, pc

    def update_axes_config(self):
        s3g = self.s3g
        msg_controls = {}
        es_control = 0
        for axe in self.axes.values():
            msg_controls.setdefault(axe._msg_control, 0)
            msg_controls[axe._msg_control] |= axe.msg_control()
            es_control |= axe.endstops_control()
            if axe.apg:
                s3g.S3G_OUTPUT(axe.apg.val_abort_a, axe.abort_a)

        for k, v in msg_controls.items():
            s3g.S3G_OUTPUT(k, v)
        s3g.S3G_OUTPUT(s3g.OUT_ENDSTOPS_OPTIONS, es_control)

        pos_to_set = {}
        for axe in self.axes.values():
            if axe.apg:
                pos_to_set[axe.name] = axe.last_pos or 0

        if pos_to_set:
            self.set_positions(**pos_to_set)

    def assign_apgs(self, axes_names):
        self.update_axes_positions()

        owners = {}

        for name in self.apgs.keys():
            owners[name] = []

        for name, axis in self.axes.items():
            if axis.apg:
                owners[axis.apg.name].append(axis)

        needs_apg = []
        for name in axes_names:
            axis = self.axes[name]
            if axis.apg:
                try:
                    del owners[axis.apg.name]
                except KeyError:
                    pass
            else:
                needs_apg.append(axis)

        if needs_apg:
            owners = list(owners.items())
            owners.sort(key=lambda x: max([0] + [a.last_used for a in x[1]]))

            while needs_apg:
                axis = needs_apg.pop(0)
                apg_name, current_owners = owners.pop(0)
                for owner in current_owners:
                    owner.apg = None

                axis.apg = self.apgs[apg_name]

            self.update_axes_config()

    def home_axes(self, axes, speed=1.0):
        print("homing: {}".format(axes))
        segs = []
        apgs = list(self.apgs.values())

        self.s3g.S3G_STB(self.s3g.STB_ENDSTOPS_UNLOCK)
        self.s3g.S3G_CLEAR(0xFFFFFFFF)

        active_ints = 0

        for axe in axes:
            current_status = axe.endstops_status()
            if current_status:
                print("{} already on endstop".format(axe.name))
                continue

            axe.apg = apgs.pop()
            axe.endstop_abort = True

            a = int(axe.home_a * speed)
            target_v = int(axe.home_v * speed)

            if not axe.endstop_at_max:
                a = -a
                target_v = -target_v

            segs.append(ProfileSegment(axe.apg, target_v=target_v, a=a * 65536, x=0, v=0))
            active_ints |= axe.endstop_int

        if not segs:
            print("All axes on endstops, skipping")
            return True

        self.update_axes_config()
        self.s3g.S3G_STB(self.s3g.STB_ENDSTOPS_UNLOCK)

        path_code = self.asg.gen_path_code([
            [30000, segs]
        ])

        self.exec_code(path_code, wait=False)
        while True:
            busy, pc = self.check_be_busy()
            if not busy:
                break

            ints = self.s3g.S3G_INPUT(self.s3g.IN_PENDING_INTS)
            #print('{:08X}'.format(ints))

            if ints & active_ints:
                self.s3g.S3G_CLEAR(0xFFFFFFFF)
                self.s3g.S3G_STB(self.s3g.STB_BE_ABORT)
                break

        for axe in axes:
            axe.apg = None
            axe.endstop_abort = False
        self.update_axes_config()

        return False

    def home(self):
        self.axe_x1.enabled = True
        self.axe_x2.enabled = True
        self.axe_y.enabled = True
        self.axe_z.enabled = True
        self.axe_x1.apg = None
        self.axe_x2.apg = None
        self.axe_y.apg = None
        self.axe_y1.apg = None
        self.axe_y2.apg = None
        self.axe_z.apg = None
        self.axe_flz.apg = None
        self.axe_frz.apg = None
        self.axe_blz.apg = None
        self.axe_brz.apg = None
        self.update_axes_config()
        time.sleep(0.5)

        # Move Z down, just in case
        self.axe_z.apg = self.apg_x
        self.update_axes_config()
        self.move(Z=30000)
        self.axe_z.apg = None
        self.update_axes_config()

        # Initial home of top axes
        ret = False
        while not ret:
            ret = self.home_axes([
                self.axe_x1,
                self.axe_x2,
                self.axe_y
            ])

        # Move X1 back, for final homing
        self.axe_x1.apg = self.apg_x
        self.update_axes_config()
        self.move(X1=-3000)
        self.axe_x1.apg = None
        self.update_axes_config()

        # Home X1 motor independently
        ret = False
        while not ret:
            ret = self.home_axes([
                self.axe_x1,
            ])

        # Move X2 back, for final homing
        self.axe_x2.apg = self.apg_x
        self.update_axes_config()
        self.move(X2=3000)
        self.axe_x2.apg = None
        self.update_axes_config()

        # Home X1 motor independently
        ret = False
        while not ret:
            ret = self.home_axes([
                self.axe_x2,
            ])

        # Move Y back, for final homing
        self.axe_y.apg = self.apg_x
        self.update_axes_config()
        self.move(Y=3000)
        self.axe_y.apg = None
        self.update_axes_config()

        # Home Y motors independently
        ret = False
        while not ret:
            ret = self.home_axes([
                self.axe_y1,
                self.axe_y2,
            ])

        # Inital home of Z
        ret = False
        while not ret:
            ret = self.home_axes([
                self.axe_z,
            ])

        # Move Z back, for final homing
        self.axe_z.apg = self.apg_x
        self.update_axes_config()
        self.move(Z=2000)
        self.axe_z.apg = None
        self.update_axes_config()

        for axe in [
            self.axe_blz,
            self.axe_brz,
            self.axe_flz,
            self.axe_frz,
            ]:
            ret = False
            while not ret:
                ret = self.home_axes([
                    axe
                ])

        # Adjust Z end-stops positions
        self.axe_z.apg = None
        self.update_axes_config()
        for axe_name, delta in [
            ("BLZ",  312 - int(( 0.0 ) * 1600)),
            ("BRZ", 4050 - int(( 0.0 ) * 1600)),
            ("FLZ", 1645 - int(( 0.0 ) * 1600)),
            ("FRZ", 4297 - int(( 0.0 ) * 1600)),
        ]:
            self.axes[axe_name].apg = self.apg_x
            self.update_axes_config()
            self.move(**{axe_name: 5000 + delta})
            self.axes[axe_name].apg = None
            self.update_axes_config()

        self.set_positions(Z=5000)
        self.axe_z.apg = self.apg_x
        self.update_axes_config()
        self.move(Z=15000)
        self.update_axes_positions()

        self.axe_z.apg = None
        self.axe_x1.apg = self.apg_x
        self.axe_x2.apg = self.apg_y
        self.axe_y.apg = self.apg_z
        self.update_axes_config()
        self.set_positions(X1=13200, X2=-14000, Y=-22500)
        self.moveto(X1=12700, X2=-13500, Y=-20000)


    def plan_move(self, min_dt = None, **deltas):
        dts = []

        for axe_name, orig_delta in deltas.items():
            axis = self.axes[axe_name]

            delta = 1.0 * orig_delta * 2**32
            delta = abs(delta)
            max_v = axis.max_v * 50000000.0
            max_a = axis.max_a * 50000000.0 * 1000.0

            accel_dt = sqrt(delta / max_a)
            top_speed = accel_dt * max_a
            plato_dt = 0
            if top_speed > max_v:
                accel_dt = max_v / max_a
                accel_delta = max_v * accel_dt # / 2 * 2 - for average and two ends
                plato_delta = delta - accel_delta
                plato_dt = plato_delta / max_v
            dt = plato_dt + 2 * accel_dt
            dts.append((dt, accel_dt, plato_dt))

        dts.sort()
        dt, accel_dt, plato_dt = dts[-1]
        segs = [[],[],[]]

        accel_dt = int(accel_dt * 1000)
        if accel_dt < 2:
            accel_dt = 2

        plato_dt = int(plato_dt * 1000)
        if plato_dt < 2:
            plato_dt = 2

        if min_dt is not None:
            if plato_dt + 2 * accel_dt < min_dt:
                k = min_dt / (plato_dt + 2 * accel_dt)

                plato_dt = round(plato_dt * k)
                accel_dt = round(accel_dt * k)

        for axe_name, orig_delta in deltas.items():
            axis = self.axes[axe_name]

            delta = 1.0 * orig_delta * 2**32

            v = round(delta / ((accel_dt + plato_dt) * 50000))
            a = round(v / accel_dt * 65536)
            a2 = round(v / (accel_dt - 1) * 65536)

            a_top = a2 * 1.5
            j_avg = a_top / (accel_dt / 2)
            j = round(j_avg * 2)
            jj = round(-j / (accel_dt / 2))

            if abs(j) < 2**31 and abs(jj) < 2**31:
                # S-profile
                segs[0].append(ProfileSegment(axis.apg, target_v=v, a=0, v=0, j=j, jj=jj))
                segs[1].append(ProfileSegment(axis.apg, target_v=0, a=0, j=-j, jj=-jj))
            else:
                # fallback to constant accel
                print("J or JJ out of bounds")
                segs[0].append(ProfileSegment(axis.apg, target_v=v, a=a, v=0))
                segs[1].append(ProfileSegment(axis.apg, target_v=0, a=-a2))

            segs[2].append(ProfileSegment(axis.apg, v=0))

        profile = []
        profile.append([accel_dt + plato_dt, segs[0]])
        profile.append([accel_dt, segs[1]])
        profile.append([10, segs[2]])

        return profile

    def move(self, **deltas):
        print("Move:", deltas)
        self.assign_apgs(deltas.keys())

        profile = self.plan_move(**deltas)

        #print(profile)
        path_code = self.asg.gen_path_code(profile)

        #print(repr(path_code))
        self.exec_code(path_code)

    def moveto(self, **point):
        print("MoveTo:", point)
        self.assign_apgs(point.keys())
        args = {}
        state = self.get_state()
        for s in state:
            pos = point.get(s["name"], None)
            if pos is not None:
                args[s["name"]] = pos - s["x"]

        self.move(**args)

    def set_positions(self, **kw):
        print("SetPositions:", kw)
        for a, v in kw.items():
            self.axes[a].last_pos = v

        set_code = self.asg.gen_set_apg_positions(**kw)
        if set_code:
            self.exec_code(set_code)

    def get_state(self):
        s3g = self.s3g
        result = []
        axes_list = sorted(self.axes.keys())
        for k in axes_list:
            axe = self.axes[k]
            if axe.apg:
                cur_x_hi = s3g.S3G_INPUT(axe.apg.cur_x_hi)
                cur_x_lo = s3g.S3G_INPUT(axe.apg.cur_x_lo)
                cur_v = s3g.S3G_INPUT(axe.apg.cur_v)
                result.append({
                    "name": axe.name,
                    "x": cur_x_hi + (1.0 * cur_x_lo)/2**32,
                    "v": cur_v
                })
        return result

    def update_axes_positions(self):
        state = self.get_state()
        for axis in self.axes.values():
            axis.update_state(state)


import cv2
import numpy as np

def main():
    p = None
    try:
        p = Valurap()
        p.setup()
        p.home()



        #optozero_calibrate_fast(p, True)

    except (KeyboardInterrupt, TimeoutError):
        raise
    finally:
        if p:
            p.setup()


def optozero_calibrate_fast(p, super_fast=False):
    from numpy.linalg import norm

    places = {}
    corners = [
        None,
        [0, 0],
        [3, 0],
        [3, 2],
        [0, 2]
    ]

    i,j = corners[3]
    pl_x, pl_y = place_coords(i, j, places)
    p.moveto(X2=pl_x, Y=pl_y)

    path = [1,2,3,4,1,3,2,1,4,2,4,3]
    random_cycles = 500
    if super_fast:
        path = [1,2,3,4]
        random_cycles = 500

    for k in range(2):
        for n in path:
            i,j = corners[n]

            pl_x, pl_y = place_coords(i, j, places)

            p.moveto(X2=pl_x, Y=pl_y)
            optozero(p)

            state = p.get_state()
            x = state[1]["x"]
            y = state[2]["x"]

            places.setdefault((i, j), []).append((x, y))

    all_places = []
    for i in range(4):
        for j in range(3):
            all_places.append((i, j))

    for i in range(random_cycles):
        i, j = random.choice(all_places)
        pl_x, pl_y = place_coords(i, j, places)

        p.moveto(X2=pl_x, Y=pl_y)
        ret = optozero(p)
        state = p.get_state()
        x = state[1]["x"]
        y = state[2]["x"]
        places.setdefault((i, j), []).append((x, y, ret))

        pickle.dump(places, open("places2.pick", "wb"))

    print(places)

    corners = {}

    for k, v in places.items():
        v = np.mean(np.array(v), 0)
        print(k, v)
        corners[k] = v

    p00 = corners[(0, 0)]
    p01 = corners[(0, 2)]
    p10 = corners[(3, 0)]
    p11 = corners[(3, 2)]

    middle = np.mean(list(corners.values()), 0)

    for k, v in corners.items():
        print(k, v - middle)

    x_ma_low = p00[0] - p01[0]
    x_ma_high = p10[0] - p11[0]
    x_base_low = p00[1] - p01[1]
    x_base_high = p10[1] - p11[1]

    y_ma_low = p00[1] - p10[1]
    y_ma_high = p01[1] - p11[1]
    y_base_low = p00[0] - p10[0]
    y_base_high = p01[0] - p11[0]

    print("x_ma", x_ma_low, x_ma_high)
    print("x_base", x_base_low, x_base_high)
    print("y_ma", y_ma_low, y_ma_high)
    print("y_base", y_base_low, y_base_high)

    x_ma = (x_ma_low + x_ma_high) / 2
    x_base = (x_base_low + x_base_high) / 2
    x_hyp = norm([x_ma, x_base])
    x_cos = (x_base / x_hyp)
    x_sin = (x_ma / x_hyp)

    fi_matrix = np.array([[x_cos, -x_sin], [x_sin, -x_cos]])

    rcorners = {}
    for k, v in corners.items():
        v = (np.matmul(fi_matrix, (v - middle).T + middle.T)).T
        print(k, v)
        rcorners[k] = v

    rp00 = rcorners[(0, 0)]
    rp01 = rcorners[(0, 2)]
    rp10 = rcorners[(3, 0)]
    rp11 = rcorners[(3, 2)]

    rdiag1 = rp11 - rp00
    rdiag2 = rp10 - rp01

    print("rdiag1", rdiag1, norm(rdiag1))
    print("rdiag2", rdiag2, norm(rdiag2))

    ry_ma_low = rp00[1] - rp10[1]
    ry_ma_high = rp01[1] - rp11[1]
    ry_base_low = rp00[0] - rp10[0]
    ry_base_high = rp01[0] - rp11[0]

    print("ry_ma", ry_ma_low, ry_ma_low)
    print("ry_base", ry_base_low, ry_base_high)

    ry_ma = (ry_ma_low + ry_ma_low) / 2
    real_delta = ry_ma / ry_base_low * 41600
    print("real_delta", real_delta)


def place_coords(i, j, places):
    if (i, j) in places:
        pl_x = sum([a[0] for a in places[(i, j)]]) / len(places[(i, j)])
        pl_y = sum([a[1] for a in places[(i, j)]]) / len(places[(i, j)])
    else:
        pl_x = -9600 + i * 6700
        pl_y = 800 + j * 6700
    return pl_x, pl_y


def optozero_calibrate_long(p):
    places = {}
    for k in range(2):
        for i in range(4):
            for j in range(3):
                p.moveto(X2=-9600 + i * 6700, Y=800 + j * 6700)
                optozero(p)

                state = p.get_state()
                x = state[1]["x"]
                y = state[2]["x"]

                places.setdefault((i, j), []).append((x, y))

    for i in range(500):
        pl = random.choice(list(places.keys()))
        pl_x = sum([a[0] for a in places[pl]]) / len(places[pl])
        pl_y = sum([a[1] for a in places[pl]]) / len(places[pl])

        p.moveto(X2=pl_x, Y=pl_y)
        optozero(p)
        state = p.get_state()
        x = state[1]["x"]
        y = state[2]["x"]
        places[pl].append((x, y))

        pickle.dump(places, open("places2.pick", "wb"))

    print(places)


def optozero(p):
    if not p.cap:
        p.cap = cv2.VideoCapture(0)

    size_x = int(640 / 1)
    size_y = int(480 / 1)
    param1 = np.zeros((6 * 6, 3), np.float32)
    param2 = (np.mgrid[-3:3, -3:3] + 0.5).T.reshape(-1, 2)
    params = [param1, param2]
    objp = params[0]
    objp[:, :2] = params[1]
    objp = 2.469438 * objp
    mtx = np.array([[1.85583369e+03, 0.00000000e+00, 7.96781205e+02],
                    [0.00000000e+00, 1.86524428e+03, 6.48427700e+02],
                    [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])
    dist = np.array([[4.38909294e-02, -3.72379589e-01, 5.96935378e-03,
                      -1.39161992e-04, -1.18364075e+00]])

    initial_delta = None
    final_delta = None
    initial_state = None
    final_state = None
    corrections = 0

    for i in range(10):
        for j in range(5):
            ret, frame = p.cap.read()
            print("cap:", ret)
            if not ret:
                print("capture failed, reopen")
                p.cap.release()
                time.sleep(2)
                p.cap = cv2.VideoCapture(0)
            time.sleep(0.2)

        if not ret:
            continue

        small = cv2.cv2.resize(frame, (size_x, size_y))

        ret, circles = cv2.findCirclesGrid(small, (6, 6))
        if not ret:
            print("not found")
            continue

        circles = circles * (1600.0 / size_x)
        print("find:", (circles[0] + circles[5] + circles[30] + circles[35] - np.array(
            [[1600 * 2, 1200 * 2]])))

        retval, rvec, tvec = cv2.solvePnP(objp, circles, mtx, dist)
        print("solved:", retval, rvec.T[0], tvec.T[0])
        dx, dy, dz = tvec.T[0]
        # p.move(Y = 80*dy, X2 = -80*dx)

        if initial_delta is None:
            initial_state = p.get_state()
            initial_delta = [rvec, tvec]

        final_state = p.get_state()
        final_delta = [rvec, tvec]

        if 0:
            rmat = cv2.Rodrigues(rvec)[0]
            camera_position = -np.matrix(rmat).T * np.matrix(tvec)
            print("cam_pos:", camera_position)
            dx = camera_position[0, 0]
            dy = camera_position[1, 0]
            print("dx, dy:", dx, dy)

        x_steps = round(-80 * dx)
        y_steps = round(-80 * dy)

        if abs(x_steps) + abs(y_steps) > 8: # 0.1mm
            p.move(X2=-x_steps, Y=y_steps)
            corrections += 1
        else:
            break

    return initial_delta, initial_state, final_delta, final_state, corrections



if __name__ == "__main__":
    main()
