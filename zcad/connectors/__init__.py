from collections.abc import Sequence

from zencad import point, vector
from pyservoce import translate, axrotation
import numpy as np


def np_point(x, y=None, z=None):
    if y is None and z is None:
        if x is None:
            return None
        elif isinstance(x, np.ndarray):
            return x
        elif isinstance(x, point):
            return np.array([x.x, x.y, x.z])
        elif isinstance(x, vector):
            return np.array([x.x, x.y, x.z])
        elif isinstance(x, Sequence) and len(x) == 3:
            return np.array([x[0], x[1], x[2]])
        else:
            raise RuntimeError("Wrong input: {}".format(repr(x)))
    return np.array([x, y, z])


def oce_point(x, y=None, z=None):
    if y is None and z is None:
        if x is None:
            return None
        elif isinstance(x, np.ndarray):
            return point(x[0], x[1], x[2])
        elif isinstance(x, point):
            return x
        elif isinstance(x, vector):
            return x
        elif isinstance(x, Sequence) and len(x) == 3:
            return point([x[0], x[1], x[2]])
        else:
            raise RuntimeError("Wrong input: {}".format(repr(x)))
    return point(x, y, z)


class Connector:
    def __init__(self, position=None, direction=None, top=None):
        self.position = np_point(position)
        self.direction = np_point(direction)
        self.top = np_point(top)

    def __repr__(self):
        s = ["<Connector"]
        if self.position is not None:
            s.append("point={}".format(self.position))
        if self.direction is not None:
            s.append("direction={}".format(self.direction))
        if self.top is not None:
            s.append("top={}".format(self.top))
        s = " ".join(s) + ">"
        return s


class Transform:
    def __init__(self, translation=None, ax=None, angle=None):
        if translation is None:
            translation = np_point(0, 0, 0)
        self.translation = np_point(translation)

        self.ax = np_point(ax)
        self.angle = angle

    def __repr__(self):
        s = ["<Transform", "translate={}".format(self.translation)]
        if self.ax is not None:
            s.append("axis={}".format(self.ax))
        if self.angle is not None:
            s.append("angle={}".format(self.angle))
        s = " ".join(s) + ">"
        return s

    def __call__(self, arg):
        translate_back = None
        if isinstance(arg, np.ndarray):
            arg = oce_point(arg)
            translate_back = np_point

        r = translate(*list(self.translation))
        if self.ax is not None and self.angle is not None and self.angle != 0:
            r = r * axrotation(self.ax[0], self.ax[1], self.ax[2], self.angle)

        result = r(arg)
        if translate_back is not None:
            result = translate_back(result)

        return result


class Solver:
    def __init__(self, connectors, constraints):
        self.connectors = connectors
        self.constraints = constraints

    def solve(self):
        points = []
        directions = []
        for connector, constraint in zip(self.connectors, self.constraints):
            print(connector, constraint)

            p1 = connector.position
            p2 = constraint.position
            if p1 is not None and p2 is not None:
                points.append([p1, p2])

            d1 = connector.direction
            d2 = constraint.direction
            t1 = connector.top
            t2 = constraint.top
            if d1 is not None and d2 is not None:
                # top vectors are intentionally optional
                directions.append([(d1, t1), (d2, t2)])

        print(points)
        print(directions)
        if len(points) == 1 and len(directions) == 0:
            print("Simple translation")
            p1, p2 = points[0]
            return Transform(p2 - p1)
        else:
            raise NotImplementedError(
                "Solver can't solve this. Points: {points} Directions: {directions}".format(
                    points=points, directions=directions
                )
            )
