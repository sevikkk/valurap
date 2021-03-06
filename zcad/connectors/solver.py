from math import acos

from pyservoce.libservoce import axrotation, translate
from zencad import deg

from .transform import NULL_TRANSFORM, Transform
from .util import cross, dot


class Solver:
    def __init__(self, connectors, constraints):
        self.connectors = connectors
        self.constraints = constraints

    def simple_translate(self, directions, points):
        if len(points) != 1 or len(directions) != 0:
            return False

        # print("Simple translation")
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

        # print("Simple attach")

        tr1 = translate(-p1[0], -p1[1], -p1[2])

        check_d = dot(d1, d2)
        if check_d > 0.99999:
            # print("rot1 skipped")
            rot1 = NULL_TRANSFORM
        elif check_d < -0.99999:
            # print("rot1 180deg")
            rot1 = axrotation(t1[0], t1[1], t1[2], deg(180))
        else:
            ax = cross(d1, d2)
            angle = acos(dot(d1, d2))
            # print("ax, angle:", ax, angle)
            rot1 = axrotation(ax[0], ax[1], ax[2], angle)

            d1_rot = rot1(d1)
            check_d1 = dot(d1_rot, d2)
            # print("check_d1:", check_d1)
            if check_d1 < 0:
                # print("d1 reverse")
                angle = angle + deg(180)

                rot1 = axrotation(ax[0], ax[1], ax[2], angle)
                d1_rot = rot1(d1)
                check_d1 = dot(d1_rot, d2)
                # print("check_d1:", check_d1)
            assert check_d1 > 0.99

        t1_rot = rot1(t1)
        # print("t1_rot, t2, d2:", t1_rot, t2, d2)

        check_t = dot(t1_rot, t2)
        if check_t > 0.99999:
            # print("rot2 skipped")
            rot2 = NULL_TRANSFORM
        elif check_t < -0.99999:
            # print("rot2 180deg")
            rot2 = axrotation(d2[0], d2[1], d2[2], deg(180))
        else:
            ax = cross(t1_rot, t2)
            angle2 = acos(dot(t1_rot, t2))
            # print("angle2:", angle2)
            # print("ax, d2", ax, d2)
            if dot(ax, d2) < 0:
                # print("Flip rot2", dot(ax, d2))
                angle2 = -angle2

            rot2 = axrotation(d2[0], d2[1], d2[2], angle2)
            t1_rot2 = rot2(t1_rot)

            # print("t1_rot2, t2:", t1_rot2, t2)
            check_t1 = dot(t1_rot2, t2)
            # print("check_t1:", check_t1)
            if check_t1 < 0:
                # print("t1 reverse")
                angle2 = angle2 + deg(180)

                rot2 = axrotation(d2[0], d2[1], d2[2], angle2)
                t1_rot2 = rot2(t1_rot)
                check_t1 = dot(t1_rot2, t2)
                # print("check_t1:", check_t1)
            assert check_t1 > 0.99

        tr2 = translate(p2[0], p2[1], p2[2])

        r = tr2 * rot2 * rot1 * tr1

        t1_rot = r(t1)
        d1_rot = r(d1)
        # print("t1_rot, t2", t1_rot, t2)
        # print("d1_rot, d2", d1_rot, d2)
        assert dot(t1_rot, t2) > 0.999
        assert dot(d1_rot, d2) > 0.999

        return Transform(r)

    def solve(self):
        points = []
        directions = []
        for connector, constraint in zip(self.connectors, self.constraints):
            if not connector.use_for_solve:
                continue

            # print(connector, constraint)

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

        # print(points)
        # print(directions)

        for solver in [self.simple_translate, self.simple_attach]:

            result = solver(directions, points)
            if result:
                # print("result:", result)
                return result

        raise NotImplementedError(
            "Solver can't solve this. Points: {points} Directions: {directions}".format(
                points=points, directions=directions
            )
        )
