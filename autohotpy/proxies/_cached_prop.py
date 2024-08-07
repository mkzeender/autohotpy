from typing import (
    Callable,
    Generic,
    Self,
    TypeVar,
    overload,
)

from sys import intern

PropT = TypeVar("PropT", infer_variance=True)
SelfT = TypeVar("SelfT", infer_variance=True)


class CachedProp(Generic[SelfT, PropT]):
    def __init__(self, func: Callable[[SelfT], PropT]):
        self.func = func

    def __set_name__(self, owner: type[SelfT], name: str) -> None:
        self.name = name
        self.qualname = owner.__qualname__ + "." + name
        self.private_name = intern("_ahk_cached_" + name.strip("_"))
        assert not hasattr(owner, "__slots__") or self.private_name in owner.__slots__  # type: ignore

    @overload
    def __get__(self, obj: None, objtype: type[SelfT]) -> Self: ...
    @overload
    def __get__(self, obj: SelfT, objtype: type[SelfT] | None = None) -> PropT: ...
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self

        val = getattr(obj, self.private_name)
        if val is None:
            val = self.func(obj)
            setattr(obj, self.private_name, val)

        return val

    def __set__(self, obj: SelfT, value: PropT) -> None:
        raise AttributeError(self.name, obj)

    def __repr__(self):
        return f"<CachedWatcher '{self.qualname}'>"


def cached_prop(method: Callable[[SelfT], PropT]) -> CachedProp[SelfT, PropT]:

    return CachedProp(method)
