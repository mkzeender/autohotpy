from autohotpy.ahk_object import AhkObject


class BaseAhkException(Exception):
    pass


class AhkError(BaseAhkException):
    def __init__(self, err: AhkObject, *args: object) -> None:
        super().__init__(*args)


class ExitApp(BaseAhkException):
    def __init__(self, reason: str, code: int, *args: object) -> None:
        super().__init__(*args)
        self.code = code
        self.reason = reason

    def __str__(self) -> str:
        return f"Exit Code: {self.code}, Reason: {self.reason}"
