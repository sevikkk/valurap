import math
from collections import namedtuple

from pyservoce.libservoce import rotateZ

from connectors import Connector, VisualConnector, copy_config, get_config_param, dot, norm, cross
from connectors.units import Shape, Unit
from zencad import circle, color, deg, linear_extrude, polygon, rectangle, square, unify, box, cylinder, vector3, point3

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

    def calculate_poses(self, pulley1, pulley2_base_point, pulley2_teeth=None, crossing=False):
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
        print("p1_origin", p1_origin)
        axe_direction = p1_origin.direction
        print("axe_direction", axe_direction)
        p1_center = p1_origin.position
        print("p1_center", p1_center)
        delta = pulley2_base_point - p1_center
        print("delta", delta)
        offset = dot(delta, axe_direction)
        print("offset", offset)
        p2_center = pulley2_base_point - axe_direction * offset
        print("p2_center", p2_center)
        p2_direction = axe_direction
        print("p2_direction", p2_direction)
        if crossing:
            p2_direction = p2_direction * -1

        result = {
            "p2_origin": Connector(position=p2_center, direction=p2_direction, top=p1_origin.top)
        }

        p1_offset = self.pulley_radiuses(pulley1.unit.teeth).pld
        if pulley2_teeth is None:
            pulley2_teeth = pulley1.unit.teeth
        p2_offset = self.pulley_radiuses(pulley2_teeth).pld

        if 1:
            # Only simple case for now
            assert crossing is False
            assert p1_offset == p2_offset

            belt_direction = p2_center - p1_center
            belt_length = norm(belt_direction)
            belt_direction = belt_direction / belt_length
            print("p2_dir", p2_direction, "belt_dir", belt_direction)
            new_top = cross(p2_direction, belt_direction)
            print("new_top", new_top)
            new_top = new_top / norm(new_top)

        result["cw_belt_start"] = Connector(
            p1_center + new_top * p1_offset,
            belt_direction,
            new_top
        )

        result["ccw_belt_start"] = Connector(
            p1_center - new_top * p1_offset,
            belt_direction,
            new_top * -1
        )

        result["cw_belt_end"] = Connector(
            p2_center + new_top * p2_offset,
            belt_direction * -1,
            new_top,
            use_for_solve=False
        )

        result["ccw_belt_end"] = Connector(
            p2_center - new_top * p2_offset,
            belt_direction * -1,
            new_top * -1,
            use_for_solve=False
        )

        return result


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
        elif param == "start":
            d = [0, 0, -1]
            t = [0, 1, 0]
            y = 0
        elif param == "tip":
            y = radiuses.tip
        elif param == "dip":
            y = radiuses.dip
        elif param == "end":
            z = config["length"]
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
            if (
                    -dot(start_c.direction, end_c.direction) > 0.999
                and
                    dot(start_c.top, end_c.top) > 0.999
            ):
                # straight
                length = localized_connectors["end"].position.z
            elif "pulley_origin" in localized_connectors:
                center_c = localized_connectors["pulley_origin"]
                left1 = cross(start_c.direction, start_c.top)
                left2 = cross(end_c.direction, end_c.top)
                print("left1", left1, "left2", left2)
                assert abs(dot(left1, left2)) > 0.999
                assert abs(dot(left1, center_c.direction)) > 0.999
                center_pos = center_c.position
                assert abs(center_pos.x) < 0.0001
                assert abs(center_pos.z) < 0.0001
                end_pos = end_c.position
                assert abs(end_pos.x) < 0.0001
                assert (norm(center_pos) - norm(end_pos - center_pos)) < 0.0001
                end_v = end_pos - center_pos
                print("end_v", end_v)
                angle = math.atan2(-end_v.z, end_v.y)
                if angle < 0:
                    angle += 2 * math.pi
                print("angle", angle/math.pi*180)
                straight = False
                final_config["angle"] = angle
                final_config["r"] = -center_pos.y
            else:
                raise RuntimeError("Unable to fit belt")


        if length is None:
            length = 100

        final_config["length"] = length
        final_config["straight"] = straight

        return final_config

    def shapes(self, config):
        body_color = color(0.1, 0.1, 0.1)
        teeth_color = color(0.3, 0.3, 0.3)
        offsets = self.pulley_radiuses()
        if config["straight"]:
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

        r = config["r"]
        angle = config["angle"]

        p1 = (
            circle(offsets.base + r, angle)
            - circle(offsets.dip + r, angle)
        )
        body = linear_extrude(p1, self.belt_width)\
            .translate(-r, 0, -self.belt_width/2)\
            .rotateY(deg(-90))\
            .rotateX(deg(-90))

        p2 = (
                circle(offsets.dip + r, angle)
                - circle(offsets.tip + r, angle)
        )
        teeth =linear_extrude(p2, self.belt_width) \
            .translate(-r, 0, -self.belt_width/2) \
            .rotateY(deg(-90)) \
            .rotateX(deg(-90))


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
        ("belt_ccw", 180),
        #("belt_ccw", 0),
        #("belt_ccw", 180),
    ]
    teeth = 20
    body_r = 8
    base_h = 7.5
    groove_h = 7
    cap_h = 1.5
    inner_r = 2.5

    belt = GT2x6BeltStd

    def shapes(self, config=None):
        offsets = self.belt().pulley_radiuses(self.teeth)
        body_color = color(0.7, 0.7, 0.7)

        body = (
            cylinder(r=self.body_r, h=self.base_h)
            + cylinder(r=offsets.tip, h=self.groove_h).up(self.base_h)
            + cylinder(r=self.body_r, h=self.cap_h).up(self.base_h + self.groove_h)
            - cylinder(r=self.inner_r, h=self.base_h + self.groove_h+self.cap_h + 2).down(1)
        )
        if self.base_h > 4:
            body = (
                body
                - cylinder(r=1.5, h=self.body_r + 1).rotateX(deg(90)).up(self.base_h/2)
                - cylinder(r=1.5, h=self.body_r + 1).rotateY(deg(90)).up(self.base_h/2)
            )
        body = body.down(self.base_h + self.groove_h/2)

        return [Shape(body, body_color)]

    def get_connector(self, params="top", part=None):
        if isinstance(params, str):
            param = params
            args = []
        else:
            param = params[0]
            args = params[1:]

        offsets = self.belt().pulley_radiuses(self.teeth)
        x = 0
        y = 0
        z = 0
        d = [0,0,1]
        t = [0,1,0]
        if param == "top":
            z = self.groove_h/2 + self.cap_h
        elif param == "bottom":
            z = -self.groove_h/2 - self.base_h
            d = [0,0,-1]
        elif param == "origin":
            z = 0
            d = [0,0,1]
        elif param in ("belt_cw", "belt_ccw"):
            t = rotateZ(deg(args[0]))(vector3(0,1,0))
            d = rotateZ(deg(args[0]))(vector3(1,0,0))
            p = point3(0,0,0) + t * offsets.pld
            if param == "belt_cw":
                d = d * -1
            return Connector(position=p, direction=d, top=t, data=params)

        return Connector(position=[x, y, z], direction=d, top=t, data=params)


class GT2x20Idler(GT2x20Pulley):
    body_r = 9
    base_h = 1
    inner_r = 1.5
    cap_h = 1

