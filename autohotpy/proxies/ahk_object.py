from __future__ import annotations
from typing import Any, TYPE_CHECKING, Iterator

from autohotpy import exceptions
from autohotpy.proxies._cached_prop import cached_prop
from autohotpy.proxies._copying import reduce_ahk_obj
from autohotpy.proxies._seq_iter import fmt_item, iterator


if TYPE_CHECKING:
    from autohotpy.ahk_instance import AhkInstance
    from autohotpy.proxies.var_ref import VarRef


def _demangle(name: str) -> str:
    if name.endswith("__"):
        return name
    lead, sep, end = name.rpartition("__")
    return sep + end


class AhkObject:
    __slots__ = (
        "_ahk_instance",
        "_ahk_ptr",
        "_ahk_cached_ahk_name",
        "_ahk_type_name",
        "_ahk_immortal",
    )

    def __init__(
        self,
        inst: AhkInstance,
        pointer: int | None,
        type_name: str,
        immortal: bool = False,
    ) -> None:
        self._ahk_instance = inst
        self._ahk_ptr = pointer
        self._ahk_cached_ahk_name = None
        self._ahk_type_name = type_name
        self._ahk_immortal = immortal

    def __del__(self):
        if not self._ahk_immortal:
            self._ahk_instance.free(self)

    def Call(self, *args, **kwargs) -> Any:
        return self._ahk_instance.call_method(self, "call", args, kwargs)

    def __call__(self, *args, **kwargs) -> Any:
        return self._ahk_instance.call_method(self, "call", args, kwargs)

    def __getattr__(self, __name: str) -> Any:
        if __name in _ahk_obj_slots:
            raise RuntimeError(f"{type(self)} does not have special attr {__name}")

        return self._ahk_instance.get_attr(self, _demangle(__name))

    def __setattr__(self, __name: str, __value: Any) -> None:
        if __name in _ahk_obj_slots:
            super().__setattr__(__name, __value)
        else:
            self._ahk_instance.set_attr(self, _demangle(__name), __value)

    def __dir__(self):
        seen = set()

        obj = self
        while True:
            try:
                seen.update(obj.OwnProps())
                obj = self._ahk_instance.get_attr(
                    obj,
                    "base",
                )
            except AttributeError:
                break

        seen.update(super(AhkObject, self).__dir__())
        return seen

    def __reduce__(self) -> str | tuple[Any, ...]:
        return reduce_ahk_obj(self)

    @cached_prop
    def _ahk_name(self) -> str:

        if self._ahk_ptr is None:
            return "ahk"
        if self._ahk_type_name == "Func":
            return self.Name
        if self._ahk_type_name == "Class":
            return getattr(self.Prototype, "__Class")
        if self._ahk_type_name == "Prototype":
            return self.__Class + ".Prototype"

        raise AttributeError(name="_ahk_name", obj=self)

    @property
    def __name__(self) -> str:
        try:
            return self._ahk_name.split(".")[-1]
        except IndexError:
            return ""

    def __str__(self) -> str:
        try:
            return self._ahk_instance.call_method(self, "ToString", ())
        except (AttributeError, ValueError, exceptions.Error):
            return repr(self)

    def __repr__(self):
        if self._ahk_ptr is None:
            return super().__repr__()
        if self._ahk_type_name in ("Func", "Class"):
            return f"ahk.{self.__name__}"
        return f"<Ahk {self._ahk_type_name} object at {self._ahk_ptr:#x}>"

    def __getitem__(self, item) -> Any:
        return self._ahk_instance.call_method(
            None, "_py_getitem", (self, *fmt_item(item))
        )

    def __setitem__(self, item, value):
        self._ahk_instance.call_method(
            None, "_py_setitem", (self, value, *fmt_item(item))
        )

    def __iter__(self) -> Iterator:
        return iterator(self, 1)  # type: ignore

    def __instancecheck__(self, instance: Any) -> bool:
        if self._ahk_type_name == "Class":
            return bool(
                self._ahk_instance.call_method(
                    None, "_py_instancecheck", (instance, self)
                )
            )
        elif self._ahk_type_name == "Array":
            return any(isinstance(instance, cls) for cls in self)

        raise TypeError("isinstance() arg 2 must be a type, Array, tuple, or union")

    def __subclasscheck__(self, subcls: type) -> bool:
        if self._ahk_type_name == "Class":
            return bool(
                subcls._ahk_instance.call_method(None, "HasBase", (subcls, self))
            )
        elif self._ahk_type_name == "Array":
            return any(issubclass(subcls, basecls) for basecls in self)

        else:
            raise ValueError(
                f"issubclass() arg 2 must be a type, Array, tuple, or union"
            )

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, AhkObject):
            return self._ahk_ptr == other._ahk_ptr
        elif isinstance(other, str) and self._ahk_type_name == "Class":
            return self._ahk_name == other

        return False

    def __hash__(self) -> int:
        if self._ahk_type_name == "Class":
            return hash(self._ahk_name)
        else:
            return hash(self._ahk_ptr)


class AhkBoundProp(AhkObject):
    __slots__ = (
        "_ahk_bound_to",
        "_ahk_method_name",
    )

    def __init__(
        self,
        inst: AhkInstance,
        pointer: int,
        type_name: str,
        immortal: bool,
        bound_to: AhkObject,
        method_name: str,
    ) -> None:
        super().__init__(
            inst=inst, pointer=pointer, type_name=type_name, immortal=immortal
        )
        self._ahk_bound_to = bound_to
        self._ahk_method_name = method_name

    def __call__(self, *args, **kwargs) -> Any:
        return self._ahk_instance.call_method(
            self._ahk_bound_to, self._ahk_method_name, args, kwargs
        )

    def __getitem__(self, item) -> Any:
        return self._ahk_instance.call_method(
            None,
            "_py_getprop",
            (self._ahk_bound_to, self._ahk_method_name, *fmt_item(item)),
        )

    def __setitem__(self, item, value):
        self._ahk_instance.call_method(
            None,
            "_py_setprop",
            (self._ahk_bound_to, self._ahk_method_name, value, *fmt_item(item)),
        )


_ahk_obj_slots = AhkObject.__slots__ + AhkBoundProp.__slots__
