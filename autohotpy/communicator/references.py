from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

_debug: References | None = None


def set_debug(debug: bool):
    global _debug
    if debug:
        _debug = References()
    else:
        _debug = None


@dataclass(slots=True)
class RefWrapper:
    value: Any
    count: int = 0

    def __eq__(self, other: object) -> bool:
        if isinstance(other, int):
            return id(self.value) == other
        elif isinstance(other, RefWrapper):
            return id(self.value) == other.ptr
        return NotImplemented

    def __hash__(self) -> int:
        return hash(id(self.value))

    @property
    def ptr(self) -> int:
        return id(self.value)


class References:
    def __init__(self) -> None:
        self._dict: dict[int, RefWrapper] = {}

    def add(self, obj):
        if id(obj) in self._dict:
            self._dict[id(obj)].count += 1
        else:
            self._dict[id(obj)] = RefWrapper(obj, 1)

    def remove(self, obj):
        if id(obj) in self._dict:
            del self._dict[id(obj)]

    def decrement_obj(self, obj):
        self.decrement_ptr(id(obj))

    def decrement_ptr(self, ptr: int) -> RefWrapper | None:
        ref = self._dict[ptr]
        ref.count -= 1
        if ref.count <= 0:
            del self._dict[ptr]
            return ref
        return None

    def get(self, ptr: int):
        return self._dict[ptr].value

    def __contains__(self, ptr: int):
        return ptr in self._dict

    def count(self, ptr: int) -> int:
        if ptr in self._dict:
            return self._dict[ptr].count
        return 0


class Immortals(References):
    def add(self, obj):
        if id(obj) not in self._dict:
            self._dict[id(obj)] = RefWrapper(obj, 1)

    def decrement(self, obj):
        pass


class ReferenceKeeper:
    def __init__(self) -> None:
        self.references = References()
        self.immortals = References()
        self.collected = References()

    def obj_to_ptr_add_ref(self, obj) -> int:
        if id(obj) not in self.immortals:
            self.references.add(obj)
        return id(obj)

    def obj_to_ptr(self, obj) -> int:
        return id(obj)

    def obj_to_immortal_ptr(self, obj) -> int:
        self.immortals.add(obj)
        self.references.remove(obj)

        return id(obj)

    def obj_from_ptr(self, ptr: int) -> Any:
        try:
            if ptr in self.immortals:
                return self.immortals.get(ptr)
            return self.references.get(ptr)
        except KeyError:
            if _debug is not None:
                val = _debug.get(ptr)
                raise RuntimeError(
                    f"Tried to access an object that has already been cleared: ptr={ptr}, value={val!r}'"
                )
            else:
                raise RuntimeError(
                    f"Tried to access ptr {ptr} which has already been cleared. Try debugging with autohotpy.communicator.references.set_debug(True)"
                ) from None

    def obj_free(self, ptr: int):
        if ptr not in self.immortals:
            ref = self.references.decrement_ptr(ptr)
            if _debug is not None and ref is not None:
                _debug.add(ref.value)

    def get_refcount(self, obj_or_ptr: int | Any) -> int | Literal["immortal"]:
        if isinstance(obj_or_ptr, int):
            ptr: int = obj_or_ptr
        else:
            ptr = id(obj_or_ptr)

        if ptr in self.immortals:
            return "immortal"
        elif ptr in self.references:
            return self.references.count(ptr)
        return 0
