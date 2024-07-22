import sys

from autohotpy import ahk as _ahk

sys.modules[__name__] = _ahk  # type: ignore
