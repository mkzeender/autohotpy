from dataclasses import dataclass
import math
import time
from autohotpy import ahk_runstr


def shit(h):
    raise ValueError(h)


@dataclass
class Wut:
    foo: dict


def main():
    ahk = ahk_runstr("#include testit.ahk")
    ahk["^q" :: ahk.ExitApp]
    ahk["^h" :: ahk.caller]

    print("starting...")

    ahk.my_py_thing = Wut({"world": "cool"})

    # print(ahk._Python.on_error(Exception("hi")))

    print(f"caller returned {ahk.caller('weee')}")

    print(ahk.my_py_thing)

    print("idling...")
    ahk.run_forever()


if __name__ == "__main__":
    main()
