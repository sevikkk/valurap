#!/usr/bin/env python

import time
from traceback import print_exc
import logging
import struct
import random
import serial

import s3g_pkt

from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306

class S3GFormatter(object):
    OUT_LEDS = 0
    OUT_ASG_STEPS_VAL = 1
    OUT_ASG_DT_VAL = 2
    OUT_ASG_CONTROL = 3

    OUT_MSG_ALL_PRE_N = 4
    OUT_MSG_ALL_PULSE_N = 5
    OUT_MSG_ALL_POST_N = 6
    OUT_MSG_CONTROL = 7
    OUT_APG_X_X_VAL_LO = 8
    OUT_APG_X_X_VAL_HI = 9
    OUT_APG_X_V_VAL = 10
    OUT_APG_X_A_VAL = 11
    OUT_APG_X_J_VAL = 12
    OUT_APG_X_JJ_VAL = 13
    OUT_APG_X_TARGET_V_VAL = 14
    OUT_APG_X_ABORT_A_VAL = 15
    OUT_BE_START_ADDR = 62
    OUT_SE_REG_LB = 63

    OUT_ASG_CONTROL_SET_STEPS_LIMIT =       0x00000001
    OUT_ASG_CONTROL_SET_DT_LIMIT =          0x00000002
    OUT_ASG_CONTROL_RESET_STEPS =           0x00000004
    OUT_ASG_CONTROL_RESET_DT =              0x00000008
    OUT_ASG_CONTROL_APG_X_SET_X =           0x00000100
    OUT_ASG_CONTROL_APG_X_SET_V =           0x00000200
    OUT_ASG_CONTROL_APG_X_SET_A =           0x00000400
    OUT_ASG_CONTROL_APG_X_SET_J =           0x00000800
    OUT_ASG_CONTROL_APG_X_SET_JJ =          0x00001000
    OUT_ASG_CONTROL_APG_X_SET_TARGET_V =    0x00002000
    OUT_ASG_CONTROL_APG_Y_SET_X =           0x00004000
    OUT_ASG_CONTROL_APG_Y_SET_V =           0x00008000
    OUT_ASG_CONTROL_APG_Y_SET_A =           0x00010000
    OUT_ASG_CONTROL_APG_Y_SET_J =           0x00020000
    OUT_ASG_CONTROL_APG_Y_SET_JJ =          0x00040000
    OUT_ASG_CONTROL_APG_Y_SET_TARGET_V =    0x00080000

    OUT_MSG_CONTROL_ENABLE_X = 0x00000001
    OUT_MSG_CONTROL_ENABLE_Y = 0x00000002

    IN_SE_REG_LB = 63

    STB_ASG_LOAD =  0x00000001
    STB_BE_START =  0x20000000
    STB_BE_ABORT =  0x40000000
    STB_SE_INT_LB = 0x80000000

    INT_ASG_DONE =      0x00000001
    INT_ASG_ABORT =     0x00000002
    INT_BE_COMPLETE =   0x40000000
    INT_SE_INT_LB =     0x80000000

    def __init__(self, port = '/dev/ttyS1', baudrate=115200):
        self.port = serial.Serial(port, baudrate=baudrate, timeout=0.1)
        self.data = bytearray()

    def unexpected_packet(self, packet):
        print("Unexpected packet: {}".format(repr(packet)))

    def send_and_wait_reply(self, payload, cmd_id=None):
        if cmd_id is None:
            cmd_id = random.randint(1000, 65000)
        buf = s3g_pkt.encode_payload(struct.pack("H", cmd_id) + payload)
        self.port.write(buf)
        self.port.flush()
        while True:
            reply = self.port.read()
            self.data += reply
            try:
                packet, rest = s3g_pkt.decode_packet(self.data)
            except ValueError as e:
                pass
            else:
                self.data = rest
                reply_cmd_id = struct.unpack("H", packet[:2])[0]
                if cmd_id == reply_cmd_id:
                    return packet[2:]
                else:
                    self.unexpected_packet(packet)


    def S3G_OUTPUT(self, reg, value, cmd_id=None):
        """
        Set output to value
        """
        payload = struct.pack('<BBi', 60, reg, value)

        reply = self.send_and_wait_reply(payload, cmd_id)
        if reply[0] != 0x81:
            raise RuntimeError("Unexpected reply code")
        return


    def S3G_INPUT(self, reg, cmd_id=None):
        """
        Get value of input
        @return value
        """
        payload = struct.pack('<BB', 61, reg)

        reply = self.send_and_wait_reply(payload, cmd_id)
        if reply[0] != 0x81 or len(reply) != 5:
            raise RuntimeError("Unexpected reply")
        value = struct.unpack("<i", reply[1:5])[0]
        return value


    def S3G_STB(self, value, cmd_id=None):
        """
        Send strobe
        """
        payload = struct.pack('<Bi', 62, value)

        reply = self.send_and_wait_reply(payload, cmd_id)
        if reply[0] != 0x81:
            raise RuntimeError("Unexpected reply code")
        return


    def S3G_CLEAR(self, value, cmd_id=None):
        """
        Clear pending interrupt
        """
        payload = struct.pack('<Bi', 63, value)

        reply = self.send_and_wait_reply(payload, cmd_id)
        if reply[0] != 0x81:
            raise RuntimeError("Unexpected reply code")
        return


    def S3G_MASK(self, value, cmd_id=None):
        """
        Mask interrupts
        """
        payload = struct.pack('<Bi', 64, value)

        reply = self.send_and_wait_reply(payload, cmd_id)
        if reply[0] != 0x81:
            raise RuntimeError("Unexpected reply code")
        return


    def S3G_WRITE_BUFFER(self, addr, *values, **kw):
        """
        Write data to buf_executor memory
        """

        data = bytearray().join(values)
        l = len(data)
        if l % 5 != 0:
            raise ValueError("Buffer length is not mutiple of 5")

        l = l / 5
        while data:
            if l < 40:
                packet_data = data
                data = None
            else:
                packet_data = data[:40*5]
                data = data[40*5:]

            packet_cmds = len(packet_data)/5
            payload = struct.pack(
                '<BBH',
                65,
                packet_cmds,
                addr
            ) + packet_data

            addr += packet_cmds
            print(`payload`)
            reply = self.send_and_wait_reply(payload, kw.get("cmd_id", None))
            if reply[0] != 0x81:
                raise RuntimeError("Unexpected reply code")
        return

    def BUF_OUTPUT(self, reg, *args):
        """
        Set output to value
        """
        val = 0
        for v in args:
            val |= v

        data = struct.pack('<iB', val, 64+reg)

        return data


    def _BUF_simple(self, cmd, args):
        """
        Generic template
        """
        val = 0
        for v in args:
            val |= v

        data = struct.pack('<iB', val, 128 + cmd)

        return data

    def BUF_STB(self, *args):
        """
        Send strobes
        """

        return self._BUF_simple(1, args)

    def BUF_WAIT_ALL(self, *args):
        """
        Wait for all specified interrupts
        """
        return self._BUF_simple(2, args)

    def BUF_WAIT_ANY(self, *args):
        """
        Wait for any of specified interrupts
        """
        return self._BUF_simple(3, args)

    def BUF_CLEAR(self, *args):
        """
        Clear pending interrupts
        """
        return self._BUF_simple(4, args)

    def BUF_DONE(self, *args):
        """
        Finish execution
        """
        return self._BUF_simple(63, args)


