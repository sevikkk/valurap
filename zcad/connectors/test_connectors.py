from zencad import point3, vector3

from connectors import Connector, Solver, np_point


def test_connector_str():
    c = Connector()
    assert str(c) == "<Connector>"
    assert repr(c) == "<Connector>"


def test_connector_str2():
    c = Connector(position=point3(1, 2, 3))
    assert str(c) == "<Connector point=[1. 2. 3.]>"


def test_connector_str3():
    c = Connector(
        position=point3(1, 2, 3), top=vector3(0, 0, 1), direction=vector3(1, 0, 0)
    )
    assert str(c) == "<Connector point=[1. 2. 3.] direction=[1. 0. 0.] top=[0. 0. 1.]>"


def test_solver_simple_translation():
    s = Solver([Connector(point3(0, 0, 0))], [Connector(point3(1, 0, 0))])

    r = s.solve()

    p1 = r(point3(0, 0, 0))
    p2 = r(point3(1, 1, 1))

    assert p1 == point3(1, 0, 0)
    assert p2 == point3(2, 1, 1)


def test_solver_simple_translation_np_points():
    s = Solver([Connector([0, 0, 0])], [Connector([1, 0, 0])])

    r = s.solve()

    p1 = r(np_point(0, 0, 0))
    p2 = r(np_point(1, 1, 1))

    assert all(p1 == [1, 0, 0])
    assert all(p2 == [2, 1, 1])
