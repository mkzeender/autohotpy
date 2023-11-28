from __future__ import annotations
from typing import Any, TYPE_CHECKING

from autohotpy._ahkdll import ahkdll
if TYPE_CHECKING:
    from autohotpy.ahk_instance import AhkInstance


from ctypes import c_int, c_int64, c_void_p
from _ctypes import CFuncPtr


class AhkObject:

    def __init__(self, inst:AhkInstance, pointer:c_int64, bound_to:Any=None) -> None:
        self.__inst:AhkInstance = inst
        self.__ptr:c_int64 = pointer
        self.__bound_to = bound_to
        
    
    def call(self, *args) -> Any:
        ...

    # def call_nowait(self, *args) -> Any:
    #     ahkdll.ahkPostFunction(*self._format_args(args))

    def __call__(self, *args: list) -> Any:

        if self.__bound_to is None:
            return self.call(*args)
        else:
            self.call(self.__bound_to, *args)

    # def _format_args(self, args):
    #     if len(args) > 10:
    #         raise RuntimeError('Could not call function {self.name}: 10 args maximum')

    #     return [self.name] + [str(arg) for arg in args] + [c_void_p()]*(10 - len(args)) + [self.ahk._thread_id]

    def _format_arg(self, arg):
        if isinstance(arg, CFuncPtr):
            ...

