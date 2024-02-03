import math
import time
from autohotpy import ahk_runstr


def main():
    ahk = ahk_runstr("#include testit.ahk")

    print("starting...")

    ahk.my_py_thing = ["hoo", "wut"]

    ahk.caller(print)

    print(ahk.my_py_thing)

    ahk["^q" :: ahk.ExitApp]
    ahk["^h" :: lambda: print("hello world")]

    print("idling...")
    ahk.run_forever()


if __name__ == "__main__":
    main()
