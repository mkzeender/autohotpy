# Autohotpy
This is still in development, some features will not work as described.

## Getting Started (for python users)
Start by creating an empty Autohotkey script

```python
from autohotpy import include

ahk = include()
```
Or importing an existing Autohotkey V2 script:
```python
ahk = include('my_ahk_script.ahk')
```

You are now free to access any built-in functions or user-defined, classes and global variables! Refer to the [Autohotkey built-in functions and classes](https://www.autohotkey.com/docs/v2/lib/index.htm).

```python
ahk.MsgBox('hello world!')
clipboard_contents = ahk.A_ClipBoard
ahk.my_custom_function('blah blah', 42)
```

### Hotkeys
You may use square bracket notation to define a hotkey. You can also treat it as a decorator.
```python
ahk['^p'::my_function] # ctrl+p runs my_function

@ahk['^h'::] # ctrl+h runs this function
def example(this_hotkey):
    print(f'You pressed {this_hotkey}')
```

For a list of hotkey codes, check out [Hotkeys and Keyboard Shortcuts](https://www.autohotkey.com/docs/v2/Hotkeys.htm) on the Autohotkey Docs

Square bracket notation can also be used to append arbitrary Ahk code to the script, and to define [Hotstrings](https://www.autohotkey.com/docs/v2/Hotstrings.htm)

```python
ahk['#ErrorStdOut']

ahk['::btw::by the way']
@ahk['::shit'::]
def cap():
    ahk.MsgBox('Language!')
```

## Getting Started (for Ahk users)

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
```
Import python modules:
```autohotkey
math := Python.import("math")
MsgBox math.factorial(5)
```