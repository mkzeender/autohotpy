
_py_parameterize_generic(this, params*) {
    return this
}
; Allow for Generic syntax. i.e. Array[int]
(Object.DefineProp)(Class.Prototype, '__Item', {get: _py_parameterize_generic})

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

_py_set_ref(&ref, value) {
    ref := value
}

_py_deref(&ref) {
    return ref
}

VarRef.Call := _py_create_ref

(Object.DefineProp)(VarRef.Prototype, 'value', {get: _py_deref, set: _py_set_ref})

_py_object_from_kwargs(obj, kw := unset) {
    if IsSet(kw) {
        if kw is Kwargs {
            for name, val in kw {
                obj.%name% := val
            }
        } else {
            throw TypeError('Too many arguments to Object()')
        }
    }
}

Object.Prototype.__New := _py_object_from_kwargs


_py_map_from_dict(map_, args*) {
    if not args.Length
        return
    last := args.Pop()
    if (last is Kwargs) {
        for k, v in last {
            args.Push(k, v)
        }
    } else {
        args.Push(last)
    }

    if Mod(args.Length, 2) == 1 {
        first := args.RemoveAt(1)
        for k in first {
            args.InsertAt(1, k, first[k])
        }
    }
    map_.Set(args*)
}

_py_new_map_from_items := Map.Prototype.__New
(Object.DefineProp)(Map.Prototype, '__New', {call: _py_map_from_dict})