import valurap.printer as vp
import valurap.asg as vas
import valurap.commands as vac
from valurap import path_planning2, emulate
import pickle
from collections import deque

prn = vp.Valurap()
prn.setup()
prn.axe_e1.max_v=20000*22
prn.axe_e2.max_v=20000*3

e1_enable = True
e2_enable = False

apgs = {
    "X": prn.apg_x,
    "Y": prn.apg_y,
    "Z": prn.apg_z,
}

codes = []

base = "tg_body_1.5/tg_body"
def load_layer(layer):
    with open("{}_{:05d}.layer".format(base, layer), "rb") as f:
        return pickle.load(f)

p = load_layer(1)
print(p[1][1])
acc_step = p[1][1]["acc_step"]

pp = path_planning2.PathPlanner()
pp.acc_step = acc_step
pp.init_coefs()

up_segs = pp.ext_to_code(0.3, 100, axe="Z")
up_code = prn.asg.gen_path_code(up_segs, accel_step=pp.accel_step, real_apgs=apgs)

for axe in prn.axes.values():
    axe.apg = None
    axe.enabled = False

prn.axe_z.enabled = True
prn.axe_y.enabled = True
prn.axe_x1.enabled = True
prn.axe_x2.enabled = True
prn.axe_e1.enabled = e1_enable
prn.axe_e2.enabled = e2_enable
prn.update_axes_config()

start = None
apg_map = None

for layer in range(1, 3):
    p = load_layer(layer)

    if len(p) == 2 and p[0][0] == "do_home":
        break
        
    print(len(p))
    for pp in p:
        print(pp[0])
        
    assert len(p) == 3
    assert p[0][0] == "start"
    assert p[1][0] == "segment"
    assert p[2][0] == "end_state"
    if start is None:
        start = p[0]

    pr_opt = [
        [1, [
            vas.ProfileSegment(apgs["X"], x=p[0][1]["X"] * pp.spm),
            vas.ProfileSegment(apgs["Y"], x=p[0][1]["Y"] * pp.spm),
            vas.ProfileSegment(apgs["Z"], x=0),
        ]]
    ]
    cms, meta, segments = p[1]
    if apg_map is None:
        apg_map = meta["map"]
        
    codes.append(prn.asg.gen_map_code(meta["map"]))
    for dt, segs in segments:
        pr_opt.append([
            dt, [vas.ProfileSegment.from_tuple(s, apgs) for s in segs]
        ])

    acc_step = 10000
    path_code = prn.asg.gen_path_code(pr_opt, accel_step=pp.accel_step, real_apgs={"X": prn.apg_x, "Y": prn.apg_y, "Z": prn.apg_z})
    print(layer, len(path_code))
    codes.append(path_code)
    codes.append(prn.asg.gen_map_code({"Z": "Z"}))
    codes.append(up_code)

prn.update_axes_config()
fullcode = deque()
for code in codes:
    fullcode.extend(code[:-1])

codes = []

fullcode.extend(code[-1:])

print(len(fullcode))

prn.setup()

for axe in prn.axes.values():
    axe.apg = None
    axe.enabled = False
    
prn.update_axes_config()
prn.home()

prn.update_axes_positions()

prn.axe_x1.enabled = True
prn.axe_x2.enabled = True
prn.axe_y.enabled = True
prn.axe_z.enabled = True
prn.axe_e1.enabled = e1_enable
prn.axe_e2.enabled = e2_enable
prn.update_axes_config()

if e1_enable:
    prn.move(E1=-50 * pp.spme)

if e2_enable:
    prn.move(E2=-20 * pp.spme)

#prn.move(E1=-20000)
prn.moveto(X1=0)
prn.moveto(Y=0)
#prn.moveto(X2=0)
prn.moveto(Y=start[1]["Y"] * pp.spm, X1=start[1]["X"] * pp.spm)
prn.moveto(Z=5040)
#prn.moveto(Z=5040-1600*1.5) # clear glass
#prn.moveto(Z=5040-1600*(0.6-0.3))
prn.moveto(Z=5040-pp.spmz*(0.6-0.5))

for k, v in apg_map.items():
    prn.axes[k].apg = prn.apgs[v]
    
#print(start[2])
#prn.moveto(X1=start[1]["X"] * 80, Y=start[1]["Y"] * 80)

try:
    prn.exec_long_code(fullcode, splits=1000, verbose=True)
    
    for axe in prn.axes.values():
        axe.apg = None
        axe.enabled = False
    
    prn.update_axes_config()
    prn.home()
    prn.setup()
except:
    prn.setup()
    

