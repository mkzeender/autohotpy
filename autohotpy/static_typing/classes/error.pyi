from autohotpy.static_typing.classes.object_ import Object

class Error(Object):
    """Error objects are thrown by built-in code when a runtime error occurs, and may also be thrown explicitly by the script."""

    def __init__(self, message, what=..., extra=...): ...

    Message: str
    What: str
    Extra: str
    File: str
    Line: int
    Stack: str

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
