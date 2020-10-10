import time

from valurap import rest_client

c = rest_client.Client()

print("heaters off")
c.sfv(ch=1, val=1000)
c.sfv(ch=2, val=1000)
c.sfv(ch=3, val=1000)
c.spt(ch=1, val=0)
c.spt(ch=2, val=0)
c.spt(ch=3, val=0)

print("home")
c.abort()
c.home()
c.wait_idle()

print("disarm")
c.abort()

print("wait for low temps")
while True:
    r = c.thermo_state()
    temp1 = r["temp1"]
    temp2 = r["temp2"]
    print(temp1, temp2)
    if temp1 < 50 and temp2 < 50:
        break

    time.sleep(20)

print("fans off")
c.sfv(ch=1, val=0)
c.sfv(ch=2, val=0)
c.sfv(ch=3, val=0)

print("done")