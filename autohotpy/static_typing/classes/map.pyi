from typing import Literal, Self
from autohotpy.static_typing.classes import BoolInt, Nothing
from autohotpy.static_typing.classes.func import Enumerator
from autohotpy.static_typing.classes.protocols import DoubleIterable, SingleIterable

class Map[KT, VT](SingleIterable[KT], DoubleIterable[KT, VT]):
    def __init__(
        self, key1: KT = ..., value1: VT = ..., /, *other_keys_and_values: KT | VT
    ): ...
    def Clear(self) -> Nothing: ...
    def Clone(self) -> Self: ...
    def Delete(self, key: KT, /) -> VT: ...
    def Get[DefaultT](self, key: KT, default: DefaultT = ..., /) -> VT | DefaultT: ...
    def Has(self, key: KT, /) -> BoolInt: ...
    def Set(
        self, key1: KT = ..., value1: VT = ..., /, *other_keys_and_values: KT | VT
    ) -> Self: ...
    def __Enum(self, n: int, /) -> Enumerator:
        """Implements for-loop and autohotpy.iterator()"""
    Count: int
    Capacity: int
    CaseSense: BoolInt | Literal["On", "Off", "Locale"]
    Default: VT

    __Item: Map[KT, VT]