def test_LEDS():
    bot = S3GFormatter()
    serial = i2c(port=0, address=0x3C)
    device = ssd1306(serial)
    bot.S3G_CLEAR(-1)

    i = 0
    while 1:
        bot.S3G_OUTPUT(bot.OUT_LEDS, i)
        bot.S3G_OUTPUT(bot.OUT_SE_REG_LB, i)
        r = bot.S3G_INPUT(bot.IN_SE_REG_LB)
        if i != r:
            print(i, r)
        i = (i + 1) % 256
        with canvas(device) as draw:
            draw.rectangle(device.bounding_box, outline="white", fill="black")
            draw.text((10, 10), "i: {:3d}".format(i), fill="white")

def test_executor():
    bot = S3GFormatter()
    bot.S3G_CLEAR(-1)
    bot.S3G_CLEAR(-1)
    bot.S3G_OUTPUT(bot.OUT_LEDS, 0x55)
    bot.S3G_WRITE_BUFFER(
        0,
        bot.BUF_OUTPUT(bot.OUT_LEDS, 0x1),

        bot.BUF_OUTPUT(bot.OUT_MSG_ALL_PRE_N, 100), # 10 ms on step cycle - 2-6-2 ms
        bot.BUF_OUTPUT(bot.OUT_MSG_ALL_PULSE_N, 500),
        bot.BUF_OUTPUT(bot.OUT_MSG_ALL_POST_N, 600),

        bot.BUF_OUTPUT(bot.OUT_ASG_DT_VAL, 50000), # 1 kHz acceleration steps
        bot.BUF_OUTPUT(bot.OUT_APG_X_ABORT_A_VAL, 100),

        bot.BUF_OUTPUT(bot.OUT_MSG_CONTROL,
                       bot.OUT_MSG_CONTROL_ENABLE_X
                       ),

        bot.BUF_OUTPUT(bot.OUT_ASG_STEPS_VAL, 10000), # 0.5 seconds
        bot.BUF_OUTPUT(bot.OUT_ASG_CONTROL,
                        bot.OUT_ASG_CONTROL_SET_STEPS_LIMIT,
                        bot.OUT_ASG_CONTROL_SET_DT_LIMIT,
                        bot.OUT_ASG_CONTROL_RESET_STEPS,
                        bot.OUT_ASG_CONTROL_RESET_DT,
                        bot.OUT_ASG_CONTROL_APG_X_SET_JJ,
                        bot.OUT_ASG_CONTROL_APG_X_SET_J,
                        bot.OUT_ASG_CONTROL_APG_X_SET_A,
                        bot.OUT_ASG_CONTROL_APG_X_SET_V,
                        bot.OUT_ASG_CONTROL_APG_X_SET_X,
                        bot.OUT_ASG_CONTROL_APG_X_SET_TARGET_V
                       ),
        bot.BUF_OUTPUT(bot.OUT_APG_X_X_VAL_LO, 0),
        bot.BUF_OUTPUT(bot.OUT_APG_X_X_VAL_HI, 0),
        bot.BUF_OUTPUT(bot.OUT_APG_X_V_VAL, 0),
        bot.BUF_OUTPUT(bot.OUT_APG_X_A_VAL, 200),
        bot.BUF_OUTPUT(bot.OUT_APG_X_J_VAL, 0),
        bot.BUF_OUTPUT(bot.OUT_APG_X_JJ_VAL, 0),
        bot.BUF_OUTPUT(bot.OUT_APG_X_TARGET_V_VAL,2000000),

        bot.BUF_STB(bot.STB_ASG_LOAD),
        bot.BUF_OUTPUT(bot.OUT_ASG_CONTROL,
                         bot.OUT_ASG_CONTROL_SET_STEPS_LIMIT |
                         bot.OUT_ASG_CONTROL_RESET_STEPS |
                         bot.OUT_ASG_CONTROL_APG_X_SET_A
                        ),
        bot.BUF_OUTPUT(bot.OUT_ASG_STEPS_VAL, 3000),
        bot.BUF_OUTPUT(bot.OUT_APG_X_A_VAL, 0),

        bot.BUF_WAIT_ALL(bot.INT_ASG_DONE),
        bot.BUF_CLEAR(bot.INT_ASG_DONE),
        bot.BUF_STB(bot.STB_ASG_LOAD),
        bot.BUF_OUTPUT(bot.OUT_LEDS, 0x3),

        bot.BUF_OUTPUT(bot.OUT_ASG_CONTROL,
                       bot.OUT_ASG_CONTROL_SET_STEPS_LIMIT |
                       bot.OUT_ASG_CONTROL_RESET_STEPS |
                       bot.OUT_ASG_CONTROL_APG_X_SET_A |
                       bot.OUT_ASG_CONTROL_APG_X_SET_TARGET_V
                       ),
        bot.BUF_OUTPUT(bot.OUT_ASG_STEPS_VAL, 10000),
        bot.BUF_OUTPUT(bot.OUT_APG_X_A_VAL, -300),
        bot.BUF_OUTPUT(bot.OUT_APG_X_TARGET_V_VAL, 0),

        bot.BUF_WAIT_ALL(bot.INT_ASG_DONE),
        bot.BUF_CLEAR(bot.INT_ASG_DONE),
        bot.BUF_STB(bot.STB_ASG_LOAD),
        bot.BUF_OUTPUT(bot.OUT_LEDS, 0x7),

        bot.BUF_OUTPUT(bot.OUT_ASG_CONTROL,
                        bot.OUT_ASG_CONTROL_SET_DT_LIMIT
                        ),
        bot.BUF_OUTPUT(bot.OUT_ASG_DT_VAL, 0), # 1 kHz acceleration steps

        bot.BUF_WAIT_ALL(bot.INT_ASG_DONE),
        bot.BUF_CLEAR(bot.INT_ASG_DONE),
        bot.BUF_STB(bot.STB_ASG_LOAD),
        bot.BUF_OUTPUT(bot.OUT_LEDS, 0xf),
        bot.BUF_OUTPUT(bot.OUT_MSG_CONTROL, 0),
        bot.BUF_DONE()
    )
    bot.S3G_OUTPUT(bot.OUT_BE_START_ADDR, 0)
    bot.S3G_MASK(0)
    bot.S3G_STB(bot.STB_BE_START)
    while 1:
        status = bot.S3G_INPUT(62)
        print("%8X" % status)
        time.sleep(0.1)
        if status > 0:
            break

    bot.S3G_CLEAR(-1)



if __name__ == "__main__":
    #test_LEDS()
    test_executor()
