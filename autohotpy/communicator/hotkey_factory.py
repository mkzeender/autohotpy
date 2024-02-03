from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, TypeAlias


if TYPE_CHECKING:
    from autohotpy.proxies.ahk_object import AhkObject
    from autohotpy.ahk_instance import AhkInstance

    HotkeyAction: TypeAlias = Callable | str | AhkObject


@dataclass
class HotkeyFactory:
    sequence: str
    action: HotkeyAction
    inst: AhkInstance = field(init=False)

    def create(self):
        self.inst.add_script(self.make_script())

    def make_script(self) -> str:
        from autohotpy.proxies.ahk_object import AhkObject

        action = self.action
        seq = self.sequence
        if isinstance(action, AhkObject):
            ptr = action._ahk_ptr

            return f"""{seq}::
                {{
                    static obj := ObjFromPtrAddRef({ptr})
                    obj(ThisHotkey)
                }}"""

        elif isinstance(action, str):
            return f"{seq}::{action}"

        elif callable(action):
            ptr = self.inst.communicator.py_references.obj_to_immortal_ptr(action)
            return f"""{seq}::
            {{
                static obj := _py_object_from_id({ptr})
                obj(ThisHotkey)
            }}
            """
        else:
            raise TypeError
