from __future__ import annotations
from ctypes import CFUNCTYPE, c_int, c_uint64, c_wchar_p
import json
from typing import TYPE_CHECKING, Any, Callable
from autohotpy._unset_type import UNSET
from autohotpy.proxies.ahk_object import AhkObject
from autohotpy.communicator.script_inject.callbacks import Callbacks
from autohotpy.exceptions import ExitApp, throw
from autohotpy.communicator.references import ReferenceKeeper
from autohotpy.communicator.script_inject.callbacks import addr_of
from autohotpy.communicator.dtypes import DTypes
from autohotpy.proxies.var_ref import VarRef

if TYPE_CHECKING:
    from autohotpy.proxies.ahk_obj_factory import AhkObjFactory


class Communicator:
    def __init__(
        self,
        on_idle: Callable,
        on_exit: Callable,
        on_error: Callable,
        on_call: Callable,
        post_init: Callable[[], None],
    ):
        self.on_idle = on_idle
        self.on_exit = on_exit
        self.on_error = on_error
        self.on_call = on_call
        self.post_init = post_init

        self.py_references = ReferenceKeeper()
        self.callbacks = Callbacks(self)

    def create_init_script(self):
        return self.callbacks.create_init_script()

    def create_user_script(self, script: tuple[str, ...]):
        return self.callbacks.create_user_script(script)

    def value_from_data(self, data, factory: AhkObjFactory | None) -> Any:
        if isinstance(data, dict):
            dtype = DTypes(data["dtype"])
            if dtype in (
                DTypes.AHK_OBJECT,
                DTypes.VARREF,
                DTypes.AHK_MAP,
                DTypes.AHK_ARRAY,
            ):
                assert factory is not None
                return factory.create(
                    ptr=int(data["ptr"]),
                    type_name=data["type_name"],
                    dtype=dtype,
                    immortal=bool(data["immortal"]),
                )
            if dtype == DTypes.UNSET:
                return UNSET
            if dtype == DTypes.INT:
                return int(data["value"])
            if dtype == DTypes.PY_OBJECT:
                return self.py_references.obj_from_ptr(int(data["ptr"]))

        else:
            return data

    def value_to_data(self, value):
        if value is UNSET:
            return dict(dtype=DTypes.UNSET.value)
        if isinstance(value, bool):
            value = int(value)
        if isinstance(value, VarRef):
            ptr = value._ahk_ptr
            return dict(dtype=DTypes.VARREF.value, ptr=ptr)
        if isinstance(value, AhkObject):
            ptr = value._ahk_ptr
            ptr = ptr if ptr is not None else self.globals_ptr
            return dict(dtype=DTypes.AHK_OBJECT.value, ptr=ptr)
        if isinstance(value, (int, float, str)):
            return value
        else:
            ptr = self.py_references.obj_to_ptr_add_ref(value)
            return dict(dtype=DTypes.PY_OBJECT.value, ptr=ptr)

    def call_method(
        self,
        obj: AhkObject | None,
        method: str,
        args: tuple,
        kwargs: dict[str, Any] | None,
        factory: AhkObjFactory,
        _call: Callable,
    ) -> Any:

        result: Any = UNSET
        success: int = 0

        @CFUNCTYPE(c_int, c_wchar_p)
        def ret_callback(val_data: str):
            nonlocal result, success
            ret_val = json.loads(val_data)
            result = self.value_from_data(ret_val["value"], factory)
            success = int(ret_val["success"])
            return 0

        obj_or_globals = (
            dict(dtype=DTypes.AHK_OBJECT, ptr=self.globals_ptr)
            if obj is None
            else self.value_to_data(obj)
        )

        arg_data = c_wchar_p(
            json.dumps(
                dict(
                    obj=obj_or_globals,
                    method=self.value_to_data(method),
                    args=[self.value_to_data(arg) for arg in args],
                    kwargs=(
                        {key: self.value_to_data(val) for key, val in kwargs.items()}
                        if kwargs
                        else {}
                    ),
                    return_callback=addr_of(ret_callback),
                )
            )
        )

        _call(arg_data)  # sets result

        # if ret_val is UNSET:
        #     raise ExitApp("unknown", 1)

        if success:
            return result
        else:
            throw(result)

    def _set_ahk_func_ptrs(
        self,
        call_ptr: int,
        call_threadsafe_ptr: int,
        get_global_var: int,
        free_obj_ptr: int,
        put_return_ptr: int,
        globals_ptr: int,
    ):
        CALLERTYPE = CFUNCTYPE(c_int, c_wchar_p)

        self.call_func: Callable[[c_wchar_p], int] = CALLERTYPE(call_ptr)
        self.call_func_threadsafe: Callable[[c_wchar_p], int]
        self.call_func_threadsafe = CALLERTYPE(call_threadsafe_ptr)

        self._get_global_var = CFUNCTYPE(c_int, c_wchar_p, CFUNCTYPE(c_int, c_wchar_p))(
            get_global_var
        )
        self.free_ahk_obj: Callable[[int], int] = CFUNCTYPE(c_int, c_uint64)(
            free_obj_ptr
        )
        self.put_return_ptr: Callable[[int, int], int] = CFUNCTYPE(
            c_int, c_uint64, c_uint64
        )(put_return_ptr)
        self.globals_ptr = globals_ptr

        self.post_init()

        return 0

    def call_callback(self, call_data: str):
        data = json.loads(call_data)
        success, ret_val = self.on_call(data)

        ret_data = c_wchar_p(
            json.dumps(dict(success=int(success), value=self.value_to_data(ret_val)))
        )

        ret_p = addr_of(ret_data)

        self.put_return_ptr(int(data["ret_call_p"]), ret_p)

        return 0

    def free_obj_callback(self, ptr: int):
        self.py_references.obj_free(ptr)
        return 0
