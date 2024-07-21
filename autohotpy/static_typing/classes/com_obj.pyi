from typing import Any, Iterator, Self

class ComValue[ValT]:
    """Wraps a value, SafeArray or COM object for use by the script or for passing to a COM method.

    NOTE: If the class is ByRef, you can deref with an empty tuple:
    >>> com_val[()] := "some value"

    """

    def __new__(cls, var_type: int, value: ValT, flags: int = ...) -> Self: ...

    Ptr: int

class ComObjArray[ValT](ComValue[ValT]):
    """Creates a SafeArray for use with COM."""

    def __new__(cls, var_type: int, /, count1: int, *counts: int) -> Self: ...
    def MaxIndex(self, n: int = 1, /) -> int:
        """Returns the upper bound of the nth dimension. If n is omitted, it defaults to 1."""

    def MinIndex(self, n: int = 1, /) -> int:
        """Returns the lower bound of the nth dimension. If n is omitted, it defaults to 1."""

    def Clone(self) -> Self:
        """Returns a copy of the array."""

    def __iter__(self) -> Iterator[ValT]: ...

class ComObject(ComValue):
    """Creates a COM object."""

    def __new__(cls, CLSID: str, IID: str = ...) -> Self | ComValue: ...
    def __getattr__(self, name: str) -> Any: ...
