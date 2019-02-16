from .commands import S3GPort


class Axe(object):
    endstop_at_max = False
    _control_enable = 0
    _control_mux = {
        "X": 0,
        "Y": 0,
        "Z": 0,
    }
    _endstops_mux = {
        "X": 0,
        "Y": 0,
        "Z": 0,
    }
    _endstops_abort = 0
    _endstops_polarity = 0
    _endstops_status = None

    endstop_int = 0

    abort_a = 20000
    home_a = 15000
    home_v = 500000

    max_v = 1000000
    max_a = 5000
    max_j = 5000

    name = None

    def __init__(self, bot):
        self.bot = bot
        self.enabled = False
        self.endstop_abort = False
        self.apg = None

    def msg_control(self):
        control = 0

        if self.enabled:
            control |= self._control_enable

        if self.apg:
            control |= self._control_mux[self.apg.name]

        return control

    def endstops_control(self):
        control = 0

        if self.endstop_abort:
            control |= self._endstops_abort | self._endstops_polarity

        if self.apg:
            control |= self._endstops_mux[self.apg.name]

        return control

    def endstops_status(self):
        if self._endstops_status is None:
            return False

        status = bool(self.bot.s3g.S3G_INPUT(self._endstops_status) & S3GPort.IN_ENDSTOPS_STATUS_MASK_STATUS)
        mask = bool(self._endstops_polarity)
        return not(status ^ mask)



class AxeX1(Axe):
    name = "X1"
    endstop_at_max = True
    _control_enable = S3GPort.OUT_MSG_CONTROL_ENABLE_3
    _control_mux = {
        "X": S3GPort.OUT_MSG_CONTROL_MUX_3_X,
        "Y": S3GPort.OUT_MSG_CONTROL_MUX_3_Y,
        "Z": S3GPort.OUT_MSG_CONTROL_MUX_3_Z,
    }
    _endstops_mux = {
        "X": S3GPort.OUT_ENDSTOPS_OPTIONS_MUX_2_X,
        "Y": S3GPort.OUT_ENDSTOPS_OPTIONS_MUX_2_Y,
        "Z": S3GPort.OUT_ENDSTOPS_OPTIONS_MUX_2_Z,
    }
    _endstops_abort = S3GPort.OUT_ENDSTOPS_OPTIONS_ABORT_ENABLED_2
    _endstops_polarity = S3GPort.OUT_ENDSTOPS_OPTIONS_ABORT_POLARITY_2
    _endstops_status = S3GPort.IN_ENDSTOPS_STATUS_2
    endstop_int = S3GPort.INT_ENDSTOP_CHANGED_2


class AxeX2(Axe):
    name = "X2"
    endstop_at_max = False
    _control_enable = S3GPort.OUT_MSG_CONTROL_ENABLE_4
    _control_mux = {
        "X": S3GPort.OUT_MSG_CONTROL_MUX_4_X,
        "Y": S3GPort.OUT_MSG_CONTROL_MUX_4_Y,
        "Z": S3GPort.OUT_MSG_CONTROL_MUX_4_Z,
    }
    _endstops_mux = {
        "X": S3GPort.OUT_ENDSTOPS_OPTIONS_MUX_1_X,
        "Y": S3GPort.OUT_ENDSTOPS_OPTIONS_MUX_1_Y,
        "Z": S3GPort.OUT_ENDSTOPS_OPTIONS_MUX_1_Z,
    }

    _endstops_abort = S3GPort.OUT_ENDSTOPS_OPTIONS_ABORT_ENABLED_1
    _endstops_polarity = S3GPort.OUT_ENDSTOPS_OPTIONS_ABORT_POLARITY_1
    _endstops_status = S3GPort.IN_ENDSTOPS_STATUS_1
    endstop_int = S3GPort.INT_ENDSTOP_CHANGED_1


class AxeY(Axe):
    name = "Y"
    """
    Combined Axe for both Y motors
    """
    endstop_at_max = True
    _control_enable = (
        S3GPort.OUT_MSG_CONTROL_ENABLE_1
        | S3GPort.OUT_MSG_CONTROL_ENABLE_2
        | S3GPort.OUT_MSG_CONTROL_INVERT_DIR_1
    )
    _control_mux = {
        "X": (
                S3GPort.OUT_MSG_CONTROL_MUX_1_X
                | S3GPort.OUT_MSG_CONTROL_MUX_2_X
        ),
        "Y": (
                S3GPort.OUT_MSG_CONTROL_MUX_1_Y
                | S3GPort.OUT_MSG_CONTROL_MUX_2_Y
        ),
        "Z": (
            S3GPort.OUT_MSG_CONTROL_MUX_1_Z
            | S3GPort.OUT_MSG_CONTROL_MUX_2_Z
        ),
    }
    _endstops_mux = {
        "X": S3GPort.OUT_ENDSTOPS_OPTIONS_MUX_3_X,
        "Y": S3GPort.OUT_ENDSTOPS_OPTIONS_MUX_3_Y,
        "Z": S3GPort.OUT_ENDSTOPS_OPTIONS_MUX_3_Z,
    }

    _endstops_abort = S3GPort.OUT_ENDSTOPS_OPTIONS_ABORT_ENABLED_3
    _endstops_polarity = S3GPort.OUT_ENDSTOPS_OPTIONS_ABORT_POLARITY_3
    _endstops_status = S3GPort.IN_ENDSTOPS_STATUS_3
    endstop_int = S3GPort.INT_ENDSTOP_CHANGED_3

    abort_a = 20000
    home_a = 5000
    home_v = 500000

class AxeY2(Axe):
    name = "Y2"
    """
    Second Y motor alone
    """
    endstop_at_max = None
    _control_enable = (
            S3GPort.OUT_MSG_CONTROL_ENABLE_2
    )
    _control_mux = {
        "X": (
                S3GPort.OUT_MSG_CONTROL_MUX_2_X
        ),
        "Y": (
                S3GPort.OUT_MSG_CONTROL_MUX_2_Y
        ),
        "Z": (
                S3GPort.OUT_MSG_CONTROL_MUX_2_Z
        ),
    }

    abort_a = 20000
    home_a = 5000
    home_v = 200000
