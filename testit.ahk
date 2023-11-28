#Requires AutoHotkey v2.0-beta.1

thing := '12345🏳️‍⚧️'

my_float := 1.2

exit_func(r, c) {
    MsgBox 'Exiting'
}


OnExit(exit_func, 1)

sleep 1000


