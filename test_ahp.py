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
    ahk["!s"::shit]

    @ahk["^b"::]
    def hi(t):
        print("that works!")

    x, y = ahk.ref("init", "init2")
    z = ahk.ref("init")

    ahk.MouseGetPos(x, y, z)

    print(x.value, y.value, z.value)

    print("starting...")
    # print(ahk.OwnProps(ahk.caller("")))

    # ahk.my_hoop.goop[1, 2] = "fart"
    # print(ahk.my_hoopla.goop[1, 2])

    # ahk.my_py_thing = Wut({"world": "cool"})

    # ahk.my_obj.foo["baz"] = "who?"

    # print(ahk.my_obj.foo["bar"])

    # print(ahk._Python.on_error(Exception("hi")))

    print(f"caller returned {ahk.caller('weee')}")

    print(ahk.my_py_thing)

    print("idling...")
    ahk.run_forever()


if __name__ == "__main__":
    main()
