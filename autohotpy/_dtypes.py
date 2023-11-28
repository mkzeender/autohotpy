from __future__ import annotations

import ctypes
from enum import IntEnum, auto

from ctypes import Array, c_buffer, c_char, POINTER, c_char_p, c_wchar, cast, create_string_buffer, pointer, _Pointer, resize, sizeof
from typing import TYPE_CHECKING, assert_type

from autohotpy._ahk_object import AhkObject

if TYPE_CHECKING:
    from autohotpy.ahk_instance import AhkInstance

BLOCK_SIZE = 64

CBUFFER = POINTER(c_char)


class DTypes(IntEnum):
    ENDARRAY = auto()
    NONE = auto()
    INT = auto()
    FLOAT = auto()
    STR = auto()
    STR_LONG = auto()
    OBJECT = auto()
    CLASS = auto()
    ERROR = auto()


def values_from_buffer(buffer_ptr:int, offset, ahk_instance:AhkInstance, bound_to:AhkObject|None = None):

    ptr = buffer_ptr+offset
    
    while True:

        dtype = DTypes(ctypes.c_int64.from_address(ptr).value)
        ptr += 1

        if dtype == DTypes.ENDARRAY:
            return ptr - buffer_ptr

        elif dtype == DTypes.NONE:
            yield None

        elif dtype == DTypes.INT:
            yield ctypes.c_int64.from_address(ptr).value
            ptr += 8

        elif dtype == DTypes.FLOAT:
            yield ctypes.c_double.from_address(ptr).value
            ptr += 8

        elif dtype == DTypes.STR:
            val = ctypes.wstring_at(ptr)
            ptr += len(val)*2 + 2
            yield val

        elif dtype == DTypes.STR_LONG:
            raise RuntimeError

        elif dtype == DTypes.OBJECT:
            yield AhkObject(
                inst=ahk_instance,
                bound_to=bound_to,
                pointer=ctypes.c_int64.from_address(ptr)
            )
            ptr += 8

        else:
            raise TypeError


def _put(value, dtype, c_type, buf, offset, space_estimate):

    req_size = offset + 1 + sizeof(value)

    if req_size > sizeof(buf):
        new_size = req_size + space_estimate
        
        resize(buf, new_size)

        

    

    return buf, offset


def values_to_buffer(*values):

    offset = 0
    
    buf = ctypes.create_string_buffer(0)

    for i, value in enumerate(values):

        if value is None:
            dtype = DTypes.NONE
            c_type = (c_char*0)
            
        elif isinstance(value, int):
            dtype = DTypes.INT
            c_type = ctypes.c_int64

        elif isinstance(value, float):
            dtype = DTypes.FLOAT
            c_type = ctypes.c_double

        elif isinstance(value, str):
            dtype = DTypes.STR
            c_type = ctypes.c_wchar * (len(value) + 1)

        else:
            dtype = DTypes.OBJECT
            c_type = ctypes.c_int64


        req_size = offset + 1 + sizeof(c_type)
        
        if req_size > sizeof(buf):
            new_size = req_size + (len(values)-i)*9
        
            resize(buf, new_size)

            buf_p = ctypes.cast(buf, ctypes.c_void_p).value
            assert type(buf_p) == int

            new_buf = (c_char*new_size).from_address(buf_p)
        else:
            buf_p = ctypes.cast(buf, ctypes.c_void_p).value
            new_buf = buf

        assert type(buf_p) == int

        ctypes.c_byte.from_address(buf_p+offset).value = dtype.value

        c_type.from_address(buf_p+offset+1).value = value

        buf = new_buf
        
        
    


    buf = create_string_buffer(0, BLOCK_SIZE+offset)