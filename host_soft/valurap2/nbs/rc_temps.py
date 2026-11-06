import time

from valurap2 import rest_client

c = rest_client.Client()

while True:
    try:
        c.thermo_state()
    except Exception as e:
        print("connection Failed", e)
        time.sleep(1)
    else:
        break

c.spt(ch=1, val=227)
c.spt(ch=2, val=227)
c.spt(ch=3, val=130)

while True:
    r = c.thermo_state()

    print("{:4d} {:3d} | {:4d} {:3d} | {:4d} {:3d}".format(
        r["ext1"], r["temp1"],
        r["ext2"], r["temp2"],
        r["ext3"], r["temp3"]
    ))

    time.sleep(5)

