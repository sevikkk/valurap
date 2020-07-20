import os
from math import hypot
from pprint import pprint

import numpy
import pytest
from numpy.testing import assert_array_equal, assert_allclose

from valurap.path_planning2 import PathPlanner
from valurap import gcode

from numpy import array, allclose

FIXTURES_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures")
NBS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "nbs")


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


SIMPLE_PATH = [
    [1.0, -40.0, 0, 0.0, 4],
    [4.0, -40.0, 50.0, -1.0, 5],
    [4.0, -43.0, 50.0, -2.0, 6],
    [7.0, -43.0, 70.0, -3.0, 7],
    [7.0, -43.0, 0, -3.0, 7],
]

SIMPLE_PATH_SHORT_SEGMENT = [
    [1.0, -40.0, 0, 0.0, 4],
    [2.0, -40.0, 50.0, -1.0, 5],
    [2.0, -41.0, 50.0, -2.0, 6],
    [2.5, -41.0, 70.0, -3.0, 7],
    [2.5, -41.0, 0, -3.0, 7],
]


def test_slowdowns():
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
    path, slowdowns = planner.make_path(SIMPLE_PATH, 1.0)
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
    "comment, gcode_path, max_delta, expected_slowdown",
    [
        ("simple case with no corner limit", SIMPLE_PATH, 100, []),
        ("simple case with corner limit", SIMPLE_PATH, 0.2, []),
    ],
)
def test_corners(comment, gcode_path, max_delta, expected_slowdown):
    planner = PathPlanner()
    planner.max_delta = max_delta
    path, slowdowns = planner.make_path(gcode_path, 1.0)
    new_slowdowns, updated, cc = planner.process_corner_errors(path, slowdowns)

    assert_no_nans(cc)
    assert_no_nans(new_slowdowns)
    print(new_slowdowns)

    second_slowdowns, updated, cc = planner.process_corner_errors(path, new_slowdowns)

    assert updated == 0

    assert_no_nans(cc)
    assert_no_nans(second_slowdowns)

    speeds = planner.gen_speeds(path, new_slowdowns)

    validate_cc_solution(cc, path, speeds)


def validate_cc_solution(cc, path, speeds, check_plato=False):
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

        if check_plato:
            plato_in_speed = hypot(next_vx, next_vy)
            plato_exit_speed = hypot(last_vx, last_vy)
            plato_len = hypot(last_x - next_x, last_y - next_y)
            max_a = speeds_dict["max_a"] * 1.1
            plato_dt = abs(plato_in_speed - plato_exit_speed) / max_a
            plato_acc_len = (plato_in_speed + plato_exit_speed) * plato_dt / 2
            assert plato_acc_len <= plato_len

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
            atol=1e-5
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


@pytest.mark.parametrize(
    "comment, gcode_path, max_delta, expected_slowdown, expected_to_fail_on_reverse",
    [
        ("simple case with no corner limit", SIMPLE_PATH, 100, [], False),
        ("simple case with corner limit", SIMPLE_PATH, 0.2, [], False),
        ("short segment with corner limit", SIMPLE_PATH_SHORT_SEGMENT, 0.2, [], False),
        (
            "alternating segments",
            [
                [0, 0, 0, 0, 1],
                [1, 0, 100, 0, 2],
                [2, 0, 50, 0, 3],
                [3, 0, 150, 0, 4],
                [4, 0, 10, 0, 5],
                [5, 0, 100, 0, 6],
                [5, 0, 0, 0, 6],
            ],
            0.2,
            [],
            True,
        ),
    ],
)
def test_reverse_path(
    comment, gcode_path, max_delta, expected_slowdown, expected_to_fail_on_reverse
):
    planner = PathPlanner()
    planner.max_delta = max_delta
    path, slowdowns = planner.make_path(gcode_path, 1.0)
    corner_slowdowns, updated, cc = planner.process_corner_errors(path, slowdowns)

    assert_no_nans(cc)
    assert_no_nans(corner_slowdowns)

    check_slowdowns, updated, cc = planner.process_corner_errors(path, corner_slowdowns)
    assert updated == 0

    assert_no_nans(cc)
    assert_no_nans(check_slowdowns)

    reverse_slowdowns, updated = planner.reverse_pass(path, corner_slowdowns)
    assert_no_nans(reverse_slowdowns)
    print(reverse_slowdowns)

    speeds = planner.gen_speeds(path, reverse_slowdowns)
    _, updated, cc = planner.process_corner_errors(path, reverse_slowdowns)
    # print(cc[["error_slowdown", "entry_slowdown", "prev_exit_slowdown"]])
    assert updated == 0

    if expected_to_fail_on_reverse:
        with pytest.raises(AssertionError):
            validate_cc_solution(cc, path, speeds, check_plato=True)
    else:
        validate_cc_solution(cc, path, speeds, check_plato=True)

    forward_slowdowns, updated = planner.forward_pass(path, reverse_slowdowns)
    assert_no_nans(forward_slowdowns)
    print(forward_slowdowns)

    speeds = planner.gen_speeds(path, forward_slowdowns)
    _, updated, cc = planner.process_corner_errors(path, forward_slowdowns)
    # print(cc[["error_slowdown", "entry_slowdown", "prev_exit_slowdown"]])
    assert updated == 0

    validate_cc_solution(cc, path, speeds, check_plato=True)

    _segments, profile = planner.gen_segments_float(path, forward_slowdowns)
    print(profile)


