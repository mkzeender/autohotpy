;
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



var_ref_gen(thing) {
    return &thing
}

p1 := var_ref_gen("i1")
p2 := var_ref_gen("i2")
%p1% := "10"
MsgBox %p1% " " %p2%

^h::
{
    static wut := 10
    MsgBox(wut)
}