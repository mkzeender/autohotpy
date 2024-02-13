from typing import Generic, TypeVar
from autohotpy.static_typing.classes import Nothing
from autohotpy.static_typing.classes.object_ import Object

KT = TypeVar("KT")
VT = TypeVar("VT")

class Map(Object, Generic[KT, VT]):
    def __init__(self, key1: KT = ..., key2: VT = ..., /, *keys_and_vals: KT | VT): ...
    def Clear(self) -> Nothing: ...
