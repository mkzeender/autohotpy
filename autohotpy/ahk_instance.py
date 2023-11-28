from __future__ import annotations

from ctypes import CFUNCTYPE, POINTER, c_char, c_int, c_uint, c_void_p, c_wchar, c_wchar_p, cast, c_ssize_t, Array, c_int64
from enum import StrEnum, auto
import os
import threading

from autohotpy.exceptions import ExitApp
from ._ahkdll import ahkdll
from ._script_injection import create_injection_script, create_user_script, Callbacks
from ._ahk_object import AhkObject
from .references import References
from autohotpy import global_state


class AhkState(StrEnum):
    IDLE = auto()
    CLOSED = auto()
    RUNNING = auto()


class AhkInstance:
    def __init__(self, *script:str, wait_for:AhkState|None=AhkState.IDLE) -> None:
        
        self._references = References()
        self._str_references = References()
        self._closed_condition = threading.Condition()
        self._error = None
        self._exit_code:int|None = None
        self._exit_reason:str = ''
        self._state:AhkState = AhkState.RUNNING

        self._callbacks = Callbacks(
            get=CFUNCTYPE(c_int, c_int64, c_wchar_p, POINTER(c_char*64))(self._get_attr_callback),
            set=self._set_attr_callback,
            call=self._call_callback,
            get_str=self._get_str_callback,
            free_obj=self._free_obj_callback,
            exit_app=CFUNCTYPE(c_int, c_wchar_p, c_int64)(self._exit_app_callback),
            idle = CFUNCTYPE(None)(self._idle_callback)
        )


        # starting ahk will change the working directory (for some reason), so we save and restore it
        cwd = os.getcwd()

        self._thread_id = c_uint(ahkdll.NewThread('Persistent', '', '', c_int(1)))

        os.chdir(cwd)

        # inject a backend library into the script, for communicating with python
        modded_script = create_injection_script(self._callbacks)
        print(modded_script)
        
        self._add_script(modded_script, wait=True, execute=True)

        if script:
            self._add_script(create_user_script(script, self._callbacks), execute=True, wait=(wait_for==AhkState.IDLE))
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
    def state(self, value:AhkState):
        if self._state == AhkState.CLOSED:
            return
        self._state = value
        

    def add_script(self, *script:str, wait_for:AhkState|None=AhkState.IDLE):
        # wait for the script to either close or become idle
        with self._closed_condition:
            self.wait(AhkState.IDLE)
            assert self.state == AhkState.IDLE

            # mark the script as running again!
            self.state = AhkState.RUNNING
            self._closed_condition.notify_all()

        user_script:str = create_user_script(script, self._callbacks)
        self._add_script(user_script, wait=(wait_for == AhkState.IDLE), execute=True)
        
        if wait_for == AhkState.CLOSED:
            self.wait(AhkState.CLOSED)
        elif wait_for == AhkState.IDLE and self.state == AhkState.CLOSED:
            assert self._exit_code is not None
            raise ExitApp(self._exit_reason, self._exit_code)

    def _add_script(self, script:str, *, wait=True, execute=True, starting=False) -> None:
        
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
        

    def wait(self, wait_for:AhkState=AhkState.IDLE) -> None:
        with self._closed_condition:
            while not self._closed_condition.wait_for(lambda: self._match_state(wait_for), timeout=1):
                # DONT DELETE, this no-op checks for KeyboardInterrupts if you're in the main thread.
                pass

    # def _call_py_function(self, func: CFUNCTYPE(c_wchar_p), *args): # TODO
    #     func_address = str(cast(func, c_void_p).value)
    #     args_list = list(args) + [c_void_p()] * (9-len(args))
        
    #     ahkdll.ahkFunction('_call_py_function', func_address, *([c_void_p()]*9), self._thread_id)

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
            gotten = (str(gotten))
            assert self._str_reference is None
            self._str_reference = gotten
            return len(gotten)          

    def _get_str_callback(self, outstr: Array):
        outstr.value = self._str_reference
        self._str_reference = None

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
            print('we are idle')
            self.state = AhkState.IDLE
            self._closed_condition.notify_all()
            