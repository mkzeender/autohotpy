from typing import Generic, Iterable, Protocol, TypeVar

from autohotpy.static_typing.classes import object_

class HwndObject(Protocol):
    HWND: int

WinTitleFinder = HwndObject | int | str

KeyT = TypeVar("KeyT", covariant=True)
ValT = TypeVar("ValT", covariant=True)

class SingleIterable(object_.Object, Iterable[ValT]): ...
class DoubleIterable(object_.Object, Generic[KeyT, ValT]): ...
