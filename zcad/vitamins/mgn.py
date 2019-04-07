from connectors import Connector, copy_config, get_config_param
from connectors.units import Shape, Unit
from zencad import box, circle, color, deg, linear_extrude, polygon, rectangle, square, unify, cylinder


class MGR12(Unit):
    def __init__(self, length):
        self.length = length
        self.demo_connectors = [
            "top",
            "bottom"
        ]
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
            - box(3, 1, self.length + 2).translate(-6 -1, 5, -1)
            - box(3, 1, self.length + 2).translate(6 -2, 5, -1)
        )

        body = body.chamfer(1, [
            [-6, 5, self.length/2],
            [-6, 6, self.length/2],
            [6, 5, self.length/2],
            [6, 6, self.length/2],
        ])

        chamfs = []
        for z in self.mounting_holes():
            body -= (
                cylinder(r=3.5/2, h = 10).down(1)
                + cylinder(r=3, h = 5.5).up(3.5)
            ).rotateX(deg(-90)).up(z)
            chamfs.append([0, 8, z + 3])
            chamfs.append([0, 0, z + 3.5/2])

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

        if param in ("origin", "top"):
            return Connector(position=[0, 0, 0], direction=[0,0,-1], top=[0,1,0])
        elif param == "bottom":
            return Connector(position=[0, 0, self.length], direction=[0,0,1], top=[0,1,0])
        elif param == "mount_hole":
            idx = args[0]
            z = self.mounting_holes()[idx]
            return Connector(position=[0, 3.5, z], direction=[0,1,0], top=[0,0,1])



