from collections.abc import Sequence

from zencad import point, vector, deg
from pyservoce import translate, axrotation
import numpy as np
import numpy.linalg as la


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
            return point(x)
        elif isinstance(x, Sequence) and len(x) == 3:
            return point([x[0], x[1], x[2]])
        else:
            raise RuntimeError("Wrong input: {}".format(repr(x)))
    return point(x, y, z)


class Connector:
    def __init__(self, position=None, direction=None, top=None):
        self.position = np_point(position)

        direction = np_point(direction)
        if direction is not None:
            direction = direction / np.linalg.norm(direction)
        self.direction = direction

        top = np_point(top)
        if top is not None:
            top = top / np.linalg.norm(top)
            if direction is not None and top is not None:
                proj = np.dot(top, direction)
                if abs(proj) > 1e-6:
                    raise RuntimeError("Top and directions are not orthogonal: {} {}".format(top, direction))

        self.top = top

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
    def __init__(self, transform):
        self.transform = transform

    def __call__(self, arg):
        if isinstance(arg, np.ndarray):
            arg = oce_point(arg)
            return np_point(self.transform(arg))

        if isinstance(arg, Connector):
            p = oce_point(arg.position)
            if p is not None:
                p = np_point(self.transform(p))

            z = oce_point(0, 0, 0)
            z = np_point(self.transform(z))

            d = oce_point(arg.direction)
            if d is not None:
                d = np_point(self.transform(d)) - z

            t = oce_point(arg.top)
            if t is not None:
                t = np_point(self.transform(t)) - z

            return Connector(p, d, t)

        if isinstance(arg, Transform):
            return Transform(self.transform * arg.transform)

        if hasattr(arg, "unlazy"):
            arg = arg.unlazy()

        return self.transform(arg)

    def gen_transform(self):
        r = translate(*list(self.translation))
        if self.ax is not None and self.angle is not None and self.angle != 0:
            r = r * axrotation(self.ax[0], self.ax[1], self.ax[2], self.angle)
        return r


class Solver:
    def __init__(self, connectors, constraints):
        self.connectors = connectors
        self.constraints = constraints

    def simple_translate(self, directions, points):
        if len(points) != 1 or len(directions) != 0:
            return False

        print("Simple translation")
        p1, p2 = points[0]
        d = p2 - p1
        return Transform(translate(d[0], d[1], d[2]))

    def simple_attach(self, directions, points):
        if len(points) != 1 or len(directions) != 1:
            return False

        p1, p2 = points[0]
        (d1, t1), (d2, t2) = directions[0]

        if t1 is None or t2 is None:
            return

        print("Simple attach")

        tr1 = translate(-p1[0], -p1[1], -p1[2])

        check_d = np.dot(d1, d2)
        if check_d > 0.99999:
            print("rot1 skipped")
            rot1 = axrotation(0, 0, 1, 0)
        elif check_d < -0.99999:
            print("rot1 180deg")
            rot1 = axrotation(t1[0], t1[1], t1[2], deg(180))
        else:
            ax = np.cross(d1, d2)
            angle = np.arccos(np.clip(np.dot(d1, d2), -1.0, 1.0))
            print("ax, angle:", ax, angle)
            rot1 = axrotation(ax[0], ax[1], ax[2], angle)

            d1_rot = np_point(rot1(oce_point(d1)))
            check_d1 = np.dot(d1_rot, d2)
            print("check_d1:", check_d1)
            if check_d1 < 0:
                print("d1 reverse")
                angle = angle + deg(180)

                rot1 = axrotation(ax[0], ax[1], ax[2], angle)
                d1_rot = np_point(rot1(oce_point(d1)))
                check_d1 = np.dot(d1_rot, d2)
                print("check_d1:", check_d1)
                assert check_d1 > 0.95

        t1_rot = np_point(rot1(oce_point(t1)))
        print("t1_rot, t2, d2:", t1_rot, t2, d2)

        check_t = np.dot(t1_rot, t2)
        if check_t > 0.99999:
            print("rot2 skipped")
            rot2 = axrotation(0, 0, 1, 0)
        elif check_t < -0.99999:
            print("rot2 180deg")
            rot2 = axrotation(d2[0], d2[1], d2[2], deg(180))
        else:
            ax = np.cross(t1_rot, t2)
            angle2 = np.arccos(np.clip(np.dot(t1_rot, t2), -1.0, 1.0))
            print("angle2:", angle2)
            print("ax, d2", ax, d2)
            if np.dot(ax, d2) < 0:
                print("Flip rot2", np.dot(ax, d2))
                angle2 = -angle2

            rot2 = axrotation(d2[0], d2[1], d2[2], angle2)
            t1_rot2 = np_point(rot2(oce_point(t1_rot)))

            print("t1_rot2, t2:", t1_rot2, t2)
            check_t1 = np.dot(t1_rot2, t2)
            print("check_t1:", check_t1)
            if check_t1 < 0:
                print("t1 reverse")
                angle2 = angle2 + deg(180)

                rot2 = axrotation(d2[0], d2[1], d2[2], angle2)
                t1_rot2 = np_point(rot2(oce_point(t1_rot)))
                check_t1 = np.dot(t1_rot2, t2)
                print("check_t1:", check_t1)
                assert check_t1 > 0.95

        tr2 = translate(p2[0], p2[1], p2[2])

        r = tr2 * rot2 * rot1 * tr1

        z1_rot = np_point(r(oce_point(0,0,0)))
        t1_rot = np_point(r(oce_point(t1)))
        d1_rot = np_point(r(oce_point(d1)))
        print("t1_rot, t2", t1_rot - z1_rot, t2)
        print("d1_rot, d2", d1_rot - z1_rot, d2)

        return Transform(r)

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

        for solver in [
            self.simple_translate,
            self.simple_attach,
        ]:

            result = solver(directions, points)
            if result:
                print("result:", result)
                return result

        raise NotImplementedError(
            "Solver can't solve this. Points: {points} Directions: {directions}".format(
                points=points, directions=directions
            )
        )


class Unit:
    def model(self):
        raise NotImplementedError

    def inst(self, transform):
        return Part(self, transform)

    def get_connector(self, *args, **kw):
        raise NotImplementedError


class Part:
    def __init__(self, unit, transform):
        self.unit = unit
        self.transform = transform

    def get_connector(self, *args, **kw):
        c = self.unit.get_connector(*args, **kw)
        return self.transform(c)

    def model(self):
        model = self.unit.model()
        return self.transform(model)



