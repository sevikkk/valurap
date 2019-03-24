from .util import oce_point, oce_vector, norm, dot


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
