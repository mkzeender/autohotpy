from __future__ import annotations
from typing import Callable, TYPE_CHECKING, Any

if TYPE_CHECKING:
    from autohotpy.ahk_instance import AhkInstance

from autohotpy.communicator.hotkey_factory import HotkeyFactory


def square_bracket_syntax(inst: AhkInstance, arg) -> Callable[[Any], Any]:
    if isinstance(arg, str):
        inst.add_script(arg)
        return lambda x: None

    def decorator(func: Callable) -> Callable:
        inst.add_hotkey(HotkeyFactory(arg.start, func))
        return func

    if isinstance(arg, slice):
        if not isinstance(arg.start, str):
            raise TypeError(
                f"Expected a string before the double-colon, got {type(arg.start)}"
            )

        if arg.stop:
            raise ValueError(f'Unexpected "{arg.stop}"')

        if arg.step is None:
            return decorator

        if isinstance(arg.step, str):
            return square_bracket_syntax(inst, f"{arg.start}::{arg.step}")

        elif callable(arg.step):
            return decorator(arg.step)

    raise TypeError(arg)
