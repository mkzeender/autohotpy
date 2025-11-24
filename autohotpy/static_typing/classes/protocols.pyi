from typing import Protocol

class HwndObject(Protocol):
    HWND: int

WinTitleFinder = HwndObject | int | str
