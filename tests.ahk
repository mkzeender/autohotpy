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

if ([1].Length) {
    MsgBox 'yes'
}
else {
    MsgBox 'no'
}