
_py_parameterize_generic(this, params*) {
    return this
}
; Allow for Generic syntax. i.e. Array[int]
Object.DefineProp('__Item', {get: _py_parameterize_generic})

class ObjBindProp {
    __New(obj, prop_name) {
        this.obj := obj
        this.prop := prop_name
    }
    __Item[params*] {
        get {
            return this.obj.%this.prop%[params*]
        }
    }
}

_py_create_ref(this, value := "") {
    return &value
}

VarRef.Call := _py_create_ref

_py_set_ref(&ref, value) {
    ref := value
}

_py_deref(&ref) {
    return ref
}