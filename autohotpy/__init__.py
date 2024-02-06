from .ahk_instance import AhkInstance
from .global_state import config
from .ahk_run import ahk_runstr

from .convenience.py_lib import pylib as Python
import argparse


def main(*args: str):
    """Run an Autohotkey script with the power of Python. Use the built-in Python
    module to access builtin python functions and classes, and use Python.import()
    to import python modules into autohotkey"""
    parser = argparse.ArgumentParser(
        "autohotpy",
        None,
        description=main.__doc__,
    )

    parser.add_argument("SCRIPT", type=str)
    parser.add_argument(
        "-c",
        "--run-str",
        help="Treat SCRIPT as autohotkey code, instead of a filename",
        action="store_true",
    )

    space = parser.parse_args()
    if space.run_str:
        ahk_runstr(space.SCRIPT)
    else:
        ahk_runstr(f"#include {space.SCRIPT}")
