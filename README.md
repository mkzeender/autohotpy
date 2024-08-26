# Autohotpy
This is still in development, some features will not work as described, and everything is subject to change.

For AutoHotkey users, this serves as a way to use powerful python libraries in your AutoHotkey scripts. The python ecosystem is very well-developed -- there's a library for everything -- and is much easier to use than COM objects and DLLCalls. See [using Python from an AHK script](#using-python-from-an-ahk-script).

For Python users, AutoHotkey is a very intelligent automation language, and I find it is more intuitive, consistent, and human-friendly than i.e. pywinauto. Other python libraries have used 

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

Square bracket notation can also be used to run arbitrary AHK code and to define [Hotstrings](https://www.autohotkey.com/docs/v2/Hotstrings.htm)

```python
ahk['#ErrorStdOut']

ahk['::btw::by the way']

@ahk['::shit'::]
def captain_america_meme():
    ahk.MsgBox('Language!')

ahk.run_forever()
```
### Calling Functions
Some AutoHotkey functions (and classes) have optional parameters. If you would like to omit a parameter in the middle of a parameter list, use UNSET.

```python
from autohotpy import ahk, UNSET

ahk.MouseClick("Left", UNSET, UNSET, 3)

```

Some AutoHotkey functions have ByRef parameters (where you pass a reference to a variable, and the function puts a value into that variable). Since Python doesn't have ByRef parameters, you will have to create explicitly create a reference to an AHK variable and then explicitly access its value:

```python

from autohotpy.ahk import MouseGetPos, VarRef

MouseGetPos(x := VarRef(), y := VarRef())

print(f"The mouse is at coords {x.value}, {y.value})

```


## Using Python from an AHK script

Install Python (minimum version 3.12). Install autohotpy.

Open a terminal and run your autohotkey script:

```sh
python -m autohotpy my_script.ahk
```

Autohotpy only supports v2.0-beta.1 so you may need to use

```AutoHotkey
#Requires AutoHotkey v2.0-beta.1
```

Use the "Python" module to access [built-in python functions, classes](https://docs.python.org/3/library/functions.html) and [constants](https://docs.python.org/3/library/constants.html).

```AutoHotkey
Python.print("hello world!")

my_list := Python.list(["foo", "bar"])
my_list.append("baz")
for value in my_list {
    MsgBox value
}
```
Import python modules, and access their functions, classes, and global variables.

```AutoHotkey
math := Python.import("math")
MsgBox math.factorial(5)
```

Python files (i.e. ```my_module.py```), as well as published modules installed using ```pip install my_module``` can both be imported this way!


## Documentation

Here will be a complete documentation of everything added and modified by this package.


### Added Autohotkey built-ins

From Python, these should be imported from autohotpy.ahk.

#### Function ```include(script_path)```

Import (and run) the AutoHotkey script file 'script_path'.

Only available from the main Python thread.

----

#### Function ```run_forever()```

Run AutoHotkey forever (roughly equivalent to ```ahk.Sleep(infinity)```).

Only available from the main Python thread.

----

#### Object ```UNSET```

Alias to autohotpy.UNSET (see below)

Only available from Python.

----

#### Module ```Python```

Contains all built-in Python functions, classes, and globals (see the python documentation)

---

#### Function ```Python.import(module_name)```

Imports a Python module and returns it, allowing access to that module's functions, classes, and globals.

---
---
---

### Module ```autohotpy```

The root package.

---

#### Module ```autohotpy.ahk```

Contains all built-in and user-defined AutoHotkey functions, classes and globals (see the [official AutoHotkey docs](https://www.autohotkey.com/docs/v2/lib/index.htm))

----

#### Module ```autohotpy.Python```

Alias for ```Python```


----

#### Object ```autohotpy.UNSET```

Represents a missing or omitted value. Passing this value to an AHK function will use that parameter's default value, and setting something in AHK to UNSET is equivalent to deleting it using a ```del``` statement.

----

#### Function ```autohotpy.iterator(loopable [, n])```

Allows you to access more than one item-value at a time in a for-loop. 

```n``` should be the number of variables in the loop (defaults to 2). For example:

```python
my_array = ahk.Array('foo', 'bar', 'baz')

for a_index, value in iterator(my_array, 2):
    ...

```

Note: you don't need this function to use an AHK object in a for-loop with only one variable:

```python
for value in my_array:
    ...
```

----

#### Object ```autohotpy.config```

Advanced settings that can be set before importing autohotpy.ahk

##### Integer|None ```autohotpy.config.dpi_scale_mode```

Set to None to disable setting the process's dpi scaling

##### Boolean ```autohotpy.config.ctrl_c_exitapp```

Set to False to disable capturing ctrl+c in the console to call autohotpy.ahk.ExitApp

----