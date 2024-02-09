from typing import Literal
from autohotpy import ahk as mod

Array = mod.Array

res = mod.Array[Literal[1]](1, 1, 1)
