from dataclasses import dataclass
from autohotpy import ahk_runstr
from autohotpy.convenience.map_view import MapView


def crap(h):
    raise ValueError(h)


@dataclass
class Wut:
    foo: dict


def main():
    ahk = ahk_runstr("#include testit.ahk")
    ahk["^q" :: ahk.ExitApp]
    ahk["^h" :: ahk.caller]
    ahk["!s"::crap]

    print("starting...")

    arr = MapView(ahk.Map(5, 4, 7, 4, 1, "ooo"))

    for k, v in arr.items():
        print(k, v)

    # ahk.test_iter({"hi": "cool", "foo": "bar"})
    # print(ahk.OwnProps(ahk.caller("")))

    # print(ahk.my_hoopla.goop[1, 2])

    # ahk.my_py_thing = Wut({"world": "cool"})

    # ahk.my_obj.foo["baz"] = "who?"

    # print(ahk.my_obj.foo["bar"])

    # print(ahk._Python.on_error(Exception("hi")))

    # print(f"caller returned {ahk.caller('weee')}")

    print(ahk.my_py_thing)

    print("idling...")
    ahk.run_forever()


if __name__ == "__main__":
    main()
