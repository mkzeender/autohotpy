from ctypes import cast, c_void_p
import os
from typing import Any

from ._dtypes import DTypes

class Callbacks:
    def __init__(self, **kwargs) -> None:
        self._dict = kwargs

    def __getattr__(self, __name: str) -> int:
        return addr_of(self._dict[__name])


def addr_of(func) -> int:
    try:
        val = cast(func, c_void_p).value
        assert val is not None
        return val
    except:
        print(f'ignoring {func}')
        return 0

def create_user_script(script:tuple[str, ...], f:Callbacks) -> str:
    s = '\n'.join(line_group for line_group in script)
    return f"""
        {s}
        DllCall({f.idle}, "cdecl int")

    """

def create_injection_script(f:Callbacks) -> str:
    

    cwd = os.getcwd()

    dtype_enum = '\t\t\t\t\n'.join(f"static {v.name} := {v.value}" for v in DTypes)
    
    
    return (f"""
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

        _value_from_pybuffer() {{
            
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
            __Set(attr, val) {{
                
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

        """

    )