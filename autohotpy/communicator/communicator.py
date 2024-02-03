from __future__ import annotations
from ctypes import CFUNCTYPE, c_int, c_uint64, c_wchar_p
import json
from typing import TYPE_CHECKING, Any, Callable
from autohotpy.ahk_obj_factory import AhkObjFactory
from autohotpy.ahk_object import AhkObject
from autohotpy.communicator.script_inject.Callbacks import Callbacks
from autohotpy.exceptions import ExitApp, throw
from autohotpy.references import ReferenceKeeper
from autohotpy.communicator.script_inject.Callbacks import addr_of
from autohotpy.communicator.dtypes import DTypes


UNSET = object()


class Communicator:
    def __init__(self, on_idle: Callable, on_exit: Callable):
        self.on_idle = on_idle
        self.on_exit = on_exit

        self.py_references = ReferenceKeeper()
        self.callbacks = Callbacks(self)

    def create_init_script(self):
        return self.callbacks.create_init_script()

    def create_user_script(self, script: tuple[str, ...]):
        return self.callbacks.create_user_script(script)

    def value_from_data(self, data, factory: AhkObjFactory) -> Any:
        if isinstance(data, dict):
            if data["dtype"] == DTypes.AHK_OBJECT:
                return factory.create(int(data["ptr"]))
            if data["dtype"] == DTypes.INT:
                return int(data["value"])
            if data["dtype"] == DTypes.PY_OBJECT:
                return self.py_references.obj_from_ptr(int(data["ptr"]))
        else:
            return data

    def value_to_data(self, value):
        if isinstance(value, AhkObject):
            ptr = value._ahk_ptr
            ptr = ptr if ptr is not None else self.globals_ptr
            return dict(dtype=DTypes.AHK_OBJECT.value, ptr=ptr)
        if isinstance(value, (bool, int, float, str)):
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
        ret_val: Any = UNSET

        @CFUNCTYPE(c_int, c_wchar_p)
        def ret_callback(val_data: str):
            nonlocal ret_val
            ret_val = json.loads(val_data)
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

        _call(arg_data)  # sets ret_val

        if ret_val is UNSET:
            raise ExitApp("unknown", 1)

        result = self.value_from_data(ret_val["value"], factory)

        if int(ret_val["success"]):
            return result
        else:
            throw(result)

    def _set_ahk_func_ptrs(
        self,
        call_ptr: int,
        call_threadsafe_ptr: int,
        get_global_var: int,
        free_obj_ptr: int,
        globals_ptr: int,
    ):
        CALLERTYPE = CFUNCTYPE(c_int, c_wchar_p)

        self.call_func: Callable[[c_wchar_p], int] = CALLERTYPE(call_ptr)
        self.call_func_threadsafe: Callable[[c_wchar_p], int]
        self.call_func_threadsafe = CALLERTYPE(call_threadsafe_ptr)

        self._get_global_var = CFUNCTYPE(c_int, c_wchar_p, CFUNCTYPE(c_int, c_wchar_p))(
            get_global_var
        )
        self._free_obj: Callable[[int], int] = CFUNCTYPE(c_int, c_uint64)(free_obj_ptr)
        self.globals_ptr = globals_ptr

        return 0

    def _get_attr_callback(self, obj_id: c_int, attr: c_wchar_p, bytecount=-1):
        # obj = self._references[obj_id.value]
        # attr_val = attr.value
        # assert attr_val is not None
        # if not hasattr(obj, attr_val):
        #     return -1
        # gotten = getattr(obj, attr_val)
        # if gotten is None:
        #     return 0
        # if isinstance(gotten, (str, int, float)):
        #     gotten = str(gotten)
        #     assert self._str_reference is None
        #     self._str_reference = gotten
        #     return len(gotten)
        ...

    def set_attr_callback(self):
        ...

    def call_callback(self):
        ...

    def free_obj_callback(self):
        ...
