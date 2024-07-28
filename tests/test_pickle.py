from autohotpy import ahk
from pickle import dumps, loads


def test_obj():

    objct = ahk.Object()
    objct.fck = "10"
    pk = dumps(objct)
    obj = loads(pk)

    assert obj.fck == "10"
    assert obj.Base
