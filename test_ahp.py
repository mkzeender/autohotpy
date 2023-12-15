import math
import time
from autohotpy import ahk_runstr
from autohotpy.ahk_instance import AhkState


def main():
    ahk = ahk_runstr("#include testit.ahk")

    ahk['::shit::\n{MsgBox("language")\n}']

    ahk["b"::](ahk.MsgBox)

    print(ahk.MsgBox("test_ahp"))
    print(ahk.my_empty)

    ahk["^q" :: ahk.ExitApp]

    ahk.run_forever()


if __name__ == "__main__":
    main()
