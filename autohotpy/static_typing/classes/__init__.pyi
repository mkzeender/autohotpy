from typing import Literal, Protocol, Self

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

class Prototype(Protocol):
    __Class: str
    base: Prototype | Nothing
