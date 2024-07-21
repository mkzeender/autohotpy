# ----------
# Primitives
# ----------
from typing import Any
from autohotpy.static_typing.classes import Primitive, Number, VarRef

Integer = int
Float = float
String = str

# -------
# Objects
# -------
from autohotpy.static_typing.classes.object_ import Object
from autohotpy.static_typing.classes.array import Array
from autohotpy.static_typing.classes.buffer import Buffer
from autohotpy.static_typing.classes.class_ import Class

# from autohotpy.static_typing.classes.error import # TODO: error typing
from autohotpy.static_typing.classes.file import File
from autohotpy.static_typing.classes.func import Func, BoundFunc, Closure, Enumerator

# from autohotpy.static_typing.classes.gui # TODO: gui typing
from autohotpy.static_typing.classes.inputhook import InputHook
from autohotpy.static_typing.classes.map import Map
from autohotpy.static_typing.classes.menu import Menu, MenuBar
from autohotpy.static_typing.classes.regex_match_info import RegExMatchInfo

# -----------
# COM objects
# -----------
from autohotpy.static_typing.classes.com_obj import ComValue, ComObject, ComObjArray
