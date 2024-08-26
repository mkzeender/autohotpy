from typing import TYPE_CHECKING
from .global_state import config
from .convenience.py_lib import pylib as Python
from .ahk_run import get_ahk
from ._unset_type import UNSET
from .proxies._seq_iter import iterator


if TYPE_CHECKING:
    import autohotpy.static_typing

    ahk = autohotpy.static_typing.AhkBuiltins()


__all__ = ["ahk", "Python", "config", "UNSET", "iterator"]


def __getattr__(__name):
    global ahk
    if __name == "ahk":
        ahk = get_ahk()
        return ahk

    import sys

    raise AttributeError(
        f"autohotpy has no attribute named {__name}",
        name=__name,
        obj=sys.modules[__name__],
    )
