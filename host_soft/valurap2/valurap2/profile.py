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
        s = ['<ProfileSegment apg={}'.format(self.apg)]
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
        ret.append(self.apg)

        ret = tuple(reversed(ret))

        return(ret)

    @classmethod
    def from_tuple(cls, tup):
        kws = {}
        l = list(tup)
        apg = l.pop(0)
        kws["apg"] = apg

        for fld in ["x", "v", "a", "target_v", "j", "jj"]:
            if not l:
                break
            kws[fld] = l.pop(0)

        kws["x"] = None
        return cls(**kws)
