from typing import Generic, Iterable, Protocol, TypeVar

from autohotpy.static_typing.classes import object_

class HwndObject(Protocol):
    HWND: int

WinTitleFinder = HwndObject | int | str

KeyT = TypeVar("KeyT", covariant=True)
ValT = TypeVar("ValT", covariant=True)

class AhkIterable(object_.Object): ...  # TODO: make Array and Map inherit from this!!!
class SingleIterable(AhkIterable, Iterable[ValT]): ...
class DoubleIterable(AhkIterable, Generic[KeyT, ValT]): ...
