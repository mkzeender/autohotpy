class Kwargs extends Map {
    
}

class _py_caller_job {

    __New(obj, method, args) {
        if (args.Length and (args[-1] is Kwargs)) {
            kwds := map()
        } else {
            kwds := map()
        }
        
        this.ret_val := ""
        this.success := false
        static vtd := ObjBindMethod(_PyCommunicator, "value_to_data")

        arg_data := []
        arg_data.Length := args.Length
        for i, v in args {
            arg_data[i] := vtd(v)
        }
        this.call_data := JSON.Stringify(map(
            "obj", vtd(obj)
            ,"method", vtd(method)
            ,"args", arg_data
            ,"kwargs", kwargs
            ,"ret_call_p", String(ObjPtr(this))
        ))

    }

    Call() {
        DllCall(_PyCallbacks.CALL_METHOD, "str", this.call_data, "int")

        if Integer(this.success) {
            if this.ret_val == _PyCommunicator.UNSET_  {
                throw Error('A function tried to return an unset variable')
            }
            return this.ret_val
        }
        else {
            throw this.ret_val
        }
    }
}

_py_call_method(obj, method, args) {
    return _py_caller_job(obj, method, args).Call()
}

_py_put_return_value(job_p, data_p) {
    job := ObjFromPtrAddRef(job_p)
    data := JSON.Parse(StrGet(data_p))
    _PyCommunicator.value_from_data(data["value"], &ret_val)
    job.ret_val := ret_val
    job.success := data["success"]
}
