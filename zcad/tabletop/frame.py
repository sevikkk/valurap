from connectors import Connector, Demo, VisualConnector, Unit, get_config_param, norm
from vitamins.mgn import MGN12H, MGR12
from vitamins.nema import Nema17
from vitamins.vslot import VSlot20x20, VSlot20x40
from vitamins.belt import GT2x6BeltPU, GT2x6BeltStd, GT2x20Pulley, GT2x20Idler
from zencad import Color, box, display, show, point3, vector3


class Frame(Unit):
    long_vslot_length = 1000
    short_vslot_length = 500
    beam_vslot_length = 500
    y_rails_length = 1000
    x_rails_length = 450

    y_rail_offset = (long_vslot_length - y_rails_length) / 2
    x_rail_offset = (beam_vslot_length - x_rails_length) / 2

    x_plate_height = 6

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
        left_vslot = base_long_vslot.place(pose={("bottom, back", -50): left_vslot_mount})
        parts.append(["left_vslot", left_vslot])

        front_vslot_mount = left_vslot.get_connector("bottom, right")
        front_vslot = base_short_vslot.place(pose={"bottom,right,mount": front_vslot_mount})
        parts.append(["front_vslot", front_vslot])

        back_vslot_mount = left_vslot.get_connector("top, right")
        back_vslot = base_short_vslot.place(pose={"bottom,left, mount": back_vslot_mount})
        parts.append(["back_vslot", back_vslot])

        right_vslot_mount = front_vslot.get_connector("top, right, mount")
        right_vslot = base_long_vslot.place(pose={"bottom,left": right_vslot_mount})
        parts.append(["right_vslot", right_vslot])

        left_rail_mount = left_vslot.get_connector(("bottom, front", self.y_rail_offset)).swapTD()
        left_rail = y_rail.place(pose={"bottom": left_rail_mount})
        parts.append(["left_rail", left_rail])

        right_rail_mount = right_vslot.get_connector(("bottom, front", self.y_rail_offset)).swapTD()
        right_rail = y_rail.place(pose={"bottom": right_rail_mount})
        parts.append(["right_rail", right_rail])

        mgn_offset = self.y_rails_length/2 - config["Y"]

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
                    y_rails_dist/2 - self.beam_vslot_length/2,
                    10,
                    self.x_plate_height
        )
        beam_mount = Connector(
            position=beam_mount_pos,
            direction=[0,0,-1],
            top=[-1,0,0]
        )

        beam_vslot = base_beam_vslot.place(pose={"bottom, left": beam_mount})
        parts.append(["beam_vslot", beam_vslot])

        x1_rail_mount = beam_vslot.get_connector(("bottom, front", self.x_rail_offset)).swapTD()
        x1_rail = x_rail.place(pose={"bottom": x1_rail_mount})
        parts.append(["x1_rail", x1_rail])

        x2_rail_mount = beam_vslot.get_connector(("bottom, back", self.x_rail_offset)).swapTD()
        x2_rail = x_rail.place(pose={"bottom": x2_rail_mount})
        parts.append(["x2_rail", x2_rail])

        x1_mgn_offset = self.x_rails_length/2 + config["X1"]
        x1_mgn_mount = x1_rail.get_connector("top")
        x1_mgn = x_mgn.place(pose={("mgr_top", x1_mgn_offset): x1_mgn_mount})
        parts.append(["x1_mgn", x1_mgn])

        x2_mgn_offset = self.x_rails_length/2 + config["X2"]
        x2_mgn_mount = x2_rail.get_connector("top")
        x2_mgn = x_mgn.place(pose={("mgr_top", x2_mgn_offset): x2_mgn_mount})
        parts.append(["x2_mgn", x2_mgn])

        return parts

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
    frame = Frame().place(pose={"origin": c1}, config={
        "Y": 100,
        "X1": 100,
        "X2": -100,
    })
    parts.append(frame)

    print(parts)

    for part in parts:
        for t, shape_list in part.shapes().values():
            for shape in shape_list:
                print(shape)
                c = display(t.transform(shape.shape.unlazy()), shape.color)

    show()

print("name:", __name__)
if __name__ == "__main__":
    main()
