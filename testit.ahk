#Requires AutoHotkey v2.0-beta.1

thing := '12345🏳️‍⚧️'

my_float := 1.2
my_empty := ''
my_py_thing := ""
my_obj := {foo: map("bar", "hoo")}

math := Python.import('math')

MsgBox math.factorial(5)

f1(thing) {
    thing()
}

f2() {
    throw Error('damn dude!')
}

test_iter(itr) {
    for k in itr {
        MsgBox k
    }
}

class Hoopla {
    static my_static() {
        MsgBox 'in my_static'
    }
    my_non_static() {

    }

    __New() {
        this.in := [[1, 2, 3], [4, 5, 6]]
    }

    goop[a:=1, b:=1] {
        set {
            this.in[a][b] := value
        }
        get {
            return this.in[a][b]
        }
    }
}

caller(ind) {
    thingy := "wow"
    t_p := &thingy
    ; MsgBox "about to index " Type(my_py_thing) " with " ind
    
    ; my_py_thing.foo['hit'] := 10
    ; MsgBox "done calling it " String(my_py_thing.foo)
    return t_p
}

my_hoop := Hoopla()

; MsgBox JSON.Stringify([1, 1.0, [1, 2, 3], {a:'hello', b:thing}])

; MsgBox JSON.Parse('[1, 2, 3]')[1]

exit_func(r, c) {
    MsgBox 'Exiting'
}


OnExit(exit_func, -1)

sleep 1000


