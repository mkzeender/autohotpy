a_globals = """
    class A_Globals {
        static __Get(_ahpy_paramname, _ahpy_itemparams) {
            if (_ahpy_itemparams.Length) {
                return %_ahpy_paramname%[_ahpy_itemparams*]
            }
            else {
                return %_ahpy_paramname%
            }
        }

        static __Set(_ahpy_paramname, _ahpy_itemparams, _ahpy_value) {
            global
            if (_ahpy_itemparams.Length) {
                    %_ahpy_paramname%[_ahpy_itemparams*] := _ahpy_value
            }
            else {
                %_ahpy_paramname% := _ahpy_value
            }
        }
        
        static __Call(_ahpy_funcname, _ahpy_funcparams) {
            return %_ahpy_funcname%(_ahpy_funcparams*)
        }

    }
    _py_get_ahk_global(name_p, ret_callback) {
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
    }
"""
