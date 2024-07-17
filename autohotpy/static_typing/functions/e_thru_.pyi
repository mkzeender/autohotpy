from typing import Any, Callable, Literal, overload
from autohotpy.proxies.var_ref import VarRef

from autohotpy.static_typing.classes import (
    Primitive,
    buffer,
    com_obj,
    object_,
    protocols,
    array,
    Bool,
    BoolInt,
    NumType,
    Number,
    Nothing,
    MouseButton,
)

class EThruBlah:
    @staticmethod
    def Edit() -> None:
        """Opens the current script for editing in the default editor."""

    @staticmethod
    def EditGetCurrentCol(Control:protocols.WinTitleFinder , WinTitle:protocols.WinTitleFinder, WinText: str, ExcludeTitle: str, ExcludeText:str) -> int:
        """Returns the column number in an Edit control where the caret (text insertion point) resides."""

    @staticmethod
    def EditGetCurrentLine(Control:protocols.WinTitleFinder , WinTitle:protocols.WinTitleFinder, WinText: str, ExcludeTitle: str, ExcludeText:str) -> int:
        """Returns the line number in an Edit control where the caret (text insert point) resides."""

    @staticmethod
    def EditGetLine(N: int, Control:protocols.WinTitleFinder , WinTitle:protocols.WinTitleFinder, WinText: str, ExcludeTitle: str, ExcludeText:str) -> str:
        """Returns the text of the specified line in an Edit control"""

    @staticmethod
    def EditGetLineCount(Control:protocols.WinTitleFinder , WinTitle:protocols.WinTitleFinder, WinText: str, ExcludeTitle: str, ExcludeText:str) -> int:
        """Returns the number of lines in an Edit control."""

    