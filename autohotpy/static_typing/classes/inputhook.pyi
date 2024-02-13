from typing import Any, Callable, Literal
from autohotpy.static_typing.classes import Bool, BoolInt, Nothing
from autohotpy.static_typing.classes.object_ import Object

EndReason_ = Literal["Stopped", "Max", "Timeout", "Match", "EndKey", ""]

class InputHook(Object):
    """Creates an object which can be used to collect or intercept keyboard input."""

    def __init__(
        self, options: str = ..., endkeys: str = ..., matchlist: str = ...
    ): ...
    def KeyOpt(self, Keys: str, KeyOptions: str) -> Nothing: ...
    def Start(self) -> Nothing: ...
    def Stop(self) -> Nothing: ...
    def Wait(self, timeout=...) -> EndReason_: ...
    @property
    def EndKey(self) -> str: ...
    @property
    def EndMods(self) -> str: ...
    @property
    def EndReason(self) -> EndReason_: ...
    @property
    def InProgress(self) -> BoolInt: ...
    @property
    def Input(self) -> str: ...
    @property
    def Match(self) -> str: ...

    OnEnd: Callable[[InputHook], Any] | Nothing
    OnChar: Callable[[InputHook, str], Any] | Nothing
    OnKeyDown: Callable[[InputHook, int, int], Any] | Nothing
    OnKeyUp: Callable[[InputHook, int, int], Any] | Nothing

    BackspaceIsUndo: Bool
    CaseSensitive: Bool
    FindAnywhere: Bool
    MinSendLevel: int
    NotifyNonText: Bool
    Timeout: float
    VisibleNonText: Bool
    VisibleText: Bool
