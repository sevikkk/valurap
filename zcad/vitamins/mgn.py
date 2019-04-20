from connectors import Connector, copy_config, get_config_param
from connectors.units import Shape, Unit
from zencad import (
    box,
    circle,
    color,
    cylinder,
    deg,
    linear_extrude,
    polygon,
    rectangle,
    square,
    unify,
)


class MGR12(Unit):
    def __init__(self, length):
        self.length = length
        self.demo_connectors = ["top", "bottom"]
        num = len(self.mounting_holes())
        self.demo_connectors.append(("mount_hole", 0))
        self.demo_connectors.append(("mount_hole", -1))
        if num > 4:
            self.demo_connectors.append(("mount_hole", 1))
            self.demo_connectors.append(("mount_hole", -2))

    def shapes(self, config=None):
        part_color = color(0.7, 0.7, 0.7)

        body = (
            box(12, 8, self.length).translate(-6, 0, 0).chamfer(0.5)
            - box(3, 1, self.length + 2).translate(-6 - 1, 5, -1)
            - box(3, 1, self.length + 2).translate(6 - 2, 5, -1)
        )

        body = body.chamfer(
            1,
            [
                [-6, 5, self.length / 2],
                [-6, 6, self.length / 2],
                [6, 5, self.length / 2],
                [6, 6, self.length / 2],
            ],
        )

        chamfs = []
        for z in self.mounting_holes():
            body -= (
                (cylinder(r=3.5 / 2, h=10).down(1) + cylinder(r=3, h=5.5).up(3.5))
                .rotateX(deg(-90))
                .up(z)
            )
            chamfs.append([0, 8, z + 3])
            chamfs.append([0, 0, z + 3.5 / 2])

        body = body.chamfer(0.5, chamfs)

        return [Shape(body, part_color)]

    def mounting_holes(self):
        num, edge = divmod(self.length, 25)
        if edge < 20:
            num -= 1
            edge += 25

        edge = edge / 2
        return [edge + 25 * i for i in range(num + 1)]

    def get_connector(self, params="top", part=None):
        if isinstance(params, str):
            param = params
            args = []
        else:
            param = params[0]
            args = params[1:]

        if param in ("origin", "bottom"):
            return Connector(position=[0, 0, 0], direction=[0, 0, -1], top=[0, 1, 0])
        elif param == "top":
            return Connector(
                position=[0, 0, self.length], direction=[0, 0, 1], top=[0, 1, 0]
            )
        elif param == "mount_hole":
            idx = args[0]
            z = self.mounting_holes()[idx]
            return Connector(position=[0, 3.5, z], direction=[0, 1, 0], top=[0, 0, 1])


class MGN12H(Unit):
    demo_connectors = [
        "top",
        "bottom",
        ("mgr_top", 50),
        ("mount_hole", 0),
        ("mount_hole", 1),
        ("mount_hole", 2),
        ("mount_hole", 3),
    ]

    length = 45.4
    body_length = 32.4
    body_width = 27
    body_height = 10
    mount_base = 20
    caps_thick = 1

    def get_connector(self, params="top", part=None):
        if isinstance(params, str):
            param = params
            args = []
        else:
            param = params[0]
            args = params[1:]

        if param in ("origin", "bottom"):
            return Connector(
                position=[0, 0, -self.length / 2], direction=[0, 0, -1], top=[0, 1, 0]
            )
        elif param == "top":
            return Connector(
                position=[0, 0, self.length / 2], direction=[0, 0, 1], top=[0, 1, 0]
            )
        elif param in ("mount_hole", "mount_plate"):
            if param == "mount_hole":
                idx = args[0]
                x, z = [[-1, -1], [-1, 1], [1, 1], [1, -1]][args[0]]
            else:
                x, z = 0, 0

            x = x * 10
            z = z * 10

            return Connector(position=[x, 0, z], direction=[0, 1, 0], top=[0, 0, 1])
        elif param == "mgr_top":
            offset = args[0]
            return Connector(
                position=[0, -13, offset], direction=[0, 0, 1], top=[0, 1, 0]
            )

        raise NotImplementedError

    def shapes(self, config=None):
        body_color = color(0.7, 0.7, 0.7)
        caps_color = color(0.8, 0.2, 0.2)
        ends_color = color(0.2, 0.8, 0.2)

        body = unify(
            box(self.body_width, self.body_height, self.body_length)
            .translate(-self.body_width / 2, -self.body_height, -self.body_length / 2)
            .chamfer(
                1,
                [
                    [-self.body_width / 2, 0, 0],
                    [self.body_width / 2, 0, 0],
                    [-self.body_width / 2, -self.body_height, 0],
                    [self.body_width / 2, -self.body_height, 0],
                ],
            )
            - cylinder(r=0.5, h=self.length).translate(
                -self.body_width / 2, -self.body_height / 2, -self.length / 2
            )
            - box(13, 6.5, self.length).translate(-13 / 2, -11, -self.length / 2)
            - box(14, 5, self.length)
            .translate(-14 / 2, -0.5, -self.length / 2)
            .chamfer(1.5)
            - cylinder(r=1.5, h=4.5).rotateX(deg(-90)).translate(-10, -3.5, -10)
            - cylinder(r=1.5, h=4.5).rotateX(deg(-90)).translate(10, -3.5, -10)
            - cylinder(r=1.5, h=4.5).rotateX(deg(-90)).translate(-10, -3.5, 10)
            - cylinder(r=1.5, h=4.5).rotateX(deg(-90)).translate(10, -3.5, 10)
        )

        cap = (
            (
                box(self.body_width, self.body_height - 0.5, self.caps_thick).translate(
                    -self.body_width / 2, -self.body_height, 0
                )
                - box(13, 6.5, self.length).translate(-13 / 2, -11, -self.length / 2)
                + cylinder(r=1, h=self.caps_thick).translate(
                    13 / 2, -self.body_height + 2.5, 0
                )
                + cylinder(r=1, h=self.caps_thick).translate(
                    -13 / 2, -self.body_height + 2.5, 0
                )
            )
            .chamfer(
                2,
                [
                    [-self.body_width / 2, -0.5, self.caps_thick / 2],
                    [self.body_width / 2, -0.5, self.caps_thick / 2],
                ],
            )
            .chamfer(
                1,
                [
                    [-self.body_width / 2, -self.body_height, self.caps_thick / 2],
                    [self.body_width / 2, -self.body_height, self.caps_thick / 2],
                ],
            )
        )

        cap = unify(cap)

        end_thick = (self.length - self.body_length - self.caps_thick * 2) / 2

        end = (
            (
                box(self.body_width, self.body_height - 0.5, end_thick).translate(
                    -self.body_width / 2, -self.body_height, 0
                )
                - box(13, 6.5, self.length).translate(-13 / 2, -11, -self.length / 2)
            )
            .chamfer(
                2,
                [
                    [-self.body_width / 2, -0.5, end_thick / 2],
                    [self.body_width / 2, -0.5, end_thick / 2],
                ],
            )
            .chamfer(
                1,
                [
                    [-self.body_width / 2, -self.body_height, end_thick / 2],
                    [self.body_width / 2, -self.body_height, end_thick / 2],
                ],
            )
        )

        return [
            Shape(body, body_color),
            Shape(cap.translate(0, 0, -self.length / 2), caps_color),
            Shape(cap.translate(0, 0, self.length / 2 - self.caps_thick), caps_color),
            Shape(end.translate(0, 0, -self.length / 2 + self.caps_thick), ends_color),
            Shape(
                end.translate(0, 0, self.length / 2 - self.caps_thick - end_thick),
                ends_color,
            ),
        ]
