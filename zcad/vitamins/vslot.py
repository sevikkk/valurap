from zencad import color, deg, polygon, circle, rectangle, linear_extrude, square
from connectors import Connector, Unit, Shape


class VSlot20x20(Unit):
    def __init__(self, length):
        self.length = length

    def shapes(self, part=None):
        if part and part.config and "color" in part.config:
            part_color = part.config["color"]
        else:
            part_color = color(0.7, 0.7, 0.7)

        corner = polygon([
            [10, 10],
            [10, 9.55 / 2],
            [10 - 1.8, 6.2 / 2],
            [10 - 1.8, 11 / 2],
            [11 / 2, 11 / 2],
            [11 / 2, 10 - 1.8],
            [6.2 / 2, 10 - 1.8],
            [9.55 / 2, 10],
            [10, 10],
        ]).fillet(1.5, [[10, 10]]).fillet(0.2, [
            [11 / 2, 10 - 1.8],
            [10 - 1.8, 11 / 2],
            [10, 9.55 / 2],
            [10 - 1.8, 6.2 / 2],
            [6.2 / 2, 10 - 1.8],
            [9.55 / 2, 10],
        ])

        s = square(a=7.3, center=True)
        for a in range(4):
            s += corner.rotateZ(deg(a * 90))
            s -= circle(r=0.3).translate(0, 7.3 / 2, 0).rotateZ(deg(a * 90))

        s += rectangle(1.8, 17 * 1.4, center=True).rotateZ(deg(45))
        s += rectangle(1.8, 17 * 1.4, center=True).rotateZ(deg(-45))
        s -= circle(r=2.1)

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


class VSlot20x40(Unit):
    def __init__(self, length):
        self.length = length
