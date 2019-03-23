import time

from pyservoce import rotateZ
from zencad import box, cylinder, display, show, Color, vector3, deg, point3
from connectors import Connector, Unit, Shape

v_up = vector3(0, 0, 1)
v_down = vector3(0, 0, -1)
v_left = vector3(-1, 0, 0)
v_right = vector3(1, 0, 0)
v_forward = vector3(0, 1, 0)
v_backward = vector3(0, -1, 0)


class Indicator(Unit):
    def shapes(self, part=None):
        indicator = cylinder(r=5, h=3)
        return [Shape(indicator, color=Color(0.7, 0, 0))]

    def get_connector(self, params, part=None):
        if params == "origin":
            return Connector([0, 0, 0], v_up, v_forward)


class Head(Unit):
    r = 10
    h = 10
    neck_r = 3
    neck_h = 3

    def shapes(self, part=None):
        head = cylinder(r=self.r, h=self.h).up(self.neck_h)
        neck = cylinder(r=self.neck_r, h=self.neck_h)

        return [Shape(head + neck, color=Color(0.5, 0.5, 0.5))]

    def get_connector(self, params, part=None):
        if params == "origin":
            return Connector([0, 0, 0], v_backward, v_up)
        if params in ("left_eye", "right_eye"):
            is_left = params == "left_eye"
            v = v_backward * self.r
            v = rotateZ(deg(45) if is_left else -deg(45))(v)
            pos = point3(0, 0, self.h * 0.7 + self.neck_h) + v

            return Connector(pos, v_backward, v_up)

    def place_subparts(self, part):
        part.add_subpart(
            "left_eye",
            Indicator().place(pose={"origin": self.get_connector("left_eye", part)}),
        )

        part.add_subpart(
            "right_eye",
            Indicator().place(pose={"origin": self.get_connector("right_eye", part)}),
        )


class Robot(Unit):
    width = 20
    height = 30
    thick = 15

    def shapes(self, part=None):
        main_body = box(self.width, self.thick, self.height)
        return [Shape(main_body, color=Color(0.4, 0.4, 0.4))]

    def get_connector(self, params, part=None):
        if params == "indicator":
            return Connector(
                [self.width / 2, 0, self.height * 0.7], v_backward, v_right
            )
        if params == "head":
            if part and part.config and "head_angle" in part.config:
                head_angle = part.config["head_angle"]
            else:
                head_angle = 0
            return Connector(
                [self.width / 2, self.thick / 2, self.height],
                rotateZ(head_angle)(v_backward),
                v_up,
            )
        if params == "origin":
            return Connector([self.width / 2, self.thick / 2, 0], v_backward, v_up)

    def place_subparts(self, part):
        part.add_subpart(
            "indicator",
            Indicator().place(pose={"origin": self.get_connector("indicator", part)}),
        )

        part.add_subpart(
            "head",
            Head().place(
                pose={"origin": self.get_connector("head", part)}, config=part.config
            ),
        )


nulltime = time.time()


def get_actor_shapes():
    t = time.time() - nulltime
    shapes = {}

    robot = Robot().place(
        pose={"origin": Connector([-30, 0, 0], v_backward, v_up)},
        config={"head_angle": t},
    )

    shapes.update(robot.shapes("robot"))

    robot2 = Robot().place(
        pose={"origin": Connector([30, 0, 0], rotateZ(-t / 4)(v_backward), v_up)}
    )

    shapes.update(robot2.shapes("robot2"))
    return shapes


display(box(200, 200, 1).translate(-100, -100, -1), Color(0.5, 0.5, 0.5))
controllers = {}

shapes = get_actor_shapes()
for n, shape in shapes.items():
    c = display(shape.shape.unlazy(), shape.color)
    # c.set_location(shape.transform)
    controllers[n] = c


def animate(widget):
    shapes = get_actor_shapes()
    for n, shape in shapes.items():
        controllers[n].set_location(shape.transform)


print(4)
show(animate=animate)
