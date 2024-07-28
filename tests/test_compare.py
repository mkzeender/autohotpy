from autohotpy import ahk


def test_obj():
    container = ahk.Object()

    container.one = ahk.Object()
    container.two = container.one
    container.three = ahk.Object()
    assert container.two == container.one
    assert container.one is not container.one
    assert container.three != container.two


def test_cls():
    cls1 = ahk.Object

    cls2 = ahk.Array.Base

    assert cls2 == cls1

    assert ahk.Array == "Array"

    assert ahk.Type(ahk.Array()) == ahk.Array
