class ProfileSegment(object):
    def __init__(self, apg, x=None, v=None, a=0, j=0, jj=0, target_v=None):
        self.apg = apg
        self.x = x
        self.v = v
        self.a = a
        self.j = j
        self.jj = jj
        self.target_v = target_v

    def __repr__(self):
        s = ['<ProfileSegment apg={}'.format(self.apg.name)]
        for a in "x v a j jj target_v".split():
            v = getattr(self, a)
            if v is not None:
                s.append('{}={}'.format(a, v))
        return " ".join(s) + '>'


class PathSegment(object):
    def __init__(self, axis, dx, base_v):
        self.axis = axis
        self.dx = dx
        self.base_v = base_v


class Asg(object):
    def __init__(self, bot):
        self.bot = bot

    def gen_reset_code(self, apgs):
        s3g = self.bot.s3g

        control = [
            s3g.OUT_ASG_CONTROL_SET_STEPS_LIMIT,
            s3g.OUT_ASG_CONTROL_SET_DT_LIMIT,
            s3g.OUT_ASG_CONTROL_RESET_STEPS,
            s3g.OUT_ASG_CONTROL_RESET_DT,
        ]

        for apg in apgs:
            control += [
                apg.control_set_x,
                apg.control_set_v,
                apg.control_set_a,
                apg.control_set_j,
                apg.control_set_jj,
            ]

        code = [
            s3g.BUF_OUTPUT(s3g.OUT_LEDS, 0x1),
            s3g.BUF_OUTPUT(s3g.OUT_MSG_ALL_PRE_N, 100), # 10 ms on step cycle - 2-6-2 ms
            s3g.BUF_OUTPUT(s3g.OUT_MSG_ALL_PULSE_N, 400),
            s3g.BUF_OUTPUT(s3g.OUT_MSG_ALL_POST_N, 500),
            s3g.BUF_OUTPUT(s3g.OUT_ASG_CONTROL, *control),
            s3g.BUF_OUTPUT(s3g.OUT_ASG_DT_VAL, 50000),
            s3g.BUF_OUTPUT(s3g.OUT_ASG_STEPS_VAL, 1),
        ]
        for apg in apgs:
            for reg in [
                apg.val_x_lo,
                apg.val_x_hi,
                apg.val_v,
                apg.val_a,
                apg.val_j,
                apg.val_jj,
            ]:
                code.append(s3g.BUF_OUTPUT(reg, 0))

        code += [
            s3g.BUF_STB(s3g.STB_ASG_LOAD),
            s3g.BUF_OUTPUT(s3g.OUT_ASG_CONTROL,
                           s3g.OUT_ASG_CONTROL_SET_DT_LIMIT
                           ),
            s3g.BUF_OUTPUT(s3g.OUT_ASG_DT_VAL, 0),
            s3g.BUF_WAIT_ALL(s3g.INT_ASG_DONE),
            s3g.BUF_CLEAR(s3g.INT_ASG_DONE),
            s3g.BUF_STB(s3g.STB_ASG_LOAD),
            s3g.BUF_OUTPUT(s3g.OUT_LEDS, 0x3),
            s3g.BUF_DONE()
        ]
        return code

    def gen_path_code(self, steps):
        s3g = self.bot.s3g
        first_step = True

        code = [
            s3g.BUF_OUTPUT(s3g.OUT_LEDS, 0x1),
        ]

        prev_regs = {}

        for dt, segments in steps:
            regs = {}
            control = [
                s3g.OUT_ASG_CONTROL_SET_STEPS_LIMIT,
                s3g.OUT_ASG_CONTROL_RESET_STEPS,
            ]
            regs[s3g.OUT_ASG_STEPS_VAL] = dt

            if first_step:
                control += [
                    s3g.OUT_ASG_CONTROL_SET_DT_LIMIT,
                    s3g.OUT_ASG_CONTROL_RESET_DT,
                ]
                regs[s3g.OUT_ASG_DT_VAL] = 50000

            for seg in segments:
                apg = seg.apg
                if seg.x is not None:
                    control.append(apg.control_set_x)
                    regs[apg.val_x_lo] = 0
                    regs[apg.val_x_hi] = int(seg.x)

                if seg.v is not None:
                    control.append(apg.control_set_v)
                    regs[apg.val_v] = int(seg.v)

                if seg.a is not None:
                    control.append(apg.control_set_a)
                    regs[apg.val_a] = int(seg.a)

                if seg.j is not None:
                    control.append(apg.control_set_j)
                    regs[apg.val_j] = int(seg.j)

                if seg.jj is not None:
                    control.append(apg.control_set_jj)
                    regs[apg.val_jj] = int(seg.jj)

                if seg.target_v is not None:
                    control.append(apg.control_set_target_v)
                    regs[apg.val_target_v] = int(seg.target_v)

            control_value = 0
            for c in control:
                control_value |= c

            regs[s3g.OUT_ASG_CONTROL] = control_value
            for k, v in regs.items():
                if prev_regs.get(k, None) != v:
                    code.append(s3g.BUF_OUTPUT(k, v))
                    prev_regs[k] = v

            if first_step:
                code += [
                    s3g.BUF_STB(s3g.STB_ASG_LOAD),
                ]
                first_step = False
            else:
                code += [
                    s3g.BUF_WAIT_ALL(s3g.INT_ASG_DONE),
                    s3g.BUF_CLEAR(s3g.INT_ASG_DONE, s3g.INT_ASG_ABORT),
                    s3g.BUF_STB(s3g.STB_ASG_LOAD),
                ]

        code += [
            s3g.BUF_OUTPUT(s3g.OUT_ASG_CONTROL,
                           s3g.OUT_ASG_CONTROL_SET_DT_LIMIT
                           ),
            s3g.BUF_OUTPUT(s3g.OUT_ASG_DT_VAL, 0),
            s3g.BUF_WAIT_ALL(s3g.INT_ASG_DONE, s3g.INT_ASG_ABORT),
            s3g.BUF_CLEAR(s3g.INT_ASG_DONE),
            s3g.BUF_STB(s3g.STB_ASG_LOAD),
            s3g.BUF_OUTPUT(s3g.OUT_LEDS, 0x3),
            s3g.BUF_DONE()
        ]

        return code

    def gen_set_apg_positions(self, **kw):
        s3g = self.bot.s3g

        control = [
            s3g.OUT_ASG_CONTROL_SET_STEPS_LIMIT,
            s3g.OUT_ASG_CONTROL_SET_DT_LIMIT,
            s3g.OUT_ASG_CONTROL_RESET_STEPS,
            s3g.OUT_ASG_CONTROL_RESET_DT,
        ]

        code = []

        for k, v in kw.items():
            axis = self.bot.axes[k]
            apg = axis.apg
            assert apg

            control += [
                apg.control_set_x,
                apg.control_set_v,
                apg.control_set_a,
                apg.control_set_j,
                apg.control_set_jj,
            ]
            x_hi = int(v)
            x_lo = int((v - x_hi) * 2**32)
            code += [
                s3g.BUF_OUTPUT(apg.val_x_lo, x_lo),
                s3g.BUF_OUTPUT(apg.val_x_hi, x_hi),
                s3g.BUF_OUTPUT(apg.val_v, 0),
                s3g.BUF_OUTPUT(apg.val_a, 0),
                s3g.BUF_OUTPUT(apg.val_j, 0),
                s3g.BUF_OUTPUT(apg.val_jj, 0),
            ]

        code += [
            s3g.BUF_OUTPUT(s3g.OUT_ASG_CONTROL, *control),
            s3g.BUF_OUTPUT(s3g.OUT_ASG_DT_VAL, 50000),
            s3g.BUF_OUTPUT(s3g.OUT_ASG_STEPS_VAL, 1),
            s3g.BUF_STB(s3g.STB_ASG_LOAD),
            s3g.BUF_OUTPUT(s3g.OUT_ASG_CONTROL,
                           s3g.OUT_ASG_CONTROL_SET_DT_LIMIT
                           ),
            s3g.BUF_OUTPUT(s3g.OUT_ASG_DT_VAL, 0),
            s3g.BUF_WAIT_ALL(s3g.INT_ASG_DONE),
            s3g.BUF_CLEAR(s3g.INT_ASG_DONE),
            s3g.BUF_STB(s3g.STB_ASG_LOAD),
            s3g.BUF_OUTPUT(s3g.OUT_LEDS, 0x3),
            s3g.BUF_DONE()
        ]
        return code