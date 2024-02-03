from __future__ import annotations
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from autohotpy.communicator import Communicator


from .create_script import (
    create_injection_script,
    create_user_script,
)

from ctypes import (
    CFUNCTYPE,
    c_char,
    c_int,
    c_int64,
    c_uint64,
    c_void_p,
    c_wchar_p,
    cast,
)


def addr_of(func) -> int:
    try:
        val = cast(func, c_void_p).value
        assert val is not None
        return val
    except:
        print(f"ignoring {func}")
        return 0


class Callbacks:
    def __init__(self, comm: Communicator) -> None:
        self._get = CFUNCTYPE(c_int, c_int64, c_wchar_p, c_char * 64)(
            comm._get_attr_callback
        )
        self._set = comm.set_attr_callback
        self._call = comm.call_callback
        self._free_obj = comm.free_obj_callback
        self._exit_app = CFUNCTYPE(c_int, c_wchar_p, c_int64)(comm.on_exit)
        self._idle = CFUNCTYPE(None)(comm.on_idle)
        self._give_pointers = CFUNCTYPE(
            c_int, c_uint64, c_uint64, c_uint64, c_uint64, c_uint64
        )(comm._set_ahk_func_ptrs)

        self.ptrs = CallbackPtrs(
            call_method=addr_of(self._call),
            free_obj=addr_of(self._free_obj),
            idle=addr_of(self._idle),
            give_pointers=addr_of(self._give_pointers),
            exit_app=addr_of(self._exit_app),
        )

    def create_init_script(self):
        return create_injection_script(self.ptrs)

    def create_user_script(self, script):
        return create_user_script(script, self.ptrs)


@dataclass
class CallbackPtrs:
    call_method: int
    free_obj: int
    idle: int
    give_pointers: int
    exit_app: int
