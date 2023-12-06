# Autohotpy
This is still in development, some features will not work as described.

## Getting Started (for python users)
Start by creating an empty Autohotkey script, or importing an existing Autohotkey V2 script:

```python
from autohotpy import ahk_script

script = ahk_script()
```

```python
script = ahk_script('my_ahk_script.ahk')
```

You are now free to access any built-in or user-defined functions, classes and global variables!

```python
script.MsgBox('hello world!')
clipboard_contents = script.A_ClipBoard
script.my_custom_function('blah blah', 42)
```

## Hotkeys
You may use square bracket notation to define a hotkey. You can also treat it as a decorator.
```python
script['^p'::script.Pause]

@script['^h'::]
def example():
    print('Hotkeys are cool!')
```
