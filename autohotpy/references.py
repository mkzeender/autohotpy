from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from autohotpy.ahk_instance import AhkInstance


@dataclass(slots=True)
class RefWrapper:
    value: Any
    count: int = 0

    def __eq__(self, other: RefWrapper | int) -> bool:
        if isinstance(other, int):
            return id(self.value) == other
        return id(self.value) == other.ptr

    def __hash__(self) -> int:
        return hash(id(self.value))

    @property
    def ptr(self) -> int:
        return id(self.value)


class References:
    __slots__ = ("_dict",)

    def __init__(self) -> None:
        self._dict: dict[int, RefWrapper]

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
        if ref.count == 0:
            del self._dict[id(obj)]

    def get(self, ptr):
        return self._dict[ptr].value


class ReferenceKeeper:
    def __init__(self) -> None:
        self.references = References()
        self.immortals = set()

    def py_obj_to_ptr_add_ref(self, obj) -> int:
        ref = RefWrapper(obj)
        if ref not in self.immortals:
            self.references.add(ref)
        return ref.ptr

    def py_obj_to_ptr(self, obj) -> int:
        return RefWrapper(obj).ptr

    def py_obj_to_immortal_ptr(self, obj) -> int:
        ref = RefWrapper(obj)
        self.immortals.add(ref)
        self.references.remove(ref)

        return ref.ptr

    def py_obj_from_ptr(self, ptr: int) -> Any:
        return self.references.get(ptr)

    def py_obj_free(self, ptr: int):
        if ptr not in self.immortals:
            self.references.decrement(ptr)
