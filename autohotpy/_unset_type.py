from typing import Any, Self


class UnsetType:
    __slots__ = ("__weakref__",)
    _UNSET = None

    def __new__(cls) -> Self:
        if cls._UNSET is None:
            cls._UNSET = super().__new__(cls)
        return cls._UNSET

    def __repr__(self) -> str:
        return "UNSET"

    def __str__(self) -> str:
        return "<UNSET>"

    def __bool__(self) -> bool:
        return False

    def __reduce__(self) -> str | tuple[Any, ...]:
        return (UnsetType, ())


UNSET = UnsetType()
