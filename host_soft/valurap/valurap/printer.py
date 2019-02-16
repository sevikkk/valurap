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
from .axes import AxeX1, AxeX2, AxeY, AxeY2
from .commands import S3GPort
from .oled import OLED
from .spi import SPIPort


class Valurap(object):
    def __init__(self):
        self.s3g = S3GPort()
        self.spi = SPIPort()
        self.oled = OLED()
        self.cap = None

        self.asg = Asg(self)

        self.axe_x1 = AxeX1(self)
        self.axe_x2 = AxeX2(self)
        self.axe_y = AxeY(self)
        self.axe_y2 = AxeY2(self)
        self.axes = {
            "X1": self.axe_x1,
            "X2": self.axe_x2,
            "Y": self.axe_y,
            "Y2": self.axe_y2,
        }

        self.apg_x = ApgX(self)
        self.apg_y = ApgY(self)
        self.apg_z = ApgZ(self)
        self.apgs = {
            "X": self.apg_x,
            "Y": self.apg_y,
            "Z": self.apg_z,
        }

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
        s3g.S3G_OUTPUT(s3g.OUT_ENDSTOPS_OPTIONS, 0)     # Disable all endstops

        reset_code = self.asg.gen_reset_code(self.apgs.values())
        print("Executing reset code")
        self.exec_code(reset_code)

        for axe in self.axes.values():
            axe.enabled = False
            axe.apg = None
            axe.endstop_abort = False
        self.update_axes_config()

        with self.oled.draw() as draw:
            draw.rectangle(self.oled.bounding_box, outline="white", fill="black")
            draw.text((10, 10), "Ready", fill="white")

    def exec_code(self, code, addr=0, wait=True):
        s3g = self.s3g
        s3g.S3G_OUTPUT(s3g.OUT_LEDS, 0x55)
        s3g.S3G_WRITE_BUFFER(addr, *code)
        s3g.S3G_OUTPUT(s3g.OUT_BE_START_ADDR, addr)
        s3g.S3G_STB(s3g.STB_ENDSTOPS_UNLOCK)
        s3g.S3G_STB(s3g.STB_BE_START)
        while wait:
            busy = self.check_be_busy()

            if not busy:
                break
            time.sleep(0.1)

    def check_be_busy(self):
        s3g = self.s3g
        status = s3g.S3G_INPUT(s3g.IN_BE_STATUS)
        busy = (status & 0x80000000) >> 31
        waiting = (status & 0x40000000) >> 30
        error = (status & 0x00FF0000) >> 16
        pc = status & 0x0000FFFF
        print("Busy: {} Wait: {} Error: {} PC: {}".format(busy, waiting, error, pc))
        lines = []
        if busy:
            lines.append("B {} W {} E {} P {}".format(busy, waiting, error, pc))
        else:
            lines.append("Idle")

        for sl in self.get_state():
            lines.append("{:2s}{:9.1f} {:8d}".format(sl["name"], sl["x"], sl["v"]))

        with self.oled.draw() as draw:
            draw.rectangle(self.oled.bounding_box, outline="white", fill="black")
            draw.multiline_text((5, 3), "\n".join(lines), fill="white")
        return busy

    def update_axes_config(self):
        s3g = self.s3g

        msg_control = 0
        es_control = 0
        for axe in self.axes.values():
            msg_control |= axe.msg_control()
            es_control |= axe.endstops_control()
            if axe.apg:
                s3g.S3G_OUTPUT(axe.apg.val_abort_a, axe.abort_a)

        s3g.S3G_OUTPUT(s3g.OUT_MSG_CONTROL, msg_control)
        s3g.S3G_OUTPUT(s3g.OUT_ENDSTOPS_OPTIONS, es_control)

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
                print("{} already on endstop")
                continue

            axe.apg = apgs.pop()
            axe.endstop_abort = True

            a = int(axe.home_a * speed)
            target_v = int(axe.home_v * speed)

            if not axe.endstop_at_max:
                a = -a
                target_v = -target_v

            segs.append(ProfileSegment(axe.apg, target_v=target_v, a=a, x=0, v=0))
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
            busy = self.check_be_busy()
            if not busy:
                break

            ints = self.s3g.S3G_INPUT(self.s3g.IN_PENDING_INTS)
            print('{:08X}'.format(ints))

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
        self.axe_x1.apg = None
        self.axe_x2.apg = None
        self.axe_y.apg = None
        self.update_axes_config()
        time.sleep(0.5)

        ret = False
        while not ret:
            ret = self.home_axes([self.axe_x1, self.axe_x2, self.axe_y])

        self.axe_x1.apg = self.apg_x
        self.axe_x2.apg = self.apg_y
        self.axe_y.apg = self.apg_z
        self.update_axes_config()
        self.set_positions(X1=13000, X2=-13000, Y=13000)
        self.move(X1=-25000, X2=13000-9650, Y=-13000+800)


    def move(self, **deltas):
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
        segs = [[],[]]

        accel_dt = int(accel_dt * 1000)
        plato_dt = int(plato_dt * 1000)

        for axe_name, orig_delta in deltas.items():
            axis = self.axes[axe_name]

            delta = orig_delta * 2**32

            v = int(delta / ((accel_dt + plato_dt) * 50000))
            a = int(v / (accel_dt - 1))

            segs[0].append(ProfileSegment(axis.apg, target_v=v, a=a, v=0))
            segs[1].append(ProfileSegment(axis.apg, target_v=0, a=-a))

        profile = []
        profile.append([accel_dt + plato_dt, segs[0]])
        profile.append([accel_dt, segs[1]])

        print(profile)

        path_code = self.asg.gen_path_code(profile)

        print(repr(path_code))
        self.exec_code(path_code)

    def set_positions(self, **kw):
        set_code = self.asg.gen_set_apg_positions(**kw)
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


