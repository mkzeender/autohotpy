from __future__ import annotations
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from autohotpy.proxies.ahk_object import AhkBoundProp, AhkObject
from autohotpy.proxies.var_ref import VarRef

if TYPE_CHECKING:
    from autohotpy.ahk_instance import AhkInstance


@dataclass(slots=True)
class AhkObjFactory:
    bind_to: AhkObject | None = None
    bound_method_name: str = ""
    inst: AhkInstance = field(init=False)

    def create(self, ptr: int) -> AhkObject:
        if self.inst is None:
            raise RuntimeError("Unable to create ahk proxy object")
        if self.bind_to is None:
            return AhkObject(self.inst, pointer=ptr)
        else:
            return AhkBoundProp(
                self.inst,
                pointer=ptr,
                bound_to=self.bind_to,
                method_name=self.bound_method_name,
            )

    def create_varref(self, ptr: int) -> VarRef:
        if self.inst is None:
            raise RuntimeError("Unable to create ahk proxy object")
        return VarRef(self.inst, pointer=ptr)
