from .commands import S3GPort


class Axe(object):
    endstop_at_max = False
    control_enable = 0
    control_mux = {
        "X": 0,
        "Y": 0,
        "Z": 0,
    }
    endstops_mux = {
        "X": 0,
        "Y": 0,
        "Z": 0,
    }
    endstops_abort = 0

    abort_a = 20000
    home_a = 5000
    home_v = 500000
    home_v2 = 50000

    def __init__(self, bot):
        self.bot = bot
        self.enabled = False
        self.endstop_abort = False
        self.apg = None

    def msg_control(self):
        control = 0

        if self.enabled:
            control |= self.control_enable

        if self.apg:
            control |= self.control_mux[self.apg.name]

        return control

    def endstops_control(self):
        control = 0

        if self.endstop_abort:
            control |= self.endstops_abort

        if self.apg:
            control |= self.endstops_mux[self.apg.name]

        return control


class AxeX1(Axe):
    endstop_at_max = True
    control_enable = S3GPort.OUT_MSG_CONTROL_ENABLE_3
    control_mux = {
        "X": S3GPort.OUT_MSG_CONTROL_MUX_3_X,
        "Y": S3GPort.OUT_MSG_CONTROL_MUX_3_Y,
        "Z": S3GPort.OUT_MSG_CONTROL_MUX_3_Z,
    }
    endstops_mux = {
        "X": S3GPort.OUT_ENDSTOPS_OPTIONS_MUX_2_X,
        "Y": S3GPort.OUT_ENDSTOPS_OPTIONS_MUX_2_Y,
        "Z": S3GPort.OUT_ENDSTOPS_OPTIONS_MUX_2_Z,
    }
    endstops_abort = (
            S3GPort.OUT_ENDSTOPS_OPTIONS_ABORT_ENABLED_2
            | S3GPort.OUT_ENDSTOPS_OPTIONS_ABORT_POLARITY_2
    )


class AxeX2(Axe):
    endstop_at_max = False
    control_enable = S3GPort.OUT_MSG_CONTROL_ENABLE_4
    control_mux = {
        "X": S3GPort.OUT_MSG_CONTROL_MUX_4_X,
        "Y": S3GPort.OUT_MSG_CONTROL_MUX_4_Y,
        "Z": S3GPort.OUT_MSG_CONTROL_MUX_4_Z,
    }
    endstops_mux = {
        "X": S3GPort.OUT_ENDSTOPS_OPTIONS_MUX_1_X,
        "Y": S3GPort.OUT_ENDSTOPS_OPTIONS_MUX_1_Y,
        "Z": S3GPort.OUT_ENDSTOPS_OPTIONS_MUX_1_Z,
    }
    endstops_abort = (
            S3GPort.OUT_ENDSTOPS_OPTIONS_ABORT_ENABLED_1
            | S3GPort.OUT_ENDSTOPS_OPTIONS_ABORT_POLARITY_1
    )


class AxeY(Axe):
    """
    Combined Axe for both Y motors
    """
    endstop_at_max = True
    control_enable = (
        S3GPort.OUT_MSG_CONTROL_ENABLE_1
        | S3GPort.OUT_MSG_CONTROL_ENABLE_2
        | S3GPort.OUT_MSG_CONTROL_INVERT_DIR_1
    )
    control_mux = {
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
    endstops_mux = {
        "X": S3GPort.OUT_ENDSTOPS_OPTIONS_MUX_3_X,
        "Y": S3GPort.OUT_ENDSTOPS_OPTIONS_MUX_3_Y,
        "Z": S3GPort.OUT_ENDSTOPS_OPTIONS_MUX_3_Z,
    }
    endstops_abort = (
            S3GPort.OUT_ENDSTOPS_OPTIONS_ABORT_ENABLED_3
            | S3GPort.OUT_ENDSTOPS_OPTIONS_ABORT_POLARITY_3
    )


class AxeY2(Axe):
    """
    Second Y motor alone
    """
    endstop_at_max = None
    control_enable = (
            S3GPort.OUT_MSG_CONTROL_ENABLE_2
    )
    control_mux = {
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
