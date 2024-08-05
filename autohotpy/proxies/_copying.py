from __future__ import annotations

from contextlib import contextmanager
import threading
from typing import TYPE_CHECKING, Any, Callable, Generator, NamedTuple, cast

from autohotpy.proxies._seq_iter import iterator
from autohotpy.ahk_run import get_ahk


if TYPE_CHECKING:
    from autohotpy.proxies.ahk_object import AhkObject


class _Local(threading.local):
    def __init__(self) -> None:
        self.memo: dict[int | None, AhkObject] | None = None


_local = _Local()


class SavedAhkObj(NamedTuple):
    func: Callable
    args: tuple


@contextmanager
def _memo[T](obj: T) -> Generator[T, None, None]:

    from autohotpy.proxies.ahk_object import AhkObject

    memo = _local.memo
    if memo is None:
        new_memo = True

        _local.memo = memo = {}
    else:
        new_memo = False

    try:
        if isinstance(obj, AhkObject):
            if obj._ahk_ptr not in memo:
                memo[obj._ahk_ptr] = obj
                yield obj
            else:
                yield cast(T, memo[obj._ahk_ptr])
        else:
            yield obj
    finally:
        if new_memo:
            _local.memo = None


def _from_qualname(qualname: str, *, location: Any) -> AhkObject:

    # qualname = qualname.removeprefix("ahk.")

    try:
        for attr in qualname.split("."):
            location = getattr(location, attr)

        return location

    except AttributeError as e:
        raise RuntimeError(
            f'"{qualname}" could not be accessed while (un)pickling'
        ) from e


def load_from_qualname(qualname: str, *, location: Any = None) -> AhkObject:

    # if not qualname.startswith("ahk."):
    #     raise ValueError(f'Invalid qualname "{qualname}" for pickling')

    if location is None:
        location = get_ahk()

    return _from_qualname(qualname, location=location)


def load_from_own_props(
    base: Any,
    own_props: dict[str, Any],
    *,
    location=None,
):

    if location is None:
        location = get_ahk()
    obj = location.Object()

    for k, v in own_props.items():
        setattr(obj, k, v)

    obj.Base = base

    return obj


def reduce_ahk_obj(self: AhkObject, location: Any = None):
    with _memo(self) as obj:
        objth: Any = obj

        if location is None:
            location = obj._ahk_instance.get_globals()

        if obj._ahk_type_name in ("Class", "Func", "Prototype"):

            qualname = obj._ahk_name

            if load_from_qualname(qualname, location=location)._ahk_ptr != obj._ahk_ptr:
                raise ValueError(f"{qualname} is not a picklable qualname")

            func = load_from_qualname
            args = (qualname,)

        elif obj._ahk_type_name == "Array":
            func = location.Array
            args = tuple(obj)
        elif obj._ahk_type_name == "Map":
            func = location.Map
            args = ()

            for kv in iterator(objth, 2):
                args += kv

        elif obj._ahk_type_name in (
            "VarRef",
            "ComValue",
            "ComObjArray",
            "ComObject",
            "ComValueRef",
        ):
            raise ValueError(f'"{obj._ahk_type_name}" type is not picklable')

        else:
            func = load_from_own_props

            state = dict[str, tuple[bool, Any]]()

            for attr in objth.OwnProps():
                desc = objth.GetOwnPropDesc(attr)
                if not hasattr(desc, "value"):
                    raise ValueError(
                        f'Cannot pickle dynamic property "{attr}" of object {objth!r}'
                    )
                with _memo(desc.value) as value:
                    state[attr] = value

            with _memo(objth.Base) as base:

                args = (base, state)

        return func, args
