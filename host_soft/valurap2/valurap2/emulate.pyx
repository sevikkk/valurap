from math import copysign

try:
    import pandas as pd
except ImportError:
    pd = None

from libc.stdint cimport int32_t, int64_t

cdef class ApgState(object):
    cdef public int64_t x
    cdef public int64_t v_in
    cdef public int64_t v_out
    cdef public int64_t v_eff
    cdef public int64_t a
    cdef public int64_t j
    cdef public int64_t jj
    cdef public int64_t target_v
    cdef public int target_v_set
    cdef public int64_t accel_step
    cdef public int64_t step_freq
    cdef public int step_bit
    cdef public float spm
    cdef public float x_k
    cdef public float v_k
    cdef public float a_k
    cdef public float j_k
    cdef public float jj_k
    cdef public float t_k

    def __init__(self, accel_step=50000, step_freq=50000000, step_bit=40, spm=1.0):
        self.x = 0
        self.v_in = 0
        self.v_out = 0
        self.v_eff = 0
        self.a = 0
        self.j = 0
        self.jj = 0
        self.target_v = 0
        self.target_v_set = False
        self.accel_step = accel_step
        self.step_bit = step_bit
        self.step_freq = step_freq
        self.spm = spm
        self.x_k = 1.0 / (2 ** step_bit) / spm
        self.v_k = self.x_k * self.step_freq
        self.a_k = self.v_k * self.step_freq / self.accel_step
        self.j_k = self.a_k * self.step_freq / self.accel_step
        self.jj_k = self.j_k * self.step_freq / self.accel_step
        self.t_k = self.accel_step / self.step_freq

    def to_floats(self):
        return {
                "x": float(self.x) * self.x_k,
                "v_in": float(self.v_in) * self.v_k,
                "v_out": float(self.v_out) * self.v_k,
                "v_eff": float(self.v_eff) * self.v_k,
                "target_v": float(self.target_v) * self.v_k,
                "a": float(self.a) * self.a_k,
                "j": float(self.j) * self.j_k,
                "jj": float(self.jj) * self.jj_k
        }

    def __str__(self):
        data = self.to_floats()
        s = "<ApgState x={x:.2f} v={v_out:.2f} a={a:.2f} j={j:.2f} jj={jj:.2f}".format(**data)
        if self.target_v_set:
            s = s + " target_v={target_v:.2f}".format(**data)
        s += ">"
        return s

    def load(self, seg):
        if seg.x is not None:
            self.x = int(seg.x)
        if seg.v is not None:
            self.v_out = int(seg.v)
        if seg.a is not None:
            self.a = int(seg.a)
        if seg.j is not None:
            self.j = int(seg.j)
        if seg.jj is not None:
            self.jj = int(seg.jj)
        if seg.target_v is not None:
            self.target_v = int(seg.target_v)
            self.target_v_set = True
        else:
            self.target_v_set = False

    def copy(self):
        c = ApgState(accel_step=self.accel_step, step_freq=self.step_freq, step_bit=self.step_bit, spm=self.spm)
        c.x = self.x
        c.v_in = self.v_in
        c.v_out = self.v_out
        c.v_eff = self.v_eff
        c.a = self.a
        c.j = self.j
        c.jj = self.jj
        c.target_v = self.target_v
        c.target_v_set = self.target_v_set
        return c

    def step(self):
        self.c_step()

    cdef void c_step(self):
        cdef int64_t next_x = self.x + self.v_eff * self.accel_step
        cdef int64_t next_v_in = self.v_out
        cdef int64_t next_v_out = self.v_out + self.a
        cdef int64_t next_a = self.a + self.j
        cdef int64_t next_j = self.j + self.jj
        cdef int64_t next_jj = self.jj

        if self.target_v_set:
            if ((self.v_out <= self.target_v) and (next_v_out >= self.target_v)) or (
                (self.v_out >= self.target_v) and (next_v_out <= self.target_v)
            ):
                next_jj = 0
                next_j = 0
                next_a = 0
                next_v_out = self.target_v

        next_v_eff = (next_v_in + next_v_out) >> 1

        self.x = next_x
        self.v_in = next_v_in
        self.v_out = next_v_out
        self.v_eff = next_v_eff
        self.a = next_a
        self.j = next_j
        self.jj = next_jj


