from connectors import Connector, VisualConnector, copy_config, get_config_param
from connectors.units import Shape, Unit
from zencad import circle, color, deg, linear_extrude, polygon, rectangle, square, unify


def base_section():
    ext_size = 10
    ext_thick = 1.8
    int_thick = 1.5
    slot_ext = 9.6
    slot_int = 6.0
    hole_int = 11
    int_size = 7.3
    corner = (
        polygon(
            list(
                reversed(
                    [
                        [ext_size, ext_size],
                        [ext_size, slot_ext / 2],
                        [ext_size - ext_thick, slot_int / 2],
                        [ext_size - ext_thick, hole_int / 2],
                        [hole_int / 2, hole_int / 2],
                        [hole_int / 2, ext_size - ext_thick],
                        [slot_int / 2, ext_size - ext_thick],
                        [slot_ext / 2, ext_size],
                        [ext_size, ext_size],
                    ]
                )
            )
        )
        .fillet(1.5, [[ext_size, ext_size]])
        .fillet(
            0.2,
            [
                [hole_int / 2, ext_size - ext_thick],
                [ext_size - ext_thick, hole_int / 2],
                [ext_size, slot_ext / 2],
                [ext_size - ext_thick, slot_int / 2],
                [slot_int / 2, ext_size - ext_thick],
                [slot_ext / 2, ext_size],
            ],
        )
    )
    s = square(a=int_size, center=True)
    for a in range(4):
        s += corner.rotateZ(deg(a * 90))
        s -= circle(r=0.3).translate(0, int_size / 2, 0).rotateZ(deg(a * 90))
    s += rectangle(int_thick, 17 * 1.4, center=True).rotateZ(deg(45))
    s += rectangle(int_thick, 17 * 1.4, center=True).rotateZ(deg(-45))
    s -= circle(r=2.1)
    s = unify(s)
    return s


class VSlot20x20(Unit):
    demo_connectors = [
        "bottom",
        "bottom, front",
        "bottom, back",
        "bottom, left",
        "bottom, right",
        "bottom, front, right",
        "bottom, front, left",
        "bottom, back, left",
        "bottom, back, right",
        "top",
        "top, front",
        "top, back",
        "top, left",
        "top, right",
        "top, front, right",
        "top, front, left",
        "top, back, left",
        "top, back, right",
    ]

    def __init__(self, length):
        self.length = length

    def shapes(self, config=None):
        part_color = get_config_param(config, "color", color(0.7, 0.7, 0.7))

        s = base_section()

        body = linear_extrude(s, self.length)

        return [Shape(body, part_color)]

    def get_connector(self, params="top", part=None):
        x = 0
        y = 0
        z = 0
        for s in params.split(","):
            s = s.strip()
            if s.startswith("to"):  # top
                z = self.length
            elif s.startswith("bo"):  # bottom
                z = 0
            elif s.startswith("f"):  # front
                y = -10
            elif s.startswith("ba"):  # back
                y = 10
            elif s.startswith("l"):  # left
                x = -10
            elif s.startswith("r"):  # right
                x = 10

        if x == 0 and y == 0:
            d = [0, 0, z - self.length / 2]
            t = [0, 1, 0]
        else:
            t = [0, 0, z - self.length / 2]
            d = [x, y, 0]

        return Connector(position=[x, y, z], direction=d, top=t, data=params)

    def finalize_config(self, config, localized_connectors):
        return copy_config(config, ["color"])


class VSlot20x40(Unit):
    demo_connectors = [
        "bottom",
        "bottom2",
        "bottom, front",
        "bottom, back",
        "bottom, left",
        "bottom, right",
        "bottom, left2",
        "bottom, right2",
        "bottom, front, right",
        "bottom, front, left",
        "bottom, back, left",
        "bottom, back, right",
        "top",
        "top2",
        "top, front",
        "top, back",
        "top, left",
        "top, right",
        "top, left2",
        "top, right2",
        "top, front, right",
        "top, front, left",
        "top, back, left",
        "top, back, right",
    ]

    def __init__(self, length):
        self.length = length

    def shapes(self, config=None):
        part_color = get_config_param(config, "color", color(0.7, 0.7, 0.7))

        s = base_section()
        s2 = s + s.translate(20, 0, 0)
        s2 += rectangle(6, 1.8).translate(10 - 3, 10 - 1.8, 0)
        s2 += rectangle(6, 1.8).translate(10 - 3, -10, 0)
        s2 -= rectangle(6.5, 20 - 2 * 1.8, center=True).translate(10, 0, 0).fillet(0.2)
        s2 = unify(s2.rotateZ(deg(90)))

        body = linear_extrude(s2, self.length)

        return [Shape(body, part_color)]

    def get_connector(self, params="top", part=None):
        if isinstance(params, str):
            param = params
            args = []
        else:
            param = params[0]
            args = params[1:]

        x = 0
        y = 0
        z = 0
        dy = 0
        mount = False
        for s in param.split(","):
            s = s.strip()
            if s.startswith("to"):  # top
                z = self.length
                if s.endswith("2"):
                    y += 20
                    dy = 20
            elif s.startswith("bo"):  # bottom
                z = 0
                if s.endswith("2"):
                    y += 20
                    dy = 20
            elif s.startswith("f"):  # front
                y = -10
            elif s.startswith("ba"):  # back
                y = 30
                dy = 20
            elif s.startswith("l"):  # left
                x = -10
                if s.endswith("2"):
                    y += 20
                    dy = 20
            elif s.startswith("r"):  # right
                x = 10
                if s.endswith("2"):
                    y += 20
                    dy = 20
            elif s.startswith("m"):  # mount_this_side
                mount = True

        if x == 0 and y - dy == 0:
            d = [0, 0, z - self.length / 2]
            t = [0, 1, 0]
        else:
            t = [0, 0, z - self.length / 2]
            d = [x, y - dy, 0]

        if mount:
            # Invert connector, so it will mount this side
            # on other beam
            d, t = t, d
            d = [-1 * a for a in d]

        if len(args) > 0:
            offset = args[0]

            if z == 0:
                z = offset
            else:
                z = z - offset

        return Connector(position=[x, y, z], direction=d, top=t, data=params)

    def finalize_config(self, config, localized_connectors):
        return copy_config(config, ["color"])
