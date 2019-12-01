from valurap.path_planning import PathPlanner, PathLimits, solve_model_simple, ir, xtov_k

DEFAULT_LIMITS = PathLimits(None, None, 3000, 3000, None, None, 0.1)


def test_simple():
    pp = PathPlanner([[0, 0, 0], [100, 0, 100], [100, 0, 0]], DEFAULT_LIMITS)

    plan, errors, notes = pp.plan_path_in_floats()
    assert not errors

    assert plan == [
        [0.03333333333333333, 1.6666666666666667, 0.0, 100.0, 0.0, "accel_0"],
        [0.9666666666666666, 98.33333333333333, 0.0, 100.0, 0.0, "plato_0"],
        [0.03333333333333333, 100.0, 0.0, 0.0, 0.0, "accel_1"],
        [5, 100.0, 0.0, 0.0, 0.0, "final"],
    ]


def test_corner_too_fast_for_precision():
    pp = PathPlanner([[0, 0, 0], [100, 0, 100], [100, 100, 100], [100, 100, 0]], DEFAULT_LIMITS)

    plan, errors, notes = pp.plan_path_in_floats()
    assert len(errors) == 1
    assert errors[0][1] == "middle_delta"


def test_corner_ok():
    pp = PathPlanner([[0, 0, 0], [100, 0, 40], [100, 100, 40], [100, 100, 0]], DEFAULT_LIMITS)

    plan, errors, notes = pp.plan_path_in_floats()
    assert not errors
    assert plan == [
        [0.013333333333333334, 0.2666666666666668, 0.0, 40.0, 0.0, "accel_0"],
        [2.486666666666667, 99.73333333333333, 0.0, 40.0, 0.0, "plato_0"],
        [0.013333333333333334, 100.0, 0.2666666666666668, 0.0, 40.0, "accel_1"],
        [2.486666666666667, 100.0, 99.73333333333333, 0.0, 40.0, "plato_1"],
        [0.013333333333333334, 100.0, 100.0, 0.0, 0.0, "accel_2"],
        [5, 100.0, 100.0, 0.0, 0.0, "final"],
    ]


def test_corner_with_useless_segment():
    pp = PathPlanner(
        [[0, 0, 0], [100, 0, 40], [100, 50, 40], [100, 100, 40], [100, 100, 0]], DEFAULT_LIMITS
    )

    plan, errors, notes = pp.plan_path_in_floats()
    assert not errors
    assert plan == [
        [0.013333333333333334, 0.2666666666666668, 0.0, 40.0, 0.0, "accel_0"],
        [2.486666666666667, 99.73333333333333, 0.0, 40.0, 0.0, "plato_0"],
        [0.013333333333333334, 100.0, 0.2666666666666668, 0.0, 40.0, "accel_1"],
        [1.2433333333333334, 100.0, 50.0, 0.0, 40.0, "plato_1"],
        [0.0, 100.0, 50.0, 0.0, 40.0, "accel_2"],  # expected, no auto join
        [1.2433333333333334, 100.0, 99.73333333333333, 0.0, 40.0, "plato_2"],
        [0.013333333333333334, 100.0, 100.0, 0.0, 0.0, "accel_3"],
        [5, 100.0, 100.0, 0.0, 0.0, "final"],
    ]


def test_zigzag():
    pp = PathPlanner(
        [[0, 0, 0], [100, 0, 40], [100, 100, 40], [200, 100, 40], [200, 100, 0]], DEFAULT_LIMITS
    )

    plan, errors, notes = pp.plan_path_in_floats()
    assert not errors
    assert plan == [
        [0.013333333333333334, 0.2666666666666668, 0.0, 40.0, 0.0, "accel_0"],
        [2.486666666666667, 99.73333333333333, 0.0, 40.0, 0.0, "plato_0"],
        [0.013333333333333334, 100.0, 0.2666666666666668, 0.0, 40.0, "accel_1"],
        [2.486666666666667, 100.0, 99.73333333333333, 0.0, 40.0, "plato_1"],
        [0.013333333333333334, 100.26666666666667, 100.0, 40.0, 0.0, "accel_2"],
        [2.486666666666667, 199.73333333333335, 100.0, 40.0, 0.0, "plato_2"],
        [0.013333333333333334, 200.00000000000003, 100.0, 0.0, 0.0, "accel_3"],
        [5, 200.00000000000003, 100.0, 0.0, 0.0, "final"],
    ]


SLOW_LIMITS = PathLimits(None, None, 300, 300, None, None, 0.1)


def test_zigzag_small():
    pp = PathPlanner(
        [[0, 0, 0], [100, 0, 40], [100, 3, 40], [200, 3, 40], [200, 3, 0]], SLOW_LIMITS
    )

    plan, errors, notes = pp.plan_path_in_floats()
    assert errors
    assert errors[0][1] == "cur_avail"


