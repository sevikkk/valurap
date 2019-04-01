from connectors import Connector, copy_config, get_config_param
from connectors.units import Shape, Unit
from zencad import circle, color, deg, linear_extrude, polygon, rectangle, square, unify, box, cylinder


class Nema17(Unit):
    def __init__(self, length=37, dshaft=True):
        self.length = length
        self.dshaft = dshaft

    def shapes(self, config=None):
        body_color = color(0.1, 0.1, 0.1)
        plates_color = color(0.5, 0.5, 0.5)
        shaft_color = color(0.7, 0.7, 0.7)
        body_size = 42
        plates_thick = 8
        body_chamfer = 5
        plates_chamfer = 3
        fillet_size = 1

        body = box(body_size, body_size, self.length - 2 * plates_thick)\
            .translate(-body_size/2, -body_size/2,plates_thick)
        body = body.chamfer(body_chamfer, [
            [body_size/2, body_size/2, self.length/2],
            [-body_size/2, body_size/2, self.length/2],
            [body_size/2, -body_size/2, self.length/2],
            [-body_size/2, -body_size/2, self.length/2],
        ]).fillet(fillet_size)
        body -= cylinder(r=3, h = self.length+2).down(1)

        bottom_plate = box(body_size, body_size, plates_thick) \
            .translate(-body_size/2, -body_size/2, 0)
        plate = bottom_plate.chamfer(plates_chamfer, [
            [body_size/2, body_size/2, plates_thick/2],
            [-body_size/2, body_size/2, plates_thick/2],
            [body_size/2, -body_size/2, plates_thick/2],
            [-body_size/2, -body_size/2, plates_thick/2],
        ]).fillet(fillet_size)

        bottom_plate = (
                plate
                - cylinder(r=5, h = plates_thick + 1).down(1)
                - cylinder(r=3, h = plates_thick + 4).down(1)
        )
        top_plate = (
                plate
                + cylinder(r=11, h = 3).up(plates_thick - 1)
                - cylinder(r=5, h = plates_thick + 1).up(plates_thick/2)
                - cylinder(r=3, h = plates_thick + 4).down(1)
        ).up(self.length - plates_thick)

        shaft = cylinder(r=2.5, h = self.length + 17 -2).up(2).fillet(0.5)
        if self.dshaft:
            shaft = shaft - box(10,10,17).translate(2, -5, self.length + 2)

        return [
            Shape(body, body_color),
            Shape(bottom_plate, plates_color),
            Shape(top_plate, plates_color),
            Shape(shaft, shaft_color),
        ]

    def get_connector(self, params="origin", config=None):
        if params == "origin":
            return Connector(position=[0, 0, 0], direction=[0,0,1], top=[1,0,0])