import numpy as np
import cv2

def main():
    p = None
    try:
        p = Valurap()
        p.setup()
        p.home()

        states = []

        for i in range(1):
            optozero(p)
            states.append(p.get_state())

            p.move(X2=6700)
            optozero(p)
            states.append(p.get_state())

            p.move(X2=6700)
            optozero(p)
            states.append(p.get_state())

            p.move(X2=6700)
            optozero(p)
            states.append(p.get_state())

            p.move(Y=6700)
            optozero(p)
            states.append(p.get_state())

            p.move(X2=-6700)
            optozero(p)
            states.append(p.get_state())

            p.move(X2=-6700)
            optozero(p)
            states.append(p.get_state())

            p.move(X2=-6700)
            optozero(p)
            states.append(p.get_state())

            p.move(Y=6700)
            optozero(p)
            states.append(p.get_state())

            p.move(X2=6700)
            optozero(p)
            states.append(p.get_state())

            p.move(X2=6700)
            optozero(p)
            states.append(p.get_state())

            p.move(X2=6700)
            optozero(p)
            states.append(p.get_state())

            p.move(X2=-6700*3, Y = -6700*2)

        places = {}
        for state in states:
            x = state[1]["x"]
            y = state[2]["x"]

            i = round((x + 9608.0)/6700)
            j = round((y - 800.0)/6700)
            print(i, j, x, y)
            places.setdefault((i, j),[]).append((x, y))

        for i in range(500):
            pl = random.choice(list(places.keys()))
            pl_x = sum([a[0] for a in places[pl]])/len(places[pl])
            pl_y = sum([a[1] for a in places[pl]])/len(places[pl])

            state = p.get_state()
            x = state[1]["x"]
            y = state[2]["x"]
            p.move(X2=pl_x - x, Y=pl_y - y)
            optozero(p)
            state = p.get_state()
            x = state[1]["x"]
            y = state[2]["x"]
            places[pl].append((x,y))

            pickle.dump(places, open("places.pick", "wb"))

        print(places)

    except (KeyboardInterrupt, TimeoutError):
        raise
    finally:
        if p:
            p.setup()


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

        if abs(dx) + abs(dy) > 0.03:
            p.move(X2=-80 * dx, Y=80 * dy)
            pos = p.get_state()
            print(pos)
        else:
            break



if __name__ == "__main__":
    main()
