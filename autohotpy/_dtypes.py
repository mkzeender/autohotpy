from __future__ import annotations

from enum import StrEnum, auto

from typing import TYPE_CHECKING


class DTypes(StrEnum):
    NONE = auto()
    INT = auto()
    FLOAT = auto()
    STR = auto()
    AHK_OBJECT = auto()
    PY_OBJECT = auto()
    CLASS = auto()
    ERROR = auto()
