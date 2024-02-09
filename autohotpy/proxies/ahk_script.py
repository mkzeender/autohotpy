from __future__ import annotations

from typing import Any, Callable, overload, TYPE_CHECKING

from autohotpy.proxies.ahk_object import AhkObject
from autohotpy.proxies.var_ref import VarRef
from autohotpy.proxies._sqr_brac_syntax import square_bracket_syntax

if TYPE_CHECKING:
    from autohotpy.ahk_instance import AhkInstance

# Start = TypeVar("Start")
# Stop = TypeVar("Stop")
# Step = TypeVar("Step")

# Func = TypeVar("Func", bound=Callable, covariant=True)


class AhkScript(AhkObject):
    def __init__(self, inst: AhkInstance) -> None:
        super().__init__(inst, pointer=None)

    def include(self, *script_files: str) -> None:
        """Run the provided file. The ".ahk" extension can be omitted."""
        self._ahk_instance.add_script(*(f"#include {file}" for file in script_files))

    def run_forever(self) -> None:
        self._ahk_instance.run_forever()

    def __getitem__(self, item: str | slice) -> Callable:
        return square_bracket_syntax(self._ahk_instance, item)  # type: ignore