def test_slowdown_zigzag_small():
    pp = PathPlanner(
        [[0, 0, 0], [100, 0, 40], [100, 3, 40], [200, 3, 40], [200, 3, 0]], SLOW_LIMITS
    )

    plan, slowdowns, notes = pp.plan_with_slow_down()
    assert list(slowdowns) == [
        0.31016931544410925,
        0.31016931544410925,
        0.31016931544410925,
        0.31016931544410925,
    ]
    print(notes)


def test_optimize_zigzag_small():
    pp = PathPlanner(
        [[0, 0, 0], [100, 0, 40], [100, 3, 40], [200, 3, 40], [200, 3, 0]], SLOW_LIMITS
    )

    plan, slowdowns, notes = pp.plan_with_slow_down()
    assert list(slowdowns) == [
        0.31016931544410925,
        0.31016931544410925,
        0.31016931544410925,
        0.31016931544410925,
    ]
    print(notes)
    speedup_slowdowns = pp.plan_speedup(slowdowns, notes)
    plan, errors, notes = pp.plan_path_in_floats(speedup_slowdowns)
    assert not errors
    assert plan == [
        [0.041355908725881234, 0.2565466779815129, 0.0, 12.40677261776437, 0.0, "accel_0"],
        [0.013333333333333435, 0.4219703128850391, 0.0, 12.40677261776437, 0.0, "plato_0"],
        [0.0919774246074521, 2.832090301570193, 0.0, 40.0, 0.0, "accel_0_1"],
        [2.35839548492149, 97.16790969842978, 0.0, 40.0, 0.0, "plato_0_1"],
        [0.0919774246074521, 99.57802968711495, 0.0, 12.40677261776437, 0.0, "accel_0_2"],
        [0.013333333333334406, 99.74345332201848, 0.0, 12.40677261776437, 0.0, "plato_0_2"],
        [0.041355908725881234, 100.0, 0.2565466779815129, 0.0, 12.40677261776437, "accel_1"],
        [0.20044750723295685, 100.0, 2.743453322018487, 0.0, 12.40677261776437, "plato_1"],
        [0.041355908725881234, 100.25654667798152, 3.0, 12.40677261776437, 0.0, "accel_2"],
        [0.013333333333334509, 100.42197031288505, 3.0, 12.40677261776437, 0.0, "plato_2"],
        [0.0919774246074521, 102.83209030157022, 3.0, 40.0, 0.0, "accel_2_1"],
        [2.35839548492149, 197.1679096984298, 3.0, 40.0, 0.0, "plato_2_1"],
        [0.0919774246074521, 199.57802968711496, 3.0, 12.40677261776437, 0.0, "accel_2_2"],
        [0.01333333333333326, 199.7434533220185, 3.0, 12.40677261776437, 0.0, "plato_2_2"],
        [0.041355908725881234, 200.0, 3.0, 0.0, 0.0, "accel_3"],
        [5, 200.0, 3.0, 0.0, 0.0, "final"],
    ]


def test_solve_model():
    plan = [
        [0.013333333333333334, 0.2666666666666668, 0.0, 40.0, 0.0, "accel_0"],
        [2.486666666666667, 99.73333333333333, 0.0, 40.0, 0.0, "plato_0"],
        [0.013333333333333334, 100.0, 0.2666666666666668, 0.0, 40.0, "accel_1"],
        [2.486666666666667, 100.0, 99.73333333333333, 0.0, 40.0, "plato_1"],
        [0.013333333333333334, 100.0, 100.0, 0.0, 0.0, "accel_2"],
        [5, 100.0, 100.0, 0.0, 0.0, "final"],
    ]
    acc_t, acc_x, acc_y, acc_vx, ac_vy, _ = plan[0]
    plato_t, plato_x, plato_y, _, _, _ = plan[1]
    res = solve_model_simple(
        0, acc_vx / 1000 * 80 * xtov_k, plato_x * 80, ir(acc_t * 1000), ir(plato_t * 1000)
    )

    print(res)
    assert res == {
        "accel_j": 594079295,
        "accel_jj": -99013216,
        "accel_middle_x": 1.8467694324897364,
        "accel_t": 13,
        "accel_x": 17.605868572800887,
        "e_delta_v": 91.90221432514954,
        "e_jerk": 0.2468719482421875,
        "e_target": 1.031621650326997e-07,
        "plato_t": 2487,
        "plato_v": 274969.8091583252,
        "plato_x": 7961.060797990704,
        "target_v": 274877.90694400005,
    }


def test_intplan_zigzag_small():
    pp = PathPlanner(
        [[0, 0, 0], [100, 0, 40], [100, 3, 40], [200, 3, 40], [200, 3, 0]], SLOW_LIMITS
    )

    int_plan = pp.plan()
    for px, py in int_plan:
        print()
        print(px)
        print(py)

        if "e_target" in px:
            assert abs(px["e_target"]) < 2
            assert abs(px["e_jerk"]) < 500
            assert abs(px["e_delta_v"]) < 1000

        if "e_target" in py:
            assert abs(py["e_target"]) < 2
            assert abs(py["e_jerk"]) < 500
            assert abs(py["e_delta_v"]) < 1000
