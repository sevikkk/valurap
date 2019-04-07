import os

from pyservoce.libservoce import Color
from zencad import cone, cylinder, deg, sphere, textshape

from .connector import Connector
from .units import Shape, Unit
from .util import copy_config, get_config_param


class VisualConnector(Unit):
    r = 1
    length = 10
    arrow_r = 2
    arror_length = 4
    sphere_r = 2
    text_size = 5
    main_color = Color(0.7, 0.7, 0.7)
    text_color = Color(0.1, 0.7, 0.1)
    text_thick = 1

    def shapes(self, config=None):
        ret = []
        text_length = 0

        text = get_config_param(config, "text")
        if text:
            fontpath = os.path.join(
                os.path.dirname(os.path.realpath(__file__)), "../fonts/testfont.ttf"
            )

            text_shape = (
                textshape(text=text, fontpath=fontpath, size=self.text_size)
                .extrude(self.text_thick)
                .rotateX(deg(90))
            )

            text_length = text_shape.center().x * 2

            text_shape = text_shape.translate(
                self.sphere_r, self.text_thick / 2, self.r * 1.5
            )
            ret.append(Shape(text_shape, color=self.text_color))

        body_length = max(
            text_length + self.sphere_r * 2, self.length - self.arror_length
        )

        main_shape = (
            cylinder(r=self.r, h=body_length).rotateY(deg(90))
            + cone(r1=self.arrow_r, r2=0, h=self.arror_length)
            .rotateY(deg(90))
            .right(body_length)
            + sphere(r=self.sphere_r)
        )
        ret.append(Shape(main_shape, color=self.main_color))

        return ret

    def get_connector(self, params, config=None):
        if params == "origin":
            return Connector([0, 0, 0], [1, 0, 0], [0, 0, 1])

    def finalize_config(self, config, localized_connectors):
        return copy_config(config, ["text"])


class Demo(Unit):
    def __init__(self, demo_unit):
        self.unit = demo_unit

    def subparts(self, config=None):
        parts = []
        base = self.unit.place(pose={"origin": self.get_connector("origin")})
        parts.append(["base", base])

        vc = VisualConnector()
        for i, conn in enumerate(self.unit.demo_connectors):
            vvc = vc.place({"origin": base.get_connector(conn)}, config={"text": str(conn)})
            parts.append(["c{}".format(i), vvc])
        return parts

    def get_connector(self, params, config=None):
        return self.unit.get_connector(params, config)
