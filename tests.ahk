; class PyObject {
;     __New(id) {
;         MsgBox "in new"
;         this._py_id := id
;     }

;     static __New() {
;         if this != PyObject {
;             MsgBox "in static new " this.BaseClass._py_id
;         }
;     }

; }

; PyObject.BaseClass := PyObject(3)

; class hit extends PyObject {
;     static BaseClass := PyObject(5)
;     __New() {
;         MsgBox "in hit new"
;     }
; }


; class PropTest {
;     __Get(key, params) {
;         MsgBox key
;         for param in params {
;             MsgBox param
;         }
;     }
;     __Item[params*] {
;         get {
;             for p in params
;                 MsgBox p
;         }
;     }
; }

; _getter(thing, params*) {
;     for p in params {
;         MsgBox p
;     }
; }

; ; PropTest.prototype.DefineProp('__Item', {get: _getter})

; PropTest()['one', 'two', 'three']

my_thing := Error('hooligan', 0, 10)

class Hoo {
    message := 'shit'
    What := 0
    Extra := ''
    File := A_ScriptDir '\autostart.py'
    Line := 10
}

MsgBox A_ScriptDir '\autostart.py'

err := Error()

err.Message := 'shit'
err.What := 's'
err.File := A_ScriptDir '\autostart.py'
err.Line := 10

throw Hoo()