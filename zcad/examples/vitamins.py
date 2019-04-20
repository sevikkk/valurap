from connectors import Connector, Demo, VisualConnector
from vitamins.belt import GT2x6BeltPU, GT2x6BeltStd, GT2x20Idler, GT2x20Pulley
from vitamins.mgn import MGN12H, MGR12
from vitamins.nema import Nema17
from vitamins.vslot import VSlot20x20, VSlot20x40
from zencad import Color, box, display, point3, show

base_long = VSlot20x40(1000)
base_short = VSlot20x40(500)
vc = VisualConnector()

parts = []

c1 = Connector([0, 0, 0], [1, 0, 0], [0, 0, 1])
vslot_demo = Demo(VSlot20x20(length=100)).place(pose={"top": c1})
parts.append(vslot_demo)

c1a = Connector([0, -100, 0], [1, 0, 0], [0, 0, 1])
vslot_demo = Demo(VSlot20x40(length=100)).place(pose={"top": c1a})
parts.append(vslot_demo)

c2 = Connector([0, 100, 0], [1, 0, 0], [0, 0, 1])
motor = Demo(Nema17()).place(pose={"top": c2})
parts.append(motor)

c3 = Connector([0, 200, 0], [1, 0, 0], [0, 0, 1])
rail = Demo(MGR12(400)).place(pose={"top": c3})
parts.append(rail)

carriage = Demo(MGN12H(), connectors=None).place(pose={("mgr_top", 150): c3})
parts.append(carriage)

c4 = Connector([0, 300, 0], [1, 0, 0], [0, 0, 1])
belt = Demo(GT2x6BeltPU(400)).place(pose={"start": c4})
parts.append(belt)

c4 = Connector([0, 310, 0], [1, 0, 0], [0, 0, 1])
belt = Demo(GT2x6BeltStd(400)).place(pose={"start": c4})
parts.append(belt)

c4 = Connector([0, 350, 0], [1, 0, 0], [0, 0, 1])
belt = Demo(GT2x20Pulley()).place(pose={"start": c4})
parts.append(belt)

c4 = Connector([0, 390, 0], [1, 0, 0], [0, 0, 1])
belt = Demo(GT2x20Idler()).place(pose={"start": c4})
parts.append(belt)

motor_bottom = Connector([100, 500, 0], [0, 0, -1], [0, 1, 0])
motor = Nema17().place(pose={"bottom": motor_bottom})
parts.append(motor)

first_pulley_bottom = motor.get_connector("top").forward(5).reverse()

pulley1 = GT2x20Pulley().place(pose={"bottom": first_pulley_bottom})
parts.append(pulley1)

belt = GT2x6BeltPU()

pose = belt.calculate_poses(pulley1, point3(200, 750, 0))
print(pose)

pulley2 = GT2x20Idler().place(pose={"origin": pose["p2_origin"]})
parts.append(pulley2)

pose2 = belt.calculate_poses(pulley2, point3(200, 300, 0))
print(pose2)

pulley3 = GT2x20Idler().place(pose={"origin": pose2["p2_origin"]})
parts.append(pulley3)

cw_belt = GT2x6BeltPU().place(
    pose={"start": pose["cw_belt_start"], "end": pose["cw_belt_end"]}
)
parts.append(cw_belt)

ccw_belt = GT2x6BeltPU().place(
    pose={"start": pose["ccw_belt_start"], "end": pose["ccw_belt_end"]}
)
parts.append(ccw_belt)

thrd_belt = GT2x6BeltPU().place(
    pose={"start": pose2["cw_belt_start"], "end": pose2["cw_belt_end"]}
)
parts.append(thrd_belt)

closing_belt = GT2x6BeltPU().place(
    pose={
        "start": pose["ccw_belt_start"].reverse(),
        "end": pose["cw_belt_start"].reverse().replace(use_for_solve=False),
        "pulley_origin": pulley1.get_connector("origin").replace(use_for_solve=False),
    }
)
parts.append(closing_belt)

cont_belt = GT2x6BeltPU().place(
    pose={
        "start": pose["cw_belt_end"].reverse(),
        "end": pose2["cw_belt_start"].reverse().replace(use_for_solve=False),
        "pulley_origin": pose["p2_origin"].replace(use_for_solve=False),
    }
)
parts.append(cont_belt)

for part in parts:
    for t, shape_list in part.shapes().values():
        for shape in shape_list:
            c = display(t.transform(shape.shape.unlazy()), shape.color)

show()
