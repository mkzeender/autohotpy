from typing import Callable
import typing

from autohotpy.static_typing import classes

from autohotpy.static_typing.classes import (
    array,
    buffer,
    class_,
    com_obj,
    error,
    file,
    func,
    gui,
    inputhook,
    menu,
    object_,
    map,
    regex_match_info,
)
from autohotpy.static_typing.functions import a_thru_d, e_thru_

class AhkBuiltinsMeta(type):
    def __getattr__(self, name: str) -> typing.Any: ...  # Enables arbitrary name lookup
    def __setattr__(self, name: str, value: typing.Any) -> None: ...

class AhkBuiltins(a_thru_d.AThruD, e_thru_.EThruBlah, metaclass=AhkBuiltinsMeta):
    def __getattr__(self, name: str) -> typing.Any: ...  # Enables arbitrary name lookup
    def __setattr__(self, name: str, value: typing.Any) -> None: ...
    def __class_getitem__(
        cls, item: str | slice
    ) -> Callable: ...  # square bracket syntax!
    def __getitem__(self, item: str | slice) -> Callable: ...  # square bracket syntax!
    @staticmethod
    def include(*script_files: str) -> None:
        """Run the provided file. The ".ahk" extension can be omitted."""

    @staticmethod
    def run_forever() -> None:
        """Run the ahk event loop."""
    Any = typing.Any
    Object = object_.Object
    Array = array.Array
    Buffer = buffer.Buffer
    ClipboardAll = buffer.ClipboardAll
    Class = class_.Class

    # Error = error.Error # TODO: Error typing
    # MemoryError = error.MemoryError
    # OSError = error.OSError
    # TargetError = error.TargetError
    # TimeoutError = error.TimeoutError
    # TypeError = error.TypeError
    # UnsetError = error.UnsetError
    # MemberError = error.MemberError
    # Property ...

    File = file.File
    Func = func.Func
    BoundFunc = func.BoundFunc
    Closure = func.Closure
    Enumerator = func.Enumerator
    Gui = gui.Gui
    InputHook = inputhook.InputHook
    Map = map.Map
    Menu = menu.Menu
    MenuBar = menu.MenuBar
    RegExMatchInfo = regex_match_info.RegExMatchInfo

    Primitive = classes.Primitive
    Number = classes.Number
    Float = float
    Integer = int
    String = str
    VarRef = classes.VarRef
    ComValue = com_obj.ComValue
    ComObjArray = com_obj.ComObjArray
    ComObject = com_obj.ComObject
    ComValueRef = com_obj.ComValueRef
