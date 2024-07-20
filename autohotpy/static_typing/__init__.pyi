from typing import Callable
import typing

from autohotpy.static_typing import classes

from autohotpy.static_typing.classes import (
    array,
    buffer,
    class_,
    error,
    file,
    func,
    inputhook,
    object_,
    map,
)
from autohotpy.static_typing.functions import a_thru_d

class AhkBuiltinsMeta(type):
    def __getattr__(self, name: str) -> typing.Any: ...  # Enables arbitrary name lookup
    def __setattr__(self, name: str, value: typing.Any) -> None: ...

class AhkBuiltins(a_thru_d.AThruD, metaclass=AhkBuiltinsMeta):
    def __getattr__(self, name: str) -> Any: ...  # Enables arbitrary name lookup
    def __setattr__(self, name: str, value: Any) -> None: ...
    def __class_getitem__(
        cls, item: str | slice
    ) -> Callable: ...  # square bracket syntax!
    @staticmethod
    def include(*script_files: str) -> None:
        """Run the provided file. The ".ahk" extension can be omitted."""
    Any = typing.Any
    Number = classes.Number
    Primitive = classes.Primitive

    Object = object_.Object
    Array = array.Array
    Buffer = buffer.Buffer
    ClipboardAll = buffer.ClipboardAll
    Class = class_.Class
    Error = error.Error

    class MemoryError(Error): ...

    class OSError(Error):
        Number: int

    class TargetError(Error): ...
    class TimeoutError(Error): ...
    class TypeError(Error): ...
    class UnsetError(Error): ...
    class MemberError(UnsetError): ...
    class PropertyError(MemberError): ...
    class MethodError(MemberError): ...
    class UnsetItemError(UnsetError): ...
    class ValueError(Error): ...
    class IndexError(ValueError): ...
    class ZeroDivisionError(Error): ...
    File = file.File
    Func = func.Func
    BoundFunc = func.BoundFunc
    Closure = func.Closure
    Enumerator = func.Enumerator
    Gui: Any
    InputHook = inputhook.InputHook
    Map = map.Map
    VarRef = classes.VarRef
