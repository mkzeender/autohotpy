from __future__ import annotations

from ctypes import CFUNCTYPE, c_int, c_uint, c_wchar_p

from enum import StrEnum, auto
import json
import os
import threading
from typing import TYPE_CHECKING, Any, Callable

from ._ahkdll import ahkdll
from ._script_injection import (
    create_injection_script,
    create_user_script,
    Callbacks,
    addr_of,
)
from .references import ReferenceKeeper
from ._dtypes import DTypes
from .global_state import thread_state

if TYPE_CHECKING:
    from .ahk_object import AhkObject


class AhkState(StrEnum):
    IDLE = auto()
    CLOSED = auto()
    RUNNING = auto()
    INITIALIZING = auto()


class AhkInstance:
    def __init__(self, *script) -> None:
        self._ahk_communicator = ReferenceKeeper()
        thread_state.current_instance = self
        self._autoexec_condition = threading.Condition()
        self._job_queue: c_wchar_p | bool = False

        self._error = None
        self._exit_code: int | None = None
        self._exit_reason: str = ""
        self.state: AhkState = AhkState.INITIALIZING

        self._callbacks = Callbacks(self)

        # starting ahk will change the working directory (for some reason), so we save and restore it
        cwd = os.getcwd()

        self._thread_id = c_uint(ahkdll.NewThread("Persistent", "", "", c_int(1)))
        self._py_thread_id = threading.get_ident()

        os.chdir(cwd)

        # inject a backend library into the script, for communicating with python
        modded_script = create_injection_script(self._callbacks)

        self._add_script(modded_script, runwait=1)

        self.add_script(*script)

    def add_script(self, *script: str):
        if thread_state.get_thread_type(self) != "autoexec":
            raise RuntimeError(
                "Global-scope ahk statements cannot be run in the middle of a function. Try running this in a different thread."
            )
        with (cond := self._autoexec_condition):
            while self._job_queue is not False or self.state == AhkState.RUNNING:
                if self.state == AhkState.CLOSED:
                    raise RuntimeError("Interpreter is already closed")
                cond.wait(timeout=1)

            # request the old script to end, and wait for it to do so
            if self.state != AhkState.INITIALIZING:
                self._job_queue = True
                cond.notify_all()
                while self._job_queue is not False:
                    cond.wait(timeout=1)

            # mark script as running again
            self.state = AhkState.RUNNING
            cond.notify_all()

            # run the script
            user_script: str = create_user_script(script, self._callbacks)
            self._add_script(user_script, runwait=2)

            # wait for it to pass control back to this thread.
            while self.state == AhkState.RUNNING:
                cond.wait(timeout=1)

    def _add_script(self, script: str, runwait) -> None:
        ahkdll.addScript(script, c_int(runwait), self._thread_id)

    def add_hotkey_or_hotstring(self, sequence: str, func: Callable | AhkObject | str):
        from autohotpy.ahk_object import AhkObject

        if isinstance(func, AhkObject):
            ptr = func._ahk_ptr

            script = f"""{sequence}::
                {{
                    static obj := ObjFromPtrAddRef({ptr})
                    obj()
                }}"""

        elif isinstance(func, str):
            script = f"{sequence}::{func}"

        elif callable(func):  # TODO
            raise NotImplementedError
        else:
            raise TypeError

        self.add_script(script)

    def ahkReady(self) -> bool:
        return bool(ahkdll.ahkReady(self._thread_id))

    def _match_state(self, state):
        if self.state == state:
            return True
        elif state != self.state == AhkState.CLOSED:
            assert self._exit_code is not None
            from autohotpy.exceptions import ExitApp

            raise ExitApp(self._exit_reason, self._exit_code)

    def run_forever(self) -> None:
        with (cond := self._autoexec_condition):
            # indicate to Ahk's main thread that it can go into persistent mode
            self._job_queue = True
            self._autoexec_condition.notify_all()
            while not self.state == AhkState.CLOSED:
                # Timeout allows for KeyboardInterrupts if you're in the main thread.
                cond.wait(timeout=1)

    def value_from_data(
        self,
        data,
        bind_to: AhkObject | None = None,
        bound_method_name: str = "",
    ) -> Any:
        from .ahk_object import AhkObject, AhkBoundProp

        if isinstance(data, dict):
            if data["dtype"] == DTypes.AHK_OBJECT:
                if bind_to is None:
                    return AhkObject(self, data["ptr"])
                else:
                    return AhkBoundProp(self, data["ptr"], bind_to, bound_method_name)

            if data["dtype"] == DTypes.INT:
                return int(data["value"])
        else:
            return data

    def value_to_data(self, value):
        from .ahk_object import AhkObject

        if isinstance(value, AhkObject):
            return dict(dtype=DTypes.AHK_OBJECT.value, ptr=value._ahk_ptr)
        if type(value) in (bool, int, float, str):
            return value

        raise TypeError

    def _call_autoexec(self, arg_data: c_wchar_p):
        cond = self._autoexec_condition
        with cond:
            while self._job_queue is not False:
                cond.wait(timeout=1)
            self._job_queue = job = arg_data
            cond.notify_all()
            while self._job_queue is arg_data:
                cond.wait(timeout=1)

    def _autoexec_thread_callback(self):
        with (cond := self._autoexec_condition):
            self.state = AhkState.IDLE
            cond.notify_all()

            while True:
                cond.wait_for(lambda: self._job_queue is not False)
                job: bool | c_wchar_p = self._job_queue

                assert job is not False

                # set to True if something has been appended to the script.
                if job is True:
                    self._job_queue = False
                    cond.notify_all()
                    return
                else:
                    self._call_func(job)
                    self._job_queue = False
                    cond.notify_all()

    def call_method(
        self,
        obj: AhkObject | None,
        method: str,
        args: tuple,
        kwargs: dict[str, Any],
        bind_to: AhkObject | None = None,
        bound_method_name: str = "",
    ) -> Any:
        ret_val: Any = None

        @CFUNCTYPE(c_int, c_wchar_p)
        def ret_callback(val_data: str):
            nonlocal ret_val
            ret_val = json.loads(val_data)
            return 0

        thread_type = thread_state.get_thread_type(self)

        if thread_type == "ahk":
            _call = self._call_func
        elif thread_type == "external":
            _call = self._call_func_threadsafe
        else:  # thread_type == 'autoexec'
            _call = self._call_autoexec
            # _call = self._call_func

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
                    kwargs={
                        key: self.value_to_data(val) for key, val in kwargs.items()
                    },
                    return_callback=addr_of(ret_callback),
                )
            )
        )

        _call(arg_data)  # sets ret_val
        ret_callback.argtypes
        arg_data.value

        if ret_val["success"]:
            return self.value_from_data(
                ret_val["value"], bind_to=bind_to, bound_method_name=bound_method_name
            )
        else:
            from autohotpy.exceptions import throw

            throw(ret_val["value"])

    def get_attr(
        self,
        obj: AhkObject,
        name: str,
    ):
        from .ahk_script import AhkScript

        if isinstance(obj, AhkScript):
            ret_val = None

            @CFUNCTYPE(c_int, c_wchar_p)
            def ret_callback(val_data: str):
                nonlocal ret_val
                ret_val = json.loads(val_data)
                return 0

            success = self._get_global_var(name, ret_callback)
            if success:
                return self.value_from_data(ret_val)
            else:
                raise AttributeError(f"Global variable {name} could not be found")
        return self.call_method(
            self._get_ahk_attr,
            "Call",
            (obj, name),
            {},
            bind_to=obj,
            bound_method_name=name,
        )

    def set_attr(self, obj: Any, name: str, value: Any):
        return self._set_ahk_attr(obj, name, value)

    def _call_py_method(self, call_inf_json: str):
        call_info = json.loads(call_inf_json)

        args = [self.value_from_data(arg) for arg in call_info["args"]]
        obj = self.value_from_data(call_info["obj"])
        method = self.value_from_data(call_info["method"])

        result = getattr(obj, method)(*args)

        if result is not None:
            result_data = json.dumps(
                {"success": True, "value": self.value_to_data(result)}
            )
            CFUNCTYPE(c_int, c_wchar_p).from_address(call_info["return_callback"])(
                result_data
            )

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

    def _set_attr_callback(self):
        ...

    def _call_callback(self):
        ...

    def _free_obj_callback(self):
        ...

    def _exit_app_callback(self, reason, code):
        with self._autoexec_condition:
            self._exit_code = code
            self._exit_reason = reason
            self.state = AhkState.CLOSED
            self._autoexec_condition.notify_all()
            return 0

    def _set_ahk_func_ptrs(
        self,
        call_ptr: int,
        call_threadsafe_ptr: int,
        get_global_var: int,
        callbacks: str,
    ):
        CALLERTYPE = CFUNCTYPE(c_int, c_wchar_p)
        self._call_func: Callable[[c_wchar_p], int] = CALLERTYPE(call_ptr)
        self._call_func_threadsafe: Callable[[c_wchar_p], int] = CALLERTYPE(
            call_threadsafe_ptr
        )
        self._get_global_var = CFUNCTYPE(c_int, c_wchar_p, CFUNCTYPE(c_int, c_wchar_p))(
            get_global_var
        )

        callback_data = json.loads(callbacks)
        self.globals_ptr = self.value_from_data(callback_data["globals_ptr"])
        self._set_ahk_attr = self.value_from_data(callback_data["set_ahk_attr"])
        self._get_ahk_attr = self.value_from_data(callback_data["get_ahk_attr"])

        return 0
