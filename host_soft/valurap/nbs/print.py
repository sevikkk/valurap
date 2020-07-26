import valurap.printer as vp
import valurap.asg as vas
import valurap.commands as vac
from valurap import path_planning, emulate
import pickle

prn = vp.Valurap()
prn.setup()
prn.axe_e2.max_v=20000*3
prn.axe_e1.max_v=20000*22

spm = 80
spme = 847
acc_step = 10000

apgs = {
    "X": prn.apg_x,
    "Y": prn.apg_y,
    "Z": prn.apg_z,
}

codes = []

up_segs = path_planning.ext_to_code(0.3, 100, spm=1600, max_a=1000)
up_code = prn.asg.gen_path_code(up_segs, accel_step=int(50000000/acc_step), real_apgs=apgs)

for axe in prn.axes.values():
    axe.apg = None
    axe.enabled = False

prn.axe_z.enabled = True
prn.axe_y.enabled = True
prn.axe_x1.enabled = True
prn.axe_e1.enabled = True
prn.axe_e2.enabled = False
prn.update_axes_config()

start = None
apg_map = None
base = "tg_body_1.5/tg_body"

for layer in range(1, 1000):
    with open("{}_{:05d}.layer".format(base, layer), "rb") as f:
        p = pickle.load(f)

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
            vas.ProfileSegment(apgs["X"], x=p[0][1]["X"] * spm),
            vas.ProfileSegment(apgs["Y"], x=p[0][1]["Y"] * spm),
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
    path_code = prn.asg.gen_path_code(pr_opt, accel_step=int(50000000/acc_step), real_apgs={"X": prn.apg_x, "Y": prn.apg_y, "Z": prn.apg_z})
    print(len(path_code))
    codes.append(path_code)
    codes.append(prn.asg.gen_map_code({"Z": "Z"}))
    codes.append(up_code)

prn.update_axes_config()
fullcode = []
for code in codes:
    fullcode.extend(code[:-1])
fullcode.extend(code[-1:])

print(len(fullcode))

prn.setup()

for axe in prn.axes.values():
    axe.apg = None
    axe.enabled = False
    
prn.update_axes_config()
prn.home()

prn.update_axes_positions()

prn.axe_e1.enabled = True
prn.axe_x1.enabled = True
prn.axe_y.enabled = True
prn.axe_z.enabled = True
prn.axe_e1.enabled = True
prn.axe_e2.enabled = False
prn.update_axes_config()

prn.move(E1=-100000)
#prn.move(E1=-20000)
prn.moveto(X1=0)
prn.moveto(Y=0)
#prn.moveto(X2=0)
prn.moveto(Y=start[1]["Y"] * 80, X1=start[1]["X"] * 80)
prn.moveto(Z=5040)
#prn.moveto(Z=5040-1600*1.5) # clear glass
#prn.moveto(Z=5040-1600*(0.6-0.3))
prn.moveto(Z=5040-1600*(0.6-0.5))

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
    

