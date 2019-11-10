import time

from .commands import S3GPort


class Axe(object):
    endstop_at_max = False
    _msg_control = S3GPort.OUT_MSG_CONTROL
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

    max_v = 2000000
    max_a = 7000
    max_j = 5000

    name = None

    def __init__(self, bot):
        self.bot = bot
        self.enabled = False
        self.endstop_abort = False
        self.apg = None
        self.last_pos = None
        self.last_used = 0

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

        if type(self._endstops_status) == int:
            self._endstops_status = [self._endstops_status]

        final_status = False

        for reg in self._endstops_status:
            status = bool(self.bot.s3g.S3G_INPUT(reg) & S3GPort.IN_ENDSTOPS_STATUS_MASK_STATUS)
            mask = bool(self._endstops_polarity)
            final_status = final_status or not(status ^ mask)

        return final_status

    def update_state(self, state):
        new_state = [a for a in state if a["name"] == self.name]
        if new_state:
            new_state = new_state[0]
            assert new_state["v"] == 0
            if self.last_pos != new_state["x"]:
                print("Save position:", self.name, new_state["x"])
                self.last_used = time.time()
                self.last_pos = new_state["x"]


class Axe_MC2(Axe):
    _msg_control = S3GPort.OUT_MSG_CONTROL2


