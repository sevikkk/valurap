import os
from collections.abc import Sequence
from math import hypot, acos

from zencad import point, vector, deg, cylinder, cone, sphere, textshape
from pyservoce import translate, axrotation, Color


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


class Connector:
    def __init__(
        self, position=None, direction=None, top=None, data=None, use_for_solve=True
    ):
        self.position = oce_point(position)

        if direction is not None:
            direction = oce_vector(direction)
            direction = direction / norm(direction)
        self.direction = direction

        if top is not None:
            top = oce_vector(top)
            top = top / norm(top)

            if direction is not None and top is not None:
                proj = dot(top, direction)
                if abs(proj) > 1e-6:
                    raise RuntimeError(
                        "Top and directions are not orthogonal: {} {}".format(
                            top, direction
                        )
                    )

        self.top = top
        self.data = data
        self.use_for_solve = use_for_solve

    def __repr__(self):
        s = ["<Connector"]
        if self.position is not None:
            s.append("point={}".format(self.position))
        if self.direction is not None:
            s.append("direction={}".format(self.direction))
        if self.top is not None:
            s.append("top={}".format(self.top))
        if self.data is not None:
            s.append("data={}".format(self.data))
        if self.use_for_solve is not None:
            s.append("use_for_solve={}".format(self.use_for_solve))
        s = " ".join(s) + ">"
        return s

    def replace(self, position=None, direction=None, top=None):
        p = self.position
        if position is not None:
            p = position
        d = self.direction
        if direction is not None:
            p = direction
        t = self.top
        if top is not None:
            t = top

        return Connector(p, d, t)


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


class Shape:
    def __init__(self, shape, color=None, tags=None):
        self.shape = shape
        self.color = color
        self.tags = tags


class Part:
    def __init__(self, unit, transform=None, localized_connectors=None, config=None):
        self.unit = unit
        if transform is None:
            transform = Transform()
        self.transform = transform

        self.subparts = {}
        self.config = unit.finalize_config(config, localized_connectors)

    def add_subpart(self, name, part, idx=None):
        if idx is None:
            assert name not in self.subparts
            self.subparts[name] = part
        else:
            self.subparts.setdefault(name, {})
            assert idx not in self.subparts[name]
            self.subparts[name][idx] = part

    def get_subpart(self, name, idx=None):
        if idx is None:
            assert name in self.subparts
            part = self.subparts[name]
            assert isinstance(part, Part)
        else:
            assert name in self.subparts
            assert idx in self.subparts[name]
            part = self.subparts[name][idx]
        return part

    def get_connector(self, *args):
        c = self.unit.get_connector(*args, self)
        return self.transform(c)

    def shapes(self, prefix="", fake_shapes=False):
        shapes = {}
        if fake_shapes:
            own_shapes = []
        else:
            own_shapes = self.unit.shapes(self.config)

        shapes[prefix] = [Transform(), own_shapes]

        for k, v in self.subparts.items():
            p_prefix = "{}.{}".format(prefix, k)
            if isinstance(v, Part):
                shapes.update(v.shapes(p_prefix, fake_shapes))
            else:
                for i, vv in v.items():
                    pp_prefix = "{}.{}".format(p_prefix, i)
                    shapes.update(vv.shapes(pp_prefix, fake_shapes))

        shapes = {k: [self.transform(t), s] for k, (t, s) in shapes.items()}
        return shapes


class Unit:
    parts_factory = Part

    # Must be implemented in actual part
    def shapes(self, config=None):
        return []

    def get_connector(self, params, config=None):
        if params == "origin":
            return Connector([0, 0, 0], [1, 0, 0], [0, 0, 1])

        raise NotImplementedError

    # Must be implemented for assemblies
    def subparts(self, config=None):
        return []

    # Public interface
    def place(self, pose, config=None):
        connectors, constraints = self.process_pose(pose)

        transform = self.calculate_transform(connectors, constraints)

        localized_connectors = self.localize_connectors(
            connectors, constraints, transform
        )

        part = self.parts_factory(self, transform, localized_connectors, config)

        for name, subpart in self.subparts(part.config):
            idx = None
            if not isinstance(name, str):
                name, idx = name
            part.add_subpart(name, subpart, idx)

        return part

    def localize_connectors(self, connectors, constraints, transform):
        localized_connectors = []
        if connectors and constraints:
            for connector, constraint in zip(connectors, constraints):
                c_local = transform.invert()(constraint)
                localized_connectors.append([connector, c_local])
        return localized_connectors

    def finalize_config(self, config, localized_connectors):
        # Generate actual config based on input and localized connectors
        # empty by default, so we can cache effectively
        return {}

    def process_pose(self, pose):
        connectors = []
        constraints = []
        for params, constraint in pose.items():
            c = self.get_connector(params)
            connectors.append(c)
            if not isinstance(constraint, Connector):
                constraint = Connector(*constraint)
            constraints.append(constraint)
        return connectors, constraints

    def calculate_transform(self, connectors, constraints):
        return Solver(connectors, constraints).solve()


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


class VisualConnector(Unit):
    r = 1
    length = 10
    arrow_r = 2
    arror_length = 4
    sphere_r = 2
    text_size = 5
    main_color = Color(0.7, 0.7, 0.7)
    text_color = Color(0.1, 0.7, 0.1)
    text_thick = 1

    def shapes(self, config=None):
        ret = []
        text_length = 0

        text = get_config_param(config, "text")
        if text:
            fontpath = os.path.join(
                os.path.dirname(os.path.realpath(__file__)), "../fonts/testfont.ttf"
            )

            text_shape = (
                textshape(text=text, fontpath=fontpath, size=self.text_size)
                .extrude(self.text_thick)
                .rotateX(deg(90))
            )

            text_length = text_shape.center().x * 2

            text_shape = text_shape.translate(
                self.sphere_r, self.text_thick / 2, self.r * 1.5
            )
            ret.append(Shape(text_shape, color=self.text_color))

        body_length = max(
            text_length + self.sphere_r * 2, self.length - self.arror_length
        )

        main_shape = (
            cylinder(r=self.r, h=body_length).rotateY(deg(90))
            + cone(r1=self.arrow_r, r2=0, h=self.arror_length)
            .rotateY(deg(90))
            .right(body_length)
            + sphere(r=self.sphere_r)
        )
        ret.append(Shape(main_shape, color=self.main_color))

        return ret

    def get_connector(self, params, part=None):
        if params == "origin":
            return Connector([0, 0, 0], [1, 0, 0], [0, 0, 1])

    def finalize_config(self, config, localized_connectors):
        return copy_config(config, ["text"])
