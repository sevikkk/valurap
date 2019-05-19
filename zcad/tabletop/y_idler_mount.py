from math import copysign

from connectors import Connector, Shape, Unit, VisualConnector
from connectors.util import uni_box, uni_cylinder
from pyservoce.libservoce import Color
from zencad import deg, unify


class YIdlerMount(Unit):
    base_thickness = 5
    base_plate_extra_length = 20
    idler_mount_space = 1
    idler_body_space = 2

    def shapes(self, config=None):
        left_x = config["left_plane"].position.x
        rail_z = config["rail_top_plane"].position.z
        top_z = config["top_plane"].position.z
        bottom_z = config["bottom_plane"].position.z
        base_y = config["mount_plane"].position.y
        left_mount_y = config["mount_holes_5"].position.y
        idler_center_y = config["idler_top"].position.y
        idler_center_z = config["idler_top"].position.z
        idler_top_x = config["idler_top"].position.x
        idler_top_z = config["idler_top"].position.z + config["idler_body_r"]
        idler_bottom_x = config["idler_bottom"].position.x
        idler_bottom_z = config["idler_bottom"].position.z - config["idler_body_r"]

        coef_x = copysign(1.0, -config["left_plane"].direction.x)
        coef_y = copysign(1.0, -config["mount_plane"].direction.y)

        belt_opening_z_top = idler_top_z + self.idler_body_space
        belt_opening_z_bottom = idler_bottom_z - self.idler_body_space
        belt_opening_x_left = idler_top_x - coef_x * self.idler_mount_space
        belt_opening_x_right = idler_bottom_x + coef_x * self.idler_mount_space
        belt_opening_y_front = idler_center_y - coef_y * (
            self.idler_body_space + config["idler_body_r"]
        )
        belt_opening_y_back = base_y + 1.0 * coef_y

        idler_mount_z_top = belt_opening_z_top + self.base_thickness
        idler_mount_z_bottom = belt_opening_z_bottom - self.base_thickness
        idler_mount_x_left = belt_opening_x_left - coef_x * self.base_thickness
        idler_mount_x_right = belt_opening_x_right + coef_x * self.base_thickness
        idler_mount_y_front = belt_opening_y_front - coef_y * self.base_thickness
        idler_mount_y_back = base_y

        base_plate_right_x = left_x + coef_x * (20 + self.base_plate_extra_length)
        base_plate_left_x = idler_mount_x_left - coef_x * self.base_thickness
        base_plate_front_y = base_y - coef_y * self.base_thickness
        base_plate_back_y = base_y + coef_y * (20 + self.base_plate_extra_length)
        base_plate_top_z = max(rail_z, belt_opening_z_top + self.base_thickness)
        base_plate_bottom_z = bottom_z

        base_plate_depth = base_plate_back_y - base_plate_front_y
        base_plate_width = base_plate_left_x - base_plate_right_x
        base_plate_height = base_plate_top_z - base_plate_bottom_z

        base_plate = uni_box(
            -base_plate_width, self.base_thickness * coef_y, base_plate_height
        ).translate(base_plate_left_x, base_plate_front_y, bottom_z)

        base_plate += uni_box(
            idler_mount_x_left - idler_mount_x_right,
            idler_mount_y_front - idler_mount_y_back,
            idler_mount_z_top - idler_mount_z_bottom,
        ).translate(idler_mount_x_right, idler_mount_y_back, idler_mount_z_bottom)

        base_plate -= uni_box(
            belt_opening_x_left - belt_opening_x_right,
            belt_opening_y_front - belt_opening_y_back,
            belt_opening_z_top - belt_opening_z_bottom,
        ).translate(belt_opening_x_right, belt_opening_y_back, belt_opening_z_bottom)

        idler_axis_r = 1.5
        tensioner_z_top = idler_center_z + idler_axis_r
        tensioner_z_bottom = idler_center_z - idler_axis_r
        tensioner_x_left = idler_mount_x_left - coef_x * 1.0
        tensioner_x_right = idler_mount_x_right + coef_x * 1.0
        tensioner_y_front = idler_center_y - coef_y * idler_axis_r
        tensioner_y_back = base_plate_front_y

        base_plate -= uni_box(
            tensioner_x_left - tensioner_x_right,
            tensioner_y_front - tensioner_y_back,
            tensioner_z_top - tensioner_z_bottom,
        ).translate(tensioner_x_right, tensioner_y_back, tensioner_z_bottom)

        for pos in [
            config["mount_holes_1"].position,
            config["mount_holes_2"].position,
            config["mount_hole_3"].position,
            config["mount_hole_4"].position,
        ]:
            base_plate -= (
                uni_cylinder(r=2.5, h=coef_y * (self.base_thickness + 2))
                .rotateX(deg(90))
                .translate(pos.x, pos.y + coef_y * 1.0, pos.z)
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
            "mount_hole_4",
            "mount_holes_5",
            "mount_holes_6",
            "idler_top",
            "idler_bottom",
        ]:
            finalized_config[name] = localized_connectors[name]

        for name in ["idler_body_r"]:
            finalized_config[name] = config[name]

        return finalized_config

    def get_connector(self, params, config=None):
        if params == "idler_top":
            return Connector([0, 0, 0], [-1, 0, 0], [0, 0, 1])

        return super().get_connector(params, config)


def gen_y_idler_mount(
    back_vslot, idler, rail, left_vslot, parts, vc_prefix, is_right=False
):
    pose = {}
    if is_right:
        back_slot_end = "top"
        left_slot_side = "right"
    else:
        back_slot_end = "bottom"
        left_slot_side = "left"

    pose["mount_plane"] = back_vslot.get_connector("{}, left2".format(back_slot_end))
    pose["top_plane"] = back_vslot.get_connector("{}, front".format(back_slot_end))
    pose["bottom_plane"] = back_vslot.get_connector("{}, back".format(back_slot_end))
    pose["left_plane"] = left_vslot.get_connector("top, {}".format(left_slot_side))
    pose["rail_top_plane"] = rail.get_connector(("front", -10))
    pose["mount_holes_1"] = back_vslot.get_connector(
        ("{}, left".format(back_slot_end), 10)
    )
    pose["mount_holes_2"] = back_vslot.get_connector(
        ("{}, left2".format(back_slot_end), 10)
    )
    pose["mount_hole_3"] = back_vslot.get_connector(
        ("{}, left2".format(back_slot_end), -10)
    )
    pose["mount_hole_4"] = back_vslot.get_connector(
        ("{}, left".format(back_slot_end), -10)
    )
    pose["mount_holes_5"] = left_vslot.get_connector(
        ("top, {}".format(left_slot_side), 10)
    )
    pose["mount_holes_6"] = left_vslot.get_connector(
        ("top, {}2".format(left_slot_side), 10)
    )
    pose["idler_bottom"] = idler.get_connector("bottom")
    pose["idler_top"] = idler.get_connector("top")
    if 1:
        for n, c in pose.items():
            vcn = vc_prefix + str(n)
            vc = VisualConnector().place(pose={"origin": c}, config={"text": str(n)})
            parts.append([vcn, vc])
    for k, v in pose.items():
        if k not in ["idler_top"]:
            pose[k] = v.replace(use_for_solve=False)
    y_idler_mount = YIdlerMount().place(
        pose=pose, config={"idler_body_r": idler.unit.body_r}
    )
    return y_idler_mount
