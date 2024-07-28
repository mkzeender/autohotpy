# ----------
# Primitives
# ----------
from typing import Any as Any
from autohotpy.static_typing.classes import (
    Primitive as Primitive,
    Number as Number,
    VarRef as VarRef,
)

Integer = int
Float = float
String = str

# -------
# Objects
# -------
from autohotpy.static_typing.classes.object_ import Object as Object
from autohotpy.static_typing.classes.array import Array as Array
from autohotpy.static_typing.classes.buffer import Buffer as Buffer
from autohotpy.static_typing.classes.class_ import Class as Class

# from autohotpy.static_typing.classes.error import # TODO: error typing
from autohotpy.static_typing.classes.file import File as File
from autohotpy.static_typing.classes.func import (
    Func as Func,
    BoundFunc as BoundFunc,
    Closure as Closure,
    Enumerator as Enumerator,
)

# from autohotpy.static_typing.classes.gui # TODO: gui typing
from autohotpy.static_typing.classes.inputhook import InputHook as InputHook
from autohotpy.static_typing.classes.map import Map as Map
from autohotpy.static_typing.classes.menu import Menu as Menu, MenuBar as MenuBar
from autohotpy.static_typing.classes.regex_match_info import (
    RegExMatchInfo as RegExMatchInfo,
)

# -----------
# COM objects
# -----------
from autohotpy.static_typing.classes.com_obj import (
    ComValue as ComValue,
    ComObject as ComObject,
    ComObjArray as ComObjArray,
)
