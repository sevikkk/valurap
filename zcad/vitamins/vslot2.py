from connectors import dot, norm
from zencad import *

corner = polygon(
    reversed(
        [
            [10, 10],
            [10, 9.55 / 2],
            [10 - 1.8, 6.2 / 2],
            [10 - 1.8, 11 / 2],
            [11 / 2, 11 / 2],
            [11 / 2, 10 - 1.8],
            [6.2 / 2, 10 - 1.8],
            [9.55 / 2, 10],
            [10, 10],
        ]
    )
).fillet(1.5, [[10, 10]])

corner = corner.fillet(
    0.2,
    [
        [11 / 2, 10 - 1.8],
        [10 - 1.8, 11 / 2],
        [10, 9.55 / 2],
        [10 - 1.8, 6.2 / 2],
        [6.2 / 2, 10 - 1.8],
        [9.55 / 2, 10],
    ],
)

s = square(a=7.3, center=True)
for a in range(4):
    s += corner.rotateZ(deg(a * 90))
    s -= circle(r=0.3).translate(0, 7.3 / 2, 0).rotateZ(deg(a * 90))

s += rectangle(1.8, 17 * 1.4, center=True).rotateZ(deg(45))
s += rectangle(1.8, 17 * 1.4, center=True).rotateZ(deg(-45))
s -= circle(r=2.1)

s = unify(s)

s2 = s + s.translate(20, 0, 0)
s2 += rectangle(6, 1.8).translate(10 - 3, 10 - 1.8, 0)
s2 += rectangle(6, 1.8).translate(10 - 3, -10, 0)
s2 -= rectangle(6.5, 20 - 2 * 1.8, center=True).translate(10, 0, 0).fillet(0.2)

s2 = unify(s2)

s3 = []
pv = None
ppv = None
z = 100
for v in s2.unlazy().faces():
    for vv in v.vertices():
        if pv and ppv:
            d1 = vv - pv
            d1 = d1 / norm(d1)
            d2 = pv - ppv
            d2 = d2 / norm(d2)
            print(vv - pv, ppv - pv, dot(d1, d2))
            print(vv.z)
            s3.append(sphere(r=0.5).translate(vv.x, vv.y, 0).up(z))
            z += 0.1
        ppv = pv
        pv = vv

ss = linear_extrude(s2, 50)

display(ss)
for v in s3:
    display(v)

show()
