import time

class ProfileSegment(object):
    def __init__(self, apg, x=None, v=None, a=0, j=0, jj=0, target_v=None):
        self.apg = apg
        self.x = x
        self.v = v
        self.a = a
        self.j = j
        self.jj = jj
        self.target_v = target_v
        if x is not None:
            print("Warning, explicit X in segment")


    def __repr__(self):
        s = ['<ProfileSegment apg={}'.format(self.apg.name)]
        for a in "x v a j jj target_v".split():
            v = getattr(self, a)
            if v is not None:
                s.append('{}={}'.format(a, v))
        return " ".join(s) + '>'

    def to_tuple(self):
        ret = []
        if self.jj != 0:
            ijj = self.jj
            if ijj is not None:
                ijj = int(ijj)
            ret.append(ijj)

        if ret or (self.j != 0):
            ij = self.j
            if ij is not None:
                ij = int(ij)
            ret.append(ij)

        if ret or (self.target_v is not None):
            itv = self.target_v
            if itv is not None:
                itv = int(itv)

            ret.append(itv)

        if ret or (self.a != 0):
            ia = self.a
            if ia is not None:
                ia = int(ia)
            ret.append(ia)

        if ret or (self.v is not None):
            iv = self.v
            if iv is not None:
                iv = int(iv)
            ret.append(iv)

        ix = self.x
        if ix is not None:
            ix = int(ix)
        ret.append(ix)
        ret.append(self.apg.name)

        ret = tuple(reversed(ret))

        return(ret)

    @classmethod
    def from_tuple(cls, tup, apgs):
        kws = {}
        l = list(tup)
        apg_name = l.pop(0)
        kws["apg"] = apgs[apg_name]

        for fld in ["x", "v", "a", "target_v", "j", "jj"]:
            if not l:
                break
            kws[fld] = l.pop(0)

        kws["x"] = None
        return cls(**kws)

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

    def gen_path_code(self, steps, accel_step=50000, real_apgs=None):
        s3g = self.bot.s3g
        first_step = True

        code = [
            s3g.BUF_OUTPUT(s3g.OUT_LEDS, 0x1),
        ]

        t0 = time.time()
        t1 = t0
        prev_regs = {}

        for dt, segments in steps:
            if time.time() - t1 > 0.01:
                print("gen_code sleep")
                time.sleep(0.001)
                t1 = time.time()

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
                regs[s3g.OUT_ASG_DT_VAL] = int(accel_step)

            for seg in segments:
                apg = seg.apg
                if real_apgs:
                    apg = real_apgs[apg.name]

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

        print("Gen time: ", time.time() - t0)
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
            if not apg:
                continue

            control += [
                apg.control_set_x,
                apg.control_set_v,
                apg.control_set_a,
                apg.control_set_j,
                apg.control_set_jj,
            ]
            x = int(v * 2**32)
            if x < 0:
                x = x + 2**64

            x_hi = x >> 32
            x_lo = x & (2**32-1)

            code += [
                s3g.BUF_OUTPUT(apg.val_x_lo, x_lo),
                s3g.BUF_OUTPUT(apg.val_x_hi, x_hi),
                s3g.BUF_OUTPUT(apg.val_v, 0),
                s3g.BUF_OUTPUT(apg.val_a, 0),
                s3g.BUF_OUTPUT(apg.val_j, 0),
                s3g.BUF_OUTPUT(apg.val_jj, 0),
            ]

        if code:
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


    def gen_map_code(self, map):
        code = []
        s3g = self.bot.s3g
        controls = {}
        print("Map: {}".format(map))
        for axe in self.bot.axes.values():
            controls.setdefault(axe._msg_control, 0)
            control = 0

            if axe.name in map:
                apg = self.bot.apgs[map[axe.name]]
                control |= axe._control_mux[apg.name]
                print("Axe {} mapped to {}".format(axe.name, apg.name))

                controls.setdefault(apg.val_abort_a, axe.abort_a)
                controls[apg.val_abort_a] = min(controls[apg.val_abort_a], axe.abort_a)

            if axe.enabled:
                control |= axe._control_enable
                print("Axe {} enabled".format(axe.name))

            controls[axe._msg_control] |= control


        for k, v in controls.items():
            code += [s3g.BUF_OUTPUT(k, v)]

        code += [s3g.BUF_DONE()]

        return code
