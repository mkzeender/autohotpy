;
my_thing := Error('hooligan', 0, 10)

class Hoo {
    message := 'crap'
    What := 0
    Extra := ''
    File := A_ScriptDir '\autostart.py'
    Line := 10
}

fn(this, val) {
    return &val
}

VarRef.Call := fn

my_ref := VarRef('thing')

MsgBox %my_ref%



^h::
{
    static wut := 10
    MsgBox(wut)
}