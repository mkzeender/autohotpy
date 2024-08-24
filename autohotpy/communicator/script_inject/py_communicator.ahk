_py_call_ahk_function(param_ptr) {
    if param_ptr is String {
        call_info := JSON.Parse(param_ptr)
    }
    else {
        call_info := JSON.Parse(StrGet(param_ptr))
    }
    args := call_info['args']
    for i, v in args {
        _PyCommunicator.value_from_data(v, &arg_entry)
        if arg_entry != _PyCommunicator.UNSET_
            args[i] := arg_entry
        else
            args.Delete(i)
    }
    kwds := call_info['kwargs']
    if kwds.Count {
        kwds.Base := Kwargs.Prototype
        args.Push(kwds)
    }
    _PyCommunicator.value_from_data(call_info['obj'], &obj)
    _PyCommunicator.value_from_data(call_info['method'], &method)
    
    try {
        if obj == _PyCommunicator.UNSET_ or method == _PyCommunicator.UNSET_ {
            throw Error('Callable or Method was unset')
        }
        result := obj.%method%(args*)
        result_data := map("success", true, "value", _PyCommunicator.value_to_data(result))
    }
    catch Any as err {
        if not (err is Error or err is PyObject) {
            err := Error(err)
        }
        result_data := map("success", false, "value", _PyCommunicator.value_to_data(err))
    }
    
    DllCall(call_info['return_callback'], "str", JSON.Stringify(result_data), "int")
    return 2
}



_py_get_ahk_attr(obj, name) {
    return obj.%name%
}

_py_set_ahk_attr(obj, name, value := unset) {
    if IsSet(value)
        obj.%name% := value
    else
        obj.DeleteProp(name)
}

_py_getitem(obj, params*) {
    return obj[params*]
}

_py_setitem(obj, value := UNSET, params*) {
    If IsSet(value)
        obj[params*] := value
    else
        obj.Delete(params*)
}

_py_getprop(obj, prop, params*) {
    return obj.%prop%[params*]
}

_py_setprop(obj, prop, value, params*) {
    obj.%prop%[params*] := value
}

_py_instancecheck(inst, cls) {
    return inst is cls
}

class _PyCommunicator {

    static UNSET_ := Object()

    static __New() {
        this.call_ptr := CallbackCreate(_py_call_ahk_function, "F")
        this.call_threadsafe_ptr := CallbackCreate(_py_call_ahk_function)
        this.get_global_ptr := CallbackCreate(_py_get_ahk_global, "F")
        this.free_obj_ptr := CallbackCreate(ObjRelease, "F")
        this.put_return_ptr := CallbackCreate(_py_put_return_value, "F")
        this.globals_ptr := this.value_to_data(A_Globals)["ptr"]
        this.callbacks := Map(
            "get_ahk_attr", this.value_to_data(ObjBindMethod(this, "get_ahk_attr")),
            "set_ahk_attr", this.value_to_data(ObjBindMethod(this, "set_ahk_attr"))
            )
    }
    
    static value_from_data(val, &out) {
        
        if val is Map {
            if (
                val["dtype"] == _PyParamTypes.AHK_OBJECT or
                val["dtype"] == _PyParamTypes.VARREF
            ) {
                out := ObjFromPtrAddRef(val["ptr"])
                return
            }
            if val["dtype"] == _PyParamTypes.INT {
                out := Integer(val["value"])
                return
            }
            if val["dtype"] == _PyParamTypes.PY_OBJECT {
                out := _py_object_from_id(val["ptr"])
                return
            }
            if val["dtype"] == _PyParamTypes.UNSET {
                out := this.UNSET_
                return
            }
            throw Error('error ' val["dtype"] " != " _PyParamTypes.AHK_OBJECT)
        }
        out := val
    }

    static value_to_data(val) {
        if val is PyObject {
            ptr := val._py_id
            return map("dtype", _PyParamTypes.PY_OBJECT, "ptr", String(ptr))
        }
        ; if val is VarRef {
        ;     ptr := ObjPtrAddRef(val)
        ;     return map("dtype", _PyParamTypes.VARREF, "ptr", String(ptr))
        ; }
        if val is Integer {
            return map("dtype", _PyParamTypes.INT, "value", String(val))
        }
        if val is Float or val is String {
            return val
        }
        immortal := this.IsImmortal(val)
        if immortal {
            ptr := ObjPtr(val)
        } else {
            ptr := ObjPtrAddRef(val)
        }
        ; Msgbox immortal ", " Type(val) ", " (val is Func and val.IsBuiltIn)
        dtype := (val is Map) ? _PyParamTypes.AHK_MAP : (val is Array ? _PyParamTypes.AHK_ARRAY : _PyParamTypes.AHK_OBJECT)
        return map("dtype", _PyParamTypes.AHK_OBJECT, "ptr", String(ptr), "type_name", Type(val), 'immortal', immortal)
    
    }

    static IsImmortal(_ahk_value) {
        if (_ahk_value is Class) {
            try {
                return %_ahk_value.Prototype.__Class% == _ahk_value
            } catch {
                return false
            }
        } else if (_ahk_value is Func) {
            try {
                return %_ahk_value.Name% == _ahk_value
            } catch {
                return false
            }
        } else {
            return false
        }
    }   

    
}
