import valurap.path_planning2 as pp2
import sys

planner = pp2.PathPlanner()
planner.max_seg = 10.0
planner.min_seg = 0.1
planner.emu_in_loop = True
planner.delta_e_err = 80
planner.delta_ve_err = 80
planner.delta_err = 3
planner.skip_plato_len = 0.03
speed_k = 1.0
planner.max_xa = 3000
planner.max_ya = 3000
#planner.espeed_by_de = True

if 1:
    speed_k = 1.5
    planner.min_seg = 0.05
    planner.skip_plato_len = 0.01
    planner.delta_err = 5
    planner.delta_v_err = 5

if 0:
    speed_k = 1.5
    planner.max_xa = 3000
    planner.max_ya = 3000

if 0:
    speed_k = 2.0
    planner.max_xa = 3000
    planner.max_ya = 3000
    planner.max_ea = 3000
    planner.delta_err = 3
    planner.delta_v_err = 3
    planner.delta_e_err = 30
    planner.delta_ve_err = 10

planner.gen_layers(sys.argv[1], speed_k=speed_k)

