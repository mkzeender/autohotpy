from typing import TYPE_CHECKING
from .global_state import config
from . import ahk_run
from .convenience.py_lib import pylib as Python


if TYPE_CHECKING:
    from autohotpy.static_typing import AhkBuiltins as ahk
else:
    ahk = ahk_run.run_str()
