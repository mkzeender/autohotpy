from __future__ import annotations

from typing import Callable, cast, overload, TypeVar, TYPE_CHECKING

from autohotpy.ahk_object import AhkObject
from autohotpy.communicator.hotkey_factory import HotkeyFactory

if TYPE_CHECKING:
    from autohotpy.ahk_instance import AhkInstance

Start = TypeVar("Start")
Stop = TypeVar("Stop")
Step = TypeVar("Step")

Func = TypeVar("Func", bound=Callable, covariant=True)


class AhkScript(AhkObject):
    def __init__(self, inst: AhkInstance) -> None:
        super().__init__(inst, pointer=None)

    def run_forever(self):
        self._ahk_instance.run_forever()

    @overload
    def __getitem__(self, item: str) -> None:
        ...

    @overload
    def __getitem__(self, item: slice) -> Callable[[Func], Func] | Func:
        ...

    # @overload
    # def __getitem__(self, item: Slice[str, None, Func]) -> Func:
    #     ...

    def __getitem__(self, item: str | slice):
        if isinstance(item, str):
            self._ahk_instance.add_script(item)
            return None

        def decorator(func: Func) -> Func:
            self._ahk_instance.add_hotkey(HotkeyFactory(item.start, item.step))
            return func

        decorator_ = cast(Callable[[Callable], Callable], decorator)

        if isinstance(item, slice):
            if not isinstance(item.start, str):
                raise TypeError(
                    f"Expected a string before the double-colon, got {type(item.start)}"
                )

            if isinstance(item.step, str):
                return self.__getitem__(f"{item.start}::{item.step}")

            if item.step is None:
                return decorator_

            elif callable(item.step):
                return decorator_(item.step)

        raise TypeError
