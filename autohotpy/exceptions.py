from functools import cached_property
from autohotpy.ahk_object import AhkObject


class BaseAhkException(Exception):
    pass


class AhkError(BaseAhkException):
    def __init__(self, err: AhkObject) -> None:
        super().__init__()
        self.error = err

    @cached_property
    def args(self):
        return self.error.Message, self.error.What, self.error.Extra

    @cached_property
    def msg(self):
        err_type = self.error._ahk_instance.call_method(None, "Type", (self.error,))
        f"{err_type}: {self.args[0]}, {self.args[2]}"

    def __str__(self):
        return (
            f'{self.error._ahk_instance.call_method(None, "Type", (self.error,), {})}'
        )


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
