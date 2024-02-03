py_object = """
    _py_object_from_id(id) {
        obj := {_py_id: id}
        obj.base := PyObject
        return obj
    }
        
    class PyObject {
        __New(id) {
            this.DefineProp("_py_id", {Value: id}) ; set value1
        }
        static __New() {
            ; called when a subclass is created. 
            if (this != PyObject) {
                
            }
        }
        __Call(method_name, params) {
            
        }
        Call(params*) {
            return this.__call__(params)
        }
        
        __Get(attr, params) {

        }
        __Set(attr, params, val) {
            
        }
        __Item[params*] {
            get {
                return this.__get_item__(params)
            }
            set {
                this.__set_item__(value)
            }
        }
        __Enum(n_vars) {
            
        }
        __Delete() {
            
        }
    }
"""
