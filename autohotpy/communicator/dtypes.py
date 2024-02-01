from __future__ import annotations
from dataclasses import dataclass

from enum import Enum, StrEnum, auto, nonmember
from typing import Any


class DTypes(StrEnum):
    NONE = auto()
    INT = auto()
    FLOAT = auto()
    STR = auto()
    AHK_OBJECT = auto()
    AHK_IMMORTAL = auto()
    PY_OBJECT = auto()
    PY_IMMORTAL = auto()
    CLASS = auto()
    ERROR = auto()


@dataclass
class DT:
    type: type | None

    enum_val: int = 0
    enum_name: str = ""

    def check_inst(self, obj: Any) -> bool:
        return self.type is not None and isinstance(obj, self.type)


class DTypesFut(Enum):
    NONE = DT(type(None))
    INT = DT(int)
    FLOAT = DT(float)
    STR = DT(str)
    AHK_OBJECT = DT(None)
    AHK_IMMORTAL = DT(None)
    PY_OBJECT = DT(None)
    PY_IMMORTAL = DT(None)
    CLASS = DT(type)
    ERROR = DT(None)

    @nonmember
    @classmethod
    def from_value(cls, value):
        for member in cls:
            if member.value.check_inst(value):
                return value


for i, member in enumerate(DTypesFut):
    member.value.enum_val = i
    member.value.enum_name = member.name
