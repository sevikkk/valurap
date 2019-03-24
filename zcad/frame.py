from vitamins.vslot import VSlot20x20
from zencad import box, display, show, Color
from connectors import Connector

base_long = VSlot20x20(150)
base_short = VSlot20x20(500)

shapes = []

for (x, y) in [[1, 0], [1, 1], [0, 1], [-1, 1], [-1, 0], [-1, -1], [0, -1], [1, -1]]:
    print("=============================================")
    top = [x, y, 0]
    c1 = Connector([0, 0, 0], [0, 0, -1], top)

    a = base_long.place(pose={"top, front": c1})
    shapes.extend(a.shapes().values())

    c2 = a.get_connector("bottom, front, left")
    new_pos = c2.position + c2.top * 10
    c3 = c2.replace(position=new_pos)

    b = base_short.place(pose={"top": c3}, config={"color": Color(0.1, 0.5, 0)})
    shapes.extend(b.shapes().values())

    c4 = b.get_connector("bottom, left")
    new_pos = c4.position + c4.top * 10
    c5 = c4.replace(position=new_pos)

    c = base_short.place(pose={"top": c5})
    shapes.extend(c.shapes().values())


display(box(200, 200, 1).translate(-100, -100, -1), Color(0.5, 0.5, 0.5))

for t, shape_list in shapes:
    for shape in shape_list:
        c = display(t.transform(shape.shape.unlazy()), shape.color)

show()
