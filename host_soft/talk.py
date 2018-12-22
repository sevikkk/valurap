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
        print("Unexpected packet: {}".format(str(packet)))

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
        Get the firmware version number of the connected machine
        @return Version number
        """
        payload = struct.pack('<BBi', 60, reg, value)

        reply = self.send_and_wait_reply(payload, cmd_id)
        if reply[0] != 0x81:
            raise RuntimeError("Unexpected reply code")
        return


    def S3G_INPUT(self, reg, cmd_id=None):
        """
        Get the firmware version number of the connected machine
        @return Version number
        """
        payload = struct.pack('<BB', 61, reg)

        reply = self.send_and_wait_reply(payload, cmd_id)
        if reply[0] != 0x81 or len(reply) != 5:
            raise RuntimeError("Unexpected reply")
        value = struct.unpack("<i", reply[1:5])[0]
        return value


    def S3G_STB(self, value, cmd_id=None):
        """
        Get the firmware version number of the connected machine
        @return Version number
        """
        payload = struct.pack('<Bi', 62, value)

        reply = self.send_and_wait_reply(payload, cmd_id)
        if reply[0] != 0x81:
            raise RuntimeError("Unexpected reply code")
        return


    def S3G_CLEAR(self, value, cmd_id=None):
        """
        Get the firmware version number of the connected machine
        @return Version number
        """
        payload = struct.pack('<Bi', 63, value)

        reply = self.send_and_wait_reply(payload, cmd_id)
        if reply[0] != 0x81:
            raise RuntimeError("Unexpected reply code")
        return


    def S3G_MASK(self, value, cmd_id=None):
        """
        Get the firmware version number of the connected machine
        @return Version number
        """
        payload = struct.pack('<Bi', 64, value)

        reply = self.send_and_wait_reply(payload, cmd_id)
        if reply[0] != 0x81:
            raise RuntimeError("Unexpected reply code")
        return


    def format_buf_cmd(self, cmd, *args):
        code = 0
        arg = 0
        if cmd == "OUTPUT":
            code = 0x40 + args[0]
            arg = args[1]
        elif cmd == "NOP":
            code = 0x80
        elif cmd == "STB":
            code = 0x81
            arg = self.list_to_val(args[0])
        elif cmd == "WAIT_ALL":
            code = 0x82
            arg = self.list_to_val(args[0])
        elif cmd == "WAIT_ANY":
            code = 0x83
            arg = self.list_to_val(args[0])
        elif cmd == "CLEAR":
            code = 0x84
            arg = self.list_to_val(args[0])
        elif cmd == "DONE":
            code = 0xBF
            if len(args) > 0:
                arg = args[0]
            else:
                arg = 127
        else:
            raise RuntimeError, "bad command"

        return code, arg


    def S3G_WRITE_BUFFER(self, addr, cmd_id=None, *values):
        """
        Get the firmware version number of the connected machine
        @return Version number
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
            reply = self.send_and_wait_reply(payload, cmd_id)
            if reply[0] != 0x81:
                raise RuntimeError("Unexpected reply code")
        return


def test_LEDS():
    bot = S3GFormatter()
    serial = i2c(port=0, address=0x3C)
    device = ssd1306(serial)

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

if __name__ == "__main__":
    test_LEDS()
