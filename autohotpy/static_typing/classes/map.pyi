from typing import Any, Literal, Self, overload, override
from autohotpy.static_typing.classes import BoolInt, Nothing
from autohotpy.static_typing.classes.func import Enumerator
from autohotpy.static_typing.classes.protocols import DoubleIterable, SingleIterable

class Map[KT, VT](SingleIterable[KT], DoubleIterable[KT, VT]):  # TODO: docs?S
    @overload
    def __new__[
        SelfT: Map
    ](
        cls: type[SelfT],
        key1: KT = ...,
        value1: VT = ...,
        /,
        *other_keys_and_values: KT | VT,
    ) -> SelfT: ...
    @overload
    def __new__(
        cls: type[Self],
        key1: KT = ...,
        value1: VT = ...,
        /,
        *other_keys_and_values: KT | VT,
        **kwargs: VT,
    ) -> Map[str | KT, VT]: ...
    def __init__(self, *args, **kwargs) -> None: ...
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

    def __getitem__(self, item: KT) -> VT: ...
