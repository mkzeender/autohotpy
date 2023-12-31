from ctypes import (
    cast,
    c_void_p,
    CFUNCTYPE,
    c_int,
    c_int64,
    c_wchar_p,
    POINTER,
    c_char,
    c_uint64,
)
import os
from typing import Any

from ._dtypes import DTypes


class Callbacks:
    def __init__(self, inst) -> None:
        self._dict = dict(
            get=CFUNCTYPE(c_int, c_int64, c_wchar_p, c_char * 64)(
                inst._get_attr_callback
            ),
            set=inst._set_attr_callback,
            call=inst._call_callback,
            free_obj=inst._free_obj_callback,
            exit_app=CFUNCTYPE(c_int, c_wchar_p, c_int64)(inst._exit_app_callback),
            idle=CFUNCTYPE(None)(inst._autoexec_thread_callback),
            give_pointers=CFUNCTYPE(c_int, c_uint64, c_uint64, c_uint64, c_wchar_p)(
                inst._set_ahk_func_ptrs
            ),
        )

    def __getattr__(self, __name: str) -> int:
        return addr_of(self._dict[__name])


def addr_of(func) -> int:
    try:
        val = cast(func, c_void_p).value
        assert val is not None
        return val
    except:
        print(f"ignoring {func}")
        return 0


def create_user_script(script: tuple[str, ...], f: Callbacks) -> str:
    s = "\n".join(line_group for line_group in script)
    return f"""
        {s}
        DllCall({f.idle}, "cdecl int")

    """


def create_injection_script(f: Callbacks) -> str:
    cwd = os.getcwd()

    dtype_enum = "\t\t\t\t\n".join(
        f"static {v.name} := {repr(v.value)}" for v in DTypes
    )

    return f"""
        #include "{cwd}"
        SetWorkingDir "{cwd}"
        
        _py_object_from_id(id) {{
            obj := {{_py_id: id}}
            obj.base := PyObject
            return obj
        }}

        _py_exit_func(reason, code) {{
            return DllCall({f.exit_app}, 'str', reason, 'int', code, 'cdecl int')
        }}
        _py_error_func(err, mode) {{
            
        }}

        OnExit(_py_exit_func, -1)
        OnError(_py_error_func, -1)

        None := _py_object_from_id({id(None)})

        class _PyParamTypes {{
            {dtype_enum}
        }}

        class A_Globals {{
            static __Get(_ahpy_paramname, _ahpy_itemparams) {{
                if (_ahpy_itemparams.Length) {{
                    return %_ahpy_paramname%[_ahpy_itemparams*]
                }}
                else {{
                    return %_ahpy_paramname%
                }}
            }}

            static __Set(_ahpy_paramname, _ahpy_itemparams, _ahpy_value) {{
                global
                if (_ahpy_itemparams.Length) {{
                     %_ahpy_paramname%[_ahpy_itemparams*] := _ahpy_value
                }}
                else {{
                    %_ahpy_paramname% := _ahpy_value
                }}
            }}
            
            static __Call(_ahpy_funcname, _ahpy_funcparams) {{
                return %_ahpy_funcname%(_ahpy_funcparams*)
            }}

        }}

        _py_call_ahk_function(param_ptr) {{
            if param_ptr is String {{
                call_info := JSON.Parse(param_ptr)
            }}
            else {{
                call_info := JSON.Parse(StrGet(param_ptr))
            }}
            args := call_info['args']
            for i, v in args {{
                call_info['args'][i] := _PyCommunicator.value_from_data(v)
            }}
            obj := _PyCommunicator.value_from_data(call_info['obj'])
            method := _PyCommunicator.value_from_data(call_info['method'])
            try {{
                result := obj.%method%(args*)
                if (result == '')
                    return 3
                result_data := map("success", true, "value", _PyCommunicator.value_to_data(result))
            }}
            catch Any as err {{
                if not (err is Error) {{
                    err := Error(err)
                }}
                result_data := map("success", false, "value", _PyCommunicator.value_to_data(err))
            }}
            
            DllCall(call_info['return_callback'], "str", JSON.Stringify(result_data), "int")
            return 2
        }}

        _py_get_ahk_global(name_p, ret_callback) {{
            name := StrGet(name_p)
            try
                value := %name%
            catch
                return 1
            if (value == '')
                return 3
            if (HasBase(value, Func) or HasBase(value, Class))
                value_data := map('dtype', _PyParamTypes.AHK_IMMORTAL, 'ptr', String(ObjPtrAddRef(value)))
            else
                value_data := _PyCommunicator.value_to_data(value)
            DllCall(ret_callback, "str", JSON.Stringify(value_data), "int")
            return 2
        }}

        class _PyCommunicator {{

            static __New() {{
                this.call_ptr := CallbackCreate(_py_call_ahk_function, "F")
                this.call_threadsafe_ptr := CallbackCreate(_py_call_ahk_function)
                this.get_global_ptr := CallbackCreate(_py_get_ahk_global, "F")
                this.callbacks := Map(
                    "get_ahk_attr", this.value_to_data(ObjBindMethod(this, "get_ahk_attr")),
                    "set_ahk_attr", this.value_to_data(ObjBindMethod(this, "set_ahk_attr")),
                    "globals_ptr", this.value_to_data(A_Globals)["ptr"]
                    )
            }}
            
            

            static get_ahk_attr(obj, name) {{
                return obj.%name%
            }}
            static set_ahk_attr(obj, name, value) {{
                obj.%name% := value
            }}

            static value_from_data(val) {{
                if val is Map {{
                    if val["dtype"] == _PyParamTypes.AHK_OBJECT {{
                        val := ObjFromPtrAddRef(val["ptr"])
                        return val
                    }}
                    if val["dtype"] == _PyParamTypes.INT {{
                        return Integer(val["value"])
                    }}
                    Msgbox 'error ' val["dtype"] " != " _PyParamTypes.AHK_OBJECT
                }}
                return val
            }}

            static value_to_data(val) {{
                if IsObject(val) {{
                    ptr := ObjPtrAddRef(val)
                    return map("dtype", _PyParamTypes.AHK_OBJECT, "ptr", String(ptr))
                }}
                if val is Integer {{
                    return map("dtype", _PyParamTypes.INT, "value", String(val))
                }}
                
                return val
            }}
            

            
        }}
           
        class PyObject {{
            __New(id) {{
                this.DefineProp("_py_id", {{Value: id}}) ; set value1
            }}
            static __New() {{
                ; called when a subclass is created. 
                if (this != PyObject) {{
                    
                }}
            }}
            __Call(method_name, params) {{
                
            }}
            Call(params*) {{
                return this.__call__(params)
            }}
            
            __Get(attr, params) {{

                attr := attr ''

                types := _PyParamTypes
                return_data := Buffer(64)

                offset := 1
                
                DllCall({f.get},"int64", this._py_id, "str", attr, "ptr", return_data, "Cdecl int")
                
                
                throw Error('fuck')
            }}
            __Set(attr, params, val) {{
                
            }}
            __Item[params*] {{
                get {{
                    return this.__get_item__(params)
                }}
                set {{
                    this.__set_item__(value)
                }}
            }}
            __Enum(n_vars) {{
                
            }}
            __Delete() {{
                
            }}
        }}

        DllCall({f.give_pointers}
            ,"ptr", _PyCommunicator.call_ptr
            ,"ptr", _PyCommunicator.call_threadsafe_ptr
            ,"ptr", _PyCommunicator.get_global_ptr
            ,"str", JSON.Stringify(_PyCommunicator.callbacks)
            ,"int")


        """
