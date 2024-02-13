from typing import Any, Callable, Literal, overload
from autohotpy.proxies.var_ref import VarRef

from autohotpy.static_typing.classes import (
    Primitive,
    buffer,
    com_obj,
    object_,
    protocols,
    array,
    Bool,
    BoolInt,
    NumType,
    Number,
    Nothing,
    MouseButton,
)

class AThruD:
    @staticmethod
    def abs(n: NumType, /) -> NumType:
        """
        Returns the absolute value of the specified number.

        Value := Abs(Number)
        The return value is the same type as Number (integer or floating point).

        MsgBox Abs(-1.2) ; Returns 1.2
        """

    @staticmethod
    def ASin(n: Number, /) -> float:
        """
        Returns the arcsine (the number whose sine is the specified number) in radians.

        Value := ASin(Number)
        If Number is less than -1 or greater than 1, a ValueError is thrown.

        MsgBox ASin(0.2) ; Returns 0.201358
        """

    @staticmethod
    def ACos(n: Number, /) -> float:
        """
        Returns the arccosine (the number whose cosine is the specified number) in radians.

        Value := ACos(Number)
        If Number is less than -1 or greater than 1, a ValueError is thrown.

        MsgBox ACos(0.2) ; Returns 1.369438
        """

    @staticmethod
    def ATan(n: Number, /) -> float:
        """
        Returns the arctangent (the number whose tangent is the specified number) in radians.

        Value := ATan(Number)
        MsgBox ATan(1.2) ; Returns 0.876058

        """

    @staticmethod
    def BlockInput(
        mode: (
            Literal[
                "On",
                "Off",
                "Send",
                "Mouse",
                "SendAndMouse",
                "Default",
                "MouseMove",
                "MouseMoveOff",
            ]
            | Bool
        ),
        /,
    ) -> Nothing:
        """
        Disables or enables the user's ability to interact with the computer via keyboard and mouse.

        BlockInput OnOff
        BlockInput SendMouse
        BlockInput MouseMove
        """
    Buffer: type[buffer.Buffer]

    @staticmethod
    def CallbackCreate(
        func: Callable, options: str = ..., param_count: int = ..., /
    ) -> int:
        """
        Creates a machine-code address that when called, redirects the call to a function in the script.
        """

    @staticmethod
    def CallbackFree(address: int, /) -> Nothing:
        """Deletes a callback and releases its reference to the function object"""

    @staticmethod
    def CaretGetPos(OutputVarX: VarRef, OutputVarY: VarRef, /) -> BoolInt:
        """Retrieves the current position of the caret (text insertion point)."""

    @staticmethod
    def Ceil(n: Number, /) -> int:
        """Returns the specified number rounded up to the nearest integer (without any .00 suffix)."""

    @staticmethod
    def Chr(n: Number, /) -> str:
        """Returns the string (usually a single character) corresponding to the character code indicated by the specified number."""

    @staticmethod
    def Click(*options: MouseButton | Literal["Relative"] | int) -> Nothing:
        """
        Clicks a mouse button at the specified coordinates. It can also hold down a mouse button, turn the mouse wheel, or move the mouse.

        """
    ClipboardAll = buffer.ClipboardAll

    @staticmethod
    def ClipWait(timeout: Number = ..., binary_data: Bool = False, /) -> BoolInt:
        """Waits until the clipboard contains data"""

    @staticmethod
    def ComCall(
        Index: int, ComObj: ComValue | buffer.BufferOrAddress, /, *args_and_types
    ) -> str | int:
        """Calls a native COM interface method by index"""

    @staticmethod
    def ComObjActive(CLSID: str, /) -> ComValue:
        """Retrieves a registered COM object."""
    ComObjArray = com_obj.ComObjArray

    @staticmethod
    def ComObjConnect(
        ComObj: ComValue, PrefixOrSink: str | object_.Object = ..., /
    ) -> Nothing:
        """Connects a COM object's event source to the script, enabling events to be handled."""
    ComObject = com_obj.ComObject

    @staticmethod
    def ComObjFlags(ComObj: ComObject, NewFlags: int = ..., Mask: int = ..., /) -> int:
        """Retrieves or changes flags which control a COM wrapper object's behaviour."""

    @staticmethod
    def ComObjFromPtr(DispPtr: int, /) -> ComValue:
        """Wraps a raw IDispatch pointer (COM object) for use by the script."""

    @staticmethod
    def ComObjGet(Name: str, /) -> ComValue:
        """Returns a reference to an object provided by a COM component."""

    @overload
    @staticmethod
    def ComObjQuery(ComObj: ComValue, SID: str, IID: str, /) -> ComValue:
        """Queries a COM object for an interface or service."""

    @overload
    @staticmethod
    def ComObjQuery(ComObj: ComValue, IID: str, /) -> ComValue:
        """Queries a COM object for an interface or service."""

    @staticmethod
    def ComObjType(ComObj: ComValue, InfoType: str = ..., /):
        """Retrieves type information from a COM object."""

    @staticmethod
    def ComObjValue(ComObj: ComValue, /) -> int:
        """Retrieves the value or pointer stored in a COM wrapper object."""
    ComValue = com_obj.ComValue

    @staticmethod
    def ControlAddItem(
        String: str,
        Control: protocols.WinTitleFinder,
        WinTitle: protocols.WinTitleFinder = ...,
        WinText: str = ...,
        ExcludeTitle: str = ...,
        ExcludeText: str = ...,
        /,
    ):
        """Adds the specified string as a new entry at the bottom of a ListBox or ComboBox."""

    @staticmethod
    def ControlChooseIndex(
        N: int,
        Control: protocols.WinTitleFinder,
        WinTitle: protocols.WinTitleFinder = ...,
        WinText: str = ...,
        ExcludeTitle: str = ...,
        ExcludeText: str = ...,
        /,
    ) -> Nothing:
        """Sets the selection in a ListBox, ComboBox or Tab control to be the Nth item."""

    @staticmethod
    def ControlChooseString(
        String: str,
        Control: protocols.WinTitleFinder,
        WinTitle: protocols.WinTitleFinder = ...,
        WinText: str = ...,
        ExcludeTitle: str = ...,
        ExcludeText: str = ...,
        /,
    ) -> Nothing:
        """Sets the selection in a ListBox or ComboBox to be the first entry whose leading part matches the specified string."""

    @staticmethod
    def ControlClick(
        Control_or_Pos: str | protocols.WinTitleFinder = ...,
        WinTitle: protocols.WinTitleFinder = ...,
        WinText: str = ...,
        WhichButton: MouseButton = ...,
        ClickCount: int = 1,
        Options: str = ...,
        ExcludeTitle: str = ...,
        ExcludeText: str = ...,
        /,
    ) -> Nothing:
        """Sends a mouse button or mouse wheel event to a control."""

    @staticmethod
    def ControlDeleteItem(
        index: int,
        Control: protocols.WinTitleFinder,
        WinTitle: protocols.WinTitleFinder = ...,
        WinText: str = ...,
        ExcludeTitle: str = ...,
        ExcludeText: str = ...,
        /,
    ) -> Nothing:
        """Deletes the specified entry number from a ListBox or ComboBox."""

    @staticmethod
    def ControlFindItem(
        String: str,
        Control: protocols.WinTitleFinder,
        WinTitle: protocols.WinTitleFinder = ...,
        WinText: str = ...,
        ExcludeTitle: str = ...,
        ExcludeText: str = ...,
        /,
    ) -> int:
        """Returns the entry number of a ListBox or ComboBox that is a complete match for the specified string."""

    @staticmethod
    def ControlFocus(
        Control: protocols.WinTitleFinder,
        WinTitle: protocols.WinTitleFinder = ...,
        WinText: str = ...,
        ExcludeTitle: str = ...,
        ExcludeText: str = ...,
        /,
    ) -> Nothing:
        """Sets input focus to a given control on a window."""

    @staticmethod
    def ControlGetChecked(
        Control: protocols.WinTitleFinder,
        WinTitle: protocols.WinTitleFinder = ...,
        WinText: str = ...,
        ExcludeTitle: str = ...,
        ExcludeText: str = ...,
        /,
    ) -> BoolInt:
        """Returns a non-zero value if the checkbox or radio button is checked."""

    @staticmethod
    def ControlGetChoice(
        Control: protocols.WinTitleFinder,
        WinTitle: protocols.WinTitleFinder = ...,
        WinText: str = ...,
        ExcludeTitle: str = ...,
        ExcludeText: str = ...,
        /,
    ) -> str:
        """Returns the name of the currently selected entry in a ListBox or ComboBox."""

    @staticmethod
    def ControlGetClassNN(
        Control: protocols.WinTitleFinder,
        WinTitle: protocols.WinTitleFinder = ...,
        WinText: str = ...,
        ExcludeTitle: str = ...,
        ExcludeText: str = ...,
        /,
    ) -> str:
        """Returns the ClassNN (class name and sequence number) of the specified control."""

    @staticmethod
    def ControlGetEnabled(
        Control: protocols.WinTitleFinder,
        WinTitle: protocols.WinTitleFinder = ...,
        WinText: str = ...,
        ExcludeTitle: str = ...,
        ExcludeText: str = ...,
        /,
    ) -> BoolInt:
        """Returns a non-zero value if the specified control is enabled."""

    @staticmethod
    def ControlGetFocus(
        WinTitle: protocols.WinTitleFinder = ...,
        WinText: str = ...,
        ExcludeTitle: str = ...,
        ExcludeText: str = ...,
        /,
    ) -> int:
        """Retrieves which control of the target window has keyboard focus, if any."""

    @staticmethod
    def ControlGetHwnd(
        Control: protocols.WinTitleFinder,
        WinTitle: protocols.WinTitleFinder = ...,
        WinText: str = ...,
        ExcludeTitle: str = ...,
        ExcludeText: str = ...,
        /,
    ) -> int:
        """Returns the unique ID number of the specified control."""

    @staticmethod
    def ControlGetIndex(
        Control: protocols.WinTitleFinder,
        WinTitle: protocols.WinTitleFinder = ...,
        WinText: str = ...,
        ExcludeTitle: str = ...,
        ExcludeText: str = ...,
        /,
    ) -> int:
        """Returns the index of the currently selected entry or tab in a ListBox, ComboBox or Tab control."""

    @staticmethod
    def ControlGetItems(
        Control: protocols.WinTitleFinder,
        WinTitle: protocols.WinTitleFinder = ...,
        WinText: str = ...,
        ExcludeTitle: str = ...,
        ExcludeText: str = ...,
        /,
    ) -> array.Array:
        """Returns an array of items/rows from a ListBox, ComboBox, or DropDownList."""

    @staticmethod
    def ControlGetPos(
        OutX: VarRef[int] = ...,
        OutY: VarRef[int] = ...,
        OutWidth: VarRef[int] = ...,
        OutHeight: VarRef[int] = ...,
        Control: protocols.WinTitleFinder = ...,
        WinTitle: protocols.WinTitleFinder = ...,
        WinText: str = ...,
        ExcludeTitle: str = ...,
        ExcludeText: str = ...,
        /,
    ) -> Nothing:
        """Retrieves the position and size of a control."""

    @staticmethod
    def ControlGetStyle(
        Control: protocols.WinTitleFinder,
        WinTitle: protocols.WinTitleFinder = ...,
        WinText: str = ...,
        ExcludeTitle: str = ...,
        ExcludeText: str = ...,
        /,
    ) -> int:
        """Returns an integer representing the style or extended style of the specified control."""

    @staticmethod
    def ControlGetExStyle(
        Control: protocols.WinTitleFinder,
        WinTitle: protocols.WinTitleFinder = ...,
        WinText: str = ...,
        ExcludeTitle: str = ...,
        ExcludeText: str = ...,
        /,
    ) -> int:
        """Returns an integer representing the style or extended style of the specified control."""

    @staticmethod
    def ControlGetText(
        Control: protocols.WinTitleFinder,
        WinTitle: protocols.WinTitleFinder = ...,
        WinText: str = ...,
        ExcludeTitle: str = ...,
        ExcludeText: str = ...,
        /,
    ) -> str:
        """Retrieves text from a control."""

    @staticmethod
    def ControlGetVisible(
        Control: protocols.WinTitleFinder,
        WinTitle: protocols.WinTitleFinder = ...,
        WinText: str = ...,
        ExcludeTitle: str = ...,
        ExcludeText: str = ...,
        /,
    ) -> BoolInt:
        """Returns a non-zero value if the specified control is visible."""

    @staticmethod
    def ControlHide(
        Control: protocols.WinTitleFinder,
        WinTitle: protocols.WinTitleFinder = ...,
        WinText: str = ...,
        ExcludeTitle: str = ...,
        ExcludeText: str = ...,
        /,
    ) -> Nothing:
        """Hides the specified control."""

    @staticmethod
    def ControlHideDropDown(
        Control: protocols.WinTitleFinder,
        WinTitle: protocols.WinTitleFinder = ...,
        WinText: str = ...,
        ExcludeTitle: str = ...,
        ExcludeText: str = ...,
        /,
    ) -> Nothing:
        """Hides the drop-down list of a ComboBox control."""

    @staticmethod
    def ControlMove(
        X: int = ...,
        Y: int = ...,
        Width: int = ...,
        Height: int = ...,
        Control: protocols.WinTitleFinder = ...,
        WinTitle: protocols.WinTitleFinder = ...,
        WinText: str = ...,
        ExcludeTitle: str = ...,
        ExcludeText: str = ...,
        /,
    ) -> Nothing:
        """Moves or resizes a control."""

    @staticmethod
    def ControlSend(
        Keys: str,
        Control: protocols.WinTitleFinder = ...,
        WinTitle: protocols.WinTitleFinder = ...,
        WinText: str = ...,
        ExcludeTitle: str = ...,
        ExcludeText: str = ...,
        /,
    ) -> Nothing:
        """Sends simulated keystrokes or text to a window or control."""

    @staticmethod
    def ControlSendText(
        Keys: str,
        Control: protocols.WinTitleFinder = ...,
        WinTitle: protocols.WinTitleFinder = ...,
        WinText: str = ...,
        ExcludeTitle: str = ...,
        ExcludeText: str = ...,
        /,
    ) -> Nothing:
        """Sends simulated keystrokes or text to a window or control."""

    @staticmethod
    def ControlSetChecked(
        NewSetting: Literal[1, 0, -1],
        Control: protocols.WinTitleFinder,
        WinTitle: protocols.WinTitleFinder = ...,
        WinText: str = ...,
        ExcludeTitle: str = ...,
        ExcludeText: str = ...,
        /,
    ) -> Nothing:
        """Turns on (checks) or turns off (unchecks) a checkbox or radio button."""

    @staticmethod
    def ControlSetEnabled(
        NewSetting: Literal[1, 0, -1],
        Control: protocols.WinTitleFinder,
        WinTitle: protocols.WinTitleFinder = ...,
        WinText: str = ...,
        ExcludeTitle: str = ...,
        ExcludeText: str = ...,
        /,
    ) -> Nothing:
        """Enables or disables the specified control."""

    @staticmethod
    def ControlSetStyle(
        Value: str | int,
        Control: protocols.WinTitleFinder,
        WinTitle: protocols.WinTitleFinder = ...,
        WinText: str = ...,
        ExcludeTitle: str = ...,
        ExcludeText: str = ...,
        /,
    ) -> Nothing:
        """Changes the style or extended style of the specified control, respectively."""

    @staticmethod
    def ControlSetExStyle(
        Value: str | int,
        Control: protocols.WinTitleFinder,
        WinTitle: protocols.WinTitleFinder = ...,
        WinText: str = ...,
        ExcludeTitle: str = ...,
        ExcludeText: str = ...,
        /,
    ) -> Nothing:
        """Changes the style or extended style of the specified control, respectively."""

    @staticmethod
    def ControlSetText(
        NewText: str,
        Control: protocols.WinTitleFinder,
        WinTitle: protocols.WinTitleFinder = ...,
        WinText: str = ...,
        ExcludeTitle: str = ...,
        ExcludeText: str = ...,
        /,
    ) -> Nothing:
        """Changes the text of a control."""

    @staticmethod
    def ControlShow(
        Control: protocols.WinTitleFinder,
        WinTitle: protocols.WinTitleFinder = ...,
        WinText: str = ...,
        ExcludeTitle: str = ...,
        ExcludeText: str = ...,
        /,
    ) -> Nothing:
        """Shows the specified control if it was previously hidden."""

    @staticmethod
    def ControlShowDropDown(
        Control: protocols.WinTitleFinder,
        WinTitle: protocols.WinTitleFinder = ...,
        WinText: str = ...,
        ExcludeTitle: str = ...,
        ExcludeText: str = ...,
        /,
    ) -> Nothing:
        """Shows the drop-down list of a ComboBox control."""

    @staticmethod
    def CoordMode(
        TargetType: Literal["ToolTip", "Pixel", "Mouse", "Caret", "Menu"],
        RelativeTo: Literal["Screen", "Window", "Client"] = ...,
        /,
    ) -> Nothing:
        """Sets coordinate mode for various built-in functions to be relative to either the active window or the screen."""

    @staticmethod
    def Cos(n: Number, /) -> float:
        """Returns the trigonometric cosine of the specified number."""

    @staticmethod
    def Critical(OnOffNumeric: Literal["On", "Off"] | int = "On", /) -> int:
        """Prevents the current thread from being interrupted by other threads, or enables it to be interrupted."""

    @staticmethod
    def DateAdd(DateTime: str, Time: Number, TimeUnits: str, /) -> str:
        """Adds or subtracts time from a date-time value."""

    @staticmethod
    def DateDiff(DateTime1: str, DateTime2: str, TimeUnits: str, /) -> int:
        """Compares two date-time values and returns the difference."""

    @staticmethod
    def DetectHiddenText(mode: Bool, /) -> BoolInt:
        """Determines whether invisible text in a window is "seen" for the purpose of finding the window. This affects windowing functions such as WinExist and WinActivate."""

    @staticmethod
    def DetectHiddenWindows(mode: Bool, /) -> BoolInt:
        """Determines whether invisible windows are "seen" by the script."""

    @staticmethod
    def DirCopy(source: str, dest: str, overwrite: Bool = False, /) -> Nothing:
        """Copies a folder along with all its sub-folders and files (similar to xcopy)."""

    @staticmethod
    def DirCreate(DirName: str, /): ...
    @staticmethod
    def DirDelete(Dirname: str, recurse: Bool = False, /) -> Nothing: ...
    @staticmethod
    def DirExist(pattern: str, /) -> str: ...
    @staticmethod
    def DirMove(source: str, dest: str, OverwriteOrRename: str) -> Nothing: ...
    @staticmethod
    def DirSelect(
        StartingFolder: str = ..., Options: int = ..., Prompt: str = ..., /
    ) -> str:
        """Displays a standard dialog that allows the user to select a folder."""

    @staticmethod
    def DllCall(
        Function: str | int, /, *types_and_args: Primitive | buffer.BufferOrAddress
    ) -> str | int:
        """Use a designated Python library, or the ctypes module, instead of this!"""

    @staticmethod
    def Download(URL: str, filename: str) -> Nothing:
        """Downloads a file from the Internet."""

    @staticmethod
    def DriveEject(drive: str) -> Nothing: ...
    @staticmethod
    def DriveRetract(drive: str) -> Nothing: ...
    @staticmethod
    def DriveGetCapacity(drive: str) -> int: ...
    @staticmethod
    def DriveGetFileSystem(drive: str) -> str: ...
    @staticmethod
    def DriveGetLabel(drive: str) -> str: ...
    @staticmethod
    def DriveGetList(drive_type: str = ...) -> str: ...
    @staticmethod
    def DriveGetSerial(drive: str) -> int: ...
    @staticmethod
    def DriveGetSpaceFree(drive: str) -> int: ...
    @staticmethod
    def DriveGetStatus(drive: str) -> str: ...
    @staticmethod
    def DriveGetStatusCD(drive: str = ...) -> str: ...
    @staticmethod
    def DriveGetType(drive: str) -> str: ...
    @staticmethod
    def DriveLock(drive: str) -> Nothing: ...
    @staticmethod
    def DriveSetLabel(drive: str, new_label: str = ...) -> Nothing: ...
    @staticmethod
    def DriveUnlock(drive: str) -> Nothing: ...
