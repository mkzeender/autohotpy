from autohotpy import ahk
from pickle import dumps, loads
import pytest as tst


def test_obj():

    objct = ahk.Object()
    objct.fck = "10"
    pk = dumps(objct)
    obj = loads(pk)

    assert obj.fck == "10"
    assert obj.Base


def test_array():

    arr1 = ahk.Array(3, 4, 5, [])

    pk = dumps(arr1)

    arr2 = loads(pk)

    assert list(arr2) == [3, 4, 5, []]

    map1 = ahk.Map("foo", "bar", "hoo", [])

    pk = dumps(map1)

    map2 = loads(pk)

    assert map2["foo"] == "bar"
    assert map2["hoo"] == []


def test_class_func():
    Array, MsgBox = loads(dumps((ahk.Array, ahk.MsgBox)))

    assert Array == ahk.Array, MsgBox == ahk.MsgBox
