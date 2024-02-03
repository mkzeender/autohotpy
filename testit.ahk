#Requires AutoHotkey v2.0-beta.1

thing := '12345🏳️‍⚧️'

my_float := 1.2
my_empty := ''
my_py_thing := ''

class Hoopla {
    static my_static() {
        MsgBox 'in my_static'
    }
    my_non_static() {

    }
}

caller(ind) {
    MsgBox "about to index " Type(my_py_thing) " with " ind
    
    my_py_thing.foo['hit'] := 10
    MsgBox "done calling it " String(my_py_thing.foo)
    return
}

my_hoop := Hoopla()

; MsgBox JSON.Stringify([1, 1.0, [1, 2, 3], {a:'hello', b:thing}])

; MsgBox JSON.Parse('[1, 2, 3]')[1]

exit_func(r, c) {
    MsgBox 'Exiting'
}


OnExit(exit_func, -1)

sleep 1000


