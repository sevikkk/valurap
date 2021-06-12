import time

from valurap2 import rest_client

c = rest_client.Client()

while True:
    try:
        c.abort()
    except Exception as e:
        print("connection Failed", e)
        time.sleep(1)
    else:
        break

tgt1 = 230
tgt2 = 230
tgt_hb = 110

c.spp(1, 60000, 0)
c.spp(2, 60000, 0)
c.sfv(ch=1, val=500)
c.sfv(ch=2, val=500)
c.sfv(ch=3, val=1000)
c.spt(ch=1, val=tgt1)
c.spt(ch=2, val=tgt2)
c.spt(ch=3, val=tgt_hb)

ok1 = 0
ok2 = 0
c.spt(ch=1, val=tgt1)
c.spt(ch=2, val=tgt2)

print("temps approach", tgt1, tgt2)
while True:
    r = c.thermo_state()
    if tgt1 > 0:
        if abs(r["temp1"] - tgt1) < 10 and r["ext1"] > 10 and r["ext1"] < 900:
            ok1 += 1
        else:
            ok1 = 0
    else:
        ok1 = 100

    if tgt2 > 0:
        if abs(r["temp2"] - tgt2) < 10 and r["ext2"] > 10 and r["ext2"] < 900:
            ok2 += 1
        else:
            ok2 = 0
    else:
        ok2 = 100

    print("{:4d} {:3d} {:2d} | {:4d} {:3d} {:2d} | {:4d} {:3d}".format(
        r["ext1"], r["temp1"], ok1,
        r["ext2"], r["temp2"], ok2,
        r["ext3"], r["temp3"]
    ))

    if ok1 > 6 and ok2 > 6:
        break

    time.sleep(5)

print("temps tracking", tgt1, tgt2)
c.spp(1, 28000, 400)
c.spp(2, 20000, 350)
ok1 = 0
ok2 = 0
while True:
    r = c.thermo_state()
    if tgt1 > 0:
        if abs(r["temp1"] - tgt1) < 3 and r["ext1"] > 10 and r["ext1"] < 900:
            ok1 += 1
        else:
            ok1 = 0
    else:
        ok1 = 100

    if tgt2 > 0:
        if abs(r["temp2"] - tgt2) < 3 and r["ext2"] > 10 and r["ext2"] < 900:
            ok2 += 1
        else:
            ok2 = 0
    else:
        ok2 = 100

    print("{:4d} {:3d} {:2d} | {:4d} {:3d} {:2d} | {:4d} {:3d}".format(
        r["ext1"], r["temp1"], ok1,
        r["ext2"], r["temp2"], ok2,
        r["ext3"], r["temp3"]
    ))

    if ok1 > 23 and ok2 > 23:
        break
    time.sleep(5)
print("temps ok")
print("prime extruders")

c.abort()
c.move(E1=-40, E2=-40)
r = c.wait_idle()
print("all done")

