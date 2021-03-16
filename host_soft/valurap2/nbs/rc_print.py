import os.path
import pickle
from valurap2.profile import ProfileSegment
from valurap2 import emulate
from valurap2 import rest_client
from valurap2 import buf_commands
import time
import sys

e1_x_offset = 0.0
e1_y_offset = 0.0
e1_z_offset = 9.3   #+ 20

e2_x_offset = 7.29 - 0.8 - 1
e2_y_offset = 122.6 - 0.2
e2_z_offset = 12.46 #+ 20

x1_parking = -190
x2_parking = 170
y_parking = -200

#base_fn = "box20"
base_fn = sys.argv[1].replace(".gcode", "")

rc = rest_client.Client()
rc.home()
rc.wait_idle()
rc.move(E1=-30, E2=-30)
rc.wait_idle()
rc.moveto(X1=x1_parking, X2=x2_parking, mode="print,e1,e2")
rc.wait_idle()
rc.moveto(Y=0, mode="print,e1,e2")
rc.wait_idle()
#rc.moveto(Z=9.60, mode="print,e1,e2")
#rc.wait_idle()
    
def send_segment(segment, accel_step, rc):
    #print(tupled_segment)
    pr_opt = []
    for dt, segs in segment:
        pr_opt.append([
            dt, [ProfileSegment.from_tuple(s) for s in segs]
        ])
        
    cb = buf_commands.CommandBuffer(debug=False)
    cb.add_segments_head(accel_step=accel_step)
    cb.add_segments(pr_opt)
    cb.add_segments_tail()
    state = rc.state()
    while state["buf_len"] > 1000000:
        time.sleep(1)
        state = rc.state()
        #print(state)
    
    rc.exec_binary(cb.buffer)


layer = 1
current_extruder = "E1"

target_z = 0

while True:
    fn = "{}_{:05d}.layer".format(base_fn, layer)
    if not os.path.exists(fn):
        break
    print(fn)
    data = pickle.load(open(fn, "rb"))
    for d in data:
        if d[0] == "segment":
            print(d[0], len(d), len(d[1]), len(d[2]), d[1])
            for p in d[2][:5]:
                print("   ", p)
            tupled_segment = d[2]
            if "accel_step" not in d[1]:
                d[1]["accel_step"] = d[1]["acc_step"]
            send_segment(tupled_segment, d[1]["accel_step"], rc)
        elif d[0] == "start":
            print("   ", d)
            code = d[5]
            target = d[1]
            target_z = target["Z"]
            if code:
                print("code", list(code.keys()), len(code["segment"]), code["segment"][:5])
                send_segment(code["segment"], code["accel_step"], rc)
            else:
                print("no code, target", target)
                state = rc.state()
                while not state["idle"]:
                    time.sleep(1)
                    state = rc.state()
                    #print(state)
                if current_extruder == "E1":
                    rc.moveto(X1=target["X"] + e1_x_offset, Y=target["Y"] + e1_y_offset, mode="print,e1,e2")
                    rc.wait_idle()
                    rc.moveto(Z=target["Z"] + e1_z_offset, mode="print,e1,e2")
                    rc.wait_idle()
                else:
                    rc.moveto(X2=target["X"] + e2_x_offset, Y=target["Y"] + e2_y_offset, mode="print,e1,e2")
                    rc.wait_idle()
                    rc.moveto(Z=target["Z"]  + e2_z_offset, mode="print,e1,e2")
                    rc.wait_idle()
        elif d[0] == "end_state":
            print("   ", d)
        elif d[0] == "do_home":
            print("   ", d)
        elif d[0] == "extruder_switch":
            new_extruder = "E{}".format(d[1] + 1)
            if current_extruder != new_extruder:
                state = rc.state()
                while not state["idle"]:
                    time.sleep(0.1)
                    state = rc.state()
                    #print(state)
                rc.move(Z=7, mode="print,e1,e2")
                rc.wait_idle()
                if current_extruder == "E1":
                    rc.moveto(X1=x1_parking, mode="print,e1,e2")
                    rc.wait_idle()
                else:
                    rc.moveto(X2=x2_parking, mode="print,e1,e2")
                    rc.wait_idle()
            current_extruder = new_extruder
        else:
            print(d[0], len(d))
    layer += 1
    if target_z > 300.0:
        break

state = rc.state()
while not state["idle"]:
    time.sleep(10)
    state = rc.state()
    print(state)
        
rc.wait_idle()
rc.move(Z=50)
rc.wait_idle()
rc.moveto(X1=x1_parking, X2=x2_parking, mode="print,e1,e2")
rc.wait_idle()
rc.moveto(Y=y_parking, mode="print,e1,e2")
rc.wait_idle()
    
print("done")
