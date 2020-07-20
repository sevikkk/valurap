import valurap.path_planning2 as pp2
import sys

planner = pp2.PathPlanner()
planner.max_seg = 10.0
planner.emu_in_loop = True
planner.delta_e_err = 10
planner.delta_err = 3

planner.gen_layers(sys.argv[1])

