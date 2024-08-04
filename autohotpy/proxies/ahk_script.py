from __future__ import annotations

from typing import Any, Callable, TYPE_CHECKING

from autohotpy import exceptions
from autohotpy.proxies.ahk_object import AhkObject
from autohotpy.proxies._sqr_brac_syntax import square_bracket_syntax

if TYPE_CHECKING:
    from autohotpy.ahk_instance import AhkInstance


class AhkScript(AhkObject):
    def __init__(self, inst: AhkInstance) -> None:
        super().__init__(inst, pointer=None, type_name="Class", immortal=True)

    def include(self, *script_files: str) -> None:
        """Run the provided file. The ".ahk" extension can be omitted."""
        self._ahk_instance.add_script(*(f"#include {file}" for file in script_files))

    def run_forever(self) -> None:
        self._ahk_instance.run_forever()

    def __getitem__(self, item: str | slice) -> Callable:
        return square_bracket_syntax(self._ahk_instance, item)  # type: ignore

    def __getattr__(self, __name: str) -> Any:
        try:
            attr = super().__getattr__(__name)
        except exceptions.Error:
            raise AttributeError(
                f'Could not find global variable "{__name}" in ahk',
                name=__name,
                obj=self,
            )
        if isinstance(attr, AhkObject) and attr._ahk_immortal:
            # if the attr is immutable, cache the result
            self.__dict__[__name] = attr
        return attr

    def __dir__(self) -> set:
        return {"include", "run_forever"}  # TODO: fill this up!

    def __str__(self) -> str:
        return "<module autohotpy.ahk>"
