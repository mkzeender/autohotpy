py_object = """
    _py_object_from_id(id) {
        obj := {_py_id: id}
        obj.base := PyObject.Prototype
        return obj
    }
        
    class PyObject {
        
        static __New() {
            ; called when a subclass is created. 
            if (this != PyObject) {
                
            }
        }
        __Call(method_name, params) {
            return _py_call_method(this, method_name, params)
        }
        Call(params*) {
            return _py_call_method(this, "", params)
        }
        
        __Get(attr, params) {
            val := (_Python.getattr)(this, attr)
            if params.Length {
                val := val[params*]
            }
            return val
        }
        __Set(attr, params, val) {
            if params.Length {
                prop := (_Python.getattr)(this, attr)
                prop[params*] := val
            } else {
                (_Python.setattr)(this, attr)
            }
        }
        __Item[params*] {
            get {
                if (params.Length == 1) {
                    item := params[1]
                }
                else {
                    item := Python.tuple(params)
                }
                return this.__getitem__(item)
            }
            set {
                if (params.Length == 1) {
                    item := params[1]
                }
                else {
                    item := Python.tuple(params)
                }
                this.__setitem__(params, value)
            }
        }
        __Enum(n_vars) {
            return _PyEnumerator((_Python.iter)(this), n_vars)
        }
        __Delete() {
            ; MsgBox(this._py_id " : " this.__class__.__name__)
            DllCall(_PyCallbacks.FREE_OBJ, "int64", Integer(this._py_id), "int")
        }

        ToString() {
            return Python.str(this)
        }
    }

    class _PyEnumerator {
        __New(iter, n_vars) {
            this.iter := iter
            this.n_vars := n_vars
        }
        Call(outputs*) {
            try {
                result := (_Python.next)(this.iter)
            } catch Any as err {
                if Python.isinstance(err, _Python.StopIteration) {
                    return 0
                }
                throw
            }
            if this.n_vars == 1 {
                %outputs[1]% := result
            } else {
                for val in result {
                     %outputs[A_Index]% := val
                }
            }
            return 1
        }
    }
"""
