from vitamins.vslot import VSlot20x20
from zencad import box, display, show, Color
from connectors import Connector

base_long = VSlot20x20(150)
base_short = VSlot20x20(500)

for (x,y) in [
    [ 1,  0],
    [ 1,  1],
    [ 0,  1],
    [-1,  1],
    [-1,  0],
    [-1, -1],
    [ 0, -1],
    [ 1, -1],
]:
    print("=============================================")
    top = [x,y,0]
    c1 = Connector([0, 0, 0], [0, 0, -1], top)

    a = base_long.inst(pose={"top, front": c1})
    a_m = a.model()
    display(a_m, Color(1, 0, 0))

    c2 = a.get_connector("bottom, front, left")
    new_pos = c2.position + c2.top * 10
    c3 = c2.replace(position=new_pos)

    b = base_short.inst(pose={"top": c3})
    b_m = b.model()
    display(b_m, Color(0, 1, 0))

    c4 = b.get_connector("bottom, left")
    new_pos = c4.position + c4.top * 10
    c5 = c4.replace(position=new_pos)

    c = base_short.inst(pose={"top": c5})
    c_m = c.model()
    display(c_m, Color(0, 0.5, 0))

display(box(200, 200, 1).translate(-100, -100, -1), Color(0.5, 0.5, 0.5))
show()