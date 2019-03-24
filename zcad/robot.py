import time

from pyservoce import rotateZ
from zencad import box, cylinder, display, show, Color, vector3, deg, point3
from connectors import (
    Connector,
    get_config_param,
    copy_config,
    Shape,
    Unit,
    VisualConnector,
)

v_up = vector3(0, 0, 1)
v_down = vector3(0, 0, -1)
v_left = vector3(-1, 0, 0)
v_right = vector3(1, 0, 0)
v_forward = vector3(0, 1, 0)
v_backward = vector3(0, -1, 0)


class Indicator(Unit):
    def shapes(self, config=None):
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

    def shapes(self, config=None):
        head = cylinder(r=self.r, h=self.h).up(self.neck_h)
        neck = cylinder(r=self.neck_r, h=self.neck_h)

        return [Shape(head + neck, color=Color(0.5, 0.5, 0.5))]

    def get_connector(self, params, config=None):
        if params == "origin":
            return Connector([0, 0, 0], v_backward, v_up)
        if params in ("left_eye", "right_eye"):
            is_left = params == "left_eye"
            v = v_backward * self.r
            v = rotateZ(deg(45) if is_left else -deg(45))(v)
            pos = point3(0, 0, self.h * 0.7 + self.neck_h) + v

            return Connector(pos, v_backward, v_up)

    def subparts(self, config=None):
        return [
            [
                "left_eye",
                Indicator().place(
                    pose={"origin": self.get_connector("left_eye", config)}
                ),
            ],
            [
                "right_eye",
                Indicator().place(
                    pose={"origin": self.get_connector("right_eye", config)}
                ),
            ],
        ]


class Robot(Unit):
    width = 20
    height = 30
    thick = 15

    def shapes(self, config=None):
        main_body = box(self.width, self.thick, self.height)
        return [Shape(main_body, color=Color(0.4, 0.4, 0.4))]

    def get_connector(self, params, config=None):
        if params == "indicator":
            return Connector(
                [self.width / 2, 0, self.height * 0.7], v_backward, v_right
            )
        if params == "head":
            head_angle = get_config_param(config, "head_angle", 0)

            return Connector(
                [self.width / 2, self.thick / 2, self.height],
                rotateZ(head_angle)(v_backward),
                v_up,
            )
        if params == "origin":
            return Connector([self.width / 2, self.thick / 2, 0], v_backward, v_up)

    def subparts(self, config=None):
        parts = []
        parts.append(
            [
                "indicator",
                Indicator().place(
                    pose={"origin": self.get_connector("indicator", config)}
                ),
            ]
        )

        parts.append(
            [
                "head",
                Head().place(
                    pose={"origin": self.get_connector("head", config)}, config=config
                ),
            ]
        )

        return parts

    def finalize_config(self, config, localized_connectors):
        return copy_config(config, ["head_angle"])


nulltime = time.time()


def get_actor_shapes(fake_shapes=False):
    t = time.time() - nulltime
    shapes = {}

    robot = Robot().place(
        pose={"origin": Connector([-30, 0, 0], v_backward, v_up)},
        config={"head_angle": t},
    )

    shapes.update(robot.shapes("robot", fake_shapes))

    robot2 = Robot().place(
        pose={"origin": Connector([30, 0, 0], rotateZ(-t / 4)(v_backward), v_up)}
    )

    shapes.update(robot2.shapes("robot2", fake_shapes))

    r1 = robot.get_connector("origin")
    r2 = robot2.get_connector("origin")
    d = r2.position - r1.position
    p = r1.position + d / 2
    u = v_up
    c = Connector(p, d, u)
    vc = VisualConnector().place(pose={"origin": c}, config={"text": "Bubu"})
    shapes.update(vc.shapes("vc", fake_shapes))
    return shapes


display(box(200, 200, 1).translate(-100, -100, -1), Color(0.5, 0.5, 0.5))
controllers = {}

shapes = get_actor_shapes()
for n, (t, shape_list) in shapes.items():
    controllers[n] = []
    for shape in shape_list:
        c = display(shape.shape.unlazy(), shape.color)
        # c.set_location(t)
        controllers[n].append(c)


def animate(widget):
    shapes = get_actor_shapes(True)
    for n, (t, shape_list) in shapes.items():
        for c in controllers[n]:
            c.set_location(t.transform)


show(animate=animate)
