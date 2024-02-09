from typing import Any, Iterable

UNSET: Any

class ComValue: ...

class ComObject(ComValue):
    def __init__(self, CLSID: str, IID: str = UNSET): ...
    def __getattr__(self, name: str) -> Any: ...

class ComObjArray(ComValue):
    """Creates a SafeArray for use with COM."""

    def __init__(self, count1, /, *counts): ...
    def MaxIndex(self, dim: int, /) -> int:
        """Returns the upper bound of the nth dimension. If n is omitted, it defaults to 1."""

    def MinIndex(self, dim: int, /) -> int:
        """Returns the lower bound of the nth dimension. If n is omitted, it defaults to 1."""

    def Clone(self) -> ComObjArray:
        """Returns a copy of the array"""

    def __iter__(self) -> Iterable: ...