@pytest.mark.parametrize(
    "comment, gcode_folder, gcode_path, max_delta, max_delta_e, speed_k, segment_number, expected_len, emu_in_loop",
    [
        ("test22", NBS_PATH, "test22.gcode", 0.2, None, 1.0, 15, 484, True),
        ("test22", NBS_PATH, "test22.gcode", 0.2, None, 10.0, 15, 484, True), # needs better source filtering
        ("test22", NBS_PATH, "test22.gcode", 0.05, None, 1.0, 15, 484, True),
        ("test4", NBS_PATH, "test4.gcode", 0.2, None, 1.0, 13, 1018, True),
        ("test4", NBS_PATH, "test4.gcode", 0.05, 0.4, 1.0, 13, 1018, True),
        ("test4", NBS_PATH, "test4.gcode", 0.1, None, 10.0, 13, 1018, True),
        ("test4", NBS_PATH, "test4.gcode", 0.05, None, 10.0, 23, 1024, True),
        ("test4", NBS_PATH, "test4.gcode", 0.5, None, 20.0, 23, 1024, True),
    ],
)
def test_real_files(
        comment, gcode_folder, gcode_path, max_delta, max_delta_e, speed_k, segment_number, expected_len, emu_in_loop
):
    lines = gcode.reader(os.path.join(gcode_folder, gcode_path))
    pg = gcode.path_gen(lines)
    sg = gcode.gen_segments(pg)

    s_n = 1

    for s in sg:
        if isinstance(s, gcode.do_move):
            pass
        elif isinstance(s, gcode.do_ext):
            pass
        elif isinstance(s, gcode.do_home):
            pass
        elif isinstance(s, gcode.do_segment):
            print("segment", s_n, len(s.path))
            if s_n == segment_number:
                break
            s_n += 1
        else:
            assert (False)

    assert len(s.path) == expected_len


    planner = PathPlanner()
    planner.max_delta = max_delta
    if max_delta_e:
        planner.max_delta_e = max_delta_e
    planner.emu_in_loop = emu_in_loop
    planner.max_ea *= speed_k
    planner.delta_e_err *= speed_k * speed_k
    planner.delta_ve_err *= speed_k
    path, slowdowns = planner.make_path(s.path, speed_k)
    corner_slowdowns, updated, cc = planner.process_corner_errors(path, slowdowns)

    assert_no_nans(cc)
    assert_no_nans(corner_slowdowns)

    check_slowdowns, updated, cc = planner.process_corner_errors(path, corner_slowdowns)
    assert updated == 0

    assert_no_nans(cc)
    assert_no_nans(check_slowdowns)

    reverse_slowdowns, updated = planner.reverse_pass(path, corner_slowdowns)
    assert_no_nans(reverse_slowdowns)
    print(reverse_slowdowns)

    forward_slowdowns, updated = planner.forward_pass(path, reverse_slowdowns)
    assert_no_nans(forward_slowdowns)
    print(forward_slowdowns)

    double_check = True

    if double_check:
        reverse_slowdowns2, updated = planner.reverse_pass(path, forward_slowdowns)
        assert_no_nans(reverse_slowdowns2)
        print("reverse2", updated)
        assert updated == 0

        forward_slowdowns2, updated = planner.forward_pass(path, reverse_slowdowns2)
        assert_no_nans(forward_slowdowns2)
        print("forward2", updated)
        assert updated == 0

        reverse_slowdowns3, updated = planner.reverse_pass(path, forward_slowdowns2)
        assert_no_nans(reverse_slowdowns3)
        print("reverse3", updated)
        assert updated == 0

        forward_slowdowns3, updated = planner.forward_pass(path, reverse_slowdowns3)
        assert_no_nans(forward_slowdowns3)
        print("forward3", updated)
        assert updated == 0

    speeds = planner.gen_speeds(path, forward_slowdowns)
    _, updated, cc = planner.process_corner_errors(path, forward_slowdowns)
    assert updated == 0

    validate_cc_solution(cc, path, speeds, check_plato=True)

    _segments, profile = planner.gen_segments_float(path, forward_slowdowns)
    print(profile)

