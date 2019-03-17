import traceback

from vitamins.vslot import VSlot20x20, VSlot20x40
from zencad import box, display, show, Color, deg
from connectors import Solver, Connector
import numpy as np
import numpy.linalg as la

base_long = VSlot20x20(1000)
base_short = VSlot20x20(500)
c1 = base_long.get_connector('top, front')
c2 = base_short.get_connector('top')

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
    top = np.array([x,y,0])
    top = top / la.norm(top)
    p1 = Connector([0,0,0], [0, 0, -1], top)
    s = Solver([c1], [p1]).solve()

    a = base_long.inst(s)
    a_m = a.model()
    display(a_m, Color(1, 0, 0))

    p2 = a.get_connector("bottom, front, left")
    new_pos = p2.position + p2.top * 10
    p3 = Connector(new_pos, p2.direction, p2.top)
    s = Solver([c2], [p3]).solve()
    b = base_short.inst(s)
    b_m = b.model()
    display(b_m, Color(0, 1, 0))

    p4 = b.get_connector("bottom, left")
    new_pos = p4.position + p4.top * 10
    p5 = Connector(new_pos, p4.direction, p4.top)
    s = Solver([c2], [p5]).solve()
    c = base_short.inst(s)
    c_m = c.model()
    display(c_m, Color(0, 0.5, 0))

display(box(200, 200, 1).translate(-100, -100, -1), Color(0.5, 0.5, 0.5))
show()