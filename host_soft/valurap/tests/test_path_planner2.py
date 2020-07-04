import os
from pprint import pprint

import numpy
import pytest
from numpy.testing import assert_array_equal, assert_allclose

from valurap.path_planning2 import PathPlanner
from valurap import gcode

from numpy import array, allclose

FIXTURES_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures")


@pytest.mark.parametrize(
    "name, expected_path, expected_array, expected_speeds",
    [
        (
            "simple.gcode",
            [
                [1.0, -40.0, 0, 0.0, 4],
                [4.0, -40.0, 50.0, -1.0, 5],
                [4.0, -44.0, 50.0, -2.33, 6],
                [4.0, -44.0, 0, -2.33, 6],
            ],
            [[3.0, 0.0, -1.0, 50.0], [0.0, -4.0, -1.33, 50.0], [0.0, 0.0, 0.0, 0.0],],
            [
                [50.0, 50.0, 50.0, 50.0, 0.0],
                [50.0, 50.0, 50.0, 0.0, -50.0],
                [0.0, 0.0, 0.0, 0.0, 0.0],
            ],
        )
    ],
)
def test_gcode_read(name, expected_path, expected_array, expected_speeds):
    lines = gcode.reader(os.path.join(FIXTURES_PATH, name))
    pg = gcode.path_gen(lines)
    sg = gcode.gen_segments(pg)
    for i, s in enumerate(sg):
        if isinstance(s, gcode.do_move):
            print(i, s)
        elif isinstance(s, gcode.do_ext):
            print(i, s)
        elif isinstance(s, gcode.do_home):
            print(i, s)
        elif isinstance(s, gcode.do_segment):
            print("segment", i, len(s.path))
        else:
            assert False

    assert s.path == expected_path
    planner = PathPlanner()
    path, slowdowns = planner.make_path(s.path, 1.0)
    assert_allclose(path[["dx", "dy", "de", "v"]].to_numpy(), array(expected_array))

    speeds = planner.gen_speeds(path, slowdowns)
    assert_allclose(
        speeds[["entry", "exit", "plato", "plato_x", "plato_y"]].to_numpy(), array(expected_speeds)
    )


def test_slowdowns():
    gcode_path = [
        [1.0, -40.0, 0, 0.0, 4],
        [4.0, -40.0, 50.0, -1.0, 5],
        [4.0, -43.0, 50.0, -2.0, 6],
        [7.0, -43.0, 70.0, -3.0, 7],
        [7.0, -43.0, 0, -3.0, 7],
    ]
    expected_unscaled_speeds = [
        [50.0, 50.0, 50.0, 50.0, 0.0],
        [50.0, 50.0, 50.0, 0.0, -50.0],
        [70.0, 70.0, 70.0, 70.0, 0.0],
        [0.0, 0.0, 0.0, 0.0, 0.0],
    ]

    expected_scaled_speeds = [
        [20.0, 50.0, 50.0, 50.0, 0.0],  # corner = 0.4
        [50.0, 25.0, 40.0, 0.0, -40.0],  # plato = 0.6
        [35.0, 42.0, 70.0, 70.0, 0.0],  # corner = 0.5
        [0.0, 0.0, 0.0, 0.0, 0.0],  # corner = 0.6 -> exit[--] = 42
    ]

    planner = PathPlanner()
    path, slowdowns = planner.make_path(gcode_path, 1.0)
    speeds = planner.gen_speeds(path, slowdowns)

    unscaled_speeds = speeds[["entry", "exit", "plato", "plato_x", "plato_y"]].to_numpy()
    print(unscaled_speeds)
    assert_allclose(unscaled_speeds, array(expected_unscaled_speeds))
    slowdowns["corner"][0] = 0.4
    slowdowns["plato"][1] = 0.6
    slowdowns["corner"][2] = 0.5
    slowdowns["corner"][3] = 0.6

    speeds = planner.gen_speeds(path, slowdowns)
    scaled_speeds = speeds[["entry", "exit", "plato", "plato_x", "plato_y"]].to_numpy()
    print(scaled_speeds)
    assert_allclose(scaled_speeds, array(expected_scaled_speeds))


