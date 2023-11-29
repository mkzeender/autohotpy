import time
from autohotpy import ahk_runstr
from autohotpy.ahk_instance import AhkState


if __name__ == "__main__":
    ahk = ahk_runstr("#include testit.ahk")

    print(f"Object Has Base: {ahk.my_hoop.base}")

    ahk.run_forever()
    print("exiting")
