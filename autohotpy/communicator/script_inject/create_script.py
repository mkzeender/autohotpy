from __future__ import annotations
from dataclasses import asdict
import os
from typing import TYPE_CHECKING

from ..dtypes import DTypes
from .py_object import py_object
from .a_globals import a_globals
from .py_call import py_call
from .py_communicator import communicator

if TYPE_CHECKING:
    from .Callbacks import CallbackPtrs, PythonConsts


def create_user_script(script: tuple[str, ...], f: CallbackPtrs) -> str:
    s = "\n".join(line_group for line_group in script)
    return f"""
        {s}
        DllCall({f.idle}, "cdecl int")

    """


def create_injection_script(f: CallbackPtrs, a: PythonConsts) -> str:
    cwd = os.getcwd()

    dtype_enum = "\t\t\t\t\n".join(
        f"static {v.name} := {repr(v.value)}" for v in DTypes
    )

    callbacks_enum = "\t\t\t\t\n".join(
        f"static {k.upper()} := {v}" for k, v in asdict(f).items()
    )

    consts_enum = "\t\t\t\t\n".join(
        f"static {k} := _py_object_from_id({v})" for k, v in asdict(a).items()
    )

    return f"""
        #include "{cwd}"
        SetWorkingDir "{cwd}"

        {py_object}
        {py_call}
        {a_globals}
        {communicator}
        
        _py_exit_func(reason, code) {{
            return DllCall({f.exit_app}, 'str', reason, 'int', code, 'cdecl int')
        }}
        _py_error_func(err, mode) {{
            if err is PyObject {{
                return (_Python.on_error)(err)
            }}
        }}

        OnExit(_py_exit_func, -1)
        OnError(_py_error_func, -1)

        class _PyParamTypes {{
            {dtype_enum}
        }}

        class _PyCallbacks {{
            {callbacks_enum}
        }}

        class _Python {{
            {consts_enum}
        }}
        Python := _Python.pylib
        
        
        DllCall({f.give_pointers}
            ,"ptr", _PyCommunicator.call_ptr
            ,"ptr", _PyCommunicator.call_threadsafe_ptr
            ,"ptr", _PyCommunicator.get_global_ptr
            ,"ptr", _PyCommunicator.free_obj_ptr
            ,"ptr", _PyCommunicator.put_return_ptr
            ,"ptr", _PyCommunicator.globals_ptr
            ,"int")


        """
