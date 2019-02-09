"""
Run:
   seva@orange:~/src/sevasoft/valurap/host_soft$ python -m valurap.printer
"""

import time

from .asg import Asg, ProfileSegment
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
        s3g.S3G_CLEAR(-1)                               # Clear any pending interrupts
        s3g.S3G_CLEAR(-1)                               # Clear any pending interrupts
        s3g.S3G_OUTPUT(s3g.OUT_MSG_CONTROL, 0)          # Disable all motors
        s3g.S3G_OUTPUT(s3g.OUT_ENDSTOPS_OPTIONS, 0)     # Disable all endstops

        reset_code = self.asg.gen_reset_code(self.apgs.values())
        print("Executing reset code")
        self.exec_code(reset_code)
        with self.oled.draw() as draw:
            draw.rectangle(self.oled.bounding_box, outline="white", fill="black")
            draw.text((10, 10), "Ready", fill="white")

    def exec_code(self, code, addr=0, wait=True):
        s3g = self.s3g
        s3g.S3G_OUTPUT(s3g.OUT_LEDS, 0x55)
        s3g.S3G_WRITE_BUFFER(addr, *code)
        s3g.S3G_OUTPUT(s3g.OUT_BE_START_ADDR, addr)
        s3g.S3G_STB(s3g.STB_BE_START)
        s3g.S3G_STB(s3g.STB_ENDSTOPS_UNLOCK)
        while wait:
            status = s3g.S3G_INPUT(s3g.IN_BE_STATUS)
            busy = (status & 0x80000000) >> 31
            waiting = (status & 0x40000000) >> 30
            error = (status & 0x00FF0000) >> 16
            pc = status & 0x0000FFFF
            x_x = s3g.S3G_INPUT(s3g.IN_APG_X_X)
            x_v = s3g.S3G_INPUT(s3g.IN_APG_X_V)
            y_x = s3g.S3G_INPUT(s3g.IN_APG_Y_X)
            y_v = s3g.S3G_INPUT(s3g.IN_APG_Y_V)
            z_x = s3g.S3G_INPUT(s3g.IN_APG_Z_X)
            z_v = s3g.S3G_INPUT(s3g.IN_APG_Z_V)
            print("Busy: {} Wait: {} Error: {} PC: {}".format(busy, waiting, error, pc))
            with self.oled.draw() as draw:
                draw.rectangle(self.oled.bounding_box, outline="white", fill="black")
                draw.multiline_text((5, 3), "B {} W {} E {} P {}\nX{:8d} {:10d}\nY{:8d} {:10d}\nZ{:8d} {:10d}".format(
                    busy, waiting, error, pc, x_x, x_v, y_x, y_v, z_x, z_v), fill="white")
            if not busy:
                break
            time.sleep(0.3)
        with self.oled.draw() as draw:
            draw.rectangle(self.oled.bounding_box, outline="white", fill="black")
            draw.multiline_text((5, 3), "Idle\nX{:8d} {:10d}\nY{:8d} {:10d}\nZ{:8d} {:10d}".format(
                x_x, x_v, y_x, y_v, z_x, z_v), fill="white")

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

    def home_axe(self, axe):
        axe.apg = self.apg_x
        axe.endstops_abort = True
        self.update_axes_config()

        a = axe.home_a
        target_v = axe.home_v

        if not axe.endstop_at_max:
            a = -a
            target_v = -target_v

        seg = ProfileSegment(self.apg_x, target_v=target_v, a=a, x=0, v=0)
        path_code = self.asg.gen_path_code([
            [30000, [seg]]
        ])

        self.exec_code(path_code, wait=False)

        axe.apg = None
        axe.endstops_abort = False
        self.update_axes_config()

    def home(self):
        self.axe_x1.enabled = True
        self.axe_x2.enabled = True
        self.axe_y.enabled = True
        self.update_axes_config()
        time.sleep(0.5)

        self.home_axe(self.axe_x1)

    def test(self):
        self.axe_x1.enabled = True
        self.axe_x2.enabled = True
        self.axe_y.enabled = True
        self.axe_x1.endstop_abort = True
        self.axe_x2.endstop_abort = True
        self.axe_y.endstop_abort = True

        self.axe_x1.apg = self.apg_x
        self.axe_x2.apg = self.apg_y
        self.axe_y.apg = self.apg_z

        self.update_axes_config()
        time.sleep(0.5)

        path_code = self.asg.gen_path_code([
            [15000, [
                ProfileSegment(self.apg_x, target_v=100000, a=5000, x=0, v=0),
                ProfileSegment(self.apg_y, target_v=-100000, a=-5000, x=0, v=0),
                ProfileSegment(self.apg_z, target_v=100000, a=5000, x=0, v=0),
            ]],
            # [1000, [
            #    ProfileSegment(self.apg_x, target_v=0, a=-5000),
            #    ProfileSegment(self.apg_y, target_v=0, a=5000),
            #    ProfileSegment(self.apg_z, target_v=0, a=-5000),
            # ]],
        ])

        print(repr(path_code))
        self.exec_code(path_code)

        self.axe_x1.enabled = False
        self.axe_x2.enabled = False
        self.axe_y.enabled = False

        self.update_axes_config()


def main():
    p = None
    try:
        p = Valurap()
        p.setup()
        p.test()
    except KeyboardInterrupt:
        if p:
            p.setup()


if __name__ == "__main__":
    main()
