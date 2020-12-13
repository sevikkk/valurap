import struct
from collections import deque

class CommandBuffer(object):
    OUT_ASG_DT_VAL = 0
    OUT_ASG_STEPS_VAL = 1

    OUT_SP_CONFIG = 2
    OUT_SP_CONFIG_STEP_BIT = (OUT_SP_CONFIG, 0, 5)

    OUT_MSG_ALL_PRE_N = 3
    OUT_MSG_ALL_PULSE_N = 4
    OUT_MSG_ALL_POST_N = 5
    OUT_MSG_X_VAL = 6

    OUT_MSG_CONFIG0 = 7
    OUT_MSG_CONFIG_ES_MUX = (OUT_MSG_CONFIG0, 0, 3)
    OUT_MSG_CONFIG_ES_ABORT = (OUT_MSG_CONFIG0, 3)
    OUT_MSG_CONFIG_SP_MUX = (OUT_MSG_CONFIG0, 4, 3)
    OUT_MSG_CONFIG_SP_ENABLE = (OUT_MSG_CONFIG0, 7)
    OUT_MSG_CONFIG_INVERT = (OUT_MSG_CONFIG0, 8)
    OUT_MSG_CONFIG_SET_X = (OUT_MSG_CONFIG0, 9)
    OUT_MSG_CONFIG_ENABLE = (OUT_MSG_CONFIG0, 15)

    OUT_MSG_CONFIG1 = 8
    OUT_MSG_CONFIG2 = 9
    OUT_MSG_CONFIG3 = 10
    OUT_MSG_CONFIG4 = 11
    OUT_MSG_CONFIG5 = 12
    OUT_ES_TIMEOUT = 13
    # Unused
    OUT_SE_REG_LB = 63

    IN_BE_STATUS = 0
    IN_BE_STATUS_BUSY = (IN_BE_STATUS, 0)
    IN_BE_STATUS_ABORTING = (IN_BE_STATUS, 1)
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
    IN_MOTOR1_X = 17
    IN_MOTOR2_X = 18
    IN_MOTOR3_X = 19
    IN_MOTOR4_X = 20
    IN_MOTOR5_X = 21
    IN_MOTOR6_X = 22
    IN_MOTOR7_X = 23
    IN_MOTOR8_X = 24
    IN_MOTOR9_X = 25
    IN_MOTOR10_X = 26
    IN_MOTOR11_X = 27
    IN_MOTOR12_X = 28
    # Unused
    IN_PENDING_INTS = 62
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

    PARAM_STATUS = 0
    PARAM_V_EFF = 1
    PARAM_V_IN = 2
    PARAM_V_OUT = 3
    PARAM_A = 4
    PARAM_J = 5
    PARAM_JJ = 6
    PARAM_TARGET_V = 7
    PARAM_ABORT_A = 8

    PARAM_STATUS_ENABLE = 0x00000001
    PARAM_STATUS_TARGET_V = 0x00000002

    def __init__(self, debug=False):
        self.debug = debug
        self.reset()

    def reset(self):
        self.buffer = deque()
        self.last_addr = None
        self.segments_state = "init"

    def format_field(self, field_descr, val):
        if len(field_descr) == 2:
            reg, bit_num = field_descr
            bit_len = 1
        else:
            reg, bit_num, bit_len = field_descr
        mask = 2 ** bit_len - 1
        return (val & mask) << bit_num

    def extract_field(self, field_descr, val):
        if len(field_descr) == 2:
            reg, bit_num = field_descr
            bit_len = 1
        else:
            reg, bit_num, bit_len = field_descr
        mask = 2 ** bit_len - 1
        return (val >> bit_num) & mask

    def BUF_OUTPUT(self, reg, val):
        """
        Set output to value
        """

        if val > 2 ** 31:
            val = val - 2 ** 32

        try:
            data = struct.pack("<iB", val, 64 + reg)
        except:
            print("regs:", reg, val)
            raise

        if self.debug:
            print("BUF_OUTPUT({}, {})".format(reg, val))

        self.buffer.append(data)

    def _BUF_simple(self, cmd, val):
        """
        Generic template
        """

        if val > 2 ** 31:
            val = val - 2 ** 32

        data = struct.pack("<iB", val, 128 + cmd)

        self.buffer.append(data)

    def BUF_STB(self, val):
        """
        Send strobes
        """

        if self.debug:
            print("BUF_STB(0x{:08X})".format(val))

        self._BUF_simple(1, val)

    def BUF_WAIT_ALL(self, val):
        """
        Wait for all specified interrupts
        """
        if self.debug:
            print("BUF_WAIT_ALL(0x{:08X})".format(val))

        self._BUF_simple(2, val)

    def BUF_WAIT_ANY(self, val):
        """
        Wait for any of specified interrupts
        """
        if self.debug:
            print("BUF_WAIT_ANY(0x{:08X})".format(val))

        self._BUF_simple(3, val)

    def BUF_CLEAR(self, val):
        """
        Clear pending interrupts
        """
        if self.debug:
            print("BUF_CLEAR(0x{:08X})".format(val))

        self._BUF_simple(4, val)

    def BUF_WAIT_FIFO(self, val):
        """
        Wait for at least this number of commands already in fifo
        """
        if self.debug:
            print("BUF_WAIT_FIFO({})".format(val))

        self._BUF_simple(5, val)

    def BUF_PARAM_ADDR(self, val):
        """
        Set address pointer
        """
        if self.debug:
            print("BUF_PARAM_ADDR({})".format(val))

        self.last_addr = val
        self._BUF_simple(6, val)

    def BUF_PARAM_WRITE_HI(self, val):
        """
        Write high half of register
        """
        if self.debug:
            print("BUF_WRITE_HI({})".format(val))

        self._BUF_simple(7, val)

    def BUF_PARAM_WRITE_LO(self, n, val):
        """
        Write low half of register and increment address
        """
        assert n >= 0 and n <= 6
        self.last_addr += n
        if self.debug:
            print("BUF_PARAM_WRITE_LO({}, {})".format(n, val))

        self._BUF_simple(8 + n, val)

    def BUF_PARAM_WRITE_LO_NC(self, val):
        """
        Write low half of register and set address to the next bank
        """
        if self.debug:
            print("BUF_PARAM_WRITE_LO_NC({})".format(val))

        self.last_addr = (self.last_addr + 0x20) & 0xE0
        self._BUF_simple(15, val)

    def BUF_DONE(self, val=0):
        """
        Finish execution
        """
        if self.debug:
            print("BUF_DONE({})".format(val))

        self._BUF_simple(63, val)

    def write_param(self, chan, addr, value):
        value_lo = value & 0xffffffff
        if value_lo >= 2 ** 31:
            value_lo -= 2 ** 32

        value_hi = value >> 32
        if value_hi >= 2 ** 31:
            value_hi -= 2 ** 32

        if value_lo >= 0 and value_hi == 0:
            value_hi = None
        elif value_lo < 0 and value_hi == -1:
            value_hi = None

        full_addr = chan * 0x20 + addr
        need_addr = False
        if self.last_addr is None:
            need_addr = True
        else:
            addr_delta = full_addr - self.last_addr
            addr_nc = (self.last_addr + 0x20) & 0xE0

            if addr_delta >= 0 and addr_delta <= 6:
                self.BUF_PARAM_WRITE_LO(addr_delta, value_lo)
            elif full_addr == addr_nc:
                self.BUF_PARAM_WRITE_LO_NC(value_lo)
            else:
                need_addr = True

        if need_addr:
            self.BUF_PARAM_ADDR(full_addr)
            self.BUF_PARAM_WRITE_LO(0, value_lo)

        if value_hi is not None:
            self.BUF_PARAM_WRITE_HI(0, value_hi)

    def hw_reset(self):
        self.BUF_STB(self.STB_ASG_ABORT)

        self.BUF_OUTPUT(self.OUT_SP_CONFIG, 40)           # step_bit = 40
        self.BUF_OUTPUT(self.OUT_MSG_ALL_PRE_N, 100)          # pre_n
        self.BUF_OUTPUT(self.OUT_MSG_ALL_PULSE_N, 400)          # pulse_n
        self.BUF_OUTPUT(self.OUT_MSG_ALL_POST_N, 500)          # post_n
        self.BUF_OUTPUT(self.OUT_ES_TIMEOUT, 500000)       # ES_TIMEOUT 10ms

        for i in range(8):
            self.BUF_OUTPUT(self.OUT_MSG_CONFIG0 + i, 1)   # disarm all motors

        self.BUF_OUTPUT(self.OUT_ASG_DT_VAL, 50000)  # 1ms accel steps
        self.BUF_OUTPUT(self.OUT_ASG_STEPS_VAL, 5)  # 5 steps

        # set zeroes
        for i in range(8):
            self.write_param(i, self.PARAM_STATUS, 0)
            self.write_param(i, self.PARAM_V_EFF, 0)
            self.write_param(i, self.PARAM_V_OUT, 0)
            self.write_param(i, self.PARAM_A, 0)
            self.write_param(i, self.PARAM_J, 0)
            self.write_param(i, self.PARAM_JJ, 0)

        self.BUF_CLEAR(-1)   # clear all ending ints just in case

        self.BUF_STB(self.STB_ASG_START)  # Start ASG cycles
        self.BUF_WAIT_ALL(self.INT_ASG_LOAD)  # Wait for APG ready for new segment
        self.BUF_CLEAR(self.INT_ASG_LOAD)  # Clear pending int
        self.BUF_OUTPUT(self.OUT_ASG_STEPS_VAL, 0)  # steps_val = 0 - End of path
        self.BUF_STB(self.STB_ASG_LOAD_DONE)
        self.BUF_WAIT_ALL(self.INT_ASG_DONE)  # Wait for ASG done
        self.BUF_CLEAR(self.INT_ASG_DONE)

        # reset counters for all motors
        val = self.format_field(self.OUT_MSG_CONFIG_SET_X, 1)
        val = val | (val << 16)
        for i in range(6):
            self.BUF_OUTPUT(self.OUT_MSG_CONFIG0 + i, val)   # set SET_X for al motors
        self.BUF_OUTPUT(self.OUT_MSG_X_VAL, 0)   # value to set
        self.BUF_STB(self.STB_MSG_SET_X)   # set x values
        self.BUF_STB(self.STB_SP_ZERO)   # reset speed integrators

        self.BUF_CLEAR(-1)   # clear all ending ints just in case

    def add_segments_head(self, pp):
        assert self.segments_state == "init"
        self.BUF_CLEAR(-1)   # clear all ending ints just in case
        self.BUF_STB(self.STB_ES_UNLOCK)
        self.BUF_OUTPUT(self.OUT_ASG_DT_VAL, pp.apg_states[0].accel_step)
        self.segments_state = "body"

    def add_segments_tail(self, pp):
        assert self.segments_state == "body"
        self.segments_state = "init"

    def add_segments(self, segments):
        assert self.segments_state == "body"
        first = True
        j_set = {}
        jj_set = {}
        for dt, segs in segments:
            self.BUF_OUTPUT(self.OUT_ASG_STEPS_VAL, dt)  # 5 steps
            all_segs = {v.apg: v for v in segs}
            for chan in range(8):
                if chan not in all_segs:
                    self.write_param(chan, self.PARAM_STATUS, 0)
                    j_set[chan] = True
                    jj_set[chan] = True
                    continue

                seg = all_segs[chan]
                status = self.PARAM_STATUS_ENABLE
                if seg.target_v is not None:
                    status |= self.PARAM_STATUS_TARGET_V

                self.write_param(chan, self.PARAM_STATUS, status)
                if seg.v is not None:
                    self.write_param(chan, self.PARAM_V_OUT, seg.v)
                self.write_param(chan, self.PARAM_A, seg.a)
                if seg.j == 0 and seg.jj == 0:
                    if j_set.get(chan, True) or jj_set.get(chan, True):
                        self.write_param(chan, self.PARAM_J, 0)
                    if jj_set.get(chan, True):
                        self.write_param(chan, self.PARAM_JJ, 0)
                    j_set[chan] = False
                    jj_set[chan] = False
                elif seg.j != 0 and seg.jj == 0:
                    self.write_param(chan, self.PARAM_J, seg.j)
                    if jj_set.get(chan, True):
                        self.write_param(chan, self.PARAM_JJ, 0)
                    j_set[chan] = True
                    jj_set[chan] = False
                else:
                    self.write_param(chan, self.PARAM_J, seg.j)
                    self.write_param(chan, self.PARAM_JJ, seg.jj)
                    j_set[chan] = True
                    jj_set[chan] = True

                if seg.target_v is not None:
                    self.write_param(chan, self.PARAM_TARGET_V, seg.target_v)

            if first:
                self.BUF_STB(self.STB_ASG_START)  # Start ASG cycles
                self.BUF_WAIT_ALL(self.INT_ASG_LOAD)  # Wait for APG ready for new segment
                self.BUF_CLEAR(self.INT_ASG_LOAD)  # Clear pending int
                first = False
            else:
                self.BUF_STB(self.STB_ASG_LOAD_DONE)  # Inform ASG, next segment setup is done
                self.BUF_WAIT_ALL(self.INT_ASG_LOAD)
                self.BUF_CLEAR(self.INT_ASG_LOAD)

        if not first:
            self.BUF_OUTPUT(self.OUT_ASG_STEPS_VAL, 0)  # steps_val = 0 - End of path
            self.BUF_STB(self.STB_ASG_LOAD_DONE)
            self.BUF_WAIT_ALL(self.INT_ASG_DONE)  # Wait for ASG done
            self.BUF_CLEAR(self.INT_ASG_DONE)

    def enable_axes(self, modes=None):
        if modes is None:
            modes = ["print", "e1", "e2"]

        # Home configuration
        # SG:   X1  X2  YL  YR  ZFL ZFR ZBL ZBR
        #        0   1   2   3   4   5   6   7
        #
        # Print configuration
        # SG:   X1  X2   Y   Z  E1  E2  --  --
        #        0   1   2   3   4   5   6   7
        #
        # EndStops: X2  X1  YL  YR  ZBR ZBL ZFR ZFL
        #            0   1   2   3   4   5   6   7
        #
        # Motor  Axe  ES Invert HomeSG PrintSG HomeCFG PrintCFG
        #   1    ZFL   7    -      4     3      80cf     80b0
        #   2    ZBR   4    -      7     3      80fc     80b0
        #   3    ZBL   5    -      6     3      80ed     80b0
        #   4    E1    -    -      -     4      0000     80c0
        #   5    E2    -    -      -     5      0000     80d0
        #   6    ZFR   6    -      5     3      80de     80b0
        #   7    X1    1    I      0     0      8189     8180
        #   8    X2    0    -      1     1      8098     8090
        #   9    --                             0000     0000
        #  10    --                             0000     0000
        #  11    YR    3    -      3     2      80bb     80a0
        #  12    YL    2    I      2     2      81aa     81a0
        cfgs = {
            "home": [
                0x80f080c0,   # ZBR   ZFL
                0x000080e0,   # E1    ZBL
                0x80d00000,   # ZFR   E2
                0x80908180,   # X2    X1
                0x00000000,   # --    --
                0x81a080b0,   # YL    YR
            ],

            "es_z": [
                0x000c000f,   # ZBR   ZFL
                0x0000000d,   # E1    ZBL
                0x000e0000,   # ZFR   E2
                0x00000000,   # X2    X1
                0x00000000,   # --    --
                0x00000000,   # YL    YR
            ],

            "es_xy": [
                0x00000000,   # ZBR   ZFL
                0x00000000,   # E1    ZBL
                0x00000000,   # ZFR   E2
                0x00080009,   # X2    X1
                0x00000000,   # --    --
                0x000a000b,   # YL    YR
            ],

            "e1": [
                0x00000000,  # ZBR   ZFL
                0x80000000,  # E1    ZBL
                0x00000000,  # ZFR   E2
                0x00000000,  # X2    X1
                0x00000000,  # --    --
                0x00000000,  # YL    YR
            ],

            "e2": [
                0x00000000,  # ZBR   ZFL
                0x00000000,  # E1    ZBL
                0x00008000,  # ZFR   E2
                0x00000000,  # X2    X1
                0x00000000,  # --    --
                0x00000000,  # YL    YR
            ],

            "print": [
                0x80b080b0,  # ZBR   ZFL
                0x00c080b0,  # E1    ZBL
                0x80b000d0,  # ZFR   E2
                0x80908180,  # X2    X1
                0x00000000,  # --    --
                0x81a080a0,  # YL    YR
            ],
        }

        cfg = [0, 0, 0, 0, 0, 0]
        for mode in modes:
            assert mode in cfgs
            for k in range(6):
                cfg[k] |= cfgs[mode][k]

        for i in range(6):
            self.BUF_OUTPUT(self.OUT_MSG_CONFIG0 + i, cfg[i])