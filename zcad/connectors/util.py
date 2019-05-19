from math import hypot
from typing import Sequence

from zencad import box, cylinder, linear_extrude, point, vector


def oce_point(x, y=None, z=None):
    if y is None and z is None:
        if x is None:
            return None
        elif isinstance(x, point):
            return x
        elif isinstance(x, vector):
            return point(x)
        elif isinstance(x, Sequence) and len(x) == 3:
            return point([x[0], x[1], x[2]])
        else:
            raise RuntimeError("Wrong input: {}".format(repr(x)))
    return point(x, y, z)


def oce_vector(x, y=None, z=None):
    if y is None and z is None:
        if x is None:
            return None
        elif isinstance(x, point):
            return vector(x)
        elif isinstance(x, vector):
            return x
        elif isinstance(x, Sequence) and len(x) == 3:
            return vector([x[0], x[1], x[2]])
        else:
            raise RuntimeError("Wrong input: {}".format(repr(x)))
    return vector(x, y, z)


def norm(a):
    return hypot(hypot(a.x, a.y), a.z)


def dot(a, b):
    return a.x * b.x + a.y * b.y + a.z * b.z


def cross(a, b):
    return vector(a.y * b.z - a.z * b.y, a.z * b.x - a.x * b.z, a.x * b.y - a.y * b.x)


def get_config_param(config, param, default=None):
    if config and param in config:
        return config[param]
    return default


def copy_config(config, param_list):
    if not config:
        return config

    final_config = {}
    for param in param_list:
        if param in config:
            final_config[param] = config[param]

    return final_config


def uni_box(sx, sy, sz):
    dx = 0
    dy = 0
    dz = 0

    if sx < 0:
        sx = -sx
        dx = -sx
    if sy < 0:
        sy = -sy
        dy = -sy
    if sz < 0:
        sz = -sz
        dz = -sz

    return box(sx, sy, sz).translate(dx, dy, dz)


def uni_cylinder(**kw):
    h = kw.pop("h", 0)
    dz = 0
    if h < 0:
        h = -h
        dz = -h

    kw["h"] = h

    return cylinder(**kw).translate(0, 0, dz)


def uni_extrude(path, h):
    dz = 0
    if h < 0:
        h = -h
        dz = -h

    return linear_extrude(path, h).translate(0, 0, dz)
