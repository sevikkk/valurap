from valurap.thermocontrol import ThermoC
import time

tc = ThermoC()
#q = tc.S3G_QUERY()
#print(q)
#q = tc.S3G_SET_PID_TARGET(1, 500)
#print(q)
q = tc.S3G_SET_PID_PARAMS(3, 20000, 200)
print(q)

#targets = list(range(30, 255, 30)) + list(range(245,20,-30)) + list(range(30,260,10)) + list(range(240,20,-10))
targets = list(range(30, 130, 20)) + list(range(110,30,-20))
print(targets)
for target in targets:
    q = tc.S3G_SET_PID_TARGET(3, target)
    print(q)
    for i in range(300):
        q = tc.S3G_QUERY()
        print(q)
        open("tc.txt", "a").write("%d %d %d %d %d\n" % (time.time(), q.k_type, q.adc3, q.target3, q.ext3))
        time.sleep(1)
