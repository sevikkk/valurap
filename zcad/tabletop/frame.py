from connectors import Connector, Shape, Unit, VisualConnector, get_config_param, norm
from pyservoce.libservoce import Color
from tabletop.y_idler_mount import gen_y_idler_mount
from tabletop.y_motor_mount import gen_y_motor_mount
from vitamins.belt import GT2x6BeltPU, GT2x20Idler, GT2x20Pulley
from vitamins.mgn import MGN12H, MGR12
from vitamins.nema import Nema17
from vitamins.vslot import VSlot20x40
from zencad import box, display, show, unify, vector3


class YCarriage(Unit):
    def shapes(self, config=None):
        base_plate = box(50, 100, 5, center=True).translate(10, 40, 2.5)
        return [Shape(unify(base_plate), Color(0.7, 0.7, 0))]

    def finalize_config(self, config, localized_connectors):
        finalized_config = {}

        for name in [
            "idler_top",
            "idler_bottom",
            "motor_top",
            "mgn_mount_plate",
            ("mgn_mount_hole", 0),
            ("mgn_mount_hole", 1),
            ("mgn_mount_hole", 2),
            ("mgn_mount_hole", 3),
            ("motor_mount_hole", 0),
            ("motor_mount_hole", 1),
            ("motor_mount_hole", 2),
            ("motor_mount_hole", 3),
            "xslot_top_holes_1",
            "xslot_top_holes_2",
            "xslot_bottom_holes_1",
            "xslot_bottom_holes_2",
            "xslot_top_plane",
            "xslot_bottom_plane",
            "xslot_front_plane",
            "xslot_back_plane",
            "xslot_side_plane",
            "front_rail_top_plane",
            "front_rail_side_plane",
            "back_rail_top_plane",
            "back_rail_side_plane",
        ]:
            finalized_config[name] = localized_connectors.get(name)

        for name in ["idler_body_r", "motor_body_size"]:
            finalized_config[name] = config[name]

        return finalized_config

    def get_connector(self, params, config=None):
        if params == "mgn_mount_plate":
            return Connector([0, 0, 0], [0, 0, 1], [0, 1, 0])

        return super().get_connector(params, config)


def gen_y_carriage(
    x_vslot, motor, idler, mgn, front_rail, back_rail, parts, vc_prefix, is_right=False
):
    pose = {}
    if is_right:
        x_slot_holes_top = "top, right2"
        x_slot_holes_top2 = "top, right"
        x_slot_holes_bottom = "top, left2"
        x_slot_holes_bottom2 = "top, left"
        x_slot_front = "top, front"
        x_slot_back = "top, back"
        x_slot_side = "top"
        front_rail_side = "top"
        front_rail_top = ("front", -10)
        back_rail_side = "top"
        back_rail_top = ("front", -10)
    else:
        x_slot_holes_top = "bottom, right"
        x_slot_holes_top2 = "bottom, right2"
        x_slot_holes_bottom = "bottom, left"
        x_slot_holes_bottom2 = "bottom, left2"
        x_slot_front = "bottom, back"
        x_slot_back = "bottom, front"
        x_slot_side = "bottom"
        front_rail_side = "bottom"
        front_rail_top = ("front", 10)
        back_rail_side = "bottom"
        back_rail_top = ("front", 10)

    mgn_mp = mgn.get_connector("mount_plate")
    if is_right:
        mgn_mp = Connector(mgn_mp.position, mgn_mp.direction, mgn_mp.top * -1)

    pose["mgn_mount_plate"] = mgn_mp
    pose["motor_top"] = motor.get_connector("top")
    pose["idler_bottom"] = idler.get_connector("bottom")
    pose["idler_top"] = idler.get_connector("top")

    for i in range(4):
        pose[("motor_mount_hole", i)] = motor.get_connector(("mount_hole", i))
        pose[("mgn_mount_hole", i)] = mgn.get_connector(("mount_hole", i))

    pose["xslot_top_holes_1"] = x_vslot.get_connector((x_slot_holes_top, 10))
    pose["xslot_top_holes_2"] = x_vslot.get_connector((x_slot_holes_top2, 10))

    pose["xslot_bottom_holes_1"] = x_vslot.get_connector((x_slot_holes_bottom, 10))
    pose["xslot_bottom_holes_2"] = x_vslot.get_connector((x_slot_holes_bottom2, 10))
    pose["xslot_top_plane"] = pose["xslot_top_holes_1"]
    pose["xslot_bottom_plane"] = pose["xslot_bottom_holes_1"]
    pose["xslot_front_plane"] = x_vslot.get_connector(x_slot_front)
    pose["xslot_back_plane"] = x_vslot.get_connector(x_slot_back)
    pose["xslot_side_plane"] = x_vslot.get_connector(x_slot_side)
    pose["front_rail_side_plane"] = front_rail.get_connector(front_rail_side)
    pose["back_rail_side_plane"] = back_rail.get_connector(back_rail_side)
    pose["front_rail_top_plane"] = front_rail.get_connector(front_rail_top)
    pose["back_rail_top_plane"] = back_rail.get_connector(back_rail_top)

    if 1:
        for n, c in pose.items():
            vcn = vc_prefix + str(n)
            color = Color(0.2, 0.7, 0.7)
            if is_right:
                color = Color(0.7, 0.2, 0.7)

            vc = VisualConnector().place(
                pose={"origin": c}, config={"text": str(n), "color": color}
            )
            parts.append([vcn, vc])
    for k, v in pose.items():
        if k not in ["mgn_mount_plate"]:
            pose[k] = v.replace(use_for_solve=False)
    y_carriage = YCarriage().place(
        pose=pose,
        config={
            "idler_body_r": idler.unit.body_r,
            "motor_body_size": motor.unit.body_size,
        },
    )
    return y_carriage


