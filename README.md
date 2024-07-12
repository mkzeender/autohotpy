# Autohotpy
This is still in development, some features will not work as described.

## Using AHK from a Python script
Import the module, and use any autohotkey function, class, object, etc. Refer to the [Autohotkey built-in functions and classes](https://www.autohotkey.com/docs/v2/lib/index.htm).

```python
from autohotpy import ahk
ahk.MsgBox('hello world!')
clipboard_contents = ahk.A_ClipBoard

array = ahk.Array('foo', 'bar')
array.Push('baz')
for elem in array:
    print(elem) # foo, bar, baz
```


You can include an Autohotkey v2 script using ```include()```, and access its functions, classes, and global variables.
```python
ahk.include('my_ahk_script.ahk')
ahk.custom_function(1, 2, 3)
my_ahk_obj = ahk.MyClass()
my_ahk_obj.method()
```


### Hotkeys
You may use __square bracket notation__ to define a hotkey. You can also treat it as a decorator.
```python
ahk['!g'::'^t'] # remap alt+g to ctrl+t

ahk['^p'::my_function] # ctrl+p runs my_function

@ahk['^h'::] # ctrl+h runs this function
def example(this_hotkey):
    print(f'You pressed {this_hotkey}')

ahk.run_forever() # keep the script alive
```

Check out [Hotkeys and Keyboard Shortcuts](https://www.autohotkey.com/docs/v2/Hotkeys.htm) to learn about Hotkeys in Ahk.

Square bracket notation can also be used to run arbitrary Ahk code and to define [Hotstrings](https://www.autohotkey.com/docs/v2/Hotstrings.htm)

```python
ahk['#ErrorStdOut']

ahk['::btw::by the way']
@ahk['::shit'::]
def cap():
    ahk.MsgBox('Language!')

ahk.run_forever()
```

## Using Python from an AHK script

Make sure python and autohotpy are installed.

Open a terminal and run your autohotkey script:

```sh
python -m autohotpy my_script.ahk
```

Autohotpy only supports v2.0-beta.1 so you may need to use

```autohotkey
#Requires AutoHotkey v2.0-beta.1
```

Use the "Python" variable to access [built-in python functions and classes](https://docs.python.org/3/library/functions.html) and [constants](https://docs.python.org/3/library/constants.html).

```autohotkey
Python.print("hello world!")

my_list := Python.list(["foo", "bar"])
my_list.append("baz")
for value in my_list {
    MsgBox value
}
```
Import python modules:
```autohotkey
math := Python.import("math")
MsgBox math.factorial(5)
```