from connectors import Connector, VisualConnector
from vitamins.vslot import VSlot20x20, VSlot20x40
from zencad import Color, box, display, show

base_long = VSlot20x20(150)
base_short = VSlot20x40(500)
vc = VisualConnector()

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

    c4 = b.get_connector("bottom, left2")
    new_pos = c4.position + c4.top * 10
    c5 = c4.replace(position=new_pos)

    c = base_short.place(pose={"top": c5})
    shapes.extend(c.shapes().values())

    for n in [
        "bottom, front",
        "bottom, back",
        "bottom, left",
        "bottom, right",
        "bottom, left2",
        "bottom, right2",
        "bottom",
        "bottom2",
    ]:
        vvc = vc.place({"origin": c.get_connector(n)}, config={"text": n})
        shapes.extend(vvc.shapes().values())


display(box(200, 200, 1).translate(-100, -100, -1), Color(0.5, 0.5, 0.5))

for t, shape_list in shapes:
    for shape in shape_list:
        c = display(t.transform(shape.shape.unlazy()), shape.color)

show()
