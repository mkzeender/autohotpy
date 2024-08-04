from __future__ import annotations
from collections.abc import Generator
from concurrent.futures import Future
from contextlib import contextmanager
from queue import Empty, Queue
from socket import timeout
import sys
from time import sleep, time
import traceback
from typing import TYPE_CHECKING, Any, NoReturn, final

from enum import StrEnum, auto
import threading
from ctypes import c_int, c_uint, c_wchar_p
from autohotpy.proxies.ahk_obj_factory import AhkObjFactory

from autohotpy.proxies.ahk_object import AhkObject
from autohotpy.proxies.ahk_script import AhkScript
from autohotpy.communicator import Communicator
from autohotpy.communicator.hotkey_factory import HotkeyFactory
from autohotpy.exceptions import AhkException, ExitApp
from .communicator import ahkdll


if TYPE_CHECKING:
    from autohotpy.static_typing import AhkBuiltins


class AhkState(StrEnum):
    IDLE = auto()
    CLOSED = auto()
    RUNNING = auto()
    INITIALIZING = auto()


class AhkInstance:
    def __init__(self, ctrl_c_exitapp: bool) -> None:
        self.ctrl_c_exitapp = ctrl_c_exitapp
        self._queue = Queue[tuple[c_wchar_p, Future[None]] | None](maxsize=1)
        self._addscript_queue = Queue[None](maxsize=1)

        self._error = None
        self._exit_code: int | None = None
        self._exit_reason: str = ""
        self._initialized = False

        self._thread_id = c_uint(ahkdll.new_thread("Persistent", "", "", c_int(1)))
        self._py_thread_id = threading.get_ident()
        self._ahk_mainthread: int | None = None

        self.communicator = Communicator(
            on_idle=self._autoexec_thread_callback,
            on_exit=self._exit_app_callback,
            on_error=self._error_callback,
            on_call=self._call_method_callback,
            post_init=self._post_init_callback,
        )

        # inject a backend library into the script, for communicating with python
        modded_script = self.communicator.create_init_script()
        self.add_script(modded_script)
        # self._post_init is called here from the ahk mainthread

        self._globals = AhkScript(self)

    def get_globals(self) -> AhkBuiltins:
        return self._globals  # type: ignore

    def add_script(self, *script_lines: str):
        if self._py_thread_id != threading.get_ident():
            raise RuntimeError(
                "Global-scope ahk statements cannot be run in the middle of a function. Try running this at the module level, or use a function instead."
            )

        self.check_exit()

        if self._initialized:
            # request the currently-paused script to go into persistent mode
            self._queue.put(None)

        # run the new script
        user_script: str = self.communicator.create_user_script(script_lines)
        self._add_script(user_script, runwait=2)

        while True:
            try:
                self._addscript_queue.get(timeout=0.5)
            except Empty:
                self.check_exit()
                continue
            self.check_exit()
            break

    def _add_script(self, script: str, runwait) -> None:
        ahkdll.add_script(script, c_int(runwait), self._thread_id)

    def check_exit(self):
        if self._exit_code is None:
            return
        if self._exit_code == -1073741510:
            raise KeyboardInterrupt() from None
        else:
            raise ExitApp(self._exit_reason, self._exit_code) from None

    def add_hotkey(self, factory: HotkeyFactory):
        factory.inst = self
        factory.create()

    def run_forever(self) -> NoReturn:

        # request the currently-paused script to go into persistent mode
        self._queue.put(None)
        while True:
            sleep(0.5)
            self.check_exit()  # raises ExitApp or KeyboardInterrupt when done

    def _call_autoexec(self, arg_data: c_wchar_p):
        fut = Future[None]()
        assert self._queue.empty()
        self._queue.put((arg_data, fut))

        while True:
            try:
                fut.result(timeout=0.5)
            except TimeoutError:
                self.check_exit()
                continue
            self.check_exit()
            break

    # @contextmanager
    # def mark_safe_thread(self) -> Generator[None, None, None]:
    #     id = threading.get_ident()
    #     new = id in self._safe_threads
    #     self._safe_threads.add(id)
    #     try:
    #         yield
    #     finally:
    #         if new:
    #             self._safe_threads.remove(id)

    def _autoexec_thread_callback(self):

        # wake up python's main thread
        self._addscript_queue.put(None)

        while True:
            task = self._queue.get()

            # set to None if something has been appended to the script.
            if task is None:
                return
            else:
                job, fut = task
                self.communicator.call_func(job)
                fut.set_result(None)

    def call_method(
        self,
        obj: AhkObject | None,
        method: str,
        args: tuple,
        kwargs: dict[str, Any] | None = None,
        factory: AhkObjFactory | None = None,
    ) -> Any:
        self.check_exit()

        if factory is None:
            factory = AhkObjFactory()
        factory.inst = self

        thread = threading.get_ident()
        if self._py_thread_id == thread:
            call = self._call_autoexec

        elif thread == self._ahk_mainthread:  # TODO: thread safety
            call = self.communicator.call_func

        else:
            call = self.communicator.call_func_threadsafe

        return self.communicator.call_method(obj, method, args, kwargs, factory, call)

    def get_attr(self, obj: Any, name: str) -> Any:
        if isinstance(obj, AhkScript):
            factory = None
        else:
            factory = AhkObjFactory(obj, name)
        return self.call_method(None, "_py_get_ahk_attr", (obj, name), None, factory)

    def set_attr(self, obj: AhkObject, name: str, value: Any):
        return self.call_method(None, "_py_set_ahk_attr", (obj, name, value))

    def free(self, obj: AhkObject):
        if obj._ahk_ptr is not None:
            self.communicator.free_ahk_obj(obj._ahk_ptr)

    def _post_init_callback(self):
        self._ahk_mainthread = threading.get_ident()
        self._initialized = True

    def _exit_app_callback(self, reason: str, code: int):
        self._exit_reason = reason
        self._exit_code = code
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
            if isinstance(e, AhkException):
                # e is a wrapper for the ahk Error object, so we unwrap it
                ret_val = e.wrapped_object
            else:
                ret_val = e
            success = False

        return success, ret_val
