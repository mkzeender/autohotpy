from typing import Any

from autohotpy.static_typing.classes import object_

class Gui(object_.Object):
    class Control(object_.Object):
        def __getattr__(self, __name: str) -> Any: ...  # TODO: gui typing

    def __getattr__(self, __name: str) -> Any: ...  # TODO: gui typing
