from pyservoce.libservoce import axrotation

from .connector import Connector

NULL_TRANSFORM = axrotation(0, 0, 1, 0)


class Transform:
    def __init__(self, transform=None):
        if transform is None:
            transform = NULL_TRANSFORM

        self.transform = transform

    def __call__(self, arg):
        if isinstance(arg, Connector):
            p = arg.position
            if p is not None:
                p = self.transform(p)

            d = arg.direction
            if d is not None:
                d = self.transform(d)

            t = arg.top
            if t is not None:
                t = self.transform(t)

            return Connector(p, d, t)

        if isinstance(arg, Transform):
            return Transform(self.transform * arg.transform)

        if hasattr(arg, "unlazy"):
            print("calling unlazy on {}".format(arg))
            arg = arg.unlazy()

        return self.transform(arg)

    def invert(self):
        return Transform(self.transform.invert())
