from .connector import Connector
from .solver import Solver
from .transform import Transform


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
        c = self.unit.get_connector(*args, self.config)
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
    demo_connectors = ["origin"]

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
            pose, transform
        )

        part = self.parts_factory(self, transform, localized_connectors, config)

        for name, subpart in self.subparts(part.config):
            idx = None
            if not isinstance(name, str):
                name, idx = name
            part.add_subpart(name, subpart, idx)

        return part

    def localize_connectors(self, pose, transform):
        localized_connectors = {}
        for c, connector in pose.items():
            c_local = transform.invert()(connector)
            localized_connectors[c] = c_local
        return localized_connectors

    def finalize_config(self, config, localized_connectors):
        # Generate actual config based on input and localized connectors
        # empty by default, so we can cache effectively
        return {}

    def process_pose(self, pose, config=None):
        connectors = []
        constraints = []
        for params, constraint in pose.items():
            if not constraint.use_for_solve:
                continue
            c = self.get_connector(params)
            connectors.append(c)
            if not isinstance(constraint, Connector):
                constraint = Connector(*constraint)
            constraints.append(constraint)
        return connectors, constraints

    def calculate_transform(self, connectors, constraints):
        return Solver(connectors, constraints).solve()
