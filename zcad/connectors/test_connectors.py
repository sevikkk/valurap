from zencad import point3, vector3

from connectors import Connector, Solver


def test_connector_str():
    c = Connector()
    assert str(c) == "<Connector use_for_solve=True>"
    assert repr(c) == "<Connector use_for_solve=True>"


def test_connector_str2():
    c = Connector(position=point3(1, 2, 3))
    assert (
        str(c) == "<Connector "
        "point=point3(1.000000,2.000000,3.000000) "
        "use_for_solve=True>"
    )


def test_connector_str3():
    c = Connector(
        position=point3(1, 2, 3), top=vector3(0, 0, 1), direction=vector3(1, 0, 0)
    )
    assert (
        str(c) == "<Connector "
        "point=point3(1.000000,2.000000,3.000000) "
        "direction=vector3(1.000000,0.000000,0.000000) "
        "top=vector3(0.000000,0.000000,1.000000) "
        "use_for_solve=True>"
    )


def test_solver_simple_translation():
    s = Solver([Connector(point3(0, 0, 0))], [Connector(point3(1, 0, 0))])

    r = s.solve()

    p1 = r(point3(0, 0, 0))
    p2 = r(point3(1, 1, 1))

    assert p1 == point3(1, 0, 0)
    assert p2 == point3(2, 1, 1)
