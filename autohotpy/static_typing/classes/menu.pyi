from typing import Any, Self
from autohotpy.static_typing.classes import object_
from autohotpy.static_typing.classes.func import Func

class Menu(object_.Object):
    def Add(
        self,
        menu_item_name: str = ...,
        callback_or_submenu: Func[[str, int, Self], Any] = ...,
        options: str = ...,
        /,
    ): ...

class MenuBar(Menu): ...
