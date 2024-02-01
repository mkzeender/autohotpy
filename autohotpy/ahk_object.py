from __future__ import annotations
from typing import Any, TYPE_CHECKING, Iterator


if TYPE_CHECKING:
    from autohotpy.ahk_instance import AhkInstance


class AhkObject:
    __slots__ = "_ahk_instance", "_ahk_ptr", "_ahk_bound_to", "_ahk_method_name"

    def __init__(
        self,
        inst: AhkInstance,
        pointer: int | None,
    ) -> None:
        self._ahk_instance = inst
        self._ahk_ptr = pointer

    def call(self, *args, **kwargs) -> Any:
        return self._ahk_instance.call_method(self, "Call", args, kwargs)

    # def __getitem__(self, name) -> Any:  # TODO: fix these
    #     if self._ahk_bound_to is None:
    #         return getattr(self, "__Item")[name]
    #     else:
    #         return getattr(self._ahk_bound_to, "__Get")(name, [self])

    # def __setitem__(self, name, value):
    #     if self._ahk_bound_to is None:
    #         return getattr(self, "__Set")(name, value)
    #     else:
    #         ...

    def __call__(self, *args, **kwargs) -> Any:
        return self._ahk_instance.call_method(self, "Call", args, kwargs)

    def __getattr__(self, __name: str) -> Any:
        return self._ahk_instance.get_attr(self, __name)

    def __setattr__(self, __name: str, __value: Any) -> None:
        if __name in AhkObject.__slots__:
            super().__setattr__(__name, __value)
            return
        self._ahk_instance.set_attr(self, __name, __value)

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

    def __iter__(self) -> Iterator:
        return self._ahk_instance.call_method(self, "__Enum", (1,), {})

    def __next__(self):
        return self._ahk_instance.call_method(self, "Call", (), {})  # TODO


class AhkBoundProp(AhkObject):
    def __init__(
        self, inst: AhkInstance, pointer: int, bound_to: AhkObject, method_name: str
    ) -> None:
        super().__init__(inst, pointer)
        self._ahk_bound_to = bound_to
        self._ahk_method_name = method_name

    def __call__(self, *args, **kwargs) -> Any:
        return self._ahk_instance.call_method(
            self._ahk_bound_to, self._ahk_method_name, args, kwargs
        )
