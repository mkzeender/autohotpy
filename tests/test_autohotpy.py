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


def test_special():
    v = ahk.VarRef("shoo")

    assert v.value == "shoo"

    v.value = "well then"

    assert v.value == "well then"

    obj = ahk.Object(foo="bar", hoo="baz")

    assert obj.foo == "bar" and obj.hoo == "baz"

    obj = ahk.Map("wut", "that", foo="bar", hoo="baz")

    assert obj["wut"] == "that"
    assert obj["foo"] == "bar"
