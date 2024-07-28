from dataclasses import dataclass

from time import perf_counter

from autohotpy import ahk
import os

# ahk.include(r"testit.ahk")


def get_count(obj):
    # return ahk._ahk_instance.communicator.py_references.get_refcount(obj)
    ...


def crap(h):
    arr = ahk.Array[int](1, 2, 3)
    print("starting...")

    start = perf_counter()
    for i in range(1000):

        for val in arr:
            ...
    end = perf_counter()
    print("done", end - start)


@dataclass
class Wut:
    foo: dict


def main():
    # ahk["^q" :: ahk.ExitApp]
    # ahk["^h" :: ahk.caller]
    # ahk["!s"::crap]

    # thing: ahk.Object = ahk.my_obj

    # ref: ahk.VarRef = ahk.VarRef(thing)

    # print(ref.value)

    # ahk.test_iter({"hi": "cool", "foo": "bar"})
    # print(ahk.OwnProps(ahk.caller("")))

    # print(ahk.my_hoopla.goop[1, 2])

    # ahk.my_py_thing = Wut({"world": "cool"})

    # ahk.my_obj.foo["baz"] = "who?"

    # print(ahk.my_obj.foo["bar"])

    # print(ahk._Python.on_error(Exception("hi")))

    # print(f"caller returned {ahk.caller('weee')}")

    ahk.run_forever()


if __name__ == "__main__":
    main()