@pytest.mark.parametrize(
    "comment, gcode_path, expected_slowdown",
    [
        (
            "simple case",
            [
                [1.0, -40.0, 0, 0.0, 4],
                [4.0, -40.0, 50.0, -1.0, 5],
                [4.0, -43.0, 50.0, -2.0, 6],
                [7.0, -43.0, 70.0, -3.0, 7],
                [7.0, -43.0, 0, -3.0, 7],
            ],
            [],
        )
    ],
)
def test_corners(comment, gcode_path, expected_slowdown):
    planner = PathPlanner()
    planner.max_delta = 100
    path, slowdowns = planner.make_path(gcode_path, 1.0)
    new_slowdowns, updated, cc = planner.process_corner_errors(path, slowdowns)

    assert_no_nans(cc)
    assert_no_nans(new_slowdowns)

    second_slowdowns, updated, cc = planner.process_corner_errors(path, new_slowdowns)

    assert updated == 0

    assert_no_nans(cc)
    assert_no_nans(second_slowdowns)

    speeds = planner.gen_speeds(path, new_slowdowns)

    print(
        cc[
            [
                "dvx",
                "dvy",
                "dt",
                "mdx",
                "mdy",
                "error_slowdown",
                "entry_slowdown",
                "prev_exit_slowdown",
            ]
        ]
    )
    path_dict = path.iloc[0].to_dict()
    last_x = path_dict["px"]
    last_y = path_dict["py"]
    last_vx = 0
    last_vy = 0
    for i in range(len(cc["dt"]) - 1):
        print("--------", i, "--------")
        path_dict = path.iloc[i].to_dict()
        cc_dict = cc.iloc[i].to_dict()
        next_cc_dict = cc.iloc[i + 1].to_dict()
        speeds_dict = speeds.iloc[i].to_dict()
        pprint(path_dict)
        pprint(cc_dict)
        pprint(speeds_dict)
        next_vx = last_vx + cc_dict["entry_ax"] * cc_dict["entry_dt"]
        next_vy = last_vy + cc_dict["entry_ay"] * cc_dict["entry_dt"]
        next_x = last_x + cc_dict["entry_dt"] * (last_vx + next_vx) / 2
        next_y = last_y + cc_dict["entry_dt"] * (last_vy + next_vy) / 2
        numpy.testing.assert_allclose(
            [next_vx, next_vy, next_x, next_y,],
            [
                speeds_dict["entry_x"],
                speeds_dict["entry_y"],
                path_dict["px"] + speeds_dict["unit_x"] * cc_dict["l_entry"],
                path_dict["py"] + speeds_dict["unit_y"] * cc_dict["l_entry"],
            ],
        )

        last_x = path_dict["x"] - speeds_dict["unit_x"] * cc_dict["l_exit"]
        last_y = path_dict["y"] - speeds_dict["unit_y"] * cc_dict["l_exit"]
        last_vx = speeds_dict["exit_x"]
        last_vy = speeds_dict["exit_y"]

        next_vx = last_vx + cc_dict["exit_ax"] * cc_dict["exit_dt"]
        next_vy = last_vy + cc_dict["exit_ay"] * cc_dict["exit_dt"]
        next_x = last_x + cc_dict["exit_dt"] * (last_vx + next_vx) / 2
        next_y = last_y + cc_dict["exit_dt"] * (last_vy + next_vy) / 2

        numpy.testing.assert_allclose(
            [next_vx, next_vy, next_x, next_y,],
            [
                next_cc_dict["mvx"],
                next_cc_dict["mvy"],
                path_dict["x"] + next_cc_dict["mdx"],
                path_dict["y"] + next_cc_dict["mdy"],
            ],
        )

        last_x = next_x
        last_y = next_y
        last_vx = next_vx
        last_vy = next_vy

    numpy.testing.assert_allclose(
        [next_vx, next_vy, next_x, next_y,], [0, 0, path_dict["x"], path_dict["y"],]
    )


def assert_no_nans(df):
    for k, v in df.items():
        ok = numpy.isfinite(v.to_numpy()).all()
        if not ok:
            print(k)
            print(v)
            assert False
