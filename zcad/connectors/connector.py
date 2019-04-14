from .util import dot, norm, oce_point, oce_vector


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

    def replace(self, position=None, direction=None, top=None, use_for_solve=True):
        p = self.position
        if position is not None:
            p = position
        d = self.direction
        if direction is not None:
            d = direction
        t = self.top
        if top is not None:
            t = top

        return Connector(p, d, t, use_for_solve=use_for_solve)

    def forward(self, offset):
        new_pos = self.position + self.direction * offset
        return self.replace(position=new_pos)

    def reverse(self):
        new_direction = self.direction * -1
        return self.replace(direction=new_direction)
