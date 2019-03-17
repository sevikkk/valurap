from vitamins.vslot import VSlot20x20, VSlot20x40
from zencad import display, show, Color, deg

a = VSlot20x20(500).inst().left(100)
b = VSlot20x20(500).inst().right(100)
c = VSlot20x20(180).inst().rotateY(deg(90)).left(0)
d = VSlot20x40(100).inst().down(100)

display(a, Color(1, 0, 0))
display(b, Color(0.5, 0.5, 0))
display(c, Color(0.5, 0.1, 0))
display(d, Color(0.5, 0.5, 0.5))
show()
