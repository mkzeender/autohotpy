from __future__ import annotations
from threading import RLock
import threading
from typing import TYPE_CHECKING


# import sys
# from typing import Any
# from autohotpy.ahk_instance import AhkInstance
# import signal
from ctypes import windll

# from autohotpy.proxies.ahk_script import AhkScript
from autohotpy.global_state import config, global_state


# def run_str(*script: str) -> AhkScript:
#     if thread_state.current_instance is None:
#         # apply config
#         with global_state.lock:
#             # if in main thread, hook into KeyboardInterrupts
#             if config.ctrl_c_exitapp and thread_state.is_main_thread:
#                 # signal.signal(signal.SIGINT, lambda num, frame: thread_state.current_script.ExitApp(-1073741510))
#                 # TODO
#                 signal.signal(signal.SIGINT, lambda num, frame: sys.exit())

#             # set dpi scaling if not already done
#             if config.dpi_scale_mode is not None and not global_state.dpi_mode_is_set:
#                 windll.shcore.SetProcessDpiAwareness(config.dpi_scale_mode)

#                 global_state.dpi_mode_is_set = True

#         AhkInstance(*script)

#     elif not thread_state.is_autoexec_thread:
#         raise RuntimeError(
#             "Autohotkey scripts can only be loaded by the auto-execute thread."
#         )
#     else:
#         thread_state.current_instance.add_script(*script)

#     assert thread_state.current_instance is not None

#     return AhkScript(thread_state.current_instance)


# def include(script: str | None = None) -> AhkScript:
#     if script is not None:
#         return run_str(f"#include {script}")
#     else:
#         return run_str()

lock = RLock()


if TYPE_CHECKING:
    from autohotpy.static_typing import AhkBuiltins


_ahk: AhkBuiltins | None = None


def get_ahk() -> AhkBuiltins:
    global _ahk
    if _ahk is None:
        with lock:
            if _ahk is None:
                if (
                    config.dpi_scale_mode is not None
                    and not global_state.dpi_mode_is_set
                ):
                    windll.shcore.SetProcessDpiAwareness(config.dpi_scale_mode)
                    global_state.dpi_mode_is_set = True

                _ahk = new_interpreter(
                    ctrl_c_exitapp=config.ctrl_c_exitapp
                    and threading.main_thread().ident == threading.get_ident()
                )

    return _ahk


def new_interpreter(ctrl_c_exitapp: bool = False) -> AhkBuiltins:
    from autohotpy.ahk_instance import AhkInstance

    with lock:
        instance = AhkInstance(ctrl_c_exitapp=ctrl_c_exitapp)

    return instance.get_globals()
