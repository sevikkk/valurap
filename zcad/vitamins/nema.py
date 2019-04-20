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


class Nema17(Unit):
    demo_connectors = [
        "origin",
        "top",
        "bottom",
        ("mount_hole", 0),
        ("mount_hole", 1),
        ("mount_hole", 2),
        ("mount_hole", 3),
    ]

    body_size = 42

    def __init__(self, length=37, dshaft=True):
        self.length = length
        self.dshaft = dshaft

    def shapes(self, config=None):
        body_color = color(0.1, 0.1, 0.1)
        plates_color = color(0.5, 0.5, 0.5)
        shaft_color = color(0.7, 0.7, 0.7)
        cables_color = color(0.4, 0.4, 0.2)
        body_size = self.body_size
        plates_thick = 8
        body_chamfer = 5
        plates_chamfer = 3
        fillet_size = 1

        body = box(body_size, body_size, self.length - 2 * plates_thick).translate(
            -body_size / 2, -body_size / 2, plates_thick
        )
        body = body.chamfer(
            body_chamfer,
            [
                [body_size / 2, body_size / 2, self.length / 2],
                [-body_size / 2, body_size / 2, self.length / 2],
                [body_size / 2, -body_size / 2, self.length / 2],
                [-body_size / 2, -body_size / 2, self.length / 2],
            ],
        ).fillet(fillet_size)
        body -= cylinder(r=3, h=self.length + 2).down(1)

        bottom_plate = box(body_size, body_size, plates_thick).translate(
            -body_size / 2, -body_size / 2, 0
        )
        plate = bottom_plate.chamfer(
            plates_chamfer,
            [
                [body_size / 2, body_size / 2, plates_thick / 2],
                [-body_size / 2, body_size / 2, plates_thick / 2],
                [body_size / 2, -body_size / 2, plates_thick / 2],
                [-body_size / 2, -body_size / 2, plates_thick / 2],
            ],
        ).fillet(fillet_size)

        bottom_plate = unify(
            plate
            - cylinder(r=5, h=plates_thick).down(plates_thick / 2)
            - cylinder(r=3, h=plates_thick + 2).down(1)
            + box(5 + 3, 16, plates_thick)
            .translate(body_size / 2 - 3, -8, 0)
            .fillet(fillet_size)
        )
        top_plate = (
            plate
            + cylinder(r=11, h=3).up(plates_thick - 1)
            - cylinder(r=5, h=plates_thick + 1).up(plates_thick / 2)
            - cylinder(r=3, h=plates_thick + 4).down(1)
        ).up(self.length - plates_thick)

        shaft = cylinder(r=2.5, h=self.length + 24 - 2).up(2).fillet(0.5)
        if self.dshaft:
            shaft = shaft - box(10, 10, 24).translate(2, -5, self.length + 2)

        for x in [31 / 2, -31 / 2]:
            for y in [31 / 2, -31 / 2]:
                top_plate -= cylinder(r=1.5, h=5).translate(x, y, self.length - 4.5)

        cables = None
        for i in range(4):
            y = (i - 1.5) * 2
            cable = (
                cylinder(r=1, h=5)
                .rotateY(deg(90))
                .translate(body_size / 2 + 5, y, plates_thick / 2)
            )
            if cables:
                cables += cable
            else:
                cables = cable

        return [
            Shape(body, body_color),
            Shape(bottom_plate, plates_color),
            Shape(top_plate, plates_color),
            Shape(shaft, shaft_color),
            Shape(cables, cables_color),
        ]

    def get_connector(self, params="origin", config=None):
        if isinstance(params, str):
            param = params
            args = []
        else:
            param = params[0]
            args = params[1:]

        if param == "origin":
            return Connector(position=[0, 0, 0], direction=[0, 0, 1], top=[1, 0, 0])
        elif param == "mount_hole":
            x, y = [[-1, -1], [-1, 1], [1, 1], [1, -1]][args[0]]

            x = x * 31 / 2
            y = y * 31 / 2
            z = self.length
            return Connector(position=[x, y, z], direction=[0, 0, 1], top=[1, 0, 0])
        elif param == "top":
            return Connector(
                position=[0, 0, self.length], direction=[0, 0, 1], top=[1, 0, 0]
            )
        elif param == "bottom":
            return Connector(position=[0, 0, 0], direction=[0, 0, -1], top=[1, 0, 0])
        raise NotImplementedError
