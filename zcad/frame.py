from connectors import Connector, Demo, VisualConnector
from vitamins.mgn import MGN12H, MGR12
from vitamins.nema import Nema17
from vitamins.vslot import VSlot20x20, VSlot20x40
from vitamins.belt import GT2x6BeltPU, GT2x6BeltStd, GT2x20Pulley, GT2x20Idler
from zencad import Color, box, display, show

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

for part in parts:
    for t, shape_list in part.shapes().values():
        for shape in shape_list:
            c = display(t.transform(shape.shape.unlazy()), shape.color)

show()
