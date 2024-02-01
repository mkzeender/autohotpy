from ctypes import Array, c_char
from dataclasses import dataclass, field
import sys
from typing import TYPE_CHECKING

from autohotpy.communicator.dtypes import DTypes
from autohotpy.ahk_object import AhkObject

if TYPE_CHECKING:
    from autohotpy.ahk_instance import AhkInstance


SIZE = 8


def _to_ptr(val: int) -> bytes:
    return val.to_bytes(SIZE, sys.byteorder, signed=False)


@dataclass
class FuncCaller:
    inst: AhkInstance
    args: list

    _arglist: list = field(default_factory=list)

    def to_bytes(self, obj, size=8) -> tuple[DTypes, bytes]:
        if isinstance(obj, int):
            return DTypes.INT, obj.to_bytes(SIZE, sys.byteorder, signed=True)
        elif isinstance(obj, AhkObject) and obj._ahk_ptr is not None:
            return DTypes.AHK_OBJECT, _to_ptr(obj._ahk_ptr)
        else:
            return DTypes.PY_OBJECT, _to_ptr(id(obj))

    def to_buffer(self, arr: list) -> tuple[Array, Array]:
        types = (c_char * len(arr))()  # 1 byte per entry
        data = (c_char * (len(arr) * SIZE))()  # 64 bits per entry

        for i, elem in enumerate(arr):
            dtype, dat = self.to_bytes(elem)
            if isinstance(dat, int):
                dat = dat.to_bytes(SIZE, sys.byteorder, signed=True)

            types[i] = dtype.value
            data[i * SIZE : (i + 1) * SIZE] = dat

        return types, data
