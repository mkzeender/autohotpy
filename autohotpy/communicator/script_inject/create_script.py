from __future__ import annotations
from dataclasses import asdict
import os
from os import path
from typing import TYPE_CHECKING


from ..dtypes import DTypes

if TYPE_CHECKING:
    from .callbacks_ import CallbackPtrs, PythonConsts, MutableMappingMixin


def include(name):
    fp = path.join(path.split(__file__)[0], name) + ".ahk"
    with open(fp, "r") as f:
        return f.read()


def create_user_script(script: tuple[str, ...], f: CallbackPtrs) -> str:
    s = "\n".join(line_group for line_group in script)
    return f"""
        {s}
        DllCall({f.idle}, "cdecl int")

    """


def create_injection_script(
    f: CallbackPtrs, a: PythonConsts, m: MutableMappingMixin
) -> str:
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

    map_mixin = "\t\t\t\t\n".join(
        f"""Map.Prototype.DefineProp("{k}", {{get: (p*) => {{}}, call: _py_object_from_id({v})}})"""
        for k, v in asdict(m).items()
    )

    return f"""
        #include "{cwd}"
        SetWorkingDir "{cwd}"

        {include("py_object")}
        {include("py_call")}
        {include("a_globals")}
        {include("py_communicator")}
        {include('Py_special')}
        
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

        {map_mixin}
        
        
        DllCall({f.give_pointers}
            ,"ptr", _PyCommunicator.call_ptr
            ,"ptr", _PyCommunicator.call_threadsafe_ptr
            ,"ptr", _PyCommunicator.get_global_ptr
            ,"ptr", _PyCommunicator.free_obj_ptr
            ,"ptr", _PyCommunicator.put_return_ptr
            ,"ptr", _PyCommunicator.globals_ptr
            ,"int")


        """