NUM_APGS = 6
def emulate(profile, verbose=0, apg_states=None, accel_step=50000, no_tracking=True, step_freq=50000000, step_bit=40, spms=None):
    cdef int int_verbose = verbose
    cdef int int_tracking = not no_tracking
    cdef int i
    cdef int int_dt
    cdef int ts_start
    cdef ApgState state

    if apg_states is None:
        apg_states = {}

    if spms is None:
        spms = []

    if len(spms) < NUM_APGS:
        spms = spms + [1.0] * (NUM_APGS - len(spms))

    for a in range(NUM_APGS):
        apg_states.setdefault(a, ApgState(accel_step=accel_step, step_freq=step_freq, step_bit=step_bit, spm=float(spms[a])))

    ts = 0
    steps = {}
    for dt, segs in profile:
        if verbose > 0:
            print(dt)
        ts_start = ts
        ts += dt
        apg_segs = {a: None for a in range(NUM_APGS)}

        for seg in segs:
            apg_segs[seg.apg] = seg

        for apg, seg in apg_segs.items():
            if verbose > 0:
                print("  ", seg)
            state = apg_states[apg]

            if seg:
                state.load(seg)
            prefix = "apg{}_".format(apg)

            vals = state.to_floats()
            if verbose == 1:
                print(
                    "    {:6d} {:10.3f} {:10.3f} {:10.3f}".format(
                        ts_start, vals["x"], vals["v_out"], vals["a"]
                    )
                )
                print("                 ...")

            last_v = None
            first_v = 0
            int_dt = dt
            i = 0

            while i < int_dt:
                if int_tracking:
                    step_data = steps.setdefault(ts_start + i, {"ts": ts_start + i})
                    step_data[prefix + "jj"] = vals["jj"]
                    step_data[prefix + "j"] = vals["j"]
                    step_data[prefix + "a"] = vals["a"]
                    step_data[prefix + "v"] = vals["v_out"]
                    step_data[prefix + "v_eff"] = vals["v_eff"]
                    step_data[prefix + "x"] = vals["x"]

                if int_verbose > 0:
                    vals = state.to_floats()
                    if state.v_out != last_v:
                        if verbose > 1:
                            if first_v > 0:
                                if first_v > 1:
                                    print("        ... {} ...".format(first_v - 1))
                                print(
                                    "    {:6d} {:10.3f} {:10.3f} {:10.3f}".format(
                                        ts_start + i - 1, prev_x, prev_v, prev_a
                                    )
                                )
                            print(
                                "    {:6d} {:10.3f} {:10.3f} {:10.3f}".format(
                                    ts_start + i, vals["x"], vals["v_out"], vals["a"]
                                )
                            )
                        last_v = state.v_out
                        first_v = 0
                    else:
                        if verbose == 1 and first_v == 0:
                            print(
                                "    {:6d} {:10.3f} {:10.3f} {:10.3f}".format(
                                    ts_start + i - 1, prev_x, prev_v, prev_a
                                )
                            )

                        first_v += 1

                    prev_x = vals["x"]
                    prev_v = vals["v_out"]
                    prev_a = vals["a"]
                state.c_step()
                i += 1

            if verbose > 1:
                if first_v != 0:
                    if first_v > 1:
                        print("           ... {} ...".format(first_v - 1))
                    vals = state.to_floats()
                    print(
                        "    {:6d} {:10.3f} {:10.3f} {:10.3}".format(
                            ts_start + i, vals["x"], vals["v_out"], vals["a"]
                        )
                    )
            elif verbose == 1:
                if first_v > 1:
                    print("                 ...")

                vals = state.to_floats()
                print(
                    "    {:6d} {:10.3f} {:10.3f} {:10.3f}".format(
                        ts_start + i, vals["x"], vals["v_out"], vals["a"]
                    )
                )

    if not no_tracking:
        steps = [a[1] for a in sorted(steps.items())]
        if pd:
            steps = pd.DataFrame(steps)
            steps["t"] = steps["ts"] * apg_states[0].t_k

    return steps

