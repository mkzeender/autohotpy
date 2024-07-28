from __future__ import annotations
from functools import cached_property
from typing import TYPE_CHECKING, Any, Protocol, cast

if TYPE_CHECKING:
    from autohotpy.proxies.ahk_object import AhkObject
    from autohotpy.static_typing.classes import error  # type: ignore
    from autohotpy.static_typing.classes import object_  # type: ignore


class ExceptionLike(Protocol):
    Message: str
    What: str
    Extra: str


_err_class_mapping: dict[str, type[AhkBaseException]] = {}


class AhkBaseException(BaseException):
    def __init_subclass__(cls, name: str = "") -> None:
        if not name:
            name = cls.__name__
        _err_class_mapping[name] = cls
        return super().__init_subclass__()


class ExitApp(SystemExit, AhkBaseException):
    def __init__(self, reason: str, code: int, *args: object) -> None:
        super().__init__(*args)
        self.code = code
        self.reason = reason

    def __str__(self) -> str:
        return f"Exit Code: {self.code}, Reason: {self.reason}"


class AhkException(AhkBaseException, Exception):
    wrapped_object: Any


class AhkNonErrorException(AhkException):
    wrapped_object: Any

    def __str__(self) -> str:
        return str(self.wrapped_object)


class Error(AhkException):
    wrapped_object: ExceptionLike

    # @cached_property
    # def args(self) -> tuple[str, str, str]:
    #     return (
    #         self.wrapped_object.Message,
    #         self.wrapped_object.What,
    #         self.wrapped_object.Extra,
    #     )

    # def args(self, val: tuple[str, str, str]) -> None:
    #     try:
    #         self.wrapped_object.Message = val[0]
    #         self.wrapped_object.What = val[1]
    #         self.wrapped_object.Extra = val[2]
    #     except IndexError:
    #         pass

    @cached_property
    def msg(self) -> str:
        msg = self.wrapped_object.Message
        if what := self.wrapped_object.What:
            msg += f'\nIn function "{what}"'
        if extra := self.wrapped_object.Extra:
            msg += ",\n" + extra
        return msg

    def __str__(self) -> str:
        return self.msg


class MemoryError(Error, MemoryError):
    pass


class OSError(Error, OSError):
    pass


class MemberError(Error, AttributeError):
    pass


class PropertyError(MemberError):
    pass


class MethodError(MemberError):
    pass


class IndexError(Error, IndexError):
    pass


class KeyError(IndexError, KeyError):
    pass


class ValueError(Error, ValueError):
    pass


def throw(err: Any):
    from autohotpy.proxies.ahk_object import AhkObject

    if isinstance(err, BaseException):
        raise err
    if isinstance(err, AhkObject):
        clsname = err._ahk_type_name
        if clsname in _err_class_mapping:
            wrapper = _err_class_mapping[clsname]()
        else:
            wrapper = AhkNonErrorException()
        if isinstance(wrapper, AhkException):
            wrapper.wrapped_object = err
        raise wrapper
