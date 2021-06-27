import valurap2.path_planning as pp2
import sys

pp = pp2.PathPlanner()
pp.emu_in_loop = True
pp.set_mode("print")

if 1:
    speed_k = 1.0
    pp.delta_e_err = 10
    pp.delta_ve_err = 1000
    pp.max_ea = 10000
else:
    speed_k = 2.5
    pp.max_ea = 20000
    pp.max_xa = 3000
    pp.max_ya = 3000

pp.gen_layers(sys.argv[1], speed_k=speed_k)
