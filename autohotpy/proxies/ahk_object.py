from __future__ import annotations
from typing import Any, TYPE_CHECKING, Iterator

from autohotpy.proxies._cached_prop import cached_prop
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
        "_ahk_cached_name",
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
        self._ahk_cached_name = None
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
        yield from super().__dir__()
        obj = self
        while True:
            try:
                yield from obj.OwnProps()
            except AttributeError:
                return

            obj = self._ahk_instance.get_attr(
                obj,
                "base",
            )

    @cached_prop
    def __name__(self) -> str:
        if self._ahk_ptr is None:
            return "ahk"
        if self._ahk_type_name == "Func":
            return self.Name
        if self._ahk_type_name == "Class":
            return getattr(self.Prototype, "__Class")
        return str(self._ahk_instance.get_attr(self, "__name__"))

    def __str__(self) -> str:
        try:
            return self._ahk_instance.call_method(self, "ToString", ())
        except (AttributeError, ValueError):
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

    def __subclasscheck__(self, subclass: type) -> bool:
        return bool()


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
