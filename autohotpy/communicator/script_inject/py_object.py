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
            if params {
                throw PropertyError()
            }
            return _Python.getattr(this, attr)
        }
        __Set(attr, params, val) {
            return _Python.setattr(this, attr)
        }
        __Item[params*] {
            get {
                Msgbox "in item"
                if (params.Length == 1) {
                    params := params[1]
                }
                return this.__getitem__(params)
            }
            set {
                if (params.Length == 1) {
                    params := params[1]
                }
                this.__setitem__(params, value)
            }
        }
        __Enum(n_vars) {
            
        }
        __Delete() {
            
        }
    }
"""
