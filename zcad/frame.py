from connectors import Connector, VisualConnector, Demo
from vitamins.vslot import VSlot20x20, VSlot20x40
from vitamins.nema import Nema17
from zencad import Color, box, display, show

base_long = VSlot20x40(1000)
base_short = VSlot20x40(500)
vc = VisualConnector()

parts = []

c1 = Connector([0,0,0], [1,0,0], [0,0,1])
vslot_demo = Demo(VSlot20x20(length=100)).place(pose={"origin": c1})
parts.append(vslot_demo)

c1a = Connector([0, -100,0], [1,0,0], [0,0,1])
vslot_demo = Demo(VSlot20x40(length=100)).place(pose={"origin": c1a})
parts.append(vslot_demo)

c2 = Connector([0, 100,0], [1,0,0], [0,0,1])
motor = Demo(Nema17()).place(pose={"origin": c2})
parts.append(motor)

#display(box(200, 200, 1).translate(-100, -100, -1), Color(0.5, 0.5, 0.5))

for part in parts:
    for t, shape_list in part.shapes().values():
        for shape in shape_list:
            c = display(t.transform(shape.shape.unlazy()), shape.color)

show()
