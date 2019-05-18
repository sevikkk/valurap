from connectors import Connector, Shape, Unit, VisualConnector
from pyservoce.libservoce import Color
from zencad import box, cylinder, deg, linear_extrude, point3, polygon, unify


def gen_y_motor_mount(
    front_vslot, left_motor, left_rail, left_vslot, parts, vc_prefix, is_right=False
):
    pose = {}
    if is_right:
        front_slot_end = "top"
        left_slot_side = "right"
    else:
        front_slot_end = "bottom"
        left_slot_side = "left"

    pose["mount_plane"] = front_vslot.get_connector("{}, right2".format(front_slot_end))
    pose["top_plane"] = front_vslot.get_connector("{}, front".format(front_slot_end))
    pose["bottom_plane"] = front_vslot.get_connector("{}, back".format(front_slot_end))
    pose["left_plane"] = left_vslot.get_connector("bottom, {}".format(left_slot_side))
    pose["rail_top_plane"] = left_rail.get_connector("front")
    pose["mount_holes_1"] = front_vslot.get_connector(
        ("{}, right".format(front_slot_end), 10)
    )
    pose["mount_holes_2"] = front_vslot.get_connector(
        ("{}, right2".format(front_slot_end), 10)
    )
    pose["mount_hole_3"] = front_vslot.get_connector(
        ("{}, right2".format(front_slot_end), -10)
    )
    pose["motor_bottom"] = left_motor.get_connector("bottom")
    pose["motor_top"] = left_motor.get_connector("top")
    for i in range(4):
        pose[("motor_mount_hole", i)] = left_motor.get_connector(("mount_hole", i))
    if 0:
        for n, c in pose.items():
            vcn = vc_prefix + str(n)
            vc = VisualConnector().place(pose={"origin": c}, config={"text": str(n)})
            parts.append([vcn, vc])
    for k, v in pose.items():
        if k not in ["motor_top"]:
            pose[k] = v.replace(use_for_solve=False)
    left_y_motor_mount = LeftYMotorMount().place(
        pose=pose, config={"motor_body_size": left_motor.unit.body_size}
    )
    return left_y_motor_mount


class LeftYMotorMount(Unit):
    motor_hole_spacing = 0.5
    base_thickness = 5
    base_plate_extra_length = 20

    def shapes(self, config=None):
        motor_body_size = config["motor_body_size"]
        left_x = config["left_plane"].position.x
        rail_z = config["rail_top_plane"].position.z
        top_z = config["top_plane"].position.z
        bottom_z = config["bottom_plane"].position.z
        base_y = config["mount_plane"].position.y
        motor_center_y = config["motor_top"].position.y
        motor_center_z = config["motor_top"].position.z

        if base_y < 0:
            left_right_c = -1
            right_c = 1
            left_c = 0
        else:
            left_right_c = 1
            right_c = 0
            left_c = 1

        motor_hole_left_x = config["motor_top"].position.x
        motor_hole_right_x = config["motor_bottom"].position.x + self.base_thickness
        motor_hole_back_y = (
            motor_center_y
            + (motor_body_size / 2 + self.motor_hole_spacing) * left_right_c
        )
        motor_hole_front_y = (
            motor_center_y
            - (motor_body_size / 2 + self.motor_hole_spacing) * left_right_c
        )
        motor_hole_top_z = (
            motor_center_z + motor_body_size / 2 + self.motor_hole_spacing
        )
        motor_hole_bottom_z = (
            motor_center_z - motor_body_size / 2 - self.motor_hole_spacing
        )
        base_plate_top_z = motor_hole_top_z + self.base_thickness
        base_plate_right_x = motor_hole_right_x + self.base_plate_extra_length
        motor_depth = config["motor_bottom"].position.x - config["motor_top"].position.x
        motor_hole_depth = motor_depth * 0.7
        motor_hole_width = motor_body_size + self.motor_hole_spacing * 2
        print("base_y", base_y)
        print("back_y", motor_hole_back_y)
        print("front_y", motor_hole_front_y)

        base_plate_height = abs(base_y - motor_hole_back_y)

        base_plate = (
            linear_extrude(
                polygon(
                    [
                        [left_x, bottom_z],
                        [left_x, base_plate_top_z],
                        [motor_hole_right_x, base_plate_top_z],
                        [base_plate_right_x, top_z],
                        [base_plate_right_x, bottom_z],
                        [left_x, bottom_z],
                    ]
                ).fillet(1.5),
                base_plate_height,
            )
            .rotateX(deg(90))
            .translate(0, base_y + base_plate_height * right_c, 0)
        )

        motor_hole = box(
            motor_hole_depth + 1, motor_hole_width, motor_hole_width
        ).translate(
            motor_hole_left_x,
            motor_hole_front_y - motor_hole_width * right_c,
            motor_hole_bottom_z,
        )

        motor_box = (
            box(
                motor_hole_depth + self.base_thickness,
                motor_hole_width + self.base_thickness + 1,
                motor_hole_width + self.base_thickness * 2,
            ).translate(
                motor_hole_left_x - self.base_thickness,
                motor_hole_front_y
                - self.base_thickness * left_right_c
                - (motor_hole_width + self.base_thickness + 1) * right_c,
                motor_hole_bottom_z - self.base_thickness,
            )
            - motor_hole
            - cylinder(r=13, h=self.base_thickness + 2)
            .rotateY(deg(90))
            .translate(
                motor_hole_left_x - self.base_thickness - 1,
                motor_center_y,
                motor_center_z,
            )
        )
        for i in range(4):
            hole_pos = config[("motor_mount_hole", i)].position
            motor_box -= (
                cylinder(r=2, h=self.base_thickness + 2)
                .rotateY(deg(-90))
                .translate(hole_pos.x - 1, hole_pos.y, hole_pos.z)
            )

        base_plate += motor_box

        h1_1 = config["mount_holes_1"].position
        h1_2 = point3(
            base_plate_right_x - self.base_plate_extra_length / 2, h1_1.y, h1_1.z
        )
        h2_1 = config["mount_holes_2"].position
        h2_2 = point3(
            base_plate_right_x - self.base_plate_extra_length / 2, h2_1.y, h2_1.z
        )
        for pos in [config["mount_hole_3"].position, h1_1, h1_2, h2_1, h2_2]:
            base_plate -= (
                cylinder(r=2.5, h=self.base_thickness + 2)
                .rotateX(deg(90))
                .translate(pos.x, pos.y + 1 + self.base_thickness * right_c, pos.z)
            )

        return [Shape(unify(base_plate), Color(0.7, 0.7, 0))]

    def finalize_config(self, config, localized_connectors):
        finalized_config = {}

        for name in [
            "mount_plane",
            "bottom_plane",
            "top_plane",
            "left_plane",
            "rail_top_plane",
            "mount_holes_1",
            "mount_holes_2",
            "mount_hole_3",
            "motor_top",
            "motor_bottom",
            ("motor_mount_hole", 0),
            ("motor_mount_hole", 1),
            ("motor_mount_hole", 2),
            ("motor_mount_hole", 3),
        ]:
            finalized_config[name] = localized_connectors[name]

        for name in ["motor_body_size"]:
            finalized_config[name] = config[name]

        return finalized_config

    def get_connector(self, params, config=None):
        if params == "motor_top":
            return Connector([0, 0, 0], [-1, 0, 0], [0, 0, 1])
        elif params == "motor_top":
            return Connector([0, 0, 0], [1, 0, 0], [0, 0, 1])

        return super().get_connector(params, config)
