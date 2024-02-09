from ctypes import c_wchar_p, cdll
from os import path, getcwd, chdir
from contextlib import contextmanager


@contextmanager
def hold_cwd():
    cwd = getcwd()
    try:
        yield
    finally:
        chdir(cwd)


def add_script(*args):
    with hold_cwd():
        return ahkdll.addScript(*args)


def new_thread(*args):
    with hold_cwd():
        return ahkdll.NewThread(*args)


ahkdll = cdll.LoadLibrary(path.join(path.split(__file__)[0], "Autohotkey_v2.dll"))
ahkdll.ahkgetvar.restype = c_wchar_p
