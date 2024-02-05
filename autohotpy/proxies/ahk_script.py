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

    def run_forever(self) -> None:
        self._ahk_instance.run_forever()

    @overload
    def ref(self, initial_value: Any) -> VarRef: ...

    @overload
    def ref(self, *initial_values: Any) -> tuple[VarRef, ...]: ...

    def ref(self, *vals):  # type: ignore
        """
        Returns a VarRef. VarRefs must be used for any function that expects ByRef
        parameters. You may provide multiple arguments to create multiple VarRefs at once.

        For example:
        >>>x, y = ahk.ref(0, 0)
        >>>MouseGetPos(x, y)
        >>>print("the mouse is at", x.value, y.value)

        """
        if len(vals) == 0:
            return self._py_create_ref("")
        elif len(vals) == 1:
            return self._py_create_ref(vals[0])
        else:
            return tuple(self._py_create_ref(v) for v in vals)

    def __getitem__(self, item: str | slice) -> Callable:
        return square_bracket_syntax(self._ahk_instance, item)  # type: ignore
