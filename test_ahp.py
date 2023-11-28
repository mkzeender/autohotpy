from ctypes import *
import time
from autohotpy import CLOSE, AhkInstance, ahk_script, config



# def my_func(thing):
#     thing = c_double(thing)
#     print(repr(thing))
#     print(thing)
#     print('cool')
#     return 0

ahk = ahk_script('#include testit.ahk')

print('thingy', ahk.state)

ahk.wait()


print('ready')

ahk.wait(CLOSE)


from autohotpy._dtypes import value_from_buffer

buf = (c_char*64)(b'\x00')