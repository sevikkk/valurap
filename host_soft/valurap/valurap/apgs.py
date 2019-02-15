from .commands import S3GPort


class APG(object):
    name = None

    control_set_jj = None
    control_set_j = None
    control_set_a = None
    control_set_v = None
    control_set_x = None
    control_set_target_v = None

    val_x_lo = None
    val_x_hi = None
    val_v = None
    val_a = None
    val_j = None
    val_jj = None
    val_target_v = None
    val_abort_a = None

    cur_x_lo = None
    cur_x_hi = None
    cur_v = None

    def __init__(self, bot):
        self.bot = bot


class ApgX(APG):
    name = "X"
    control_set_jj = S3GPort.OUT_ASG_CONTROL_APG_X_SET_JJ
    control_set_j = S3GPort.OUT_ASG_CONTROL_APG_X_SET_J
    control_set_a = S3GPort.OUT_ASG_CONTROL_APG_X_SET_A
    control_set_v = S3GPort.OUT_ASG_CONTROL_APG_X_SET_V
    control_set_x = S3GPort.OUT_ASG_CONTROL_APG_X_SET_X
    control_set_target_v = S3GPort.OUT_ASG_CONTROL_APG_X_SET_TARGET_V

    val_x_lo = S3GPort.OUT_APG_X_X_VAL_LO
    val_x_hi = S3GPort.OUT_APG_X_X_VAL_HI
    val_v = S3GPort.OUT_APG_X_V_VAL
    val_a = S3GPort.OUT_APG_X_A_VAL
    val_j = S3GPort.OUT_APG_X_J_VAL
    val_jj = S3GPort.OUT_APG_X_JJ_VAL
    val_target_v = S3GPort.OUT_APG_X_TARGET_V_VAL
    val_abort_a = S3GPort.OUT_APG_X_ABORT_A_VAL

    cur_x_lo = S3GPort.IN_APG_X_X_LO
    cur_x_hi = S3GPort.IN_APG_X_X_HI
    cur_v = S3GPort.IN_APG_X_V


class ApgY(APG):
    name = "Y"
    control_set_jj = S3GPort.OUT_ASG_CONTROL_APG_Y_SET_JJ
    control_set_j = S3GPort.OUT_ASG_CONTROL_APG_Y_SET_J
    control_set_a = S3GPort.OUT_ASG_CONTROL_APG_Y_SET_A
    control_set_v = S3GPort.OUT_ASG_CONTROL_APG_Y_SET_V
    control_set_x = S3GPort.OUT_ASG_CONTROL_APG_Y_SET_X
    control_set_target_v = S3GPort.OUT_ASG_CONTROL_APG_Y_SET_TARGET_V

    val_x_lo = S3GPort.OUT_APG_Y_X_VAL_LO
    val_x_hi = S3GPort.OUT_APG_Y_X_VAL_HI
    val_v = S3GPort.OUT_APG_Y_V_VAL
    val_a = S3GPort.OUT_APG_Y_A_VAL
    val_j = S3GPort.OUT_APG_Y_J_VAL
    val_jj = S3GPort.OUT_APG_Y_JJ_VAL
    val_target_v = S3GPort.OUT_APG_Y_TARGET_V_VAL
    val_abort_a = S3GPort.OUT_APG_Y_ABORT_A_VAL

    cur_x_lo = S3GPort.IN_APG_Y_X_LO
    cur_x_hi = S3GPort.IN_APG_Y_X_HI
    cur_v = S3GPort.IN_APG_Y_V

class ApgZ(APG):
    name = "Z"
    control_set_jj = S3GPort.OUT_ASG_CONTROL_APG_Z_SET_JJ
    control_set_j = S3GPort.OUT_ASG_CONTROL_APG_Z_SET_J
    control_set_a = S3GPort.OUT_ASG_CONTROL_APG_Z_SET_A
    control_set_v = S3GPort.OUT_ASG_CONTROL_APG_Z_SET_V
    control_set_x = S3GPort.OUT_ASG_CONTROL_APG_Z_SET_X
    control_set_target_v = S3GPort.OUT_ASG_CONTROL_APG_Z_SET_TARGET_V

    val_x_lo = S3GPort.OUT_APG_Z_X_VAL_LO
    val_x_hi = S3GPort.OUT_APG_Z_X_VAL_HI
    val_v = S3GPort.OUT_APG_Z_V_VAL
    val_a = S3GPort.OUT_APG_Z_A_VAL
    val_j = S3GPort.OUT_APG_Z_J_VAL
    val_jj = S3GPort.OUT_APG_Z_JJ_VAL
    val_target_v = S3GPort.OUT_APG_Z_TARGET_V_VAL
    val_abort_a = S3GPort.OUT_APG_Z_ABORT_A_VAL

    cur_x_lo = S3GPort.IN_APG_Z_X_LO
    cur_x_hi = S3GPort.IN_APG_Z_X_HI
    cur_v = S3GPort.IN_APG_Z_V