class AxeX1(Axe):
    """
    Back X motor
    """
    name = "X1"
    endstop_at_max = True
    _control_enable = S3GPort.OUT_MSG_CONTROL_ENABLE_7
    _control_mux = {
        "X": S3GPort.OUT_MSG_CONTROL_MUX_7_X,
        "Y": S3GPort.OUT_MSG_CONTROL_MUX_7_Y,
        "Z": S3GPort.OUT_MSG_CONTROL_MUX_7_Z,
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
    """
    Front X motor
    """
    name = "X2"
    endstop_at_max = False
    _control_enable = (
            S3GPort.OUT_MSG_CONTROL_ENABLE_8
            | S3GPort.OUT_MSG_CONTROL_INVERT_DIR_8
    )
    _control_mux = {
        "X": S3GPort.OUT_MSG_CONTROL_MUX_8_X,
        "Y": S3GPort.OUT_MSG_CONTROL_MUX_8_Y,
        "Z": S3GPort.OUT_MSG_CONTROL_MUX_8_Z,
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


class AxeY(Axe_MC2):
    name = "Y"
    """
    Combined Axe for both Y motors
    """
    endstop_at_max = False
    _control_enable = (
        S3GPort.OUT_MSG_CONTROL2_ENABLE_11
        | S3GPort.OUT_MSG_CONTROL2_INVERT_DIR_11
        | S3GPort.OUT_MSG_CONTROL2_ENABLE_12
    )
    _control_mux = {
        "X": (
                S3GPort.OUT_MSG_CONTROL2_MUX_11_X
                | S3GPort.OUT_MSG_CONTROL2_MUX_12_X
        ),
        "Y": (
                S3GPort.OUT_MSG_CONTROL2_MUX_11_Y
                | S3GPort.OUT_MSG_CONTROL2_MUX_12_Y
        ),
        "Z": (
            S3GPort.OUT_MSG_CONTROL2_MUX_11_Z
            | S3GPort.OUT_MSG_CONTROL2_MUX_12_Z
        ),
    }
    _endstops_mux = {
        "X": (
                S3GPort.OUT_ENDSTOPS_OPTIONS_MUX_3_X
                | S3GPort.OUT_ENDSTOPS_OPTIONS_MUX_4_X
        ),
        "Y": (
                S3GPort.OUT_ENDSTOPS_OPTIONS_MUX_3_Y
                | S3GPort.OUT_ENDSTOPS_OPTIONS_MUX_4_Y
        ),
        "Z": (
            S3GPort.OUT_ENDSTOPS_OPTIONS_MUX_3_Z
            | S3GPort.OUT_ENDSTOPS_OPTIONS_MUX_4_Z
        ),
    }

    _endstops_abort = (
        S3GPort.OUT_ENDSTOPS_OPTIONS_ABORT_ENABLED_3
        | S3GPort.OUT_ENDSTOPS_OPTIONS_ABORT_ENABLED_4
    )
    _endstops_polarity = (
        S3GPort.OUT_ENDSTOPS_OPTIONS_ABORT_POLARITY_3
        | S3GPort.OUT_ENDSTOPS_OPTIONS_ABORT_POLARITY_4
    )
    _endstops_status = [
        S3GPort.IN_ENDSTOPS_STATUS_3,
        S3GPort.IN_ENDSTOPS_STATUS_4,
    ]
    endstop_int = S3GPort.INT_ENDSTOP_CHANGED_3 | S3GPort.INT_ENDSTOP_CHANGED_4


    abort_a = 20000
    home_a = 5000
    home_v = 500000

class AxeY1(Axe_MC2):
    name = "Y1"
    """
    First (left) Y motor alone
    """
    endstop_at_max = False
    _control_enable = (
            S3GPort.OUT_MSG_CONTROL2_ENABLE_12
    )
    _control_mux = {
        "X": (
                S3GPort.OUT_MSG_CONTROL2_MUX_12_X
        ),
        "Y": (
                S3GPort.OUT_MSG_CONTROL2_MUX_12_Y
        ),
        "Z": (
                S3GPort.OUT_MSG_CONTROL2_MUX_12_Z
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
    home_v = 200000


class AxeY2(Axe_MC2):
    name = "Y2"
    """
    Second (right) Y motor alone
    """
    endstop_at_max = False
    _control_enable = (
            S3GPort.OUT_MSG_CONTROL2_ENABLE_11
            | S3GPort.OUT_MSG_CONTROL2_INVERT_DIR_11
    )
    _control_mux = {
        "X": (
                S3GPort.OUT_MSG_CONTROL2_MUX_11_X
        ),
        "Y": (
                S3GPort.OUT_MSG_CONTROL2_MUX_11_Y
        ),
        "Z": (
                S3GPort.OUT_MSG_CONTROL2_MUX_11_Z
        ),
    }

    _endstops_mux = {
        "X": S3GPort.OUT_ENDSTOPS_OPTIONS_MUX_4_X,
        "Y": S3GPort.OUT_ENDSTOPS_OPTIONS_MUX_4_Y,
        "Z": S3GPort.OUT_ENDSTOPS_OPTIONS_MUX_4_Z,
    }

    _endstops_abort = S3GPort.OUT_ENDSTOPS_OPTIONS_ABORT_ENABLED_4
    _endstops_polarity = S3GPort.OUT_ENDSTOPS_OPTIONS_ABORT_POLARITY_4
    _endstops_status = S3GPort.IN_ENDSTOPS_STATUS_4
    endstop_int = S3GPort.INT_ENDSTOP_CHANGED_4

    abort_a = 20000
    home_a = 5000
    home_v = 200000


class AxeE1(Axe):
    name = "E1"
    """
    First Extruder
    """

    endstop_at_max = None
    _control_enable = (
        S3GPort.OUT_MSG_CONTROL_ENABLE_4
    )
    _control_mux = {
        "X": (
            S3GPort.OUT_MSG_CONTROL_MUX_4_X
        ),
        "Y": (
            S3GPort.OUT_MSG_CONTROL_MUX_4_Y
        ),
        "Z": (
            S3GPort.OUT_MSG_CONTROL_MUX_4_Z
        ),
    }

    abort_a = 20000
    home_a = 5000
    home_v = 200000


class AxeE2(Axe):
    name = "E2"
    """
    Second Extruder
    """

    endstop_at_max = None
    _control_enable = (
            S3GPort.OUT_MSG_CONTROL_ENABLE_5
    )
    _control_mux = {
        "X": (
                S3GPort.OUT_MSG_CONTROL_MUX_5_X
        ),
        "Y": (
                S3GPort.OUT_MSG_CONTROL_MUX_5_Y
        ),
        "Z": (
                S3GPort.OUT_MSG_CONTROL_MUX_5_Z
        ),
    }

    abort_a = 20000
    home_a = 5000
    home_v = 200000

class AxeE3(Axe_MC2):
    name = "E3"
    """
    Third Extruder
    """

    endstop_at_max = None
    _control_enable = (
            S3GPort.OUT_MSG_CONTROL2_ENABLE_9
    )
    _control_mux = {
        "X": (
                S3GPort.OUT_MSG_CONTROL2_MUX_9_X
        ),
        "Y": (
                S3GPort.OUT_MSG_CONTROL2_MUX_9_Y
        ),
        "Z": (
                S3GPort.OUT_MSG_CONTROL2_MUX_9_Z
        ),
    }

    abort_a = 20000
    home_a = 5000
    home_v = 200000


class AxeM10(Axe_MC2):
    name = "M10"
    """
    Motor 10
    """

    endstop_at_max = None
    _control_enable = (
        S3GPort.OUT_MSG_CONTROL2_ENABLE_10
    )
    _control_mux = {
        "X": (
            S3GPort.OUT_MSG_CONTROL2_MUX_10_X
        ),
        "Y": (
            S3GPort.OUT_MSG_CONTROL2_MUX_10_Y
        ),
        "Z": (
            S3GPort.OUT_MSG_CONTROL2_MUX_10_Z
        ),
    }

    abort_a = 20000
    home_a = 5000
    home_v = 200000


class AxeZ(Axe):
    name = "Z"
    """
    All motors of Z
    """

    endstop_at_max = False
    _control_enable = (
        S3GPort.OUT_MSG_CONTROL_ENABLE_1
        | S3GPort.OUT_MSG_CONTROL_ENABLE_2
        | S3GPort.OUT_MSG_CONTROL_ENABLE_3
        | S3GPort.OUT_MSG_CONTROL_ENABLE_6
        | S3GPort.OUT_MSG_CONTROL_INVERT_DIR_1
        | S3GPort.OUT_MSG_CONTROL_INVERT_DIR_2
        | S3GPort.OUT_MSG_CONTROL_INVERT_DIR_3
        | S3GPort.OUT_MSG_CONTROL_INVERT_DIR_6
    )
    _control_mux = {
        "X": (
            S3GPort.OUT_MSG_CONTROL_MUX_1_X
            | S3GPort.OUT_MSG_CONTROL_MUX_2_X
            | S3GPort.OUT_MSG_CONTROL_MUX_3_X
            | S3GPort.OUT_MSG_CONTROL_MUX_6_X
        ),
        "Y": (
                S3GPort.OUT_MSG_CONTROL_MUX_1_Y
                | S3GPort.OUT_MSG_CONTROL_MUX_2_Y
                | S3GPort.OUT_MSG_CONTROL_MUX_3_Y
                | S3GPort.OUT_MSG_CONTROL_MUX_6_Y
        ),
        "Z": (
                S3GPort.OUT_MSG_CONTROL_MUX_1_Z
                | S3GPort.OUT_MSG_CONTROL_MUX_2_Z
                | S3GPort.OUT_MSG_CONTROL_MUX_3_Z
                | S3GPort.OUT_MSG_CONTROL_MUX_6_Z
        ),
    }

    _endstops_mux = {
        "X": (
                S3GPort.OUT_ENDSTOPS_OPTIONS_MUX_5_X
                | S3GPort.OUT_ENDSTOPS_OPTIONS_MUX_6_X
                | S3GPort.OUT_ENDSTOPS_OPTIONS_MUX_7_X
                | S3GPort.OUT_ENDSTOPS_OPTIONS_MUX_8_X
        ),
        "Y": (
                S3GPort.OUT_ENDSTOPS_OPTIONS_MUX_5_Y
                | S3GPort.OUT_ENDSTOPS_OPTIONS_MUX_6_Y
                | S3GPort.OUT_ENDSTOPS_OPTIONS_MUX_7_Y
                | S3GPort.OUT_ENDSTOPS_OPTIONS_MUX_8_Y
        ),
        "Z": (
            S3GPort.OUT_ENDSTOPS_OPTIONS_MUX_5_Z
            | S3GPort.OUT_ENDSTOPS_OPTIONS_MUX_6_Z
            | S3GPort.OUT_ENDSTOPS_OPTIONS_MUX_7_Z
            | S3GPort.OUT_ENDSTOPS_OPTIONS_MUX_8_Z
        ),
    }

    _endstops_abort = (
        S3GPort.OUT_ENDSTOPS_OPTIONS_ABORT_ENABLED_5
        | S3GPort.OUT_ENDSTOPS_OPTIONS_ABORT_ENABLED_6
        | S3GPort.OUT_ENDSTOPS_OPTIONS_ABORT_ENABLED_7
        | S3GPort.OUT_ENDSTOPS_OPTIONS_ABORT_ENABLED_8
    )
    _endstops_polarity = (
        S3GPort.OUT_ENDSTOPS_OPTIONS_ABORT_POLARITY_5
        | S3GPort.OUT_ENDSTOPS_OPTIONS_ABORT_POLARITY_6
        | S3GPort.OUT_ENDSTOPS_OPTIONS_ABORT_POLARITY_7
        | S3GPort.OUT_ENDSTOPS_OPTIONS_ABORT_POLARITY_8
    )
    _endstops_status = [
        S3GPort.IN_ENDSTOPS_STATUS_5,
        S3GPort.IN_ENDSTOPS_STATUS_6,
        S3GPort.IN_ENDSTOPS_STATUS_7,
        S3GPort.IN_ENDSTOPS_STATUS_8,
    ]

    endstop_int = (
        S3GPort.INT_ENDSTOP_CHANGED_5
        | S3GPort.INT_ENDSTOP_CHANGED_6
        | S3GPort.INT_ENDSTOP_CHANGED_7
        | S3GPort.INT_ENDSTOP_CHANGED_8
    )

    abort_a = 20000
    home_a = 1000
    home_v = 500000

    max_v = 500000
    max_a = 1000
    max_j = 3000

class AxeFLZ(AxeZ):
    name = "FLZ"
    """
    Front Left Z Motor
    """

    _control_enable = (
        S3GPort.OUT_MSG_CONTROL_ENABLE_1
        | S3GPort.OUT_MSG_CONTROL_INVERT_DIR_1
    )
    _control_mux = {
        "X": (
            S3GPort.OUT_MSG_CONTROL_MUX_1_X
        ),
        "Y": (
            S3GPort.OUT_MSG_CONTROL_MUX_1_Y
        ),
        "Z": (
            S3GPort.OUT_MSG_CONTROL_MUX_1_Z
        ),
    }

    _endstops_mux = {
        "X": (
                S3GPort.OUT_ENDSTOPS_OPTIONS_MUX_8_X
        ),
        "Y": (
                S3GPort.OUT_ENDSTOPS_OPTIONS_MUX_8_Y
        ),
        "Z": (
            S3GPort.OUT_ENDSTOPS_OPTIONS_MUX_8_Z
        ),
    }

    _endstops_abort = (
        S3GPort.OUT_ENDSTOPS_OPTIONS_ABORT_ENABLED_8
    )
    _endstops_polarity = (
        S3GPort.OUT_ENDSTOPS_OPTIONS_ABORT_POLARITY_8
    )
    _endstops_status = [
        S3GPort.IN_ENDSTOPS_STATUS_8,
    ]

    endstop_int = (
        S3GPort.INT_ENDSTOP_CHANGED_8
    )


class AxeBRZ(AxeZ):
    name = "BRZ"
    """
    Back Right Z Motor
    """

    _control_enable = (
        S3GPort.OUT_MSG_CONTROL_ENABLE_2
        | S3GPort.OUT_MSG_CONTROL_INVERT_DIR_2
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

    _endstops_mux = {
        "X": (
                S3GPort.OUT_ENDSTOPS_OPTIONS_MUX_5_X
        ),
        "Y": (
                S3GPort.OUT_ENDSTOPS_OPTIONS_MUX_5_Y
        ),
        "Z": (
            S3GPort.OUT_ENDSTOPS_OPTIONS_MUX_5_Z
        ),
    }

    _endstops_abort = (
        S3GPort.OUT_ENDSTOPS_OPTIONS_ABORT_ENABLED_5
    )
    _endstops_polarity = (
        S3GPort.OUT_ENDSTOPS_OPTIONS_ABORT_POLARITY_5
    )
    _endstops_status = [
        S3GPort.IN_ENDSTOPS_STATUS_5,
    ]

    endstop_int = (
        S3GPort.INT_ENDSTOP_CHANGED_5
    )



class AxeBLZ(AxeZ):
    name = "BLZ"
    """
    Back Left Z Motor
    """

    _control_enable = (
        S3GPort.OUT_MSG_CONTROL_ENABLE_3
        | S3GPort.OUT_MSG_CONTROL_INVERT_DIR_3
    )
    _control_mux = {
        "X": (
            S3GPort.OUT_MSG_CONTROL_MUX_3_X
        ),
        "Y": (
            S3GPort.OUT_MSG_CONTROL_MUX_3_Y
        ),
        "Z": (
            S3GPort.OUT_MSG_CONTROL_MUX_3_Z
        ),
    }

    _endstops_mux = {
        "X": (
                S3GPort.OUT_ENDSTOPS_OPTIONS_MUX_6_X
        ),
        "Y": (
                S3GPort.OUT_ENDSTOPS_OPTIONS_MUX_6_Y
        ),
        "Z": (
            S3GPort.OUT_ENDSTOPS_OPTIONS_MUX_6_Z
        ),
    }

    _endstops_abort = (
        S3GPort.OUT_ENDSTOPS_OPTIONS_ABORT_ENABLED_6
    )
    _endstops_polarity = (
        S3GPort.OUT_ENDSTOPS_OPTIONS_ABORT_POLARITY_6
    )
    _endstops_status = [
        S3GPort.IN_ENDSTOPS_STATUS_6,
    ]

    endstop_int = (
        S3GPort.INT_ENDSTOP_CHANGED_6
    )



class AxeFRZ(AxeZ):
    name = "FRZ"
    """
    Front Right Z Motor
    """

    _control_enable = (
        S3GPort.OUT_MSG_CONTROL_ENABLE_6
        | S3GPort.OUT_MSG_CONTROL_INVERT_DIR_6
    )
    _control_mux = {
        "X": (
            S3GPort.OUT_MSG_CONTROL_MUX_6_X
        ),
        "Y": (
            S3GPort.OUT_MSG_CONTROL_MUX_6_Y
        ),
        "Z": (
            S3GPort.OUT_MSG_CONTROL_MUX_6_Z
        ),
    }

    _endstops_mux = {
        "X": (
                S3GPort.OUT_ENDSTOPS_OPTIONS_MUX_7_X
        ),
        "Y": (
                S3GPort.OUT_ENDSTOPS_OPTIONS_MUX_7_Y
        ),
        "Z": (
            S3GPort.OUT_ENDSTOPS_OPTIONS_MUX_7_Z
        ),
    }

    _endstops_abort = (
        S3GPort.OUT_ENDSTOPS_OPTIONS_ABORT_ENABLED_7
    )
    _endstops_polarity = (
        S3GPort.OUT_ENDSTOPS_OPTIONS_ABORT_POLARITY_7
    )
    _endstops_status = [
        S3GPort.IN_ENDSTOPS_STATUS_7,
    ]

    endstop_int = (
        S3GPort.INT_ENDSTOP_CHANGED_7
    )


