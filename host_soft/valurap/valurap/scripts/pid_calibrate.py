from valurap.thermocontrol import ThermoC
import time

tc = ThermoC()
#q = tc.S3G_QUERY()
#print(q)
#q = tc.S3G_SET_PID_TARGET(1, 500)
#print(q)
q = tc.S3G_SET_PID_PARAMS(1, 20000, 200)
print(q)

targets = list(range(200, 255, 5)) + list(range(245,20,-5)) + list(range(30,260,10)) + list(range(240,20,-10))
print(targets)
for target in targets:
    q = tc.S3G_SET_PID_TARGET(1, target)
    print(q)
    for i in range(180):
        q = tc.S3G_QUERY()
        print(q)
        open("tc.txt", "a").write("%d %d %d %d %d\n" % (time.time(), q.k_type, q.adc1, q.target1, q.ext1))
        time.sleep(1)
