from __future__ import annotations
import sys
import traceback
from typing import Any

from enum import StrEnum, auto
import os
import threading
from ctypes import c_int, c_uint, c_wchar_p
from autohotpy.proxies.ahk_obj_factory import AhkObjFactory

from autohotpy.proxies.ahk_object import AhkObject
from autohotpy.proxies.ahk_script import AhkScript
from autohotpy.communicator import Communicator
from autohotpy.communicator.hotkey_factory import HotkeyFactory
from autohotpy.exceptions import ExitApp, throw
from .communicator.ahkdll import ahkdll

from .global_state import thread_state


class AhkState(StrEnum):
    IDLE = auto()
    CLOSED = auto()
    RUNNING = auto()
    INITIALIZING = auto()


class AhkInstance:
    def __init__(self, *script) -> None:
        thread_state.current_instance = self
        self._autoexec_condition = threading.Condition()
        self._job_queue: c_wchar_p | bool = False

        self._error = None
        self._exit_code: int | None = None
        self._exit_reason: str = ""
        self.state: AhkState = AhkState.INITIALIZING

        # starting ahk will change the working directory (for some reason)
        # so we save and restore it
        cwd = os.getcwd()

        self._thread_id = c_uint(ahkdll.NewThread("Persistent", "", "", c_int(1)))
        self._py_thread_id = threading.get_ident()

        os.chdir(cwd)

        self.communicator = Communicator(
            on_idle=self._autoexec_thread_callback,
            on_exit=self._exit_app_callback,
            on_error=self._error_callback,
            on_call=self._call_method_callback,
        )

        # inject a backend library into the script, for communicating with python
        modded_script = self.communicator.create_init_script()

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
            user_script: str = self.communicator.create_user_script(script)
            self._add_script(user_script, runwait=2)

            # wait for it to pass control back to this thread.
            while self.state == AhkState.RUNNING:
                cond.wait(timeout=1)

    def _add_script(self, script: str, runwait) -> None:
        ahkdll.addScript(script, c_int(runwait), self._thread_id)

    def add_hotkey(self, factory: HotkeyFactory):
        factory.inst = self
        factory.create()

    def _match_state(self, state):
        if self.state == state:
            return True
        elif state != self.state == AhkState.CLOSED:
            assert self._exit_code is not None
            raise ExitApp(self._exit_reason, self._exit_code)

    def run_forever(self) -> None:
        with (cond := self._autoexec_condition):
            # indicate to Ahk's main thread that it can go into persistent mode
            self._job_queue = True
            self._autoexec_condition.notify_all()
            while not self.state == AhkState.CLOSED:
                # Timeout allows for KeyboardInterrupts if you're in the main thread.
                cond.wait(timeout=1)

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
                    self.communicator.call_func(job)
                    self._job_queue = False
                    cond.notify_all()

    def call_method(
        self,
        obj: AhkObject | None,
        method: str,
        args: tuple,
        kwargs: dict[str, Any] | None = None,
        factory: AhkObjFactory | None = None,
    ) -> Any:
        if factory is None:
            factory = AhkObjFactory()
        factory.inst = self

        thread_type = thread_state.get_thread_type(self)
        if thread_type == "ahk":
            call = self.communicator.call_func
        elif thread_type == "external":
            call = self.communicator.call_func_threadsafe
        else:  # thread_type == 'autoexec'
            call = self._call_autoexec

        return self.communicator.call_method(obj, method, args, kwargs, factory, call)

    def get_attr(self, obj: Any, name: str) -> Any:
        if isinstance(obj, AhkScript):
            factory = None
        else:
            factory = AhkObjFactory(obj, name)
        return self.call_method(None, "_py_get_ahk_attr", (obj, name), None, factory)

    def set_attr(self, obj: Any, name: str, value: Any):
        return self.call_method(None, "_py_set_ahk_attr", (obj, name, value))

    def _exit_app_callback(self, reason, code):
        with self._autoexec_condition:
            self._exit_code = code
            self._exit_reason = reason
            self.state = AhkState.CLOSED
            self._autoexec_condition.notify_all()
            return 0

    def _error_callback(self, e):
        if isinstance(e, BaseException):
            print("Python exception ignored in Autohotkey thread:", file=sys.stderr)
            traceback.print_exception(e)
            return 1
        return 0

    def _call_method_callback(self, data: dict) -> tuple[bool, Any]:
        factory = AhkObjFactory()
        factory.inst = self

        vfd = self.communicator.value_from_data  # method alias

        # always a python object or function
        obj = vfd(data["obj"], factory=None)
        # always a string, no factory needed.
        method_name: str = vfd(data["method"], factory=None)

        args = [vfd(arg, factory=factory) for arg in data["args"]]
        kwargs = {}
        # kwargs = {k: vfd(v, factory=factory) for k, v in data["kwargs"].items()}

        if method_name:
            func = getattr(obj, method_name)
        else:
            func = obj

        try:
            ret_val = func(*args, **kwargs)
            success = True
        except BaseException as e:
            ret_val = e
            success = False

        return success, ret_val
