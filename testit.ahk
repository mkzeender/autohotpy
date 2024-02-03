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

caller(fn) {
    MsgBox "about to call function"
    fn('hello world!')
    MsgBox "done calling it"
}

my_hoop := Hoopla()

; MsgBox JSON.Stringify([1, 1.0, [1, 2, 3], {a:'hello', b:thing}])

; MsgBox JSON.Parse('[1, 2, 3]')[1]

exit_func(r, c) {
    MsgBox 'Exiting'
}

+l::ExitApp


OnExit(exit_func, -1)

sleep 1000


