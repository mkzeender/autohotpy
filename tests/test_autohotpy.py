from autohotpy.ahk import Menu
from autohotpy import ahk

ahk.include(r"tests/test_autohotpy.ahk")


def test_object():
    obj = ahk.my_obj
    obj.bar = "baz"
    assert obj.bar == "baz"


def test_function():
    n = ahk.abs(-1.0)
    assert type(n) == float
    assert n == 1.0
