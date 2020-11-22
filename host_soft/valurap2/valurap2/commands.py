import struct

from valurap.s3g import S3GPortBase


class S3GPort(S3GPortBase):
    default_baudrate = 1500000
    OUT_ASG_DT_VAL = 0
    OUT_ASG_STEPS_VAL = 1

    OUT_SP_CONFIG = 2
    OUT_SP_CONFIF_STEP_BIT = (OUT_SP_CONFIG, 5, 0)

    OUT_MSG_ALL_PRE_N = 3
    OUT_MSG_ALL_PULSE_N = 4
    OUT_MSG_ALL_POST_N = 5
    OUT_MSG_X_VAL = 6

    OUT_MSG_CONFIG0 = 7
    OUT_MSG_CONFIG_ES_MUX = (OUT_MSG_CONFIG0, 2, 0)
    OUT_MSG_CONFIG_ES_ABORT = (OUT_MSG_CONFIG0, 3)
    OUT_MSG_CONFIG_SP_MUX = (OUT_MSG_CONFIG0, 6, 4)
    OUT_MSG_CONFIG_SP_ENABLE = (OUT_MSG_CONFIG0, 7)
    OUT_MSG_CONFIG_INVERT = (OUT_MSG_CONFIG0, 8)
    OUT_MSG_CONFIG_SET_X = (OUT_MSG_CONFIG0, 9)
    OUT_MSG_CONFIG_ENABLE = (OUT_MSG_CONFIG0, 15)

    OUT_MSG_CONFIG1 = 8
    OUT_MSG_CONFIG2 = 9
    OUT_MSG_CONFIG3 = 10
    OUT_MSG_CONFIG4 = 11
    OUT_MSG_CONFIG5 = 12
    # Unused
    OUT_SE_REG_LB = 63

    IN_BE_STATUS = 0
    IN_APG_STATUS = 1
    IN_ES_STATUS = 2
    IN_FIFO_FREE_SPACE = 3
    IN_FIFO_DATA_COUNT = 4
    IN_MOTOR1_HOLD_X = 5
    IN_MOTOR2_HOLD_X = 6
    IN_MOTOR3_HOLD_X = 7
    IN_MOTOR4_HOLD_X = 8
    IN_MOTOR5_HOLD_X = 9
    IN_MOTOR6_HOLD_X = 10
    IN_MOTOR7_HOLD_X = 11
    IN_MOTOR8_HOLD_X = 12
    IN_MOTOR9_HOLD_X = 13
    IN_MOTOR10_HOLD_X = 14
    IN_MOTOR11_HOLD_X = 15
    IN_MOTOR12_HOLD_X = 16
    # Unused
    IN_SE_REG_LB = 63

    STB_BE_START = 0x00000001
    STB_BE_ABORT = 0x00000002
    STB_ASG_START = 0x00000004
    STB_ASG_ABORT = 0x00000008
    STB_ASG_LOAD_DONE = 0x00000010
    STB_SP_ZERO = 0x00000020
    STB_MSG_SET_X = 0x00000040
    STB_ES_UNLOCK = 0x00000080
    STB_APG0_ABORT = 0x00000100
    STB_APG1_ABORT = 0x00000200
    STB_APG2_ABORT = 0x00000400
    STB_APG3_ABORT = 0x00000800
    STB_APG4_ABORT = 0x00001000
    STB_APG5_ABORT = 0x00002000
    STB_APG6_ABORT = 0x00004000
    STB_APG7_ABORT = 0x00008000
    # Unused
    STB_SE_INT_LB = 0x80000000

    INT_BE_DONE = 0x00000001
    INT_ASG_LOAD = 0x00000002
    INT_ASG_DONE = 0x00000004
    INT_ASG_ABORT = 0x00000008
    # Unused
    INT_APG0_ABORT_DONE = 0x00000100
    INT_APG1_ABORT_DONE = 0x00000200
    INT_APG2_ABORT_DONE = 0x00000400
    INT_APG3_ABORT_DONE = 0x00000800
    INT_APG4_ABORT_DONE = 0x00001000
    INT_APG5_ABORT_DONE = 0x00002000
    INT_APG6_ABORT_DONE = 0x00004000
    INT_APG7_ABORT_DONE = 0x00008000
    # Unused
    INT_SE_INT_LB = 0x80000000

    def S3G_OUTPUT(self, reg, value, cmd_id=None):
        """
        Set output to value
        """
        if value > 2 ** 31:
            value = value - 2 ** 32

        payload = struct.pack("<BBi", 60, reg, value)

        reply = self.send_and_wait_reply(payload, cmd_id)
        if reply[0] != 0x81:
            raise RuntimeError("Unexpected reply code")
        return

    def S3G_INPUT(self, reg, cmd_id=None):
        """
        Get value of input
        @return value
        """
        payload = struct.pack("<BB", 61, reg)

        reply = self.send_and_wait_reply(payload, cmd_id)
        if reply[0] != 0x81 or len(reply) != 5:
            raise RuntimeError("Unexpected reply")
        value = struct.unpack("<i", reply[1:5])[0]
        return value

    def S3G_STB(self, value, cmd_id=None):
        """
        Send strobe
        """
        payload = struct.pack("<BI", 62, value)

        reply = self.send_and_wait_reply(payload, cmd_id)
        if reply[0] != 0x81:
            raise RuntimeError("Unexpected reply code")
        return

    def S3G_CLEAR(self, value, cmd_id=None):
        """
        Clear pending interrupt
        """
        payload = struct.pack("<BI", 63, value)

        reply = self.send_and_wait_reply(payload, cmd_id)
        if reply[0] != 0x81:
            raise RuntimeError("Unexpected reply code")
        return

    def S3G_MASK(self, value, cmd_id=None):
        """
        Mask interrupts
        """
        payload = struct.pack("<BI", 64, value)

        reply = self.send_and_wait_reply(payload, cmd_id)
        if reply[0] != 0x81:
            raise RuntimeError("Unexpected reply code")
        return

    def S3G_WRITE_FIFO(self, *values, **kw):
        """
        Write data to buf_executor memory
        """

        data = bytearray().join(values)
        l = len(data)
        if l % 5 != 0:
            raise ValueError("Buffer length is not multiple of 5")

        l = l / 5
        while data:
            if l < 40:
                packet_data = data
                data = None
            else:
                packet_data = data[: 40 * 5]
                data = data[40 * 5 :]

            packet_cmds = int(len(packet_data) / 5)
            payload = struct.pack("<BB", 66, packet_cmds) + packet_data
            #s = []
            #for ch in payload:
            #    s.append("%02X" % ch)
            #print("".join(s))

            # print(`payload`)
            reply = self.send_and_wait_reply(payload, kw.get("cmd_id", None), timeout=0.1)
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

        if val > 2 ** 31:
            val = val - 2 ** 32

        try:
            data = struct.pack("<iB", val, 64 + reg)
        except:
            print("regs:", reg, val)
            raise

        return data

    def _BUF_simple(self, cmd, args):
        """
        Generic template
        """
        val = 0
        for v in args:
            val |= v

        data = struct.pack("<iB", val, 128 + cmd)

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

    def BUF_WAIT_FIFO(self, *args):
        """
        Wait for at least this number of commands already in fifo
        """
        return self._BUF_simple(5, args)

    def BUF_PARAM_ADDR(self, *args):
        """
        Set address pointer
        """
        return self._BUF_simple(6, args)

    def BUF_PARAM_WRITE_HI(self, *args):
        """
        Write high half of register
        """
        return self._BUF_simple(7, args)

    def BUF_PARAM_WRITE_LO(self, n, *args):
        """
        Write low half of register and increment address
        """
        assert n >= 0 and n <= 6
        return self._BUF_simple(8 + n, args)

    def BUF_PARAM_WRITE_LO_NC(self, *args):
        """
        Write low half of register and set address to the next bank
        """
        return self._BUF_simple(15, args)

    def BUF_DONE(self, *args):
        """
        Finish execution
        """
        return self._BUF_simple(63, args)
