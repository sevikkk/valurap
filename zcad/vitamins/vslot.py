from zencad import box, color, deg
from connectors import Connector, Unit, Shape


class VSlot20x20(Unit):
    def __init__(self, length):
        self.length = length

    def shapes(self, part=None):
        if part and part.config and "color" in part.config:
            part_color = part.config["color"]
        else:
            part_color = color(0.7, 0.7, 0.7)

        body = box([20, 20, self.length]).translate(-10, -10, 0)
        for angle in range(0,360,90):
            body = body - box([6, 7, self.length]).translate(-3, 4, 0).rotateZ(deg(angle))

        return [Shape(body, part_color)]

    def get_connector(self, params="top", part=None):
        x = 0
        y = 0
        z = 0
        for s in params.split(','):
            s = s.strip()
            if s.startswith("to"): # top
                z = self.length
            elif s.startswith("bo"): # bottom
                z = 0
            elif s.startswith("f"): # front
                y = -10
            elif s.startswith("ba"): # back
                y = 10
            elif s.startswith("l"): # left
                x = -10
            elif s.startswith("r"): # right
                x = 10

        if x == 0 and y == 0:
            d = [0, 0,z - self.length/2 ]
            t = [0, 1, 0]
        else:
            t = [0,0,z - self.length/2 ]
            d = [x, y, 0]

        return Connector(position=[x, y, z], direction=d, top=t, data=params)


class VSlot20x40(Unit):
    def __init__(self, length):
        self.length = length


