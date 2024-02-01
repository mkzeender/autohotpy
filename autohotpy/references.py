from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any


@dataclass(slots=True)
class RefWrapper:
    value: Any
    count: int = 0

    def __eq__(self, other: RefWrapper | int) -> bool:
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

    def decrement(self, obj):
        ref = self._dict[id(obj)]
        ref.count -= 1
        if ref.count <= 0:
            del self._dict[id(obj)]

    def get(self, ptr: int):
        return self._dict[ptr].value

    def __contains__(self, ptr: int):
        return ptr in self._dict


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
        return self.references.get(ptr)

    def obj_free(self, ptr: int):
        if ptr not in self.immortals:
            self.references.decrement(ptr)
