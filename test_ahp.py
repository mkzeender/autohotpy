import math
import time
from autohotpy import ahk_runstr
from autohotpy.ahk_instance import AhkState


if __name__ == "__main__":
    ahk = ahk_runstr("#include testit.ahk")
    a = time.perf_counter()
    for i in range(5000):
        ahk.Sin(10)
    b = time.perf_counter()
    ahk.MsgBox(f"{(b-a)} seconds")
    ahk.run_forever()
    print("exiting")
