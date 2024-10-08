from typing import Any, Iterable, Self

from autohotpy.static_typing.classes import BoolInt

class Object:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def Clone(self) -> Self:
        """Returns a shallow copy of an object."""

    def DefineProp(self, name: str, descriptor: Object) -> Self:
        """Defines a new own property."""

    def DeleteProp(self, name: str) -> Any:
        """Removes an own property from an object."""

    def GetOwnPropDesc(self, name: str) -> Object:
        """Returns a descriptor for a given own property, compatible with DefineProp."""

    def HasOwnProp(self, name: str) -> BoolInt:
        """Returns 1 (true) if an object owns a property by the specified name, otherwise 0 (false)."""

    def OwnProps(self) -> Iterable[str]:
        """Enumerates an object's own properties."""
    Base: Object

    def __getattr__(self, __name: str) -> Any: ...
    def __setattr__(self, __name: str, __value: Any) -> None: ...
