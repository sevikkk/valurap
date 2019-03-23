from zencad import *

corner = polygon([
    [10, 10],
    [10, 9.55/2],
    [10 - 1.8, 6.2/2],
    [10-1.8, 11/2],
    [11/2, 11/2],
    [11/2, 10 - 1.8],
    [6.2/2, 10 - 1.8],
    [9.55/2, 10],
    [10, 10],
]).fillet(1.5, [[10,10]])

corner = corner.fillet(0.2, [
    [11/2, 10 - 1.8],
    [10 - 1.8, 11/2],
    [10, 9.55 / 2],
    [10 - 1.8, 6.2 / 2],
    [6.2 / 2, 10 - 1.8],
    [9.55 / 2, 10],
])

s = square(a=7.3, center=True)
for a in range(4):
    s += corner.rotateZ(deg(a*90))
    s -= circle(r=0.3).translate(0, 7.3/2, 0).rotateZ(deg(a*90))

s += rectangle(1.8, 17*1.4, center=True).rotateZ(deg(45))
s += rectangle(1.8, 17*1.4, center=True).rotateZ(deg(-45))
s -= circle(r=2.1)

s2 = s + s.translate(20,0,0)
s2 += rectangle(6, 1.8).translate(10-3, 10-1.8, 0)
s2 += rectangle(6, 1.8).translate(10-3, -10, 0)
s2 -= rectangle(6.5, 20-2*1.8, center=True).translate(10,0, 0)
if 1:
    s2 = s2.fillet(0.01, [
        [10 - 6.5/2, 10 - 1.8],
        #[10+6.5/2, 10 - 1.8],
        #[10 + 6.5/2, -10 + 1.8],
        #[10 - 6.5/2, -10 + 1.8],
    ])

for v in s2.unlazy().vertices():
    print( v - point3(10 - 6.5/2, 10 - 1.8,0))

ss = linear_extrude(s2, 50)

display(ss)

show()
