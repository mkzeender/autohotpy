from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from autohotpy.proxies.ahk_object import AhkObject


def _fmt_item(item):
    if isinstance(item, tuple):
        params = item
    else:
        params = (item,)

    return params


class Enumerator:
    def __init__(self, obj: AhkObject, nargs):
        enum = obj.__Enum()
        self.nargs = nargs

    def __iter__(self):
        return self

    def __next__(self):
        ...
