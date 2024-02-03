import math
import time
from autohotpy import ahk_runstr


def main():
    ahk = ahk_runstr("#include testit.ahk")
    ahk["^q" :: ahk.ExitApp]
    ahk["^h"::print]

    print("starting...")

    ahk.my_py_thing = {"world": "cool"}

    # print(f"caller returned {ahk.caller('world')}")

    print(ahk.my_py_thing)

    print("idling...")
    ahk.run_forever()


if __name__ == "__main__":
    main()
