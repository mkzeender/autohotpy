from __future__ import annotations


from typing import TYPE_CHECKING, Any, Literal


if TYPE_CHECKING:
    from autohotpy.static_typing.classes import Prototype

from autohotpy.proxies.ahk_object import AhkObject


def mro(obj: Any) -> list[Prototype | type]:
    lst: list[Prototype | type] = []

    if isinstance(obj, AhkObject):
        call = obj._ahk_instance.call_method
        ogb = lambda o: call(None, "ObjGetBase", (o,))
        proto: Prototype | Literal[""] = ogb(obj)
        while proto:
            lst.append(proto)
            proto = ogb(proto)
        return lst

    else:
        tp = type(obj)
        if isinstance(obj, type):
            lst += obj.mro()
            lst += type.mro(tp)[:-1]
        else:
            lst += tp.mro()

        return lst
