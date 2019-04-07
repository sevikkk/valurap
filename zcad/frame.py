from connectors import Connector, Demo, VisualConnector
from vitamins.mgn import MGR12
from vitamins.nema import Nema17
from vitamins.vslot import VSlot20x20, VSlot20x40
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


for part in parts:
    for t, shape_list in part.shapes().values():
        for shape in shape_list:
            c = display(t.transform(shape.shape.unlazy()), shape.color)

show()
