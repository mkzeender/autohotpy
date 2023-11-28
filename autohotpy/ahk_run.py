from __future__ import annotations
from typing import Any
from ahk_instance import AhkState, AhkInstance
import signal
from ctypes import windll

from autohotpy._ahk_object import AhkObject
from autohotpy.global_state import thread_state, config, global_state


def ahk_script(*script:str, wait_for:AhkState|None=AhkState.IDLE) -> AhkScript:
    if thread_state.current_script is None:
        thread_state.current_script = AhkScript(*script, wait_for=wait_for)

            #apply config 
        with global_state.lock:

            # if in main thread, hook into KeyboardInterrupts 
            if config.ctrl_c_exitapp and thread_state.is_main_thread:

                # signal.signal(signal.SIGINT, lambda num, frame: thread_state.current_script.ExitApp(-1073741510))
                # TODO
                signal.signal(signal.SIGINT, lambda num, frame: print('ctrl+c'))

            # set dpi scaling if not already done
            if config.dpi_scale_mode is not None and not global_state.dpi_mode_is_set:
                windll.shcore.SetProcessDpiAwareness(config.dpi_scale_mode)

                global_state.dpi_mode_is_set = True

    else:
        thread_state.current_script.add_script(*script, wait_for=wait_for)
        
    return thread_state.current_script


class AhkScript:
    def __init__(self, *script, wait_for:AhkState|None=AhkState.IDLE) -> None:
        self._inst:AhkInstance = AhkInstance(*script, wait_for=wait_for)

    def __getattr__(self, __name: str) -> Any:
        # return self._inst.get_global(__name)
        ...

    def __setattr__(self, __name: str, __value: Any) -> None:
        if __name == '_inst':
            super().__setattr__(__name, __value)
        else:
            # self._inst.set_global(__name, __value)
            ...

    def run_forever(self):
        self._inst.wait(AhkState.CLOSED)