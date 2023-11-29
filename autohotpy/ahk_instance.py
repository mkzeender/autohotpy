from __future__ import annotations

from ctypes import (
    CFUNCTYPE,
    POINTER,
    c_char,
    c_int,
    c_uint,
    c_uint64,
    c_wchar_p,
    c_int64,
)
from enum import StrEnum, auto
import json
import os
import threading
from typing import TYPE_CHECKING, Any, Callable

from autohotpy.exceptions import ExitApp
from ._ahkdll import ahkdll
from ._script_injection import (
    create_injection_script,
    create_user_script,
    Callbacks,
    addr_of,
)
from .references import References
from ._dtypes import DTypes
from .global_state import thread_state

if TYPE_CHECKING:
    from .ahk_object import AhkObject


class AhkState(StrEnum):
    IDLE = auto()
    CLOSED = auto()
    RUNNING = auto()


_UNSET = object()


class AhkInstance:
    def __init__(self, *script: str, wait_for: AhkState | None = AhkState.IDLE) -> None:
        self._references = References()
        self._str_references = References()
        self._closed_condition = threading.Condition()
        self._error = None
        self._exit_code: int | None = None
        self._exit_reason: str = ""
        self._state: AhkState = AhkState.RUNNING

        self._callbacks = Callbacks(
            get=CFUNCTYPE(c_int, c_int64, c_wchar_p, POINTER(c_char * 64))(
                self._get_attr_callback
            ),
            set=self._set_attr_callback,
            call=self._call_callback,
            free_obj=self._free_obj_callback,
            exit_app=CFUNCTYPE(c_int, c_wchar_p, c_int64)(self._exit_app_callback),
            idle=CFUNCTYPE(None)(self._idle_callback),
            give_pointers=CFUNCTYPE(c_int, c_uint64, c_uint64, c_wchar_p)(
                self._set_ahk_func_ptrs
            ),
        )

        # starting ahk will change the working directory (for some reason), so we save and restore it
        cwd = os.getcwd()

        self._thread_id = c_uint(ahkdll.NewThread("Persistent", "", "", c_int(1)))

        os.chdir(cwd)

        # inject a backend library into the script, for communicating with python
        modded_script = create_injection_script(self._callbacks)

        self._add_script(modded_script, wait=True, execute=True)

        if script:
            self._add_script(
                create_user_script(script, self._callbacks),
                execute=True,
                wait=(wait_for == AhkState.IDLE),
            )
        else:
            with self._closed_condition:
                self.state = AhkState.IDLE
                self._closed_condition.notify_all()

        if wait_for == AhkState.CLOSED:
            self.wait(AhkState.CLOSED)
        elif wait_for == AhkState.IDLE and self.state == AhkState.CLOSED:
            assert self._exit_code is not None
            raise ExitApp(self._exit_reason, self._exit_code)

    @property
    def state(self) -> AhkState:
        return self._state

    @state.setter
    def state(self, value: AhkState):
        if self._state == AhkState.CLOSED:
            return
        self._state = value

    def add_script(self, *script: str, wait_for: AhkState | None = AhkState.IDLE):
        # wait for the script to either close or become idle
        with self._closed_condition:
            self.wait(AhkState.IDLE)
            assert self.state == AhkState.IDLE

            # mark the script as running again!
            self.state = AhkState.RUNNING
            self._closed_condition.notify_all()

        user_script: str = create_user_script(script, self._callbacks)
        self._add_script(user_script, wait=(wait_for == AhkState.IDLE), execute=True)

        if wait_for == AhkState.CLOSED:
            self.wait(AhkState.CLOSED)
        elif wait_for == AhkState.IDLE and self.state == AhkState.CLOSED:
            assert self._exit_code is not None
            raise ExitApp(self._exit_reason, self._exit_code)

    def _add_script(
        self, script: str, *, wait=True, execute=True, starting=False
    ) -> None:
        waitexec = 0 if not execute else 1 if wait else 2

        ahkdll.addScript(script, c_int(waitexec), self._thread_id)

    def ahkReady(self) -> bool:
        return bool(ahkdll.ahkReady(self._thread_id))

    def _match_state(self, state):
        if self.state == state:
            return True
        elif state != self.state == AhkState.CLOSED:
            assert self._exit_code is not None
            raise ExitApp(self._exit_reason, self._exit_code)

    def wait(self, wait_for: AhkState = AhkState.IDLE) -> None:
        with self._closed_condition:
            while not self._closed_condition.wait_for(
                lambda: self._match_state(wait_for), timeout=1
            ):
                # DONT DELETE, this no-op checks for KeyboardInterrupts if you're in the main thread.
                pass

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

    def call_method(
        self,
        obj: AhkObject,
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
            _call = self._call_func  # TODO: change mainthread behavior

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
            raise RuntimeError

    def get_attr(
        self,
        obj: AhkObject,
        name: str,
    ):
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

    def _get_attr_callback(self, obj_id: c_int, attr: c_wchar_p, bytecount=-1):
        obj = self._references[obj_id.value]
        attr_val = attr.value
        assert attr_val is not None
        if not hasattr(obj, attr_val):
            return -1
        gotten = getattr(obj, attr_val)
        if gotten is None:
            return 0
        if isinstance(gotten, (str, int, float)):
            gotten = str(gotten)
            assert self._str_reference is None
            self._str_reference = gotten
            return len(gotten)

    def _set_attr_callback(self):
        ...

    def _call_callback(self):
        ...

    def _free_obj_callback(self):
        ...

    def _exit_app_callback(self, reason, code):
        with self._closed_condition:
            self._exit_code = code
            self._exit_reason = reason
            self.state = AhkState.CLOSED
            self._closed_condition.notify_all()
            return 0

    def _idle_callback(self):
        with self._closed_condition:
            self.state = AhkState.IDLE
            self._closed_condition.notify_all()

    def _set_ahk_func_ptrs(
        self, call_ptr: int, call_threadsafe_ptr: int, callbacks: str
    ):
        CALLERTYPE = CFUNCTYPE(c_int, c_wchar_p)
        self._call_func: Callable[[c_wchar_p], int] = CALLERTYPE(call_ptr)
        self._call_func_threadsafe: Callable[[c_wchar_p], int] = CALLERTYPE(
            call_threadsafe_ptr
        )

        callback_data = json.loads(callbacks)
        self.globals_ptr = self.value_from_data(callback_data["globals_ptr"])
        self._set_ahk_attr = self.value_from_data(callback_data["set_ahk_attr"])
        self._get_ahk_attr = self.value_from_data(callback_data["get_ahk_attr"])

        return 0
