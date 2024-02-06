from dataclasses import dataclass
from autohotpy import ahk_runstr
from autohotpy.convenience.map_view import MapView
from autohotpy.proxies.ahk_object import AhkObject


ahk = ahk_runstr("#include testit.ahk")


def get_count(obj):
    return ahk._ahk_instance.communicator.py_references.get_refcount(obj)


def crap(h):
    raise ValueError(h)


@dataclass
class Wut:
    foo: dict


def main():
    ahk["^q" :: ahk.ExitApp]
    ahk["^h" :: ahk.caller]
    ahk["!s"::crap]

    print("starting...")
    thing: AhkObject = ahk.my_obj
    for i in range(153):
        thing = ahk.my_obj
    print(ahk.ObjAddRef(thing._ahk_ptr))

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
