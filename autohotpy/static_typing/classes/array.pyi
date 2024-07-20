from typing import Iterator, overload
from autohotpy.static_typing.classes import Nothing, object_
from autohotpy.static_typing.classes.protocols import DoubleIterable, SingleIterable

class Array[T](SingleIterable[T], DoubleIterable[int, T], object_.Object):
    """An Array object contains a list or sequence of values."""

    Length: int
    Capacity: int
    Default: T

    def __init__(self, *values: T): ...
    def Delete(self, index: int, /) -> T:
        """Removes the value of an array element, leaving the index without a value."""

    def Get[DefaultT](self, index: int, default: DefaultT = ..., /) -> T | DefaultT:
        """Returns the value at a given index, or a default value."""

    def Has(self, index: int, /) -> int:
        """Returns a non-zero number if the index is valid and there is a value at that position."""

    def InsertAt(self, /, *values: T) -> Nothing:
        """Inserts one or more values at a given position."""

    def Pop(self) -> T:
        """Removes and returns the last array element."""

    def Push(self, *values: T) -> Nothing:
        """Appends values to the end of an array."""

    @overload
    def RemoveAt(self, Index: int) -> T:
        """Removes item or items from an array."""

    @overload
    def RemoveAt(self, Index: int, Length: int) -> Nothing:
        """Removes items from an array."""

    def __iter__(self) -> Iterator[T]: ...
    def __getitem__(self) -> T: ...
    def __setitem__(self, value: T): ...
