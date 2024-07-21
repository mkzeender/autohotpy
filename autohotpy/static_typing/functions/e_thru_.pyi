from autohotpy.static_typing.classes import protocols

def Edit() -> None:
    """Opens the current script for editing in the default editor."""

def EditGetCurrentCol(
    Control: protocols.WinTitleFinder,
    WinTitle: protocols.WinTitleFinder,
    WinText: str,
    ExcludeTitle: str,
    ExcludeText: str,
) -> int:
    """Returns the column number in an Edit control where the caret (text insertion point) resides."""

def EditGetCurrentLine(
    Control: protocols.WinTitleFinder,
    WinTitle: protocols.WinTitleFinder,
    WinText: str,
    ExcludeTitle: str,
    ExcludeText: str,
) -> int:
    """Returns the line number in an Edit control where the caret (text insert point) resides."""

def EditGetLine(
    N: int,
    Control: protocols.WinTitleFinder,
    WinTitle: protocols.WinTitleFinder,
    WinText: str,
    ExcludeTitle: str,
    ExcludeText: str,
) -> str:
    """Returns the text of the specified line in an Edit control"""

def EditGetLineCount(
    Control: protocols.WinTitleFinder,
    WinTitle: protocols.WinTitleFinder,
    WinText: str,
    ExcludeTitle: str,
    ExcludeText: str,
) -> int:
    """Returns the number of lines in an Edit control."""
