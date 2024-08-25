from __future__ import annotations

from typing import Any, Callable, TYPE_CHECKING, NoReturn, TypeGuard
from xml.dom.minidom import Attr

from autohotpy import exceptions
from autohotpy._unset_type import UNSET, UnsetType
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
            if (lname := __name.lower()) != __name:
                try:
                    attr = getattr(self, lname)
                except AttributeError:
                    _not_found(self, __name)
            else:
                _not_found(self, __name)

        if isinstance(attr, AhkObject) and attr._ahk_immortal:
            # if the attr is an immortal global (i.e. a function), cache the result in self
            self.__dict__[__name] = attr
            self.__dict__[__name.lower()] = attr
        return attr

    def __dir__(self) -> set:
        return {"include", "run_forever"}  # TODO: fill this up!

    def __str__(self) -> str:
        return "<module autohotpy.ahk>"

    def IsSet(self, value: Any = UNSET, /):
        return value is not UNSET

    isset = IsSet
    UNSET: UnsetType = UNSET
    unset: UnsetType = UNSET


def _not_found(ahk, __name: str, /) -> NoReturn:
    raise AttributeError(
        f'No function, class, or global variable named "{__name}" exists',
        name=__name,
        obj=ahk,
    ) from None
