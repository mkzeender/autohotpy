communicator = """
    _py_call_ahk_function(param_ptr) {
        if param_ptr is String {
            call_info := JSON.Parse(param_ptr)
        }
        else {
            call_info := JSON.Parse(StrGet(param_ptr))
        }
        args := call_info['args']
        for i, v in args {
            call_info['args'][i] := _PyCommunicator.value_from_data(v)
        }
        obj := _PyCommunicator.value_from_data(call_info['obj'])
        method := _PyCommunicator.value_from_data(call_info['method'])
        try {
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
    
    _py_set_ahk_attr(obj, name, value) {
        obj.%name% := value
    }

    _py_getitem(obj, params*) {
        return obj[params*]
    }

    _py_setitem(obj, value, params*) {
        obj[params*] := value
    }

    class _PyCommunicator {

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
        
        static value_from_data(val) {
            
            if val is Map {
                if val["dtype"] == _PyParamTypes.AHK_OBJECT {
                    val := ObjFromPtrAddRef(val["ptr"])
                    return val
                }
                if val["dtype"] == _PyParamTypes.INT {
                    return Integer(val["value"])
                }
                if val["dtype"] == _PyParamTypes.PY_OBJECT {
                    return _py_object_from_id(val["ptr"])
                }
                Msgbox 'error ' val["dtype"] " != " _PyParamTypes.AHK_OBJECT
            }
            return val
        }

        static value_to_data(val) {
            if val is PyObject {
                ptr := val._py_id
                return map("dtype", _PyParamTypes.PY_OBJECT, "ptr", String(ptr))
            }
            if IsObject(val) {
                ptr := ObjPtrAddRef(val)
                return map("dtype", _PyParamTypes.AHK_OBJECT, "ptr", String(ptr))
            }
            if val is Integer {
                return map("dtype", _PyParamTypes.INT, "value", String(val))
            }
            
            return val
        }
        

        
    }
"""
