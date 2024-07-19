from __future__ import annotations
from typing import Any, TYPE_CHECKING, Generator, Iterator

from autohotpy.exceptions import AhkError
from autohotpy.proxies._cached_prop import cached_prop, ahkobject_slots
from autohotpy.proxies._seq_iter import _fmt_item


if TYPE_CHECKING:
    from autohotpy.ahk_instance import AhkInstance
    from autohotpy.proxies.var_ref import VarRef


def _demangle(name:str) -> str:
    if name.endswith('__'):
        return name
    lead, sep, end = name.rpartition('__')
    return sep+end
    

class AhkObject:
    __slots__ = ahkobject_slots

    def __init__(
        self,
        inst: AhkInstance,
        pointer: int | None,
    ) -> None:
        self._ahk_instance = inst
        self._ahk_ptr = pointer
        self._ahk_cached_name = None
        self._ahk_cached_ahk_type = None

    def __del__(self):
        self._ahk_instance.free(self)

    def call(self, *args, **kwargs) -> Any:
        return self._ahk_instance.call_method(self, "call", args, kwargs)

    def __call__(self, *args, **kwargs) -> Any:
        return self._ahk_instance.call_method(self, "call", args, kwargs)

    def __getattr__(self, __name: str) -> Any:
        return self._ahk_instance.get_attr(self, _demangle(__name))

    def __setattr__(self, __name: str, __value: Any) -> None:
        if __name in AhkObject.__slots__:
            super().__setattr__(__name, __value)
            return
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
            return 'ahk'
        if self._ahk_type == 'Func':
            return self.Name
        if self._ahk_type == 'Class':
            return getattr(self.Prototype, '__Class')
        try:
            return str(self._ahk_instance.get_attr(self, '__name__'))
        except AhkError:
            raise AttributeError(name='__name__', obj=self)

    @cached_prop
    def _ahk_type(self) -> str:
        return self._ahk_instance.call_method(None, "Type", (self,))

    def __str__(self) -> str:
        try:
            return self._ahk_instance.call_method(self, "ToString", ())
        except (AhkError, AttributeError, ValueError):
            return repr(self)

    def __repr__(self):
        if self._ahk_ptr is None:
            return super().__repr__()
        if self._ahk_type in ('Func', 'Class'):
            return f'ahk.{self.__name__}'
        return f"<Ahk {self._ahk_type} object at {hex(self._ahk_ptr)}>"

    def __getitem__(self, item) -> Any:
        return self._ahk_instance.call_method(
            None, "_py_getitem", (self, *_fmt_item(item))
        )

    def __setitem__(self, item, value):
        self._ahk_instance.call_method(
            None, "_py_setitem", (self, value, *_fmt_item(item))
        )

    def __iter__(self) -> Generator:
        enumer = self._ahk_instance.call_method(self, "__Enum", (1,), {})

        ref: VarRef = self._ahk_instance.call_method(None, "VarRef", ("",))
        while enumer(ref):
            yield ref.value

    


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

    def __getitem__(self, item) -> Any:
        return self._ahk_instance.call_method(
            None,
            "_py_getprop",
            (self._ahk_bound_to, self._ahk_method_name, *_fmt_item(item)),
        )

    def __setitem__(self, item, value):
        self._ahk_instance.call_method(
            None,
            "_py_setprop",
            (self._ahk_bound_to, self._ahk_method_name, value, *_fmt_item(item)),
        )
