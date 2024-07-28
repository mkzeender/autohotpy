from __future__ import annotations

from typing import TYPE_CHECKING, Any, cast

from autohotpy.proxies._seq_iter import iterator


if TYPE_CHECKING:
    from autohotpy.proxies.ahk_object import AhkObject
    from autohotpy.static_typing.classes import object_  # type: ignore
    from autohotpy.static_typing.classes import map as map_  # type: ignore


def _from_qualname(qualname: str, location) -> AhkObject:

    # qualname = qualname.removeprefix("ahk.")

    try:
        for attr in qualname.split("."):
            location = getattr(location, attr)

        return location

    except AttributeError as e:
        raise RuntimeError(
            f'"{qualname}" could not be accessed while (un)pickling'
        ) from e


def load_from_qualname(qualname: str) -> AhkObject:

    # if not qualname.startswith("ahk."):
    #     raise ValueError(f'Invalid qualname "{qualname}" for pickling')

    from autohotpy import ahk

    return _from_qualname(qualname, ahk)


def load_from_own_props(base: Any, own_props: dict[str, Any]):
    from autohotpy import ahk

    obj = ahk.Object()

    obj.Base = base

    for k, v in own_props.items():
        desc = ahk.Object()
        desc.value = v
        obj.DefineProp(k, desc)

    return obj


def reduce_ahk_obj(self: AhkObject):
    from autohotpy import ahk

    if TYPE_CHECKING:
        obj = cast(object_.Object, self)
    else:
        obj = self

    if ahk._ahk_instance is not self._ahk_instance:
        raise ValueError(
            f"{self} cannot be pickled because it is not from the default ahk interpreter."
        )

    if self._ahk_type_name in ("Class", "Func", "Prototype"):

        qualname = self._ahk_name

        if load_from_qualname(qualname)._ahk_ptr != self._ahk_ptr:
            raise ValueError(f"{qualname} is not a picklable qualname")

        func = load_from_qualname
        args = (qualname,)

    elif self._ahk_type_name == "Array":
        func = ahk.Array
        args = tuple(self)
    elif self._ahk_type_name == "Map":
        func = ahk.Map
        args = ()
        if TYPE_CHECKING:
            obj = cast(map_.Map, obj)
        for kv in iterator(obj, 2):
            args += kv

    elif self._ahk_type_name in (
        "VarRef",
        "ComValue",
        "ComObjArray",
        "ComObject",
        "ComValueRef",
    ):
        raise ValueError(f'"{self._ahk_type_name}" type is not picklable')

    else:
        func = load_from_own_props

        state = dict[str, Any]()

        for attr in obj.OwnProps():
            desc = obj.GetOwnPropDesc(attr)
            if not hasattr(desc, "value"):
                raise ValueError(
                    f'Cannot pickle dynamic property "{attr}" of object {obj!r}'
                )
            state[attr] = desc.value

        args = (obj.Base, state)
    return func, args
