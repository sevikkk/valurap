from zencad import box
from connectors import Connector, np_point, Unit


class VSlot20x20(Unit):
    def __init__(self, length):
        self.length = length

    def model(self):
        body = box([20, 20, self.length]).translate(-10, -10, 0)
        slot = box([6, 7, self.length]).translate(-3, 4, 0)
        return body - slot

    def get_connector(self, side="top"):
        x = 0
        y = 0
        z = 0
        for s in side.split(','):
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

        return Connector([x, y, z], d, t)


class VSlot20x40(Unit):
    def __init__(self, length):
        self.length = length

    def model(self):
        return box([20, 40, self.length]).translate(-10, -20, 0)
