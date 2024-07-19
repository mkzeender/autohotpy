from typing import Literal, Self, TypeVar, overload

NumType = TypeVar("NumType", bound=Number)

Nothing = Literal[""]

BoolInt = Literal[0, 1]

Bool = BoolInt | bool

Number = bool | int | float

Primitive = Number | str

class VarRef[ValT]:
    def __new__(cls, initial_value: ValT = ...) -> Self: ...
    value: ValT

MouseButton = Literal[
    "Left",
    "Right",
    "Middle",
    "X1",
    "X2",
    "WheelUp",
    "WheelDown",
    "WheelLeft",
    "WheelRight",
]
