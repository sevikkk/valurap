import math
from collections import namedtuple

from connectors import Connector, VisualConnector, copy_config, get_config_param, dot, norm, cross
from connectors.units import Shape, Unit
from zencad import circle, color, deg, linear_extrude, polygon, rectangle, square, unify, box

BeltRadiuses = namedtuple("BeltRadiuses", "tip dip pld base")

class GT2Belt(Unit):
    demo_connectors = [
        "base",
        "start",
        "tip",
        "dip",
        "end",
    ]
    tooth_pitch = 2.0
    tooth_height = 0.75
    belt_width = 10
    pld = 0.254
    belt_height = 1.38

    def __init__(self, length=None):
        self.length = length

    def pulley_radiuses(self, teeth=None):
        if teeth:
            pld_r = teeth * self.tooth_pitch / 2 / math.pi
        else:
            pld_r = 0

        dip_r = pld_r - self.pld
        tip_r = dip_r - self.tooth_height
        base_r = tip_r + self.belt_height
        return BeltRadiuses(tip_r, dip_r, pld_r, base_r)

    def calculate_poses(self, pulley1, pulley2_base_point, pulley2_teeth, crossing=False):
        """
        Calculate poses for cw and ccw belts and second pulley, so second pulley
        axe is parallel to first and goes through pulley2_base_point

        :param pulley1: placed first pulley
        :param pulley2_base_point: point on second pulley axe
        :param pulley2_teeth: number of teeth for second pulley
        :param crossing: cw and ccw belts must cross on the way and second pulley axe
                            will be opposite to the first
        :return: poses for 2 belts, and second pulley
            {
                "cw_belt_start" : Connector,
                "cw_belt_end" : Connector with use_for_solve=False,
                "ccw_belt_start": Connector,
                "ccw_belt_end": Connector with use_for_solve=False,
                "second_pulley_origin" : Connector
            }
        """

        p1_origin = pulley1.get_connector("origin")
        axe_direction = p1_origin.direction
        p1_center = p1_origin.position
        delta = pulley2_base_point - p1_center
        offset = dot(delta, axe_direction)
        p2_center = p1_center + offset * axe_direction
        p2_direction = p1_origin.direction
        if crossing:
            p2_direction = -1 * p2_direction

        p2_origin = Connector(position=p2_center, direction=p2_direction, top=p1_origin.top)

        p1_offset = self.pulley_radiuses(pulley1.teeth).pld
        p2_offset = self.pulley_radiuses(pulley2_teeth).pld

        if 1:
            # Only simple case for now
            assert crossing is False
            assert p1_offset == p2_offset

            belt_direction = p2_center - p1_center
            belt_length = norm(belt_direction)
            belt_direction = belt_direction / belt_length
            new_top = cross(p2_direction, belt_direction)
            new_top = new_top / norm(new_top)

        cw_belt_start = p1_center + new_top * p1_offset
        ccw_belt_start = p1_center - new_top * p1_offset
        cw_belt_end = p2_center + new_top * p2_offset
        ccw_belt_end = p2_center - new_top * p2_offset

    def get_connector(self, params="base", config=None):
        if isinstance(params, str):
            param = params
            args = []
        else:
            param = params[0]
            args = params[1:]

        radiuses = self.pulley_radiuses()

        x = 0
        y = 0
        z = 0
        d = [0, 1, 0]
        t = [0, 0, -1]

        if param == "base":
            y = radiuses.base
            z = 10
        elif param == "start":
            d = [0, 0, -1]
            t = [0, 1, 0]
            y = 0
        elif param == "tip":
            y = radiuses.tip
            z = 20
        elif param == "dip":
            y = radiuses.dip
            z = 30
        elif param == "end":
            z = self.length
            d = [0, 0, 1]
            t = [0, 1, 0]

        return Connector(position=[x, y, z], direction=d, top=t, data=params)

    def finalize_config(self, config, localized_connectors):
        final_config = {}
        length = self.length
        straight = True
        if "end" in localized_connectors:
            end_c = localized_connectors["end"]
            start_c = self.get_connector("start")
            assert abs(dot(start_c.direction, end_c.direction)) > 0.999
            assert dot(start_c.top, end_c.top) > 0.999
            length = localized_connectors["end"].position.z

        if length is None:
            length = 100

        final_config["length"] = length
        final_config["straight"] = straight

        return final_config

    def shapes(self, config):
        body_color = color(0.1, 0.1, 0.1)
        teeth_color = color(0.3, 0.3, 0.3)
        assert config["straight"]
        offsets = self.pulley_radiuses()
        body = box(self.belt_width, offsets.base - offsets.dip, config["length"]).translate(
            -self.belt_width / 2, offsets.dip, 0
        )
        teeth = box(self.belt_width, offsets.dip - offsets.tip, config["length"]).translate(
            -self.belt_width / 2, offsets.tip, 0
        )
        return [
            Shape(body, body_color),
            Shape(teeth, teeth_color),
        ]


class GT2x6BeltStd(GT2Belt):
    belt_width = 6

class GT2x6BeltPU(GT2x6BeltStd):
    belt_height = 1.7

class GT2x20Pulley(Unit):
    demo_connectors = [
        "top",
        "bottom",
        ("belt_cw", 0),
        ("belt_cw", 90),
        ("belt_cw", 180),
        ("belt_ccw", 0),
        ("belt_ccw", 180),
    ]
    teeth = 20

    def shapes(self, config=None):
        part_color = get_config_param(config, "color", color(0.7, 0.7, 0.7))

        s = base_section()

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

    def finalize_config(self, config, localized_connectors):
        return copy_config(config, ["color"])



class GT2x20Idler(Unit):
    demo_connectors = [
        "top",
        "bottom",
        ("belt_cw", 0),
        ("belt_cw", 90),
        ("belt_cw", 180),
        ("belt_ccw", 0),
        ("belt_ccw", 180),
    ]

    def __init__(self, toothed=True):
        self.toothed = toothed

    def shapes(self, config=None):
        part_color = get_config_param(config, "color", color(0.7, 0.7, 0.7))

        s = base_section()

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

    def finalize_config(self, config, localized_connectors):
        return copy_config(config, ["color"])

