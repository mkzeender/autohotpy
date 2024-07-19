from __future__ import annotations
from functools import cached_property
from typing import TYPE_CHECKING, Any, override

if TYPE_CHECKING:
    from autohotpy.proxies.ahk_object import AhkObject


class BaseAhkException(Exception):
    pass


class AhkError(BaseAhkException):
    def __init__(self, err: AhkObject) -> None:
        super().__init__()
        self.error = err

    @property
    def args(self) -> tuple[Any, Any, Any]:
        return self.error.Message, self.error.What, self.error.Extra

    @args.setter
    def args(self, val:tuple[Any, Any, Any]): # type: ignore # TODO: investigate this?
        try:
            self.error.Message = val[0]
            self.error.What = val[1]
            self.error.Extra = val[2]
        except IndexError:
            pass

    @cached_property
    def msg(self):
        err_type = self.error._ahk_instance.call_method(None, "Type", (self.error,))
        return f"{err_type}: {self.args[0]}, {self.args[2]}"

    def __str__(self):
        return self.msg


class ExitApp(BaseAhkException):
    def __init__(self, reason: str, code: int, *args: object) -> None:
        super().__init__(*args)
        self.code = code
        self.reason = reason

    def __str__(self) -> str:
        return f"Exit Code: {self.code}, Reason: {self.reason}"


def throw(exc_value: Exception | AhkObject):
    if isinstance(exc_value, BaseException):
        raise exc_value
    else:
        raise AhkError(exc_value)
