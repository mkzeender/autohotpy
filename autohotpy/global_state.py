from __future__ import annotations

from ctypes import windll
from dataclasses import field, dataclass
import signal
import threading
from threading import RLock, main_thread, get_ident
from typing import Literal, TYPE_CHECKING


if TYPE_CHECKING:
    from autohotpy.ahk_run import AhkScript


@dataclass
class _ThreadLocals(threading.local):
    current_script: AhkScript|None = None # the interpreter owned by this thread

    # whether this thread was spawned by the ahk interpreter
    # if current_instance is defined and this is true, then this thread behaves as the autoexecute thread of the ahk interpreter
    is_autoexec_thread: bool = True

    @property
    def is_main_thread(self):
        return get_ident() == main_thread().ident


@dataclass
class _GlobalState:
    lock:RLock = field(default_factory=RLock)
    dpi_mode_is_set:bool = False
    

@dataclass
class _Config:
    dpi_scale_mode: Literal[None, 0, 1, 2] = 2
    ctrl_c_exitapp: bool = True


config = _Config()
thread_state = _ThreadLocals()
global_state = _GlobalState()



