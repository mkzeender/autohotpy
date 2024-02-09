from typing import Literal, TypeVar

NumType = TypeVar("NumType", bound=Number)

Nothing = Literal[""]

BoolInt = Literal[0, 1]

Bool = BoolInt | bool

Number = bool | int | float

Primitive = Number | str

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
