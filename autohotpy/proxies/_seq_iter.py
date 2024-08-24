from __future__ import annotations
from typing import TYPE_CHECKING, Iterable, Literal, cast, overload

from autohotpy import exceptions
from autohotpy._unset_type import UNSET, UnsetType


if TYPE_CHECKING:
    from autohotpy.proxies.ahk_object import AhkObject
    from autohotpy.static_typing.classes.protocols import SingleIterable, DoubleIterable  # type: ignore
    from autohotpy.static_typing.classes.object_ import Object  # type: ignore
    from autohotpy.static_typing.classes import VarRef


def _val_or_unset[VT](ref: VarRef[VT]) -> VT | UnsetType:
    try:
        return ref.value
    except exceptions.Error:
        return UNSET


@overload
def fmt_item[TupleT: tuple](item: TupleT) -> TupleT: ...
@overload
def fmt_item[T](item: T) -> tuple[T]: ...


def fmt_item(item):
    if isinstance(item, tuple):
        params = item
    else:
        params = (item,)

    return params


@overload
def iterator[
    KeyT, ValT
](iterable: DoubleIterable[KeyT, ValT], n: Literal[2] = 2) -> Iterable[
    tuple[KeyT, ValT]
]: ...


@overload
def iterator[ValT](iterable: SingleIterable[ValT], n: Literal[1]) -> Iterable[ValT]: ...


@overload
def iterator(iterable: Object, n: int) -> Iterable: ...


def iterator(iterable, n=2):  # type: ignore
    """Iterate over 2 or more parameters in an ahk iterable.
    The parameter n should be used to specify the number of variables
    to unpack in the for-loop (default is 2)
    Examples:

    >>> arr = ahk.Array('foo', 'bar')
    >>> for index, value in iterator(arr):
    ...     print(index, value)

    1 foo
    2 bar

    >>> for key, value in iterator(ahk.Map('foo', 'bar', 'hoo', 'baz')):
    ...     print(key, value)

    foo bar
    hoo baz


    """
    if TYPE_CHECKING:
        iterable = cast(AhkObject, iterable)

    if iterable._ahk_type_name == "Enumerator":
        enumer = iterable
    else:

        enumer = iterable._ahk_instance.call_method(iterable, "__Enum", (n,), {})

    refs: list[VarRef] = [
        iterable._ahk_instance.call_method(None, "VarRef", ()) for _ in range(n)
    ]
    while enumer(*refs):
        if n == 1:
            yield _val_or_unset(refs[0])
        else:
            yield tuple(_val_or_unset(r) for r in refs)
