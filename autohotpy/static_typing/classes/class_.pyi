from typing import Any
from autohotpy.static_typing.classes.object_ import Object

class Class(Object):
    """
    A Class object represents a class definition; it contains static methods and properties.


    """

    def __call__(self, *args: Any) -> Any:
        """Constructs a new instance of the class."""
    Prototype: Object
