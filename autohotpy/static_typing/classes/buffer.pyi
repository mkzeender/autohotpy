from typing import Protocol
from autohotpy.static_typing.classes.object_ import Object

class Buffer(Object):
    """
    Encapsulates a block of memory for use with advanced techniques such as DllCall, structures, StrPut and raw file I/O.
    """

    Ptr: int
    Size: int

class BufferLike(Protocol):
    Ptr: int
    Size: int

BufferOrAddress = BufferLike | int

class ClipboardAll(Buffer):
    """
    Creates an object containing everything on the clipboard (such as pictures and formatting).

    """

    def __init__(self, data: BufferOrAddress | int = ..., size=...) -> None: ...

    Data: BufferOrAddress
