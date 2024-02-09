from typing import Generic, TypeVar
from autohotpy.proxies.ahk_object import AhkObject

T = TypeVar("T")


class VarRef(AhkObject, Generic[T]):
    @property
    def value(self) -> T:
        return self._ahk_instance.call_method(None, "_py_deref", (self,))

    @value.setter
    def value(self, new_value: T):
        self._ahk_instance.call_method(None, "_py_set_ref", (self, new_value))
