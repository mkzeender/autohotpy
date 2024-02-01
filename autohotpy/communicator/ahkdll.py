from ctypes import c_wchar_p, cdll
from os import path


ahkdll = cdll.LoadLibrary(path.join(path.split(__file__)[0], "Autohotkey_v2.dll"))
ahkdll.ahkgetvar.restype = c_wchar_p
