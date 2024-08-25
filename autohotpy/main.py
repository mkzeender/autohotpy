import argparse

from autohotpy import ahk


def main(*args: str):
    """Run an Autohotkey script with the power of Python. Use the built-in Python
    module to access builtin python functions and classes, and use Python.import()
    to import python modules into autohotkey"""
    parser = argparse.ArgumentParser(
        prog="autohotpy",
        usage=None,
        description=main.__doc__,
    )

    parser.add_argument("SCRIPT", type=str)
    parser.add_argument(
        "-c",
        "--run-str",
        help="Treat SCRIPT as autohotkey code, instead of a filename",
        action="store_true",
    )

    space = parser.parse_args(args=args)
    if space.run_str:
        ahk[space.SCRIPT]
    else:
        ahk[f"#include {space.SCRIPT}"]
