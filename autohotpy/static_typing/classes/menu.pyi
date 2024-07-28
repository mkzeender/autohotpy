from typing import Any, Callable, Self
from autohotpy.static_typing.classes import Bool, Nothing, object_

class Menu(object_.Object):  # TODO
    """Provides an interface to create and modify a menu or menu bar, add and modify menu items, and retrieve information about the menu or menu bar."""

    def Add(
        self,
        menu_item_name: str = ...,
        callback_or_submenu: Callable[[str, int, Self], Any] | Menu = ...,
        options: str = ...,
        /,
    ) -> Nothing:
        """Adds or modifies a menu item."""

    def AddStandard(self) -> Nothing:
        """Adds the standard tray menu items."""

    def Check(self, menu_item_name: str) -> Nothing:
        """Adds a visible checkmark in the menu next to a menu item (if there isn't one already)."""

    def Delete(self, menu_item_name: str = ...) -> Nothing:
        """Deletes one or all menu items."""

    def Disable(self, menu_item_name: str) -> Nothing:
        """Grays out a menu item to indicate that the user cannot select it."""

    def Enable(self, menu_item_name: str) -> Nothing:
        """Allows the user to once again select a menu item if it was previously disabled (grayed out)."""

    def Insert(
        self,
        menu_item_name: str = ...,
        item_to_insert: str = ...,
        callback_or_submenu: Callable[[str, int, Self], Any] | Menu = ...,
        options: str = ...,
    ) -> Nothing:
        """Inserts a new item before the specified item."""

    def Rename(self, menu_item_name: str, new_name: str = ...) -> Nothing:
        """Renames a menu item."""

    def SetColor(
        self, color_value: str | int = "Default", apply_to_submenus: Bool = True
    ) -> Nothing:
        """Changes the background color of the menu."""

    def SetIcon(
        self,
        menu_item_name: str,
        filename: str,
        icon_number: int = 1,
        icon_width: int = ...,
    ) -> Nothing:
        """Sets the icon to be displayed next to a menu item."""

    def Show(self, x: int = ..., y: int = ...) -> Nothing:
        """Displays the menu."""

    def ToggleCheck(self, menu_item_name: str) -> Nothing:
        """Adds a checkmark if there wasn't one; otherwise, removes it."""

    def ToggleEnable(self, menu_item_name: str) -> Nothing:
        """Disables a menu item if it was previously enabled; otherwise, enables it."""

    def UnCheck(self, menu_item_name: str) -> Nothing:
        """Removes the checkmark (if there is one) from a menu item."""
    ClickCount: int
    Default: str
    Handle: int

class MenuBar(Menu): ...
