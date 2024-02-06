from __future__ import annotations
from typing import TYPE_CHECKING

# from autohotpy.proxies.ahk_object import AhkObject


def _fmt_item(item):
    if isinstance(item, tuple):
        params = item
    else:
        params = (item,)

    return params
