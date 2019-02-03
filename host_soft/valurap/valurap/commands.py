import random
import struct

import serial

from .packet import encode_payload, decode_packet


class S3GPort(object):
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

    OUT_APG_Y_X_VAL_LO = 16
    OUT_APG_Y_X_VAL_HI = 17
    OUT_APG_Y_V_VAL = 18
    OUT_APG_Y_A_VAL = 19
    OUT_APG_Y_J_VAL = 20
    OUT_APG_Y_JJ_VAL = 21
    OUT_APG_Y_TARGET_V_VAL = 22
    OUT_APG_Y_ABORT_A_VAL = 23

    OUT_APG_Z_X_VAL_LO = 24
    OUT_APG_Z_X_VAL_HI = 25
    OUT_APG_Z_V_VAL = 26
    OUT_APG_Z_A_VAL = 27
    OUT_APG_Z_J_VAL = 28
    OUT_APG_Z_JJ_VAL = 29
    OUT_APG_Z_TARGET_V_VAL = 30
    OUT_APG_Z_ABORT_A_VAL = 31

    OUT_ENDSTOPS_TIMEOUT = 32
    OUT_ENDSTOPS_OPTIONS = 33

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

    OUT_ASG_CONTROL_APG_Y_SET_X =           0x00010000
    OUT_ASG_CONTROL_APG_Y_SET_V =           0x00020000
    OUT_ASG_CONTROL_APG_Y_SET_A =           0x00040000
    OUT_ASG_CONTROL_APG_Y_SET_J =           0x00080000
    OUT_ASG_CONTROL_APG_Y_SET_JJ =          0x00100000
    OUT_ASG_CONTROL_APG_Y_SET_TARGET_V =    0x00200000

    OUT_ASG_CONTROL_APG_Z_SET_X =           0x01000000
    OUT_ASG_CONTROL_APG_Z_SET_V =           0x02000000
    OUT_ASG_CONTROL_APG_Z_SET_A =           0x04000000
    OUT_ASG_CONTROL_APG_Z_SET_J =           0x08000000
    OUT_ASG_CONTROL_APG_Z_SET_JJ =          0x10000000
    OUT_ASG_CONTROL_APG_Z_SET_TARGET_V =    0x20000000

    OUT_MSG_CONTROL_ENABLE_1 =      0x00000001
    OUT_MSG_CONTROL_MUX_1_NONE =    0x00000000
    OUT_MSG_CONTROL_MUX_1_X =       0x00000002
    OUT_MSG_CONTROL_MUX_1_Y =       0x00000004
    OUT_MSG_CONTROL_MUX_1_Z =       0x00000006
    OUT_MSG_CONTROL_INVERT_DIR_1 =  0x00000008

    OUT_MSG_CONTROL_ENABLE_2 =      0x00000010
    OUT_MSG_CONTROL_MUX_2_NONE =    0x00000000
    OUT_MSG_CONTROL_MUX_2_X =       0x00000020
    OUT_MSG_CONTROL_MUX_2_Y =       0x00000040
    OUT_MSG_CONTROL_MUX_2_Z =       0x00000060
    OUT_MSG_CONTROL_INVERT_DIR_2 =  0x00000080

    OUT_MSG_CONTROL_ENABLE_3 =      0x00000100
    OUT_MSG_CONTROL_MUX_3_NONE =    0x00000000
    OUT_MSG_CONTROL_MUX_3_X =       0x00000200
    OUT_MSG_CONTROL_MUX_3_Y =       0x00000400
    OUT_MSG_CONTROL_MUX_3_Z =       0x00000600
    OUT_MSG_CONTROL_INVERT_DIR_3 =  0x00000800

    OUT_MSG_CONTROL_ENABLE_4 =      0x00001000
    OUT_MSG_CONTROL_MUX_4_NONE =    0x00000000
    OUT_MSG_CONTROL_MUX_4_X =       0x00002000
    OUT_MSG_CONTROL_MUX_4_Y =       0x00004000
    OUT_MSG_CONTROL_MUX_4_Z =       0x00006000
    OUT_MSG_CONTROL_INVERT_DIR_4 =  0x00008000

    OUT_MSG_CONTROL_ENABLE_5 =      0x00010000
    OUT_MSG_CONTROL_MUX_5_NONE =    0x00000000
    OUT_MSG_CONTROL_MUX_5_X =       0x00020000
    OUT_MSG_CONTROL_MUX_5_Y =       0x00040000
    OUT_MSG_CONTROL_MUX_5_Z =       0x00060000
    OUT_MSG_CONTROL_INVERT_DIR_5 =  0x00080000

    OUT_MSG_CONTROL_ENABLE_6 =      0x00100000
    OUT_MSG_CONTROL_MUX_6_NONE =    0x00000000
    OUT_MSG_CONTROL_MUX_6_X =       0x00200000
    OUT_MSG_CONTROL_MUX_6_Y =       0x00400000
    OUT_MSG_CONTROL_MUX_6_Z =       0x00600000
    OUT_MSG_CONTROL_INVERT_DIR_6 =  0x00800000

    OUT_ENDSTOPS_OPTIONS_MUX_1_NONE =       0x00000000
    OUT_ENDSTOPS_OPTIONS_MUX_1_X =          0x00000001
    OUT_ENDSTOPS_OPTIONS_MUX_1_Y =          0x00000002
    OUT_ENDSTOPS_OPTIONS_MUX_1_Z =          0x00000003
    OUT_ENDSTOPS_OPTIONS_ABORT_POLARITY_1 = 0x00000004
    OUT_ENDSTOPS_OPTIONS_ABORT_ENABLED_1 =  0x00000008

    OUT_ENDSTOPS_OPTIONS_MUX_2_NONE =       0x00000000
    OUT_ENDSTOPS_OPTIONS_MUX_2_X =          0x00000010
    OUT_ENDSTOPS_OPTIONS_MUX_2_Y =          0x00000020
    OUT_ENDSTOPS_OPTIONS_MUX_2_Z =          0x00000030
    OUT_ENDSTOPS_OPTIONS_ABORT_POLARITY_2 = 0x00000040
    OUT_ENDSTOPS_OPTIONS_ABORT_ENABLED_2 =  0x00000080

    OUT_ENDSTOPS_OPTIONS_MUX_3_NONE =       0x00000000
    OUT_ENDSTOPS_OPTIONS_MUX_3_X =          0x00000100
    OUT_ENDSTOPS_OPTIONS_MUX_3_Y =          0x00000200
    OUT_ENDSTOPS_OPTIONS_MUX_3_Z =          0x00000300
    OUT_ENDSTOPS_OPTIONS_ABORT_POLARITY_3 = 0x00000400
    OUT_ENDSTOPS_OPTIONS_ABORT_ENABLED_3 =  0x00000800

    IN_ASG_DT = 0
    IN_ASG_STEPS = 1

    IN_ENDSTOPS_STATUS_1 = 2
    IN_ENDSTOPS_POS_LO_1 = 3
    IN_ENDSTOPS_POS_HI_1 = 4
    IN_ENDSTOPS_MAX_BOUNCE_1 = 5

    IN_ENDSTOPS_STATUS_2 = 6
    IN_ENDSTOPS_POS_LO_2 = 7
    IN_ENDSTOPS_POS_HI_2 = 8
    IN_ENDSTOPS_MAX_BOUNCE_2 = 9

    IN_ENDSTOPS_STATUS_3 = 10
    IN_ENDSTOPS_POS_LO_3 = 11
    IN_ENDSTOPS_POS_HI_3 = 12
    IN_ENDSTOPS_MAX_BOUNCE_3 = 13

    IN_BE_STATUS = 62
    IN_SE_REG_LB = 63

    STB_ASG_LOAD =  0x00000001
    STB_ENDSTOPS_UNLOCK =  0x00000002
    STB_BE_START =  0x20000000
    STB_BE_ABORT =  0x40000000
    STB_SE_INT_LB = 0x80000000

    INT_ASG_DONE =      0x00000001
    INT_ASG_ABORT =     0x00000002
    INT_ENDSTOP_CHANGED_1 =     0x00000004
    INT_ENDSTOP_CHANGED_2 =     0x00000008
    INT_ENDSTOP_CHANGED_3 =     0x00000010
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
        buf = encode_payload(struct.pack("H", cmd_id) + payload)
        self.port.write(buf)
        self.port.flush()
        while True:
            reply = self.port.read()
            self.data += reply
            try:
                packet, rest = decode_packet(self.data)
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

            packet_cmds = int(len(packet_data)/5)
            payload = struct.pack(
                '<BBH',
                65,
                packet_cmds,
                addr
            ) + packet_data

            addr += packet_cmds
            #print(`payload`)
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