from typing import Any
from autohotpy.static_typing.classes import object_

class RegExMatchInfo(object_.Object):
    """Determines whether a string contains a pattern (regular expression).

    WARNING: This object is not well-behaved in python. Consider using the python regex module instead.
    """

    def __getattr__(self, name) -> Any: ...
