# Autohotpy
This is still in development, some features will not work as described.

## Getting Started (for python users)
Start by creating an empty Autohotkey script, or importing an existing Autohotkey V2 script:

```python
from autohotpy import ahk_runstr

ahk = ahk_runstr()
```

```python
ahk = ahk_runstr('#include my_ahk_script.ahk')
```

You are now free to access any built-in or user-defined functions, classes and global variables!

```python
ahk.MsgBox('hello world!')
clipboard_contents = ahk.A_ClipBoard
ahk.my_custom_function('blah blah', 42)
```

## Hotkeys
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

