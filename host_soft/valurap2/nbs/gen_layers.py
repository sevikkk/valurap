import valurap2.path_planning as pp2
import sys

pp = pp2.PathPlanner()
pp.emu_in_loop = True

if 1:
    speed_k = 1.0
    pp.delta_e_err = 50
    pp.delta_ve_err = 20
    pp.max_ea = 10000
    pp.accel_step = 5000
else:
    speed_k = 10.0
    pp.delta_e_err = 100
    pp.delta_ve_err = 100
    pp.max_ea = 20000
    pp.accel_step = 5000

pp.gen_layers(sys.argv[1], speed_k=speed_k)