class Frame(Unit):
    long_vslot_length = 1000
    short_vslot_length = 500
    beam_vslot_length = 500
    y_rails_length = 1000
    x_rails_length = 450
    y_belt_offset = 15
    x_belt_offset = 15

    y_rail_offset = (long_vslot_length - y_rails_length) / 2
    x_rail_offset = (beam_vslot_length - x_rails_length) / 2

    x_plate_height = 6
    y_motor_offset = 5
    y_idler_offset = 5
    x_motor_offset = 5
    x_idler_offset = 5

    def subparts(self, config=None):
        parts = []
        base_long_vslot = VSlot20x40(self.long_vslot_length)
        base_short_vslot = VSlot20x40(self.short_vslot_length)
        base_beam_vslot = VSlot20x40(self.beam_vslot_length)
        y_rail = MGR12(self.y_rails_length)
        y_mgn = MGN12H()

        x_rail = MGR12(self.x_rails_length)
        x_mgn = MGN12H()

        left_vslot_mount = self.get_connector("left_vslot_bottom", config)
        left_vslot = base_long_vslot.place(
            pose={("bottom, back", -50): left_vslot_mount}
        )
        parts.append(["left_vslot", left_vslot])

        front_vslot_mount = left_vslot.get_connector("bottom, right")
        front_vslot = base_short_vslot.place(
            pose={"bottom,right,mount": front_vslot_mount}
        )
        parts.append(["front_vslot", front_vslot])

        back_vslot_mount = left_vslot.get_connector("top, right")
        back_vslot = base_short_vslot.place(
            pose={"bottom,left, mount": back_vslot_mount}
        )
        parts.append(["back_vslot", back_vslot])

        right_vslot_mount = front_vslot.get_connector("top, right, mount")
        right_vslot = base_long_vslot.place(pose={"bottom,left": right_vslot_mount})
        parts.append(["right_vslot", right_vslot])

        left_rail_mount = left_vslot.get_connector(
            ("bottom, front", self.y_rail_offset)
        ).swapTD()
        left_rail = y_rail.place(pose={"bottom": left_rail_mount})
        parts.append(["left_rail", left_rail])

        right_rail_mount = right_vslot.get_connector(
            ("bottom, front", self.y_rail_offset)
        ).swapTD()
        right_rail = y_rail.place(pose={"bottom": right_rail_mount})
        parts.append(["right_rail", right_rail])

        mgn_offset = self.y_rails_length / 2 - config["Y"]

        left_mgn_mount = left_rail.get_connector("top")
        left_mgn = y_mgn.place(pose={("mgr_top", mgn_offset): left_mgn_mount})
        parts.append(["left_mgn", left_mgn])

        right_mgn_mount = right_rail.get_connector("top")
        right_mgn = y_mgn.place(pose={("mgr_top", mgn_offset): right_mgn_mount})
        parts.append(["right_mgn", right_mgn])

        beam_mount_left = left_mgn.get_connector("mount_plate")
        beam_mount_right = right_mgn.get_connector("mount_plate")
        y_rails_dist = norm(beam_mount_right.position - beam_mount_left.position)
        beam_mount_pos = beam_mount_left.position + vector3(
            y_rails_dist / 2 - self.beam_vslot_length / 2, 10, self.x_plate_height
        )
        beam_mount = Connector(
            position=beam_mount_pos, direction=[0, 0, -1], top=[-1, 0, 0]
        )

        beam_vslot = base_beam_vslot.place(pose={"bottom, left": beam_mount})
        parts.append(["beam_vslot", beam_vslot])

        x1_rail_mount = beam_vslot.get_connector(
            ("bottom, front", self.x_rail_offset)
        ).swapTD()
        x1_rail = x_rail.place(pose={"bottom": x1_rail_mount})
        parts.append(["x1_rail", x1_rail])

        x2_rail_mount = beam_vslot.get_connector(
            ("bottom, back", self.x_rail_offset)
        ).swapTD()
        x2_rail = x_rail.place(pose={"bottom": x2_rail_mount})
        parts.append(["x2_rail", x2_rail])

        x1_mgn_offset = self.x_rails_length / 2 + config["X1"]
        x1_mgn_mount = x1_rail.get_connector("top")
        x1_mgn = x_mgn.place(pose={("mgr_top", x1_mgn_offset): x1_mgn_mount})
        parts.append(["x1_mgn", x1_mgn])

        x2_mgn_offset = self.x_rails_length / 2 + config["X2"]
        x2_mgn_mount = x2_rail.get_connector("top")
        x2_mgn = x_mgn.place(pose={("mgr_top", x2_mgn_offset): x2_mgn_mount})
        parts.append(["x2_mgn", x2_mgn])

        y_belt = GT2x6BeltPU()
        y_pulley = GT2x20Pulley()
        y_idler = GT2x20Idler()
        y_motor = Nema17()

        left_mgn_top = left_mgn.get_connector("mount_plate").position
        right_mgn_top = right_mgn.get_connector("mount_plate").position
        belt_top_z = left_mgn_top.z
        offsets = y_belt.pulley_radiuses(y_pulley.teeth)
        pulley_z = belt_top_z - offsets.base
        left_pulley_x = left_mgn_top.x - self.y_belt_offset - y_belt.belt_width / 2
        right_pulley_x = right_mgn_top.x + self.y_belt_offset + y_belt.belt_width / 2
        pulley_y = (
            front_vslot.get_connector("right").position.y
            - y_motor.body_size / 2
            - self.y_motor_offset
        )
        idler_y = (
            back_vslot.get_connector("left").position.y
            + self.y_idler_offset
            + y_idler.body_r
        )

        left_pulley_mount = Connector(
            position=[left_pulley_x, pulley_y, pulley_z],
            direction=[-1, 0, 0],
            top=[0, 0, 1],
        )
        left_pulley = y_pulley.place(pose={"origin": left_pulley_mount})
        parts.append(["left_pulley", left_pulley])

        right_pulley_mount = Connector(
            position=[right_pulley_x, pulley_y, pulley_z],
            direction=[1, 0, 0],
            top=[0, 0, 1],
        )
        right_pulley = y_pulley.place(pose={"origin": right_pulley_mount})
        parts.append(["right_pulley", right_pulley])

        left_motor = y_motor.place(
            pose={"top": left_pulley.get_connector("bottom").forward(5).reverse()}
        )
        parts.append(["left_motor", left_motor])

        right_motor = y_motor.place(
            pose={"top": right_pulley.get_connector("bottom").forward(5).reverse()}
        )
        parts.append(["right_motor", right_motor])

        left_idler_mount = Connector(
            position=[left_pulley_x, idler_y, pulley_z],
            direction=[-1, 0, 0],
            top=[0, 0, 1],
        )
        left_idler = y_idler.place(pose={"origin": left_idler_mount})
        parts.append(["left_idler", left_idler])

        right_idler_mount = Connector(
            position=[right_pulley_x, idler_y, pulley_z],
            direction=[1, 0, 0],
            top=[0, 0, 1],
        )
        right_idler = y_idler.place(pose={"origin": right_idler_mount})
        parts.append(["right_idler", right_idler])

        self.gen_belt(left_idler, left_pulley, parts, y_belt, "y_left")
        self.gen_belt(right_pulley, right_idler, parts, y_belt, "y_right")

        x_belt = GT2x6BeltPU()
        x_pulley = GT2x20Pulley()
        x_idler = GT2x20Idler()
        x_motor = Nema17()

        x1_mgn_top = x1_mgn.get_connector("mount_plate").position
        x2_mgn_top = x2_mgn.get_connector("mount_plate").position
        offsets = y_belt.pulley_radiuses(y_pulley.teeth)

        x1_pulley_y = x1_mgn_top.y - offsets.base
        x_pulley_z = x1_mgn_top.z + self.x_belt_offset + x_belt.belt_width / 2
        x1_pulley_x = (
            left_pulley_x
            - self.x_motor_offset
            - y_belt.belt_width / 2
            - x_motor.body_size / 2
        )
        x1_idler_x = right_mgn_top.x

        x1_pulley_mount = Connector(
            position=[x1_pulley_x, x1_pulley_y, x_pulley_z],
            direction=[0, 0, 1],
            top=[0, 1, 0],
        )
        x1_pulley = x_pulley.place(pose={"origin": x1_pulley_mount})
        parts.append(["x1_pulley", x1_pulley])

        x1_idler_mount = Connector(
            position=[x1_idler_x, x1_pulley_y, x_pulley_z],
            direction=[0, 0, 1],
            top=[0, 1, 0],
        )
        x1_idler = x_idler.place(pose={"origin": x1_idler_mount})
        parts.append(["x1_idler", x1_idler])

        x1_motor = x_motor.place(
            pose={"top": x1_pulley.get_connector("bottom").forward(5).reverse()}
        )
        parts.append(["x1_motor", x1_motor])
        self.gen_belt(x1_pulley, x1_idler, parts, x_belt, "x1")

        x2_pulley_y = x2_mgn_top.y + offsets.base
        x2_pulley_x = (
            right_pulley_x
            + self.x_motor_offset
            + y_belt.belt_width / 2
            + x_motor.body_size / 2
        )
        x2_idler_x = left_mgn_top.x

        x2_pulley_mount = Connector(
            position=[x2_pulley_x, x2_pulley_y, x_pulley_z],
            direction=[0, 0, 1],
            top=[0, 1, 0],
        )
        x2_pulley = x_pulley.place(pose={"origin": x2_pulley_mount})
        parts.append(["x2_pulley", x2_pulley])

        x2_idler_mount = Connector(
            position=[x2_idler_x, x2_pulley_y, x_pulley_z],
            direction=[0, 0, 1],
            top=[0, 1, 0],
        )
        x2_idler = x_idler.place(pose={"origin": x2_idler_mount})
        parts.append(["x2_idler", x2_idler])

        x2_motor = x_motor.place(
            pose={"top": x2_pulley.get_connector("bottom").forward(5).reverse()}
        )
        parts.append(["x2_motor", x2_motor])
        self.gen_belt(x2_idler, x2_pulley, parts, x_belt, "x2")

        left_y_motor_mount = gen_y_motor_mount(
            front_vslot, left_motor, left_rail, left_vslot, parts, "vcrm_"
        )
        parts.append(["left_y_motor_mount", left_y_motor_mount])

        right_y_motor_mount = gen_y_motor_mount(
            front_vslot, right_motor, right_rail, right_vslot, parts, "vclm_", True
        )
        parts.append(["right_y_motor_mount", right_y_motor_mount])

        left_y_idler_mount = gen_y_idler_mount(
            back_vslot, left_idler, left_rail, left_vslot, parts, "vcli_"
        )
        parts.append(["left_y_idler_mount", left_y_idler_mount])

        right_y_idler_mount = gen_y_idler_mount(
            back_vslot, right_idler, right_rail, right_vslot, parts, "vcri_", True
        )
        parts.append(["right_y_idler_mount", right_y_idler_mount])

        left_y_carriage = gen_y_carriage(
            beam_vslot, x1_motor, x2_idler, left_mgn, x2_rail, x1_rail, parts, "vclx_"
        )
        parts.append(["left_y_carriage", left_y_carriage])

        right_y_carriage = gen_y_carriage(
            beam_vslot,
            x2_motor,
            x1_idler,
            right_mgn,
            x1_rail,
            x2_rail,
            parts,
            "vcrx_",
            True,
        )
        parts.append(["right_y_carriage", right_y_carriage])

        return parts

    def gen_belt(self, left_idler, left_pulley, parts, y_belt, prefix):
        left_belt_a = y_belt.place(
            pose={
                "start": left_pulley.get_connector(("belt_cw", 0)),
                "end": left_idler.get_connector(("belt_ccw", 0)).replace(
                    use_for_solve=False
                ),
            }
        )
        parts.append(["{}_belt_a".format(prefix), left_belt_a])
        left_belt_b = y_belt.place(
            pose={
                "start": left_pulley.get_connector(("belt_ccw", 180)),
                "end": left_idler.get_connector(("belt_cw", 180)).replace(
                    use_for_solve=False
                ),
            }
        )
        parts.append(["{}_belt_b".format(prefix), left_belt_b])
        left_belt_c = y_belt.place(
            pose={
                "start": left_pulley.get_connector(("belt_ccw", 0)),
                "pulley_origin": left_pulley.get_connector("origin").replace(
                    use_for_solve=False
                ),
                "end": left_pulley.get_connector(("belt_cw", 180)).replace(
                    use_for_solve=False
                ),
            }
        )
        parts.append(["{}_belt_c".format(prefix), left_belt_c])
        left_belt_d = y_belt.place(
            pose={
                "start": left_idler.get_connector(("belt_cw", 0)),
                "pulley_origin": left_idler.get_connector("origin").replace(
                    use_for_solve=False
                ),
                "end": left_idler.get_connector(("belt_ccw", 180)).replace(
                    use_for_solve=False
                ),
            }
        )
        parts.append(["{}_belt_d".format(prefix), left_belt_d])

    def finalize_config(self, config, localized_connectors):
        final_config = {}
        final_config["Y"] = get_config_param(config, "Y", 0)
        final_config["X1"] = get_config_param(config, "X1", 0)
        final_config["X2"] = get_config_param(config, "X2", 0)
        final_config["Z"] = get_config_param(config, "Z", 0)

        return final_config

    def get_connector(self, params, config=None):
        if params == "origin":
            return Connector([0, 0, 0], [1, 0, 0], [0, 0, 1])
        elif params == "left_vslot_bottom":
            return Connector([0, 0, 0], [0, 0, -1], [0, -1, 0])

        raise NotImplementedError


def main():
    parts = []

    c1 = Connector([0, 0, 0], [1, 0, 0], [0, 0, 1])
    frame = Frame().place(pose={"origin": c1}, config={"Y": 100, "X1": 100, "X2": -100})
    parts.append(frame)

    print(parts)
    if 0:
        lym = frame.transform(
            frame.subparts["left_y_idler_mount"].get_connector("idler_top").position
        )
        view_port = (
            box(200, 200, 200, center=True).translate(lym.x, lym.y, lym.z).unlazy()
        )

    if 0:
        rym = frame.transform(
            frame.subparts["right_y_idler_mount"].get_connector("origin").position
        )
        view_port += (
            box(200, 200, 200, center=True).translate(rym.x, rym.y, rym.z).unlazy()
        )

    if 1:
        view_port = box(3000, 3000, 3000, center=True).unlazy()

    for part in parts:
        for t, shape_list in part.shapes().values():
            for shape in shape_list:
                print(shape)
                disp_shape = t.transform(shape.shape.unlazy()) ^ view_port
                c = display(disp_shape, shape.color)

    show()


print("name:", __name__)
if __name__ == "__main__":
    main()
