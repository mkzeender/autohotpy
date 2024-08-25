from typing import Callable
import pytest
from autohotpy import ahk
from autohotpy.communicator.references import set_debug

set_debug(True)

ahk.include("tests/test_errors.ahk")
f = ahk.call_me_back


thingy = object()


def _returns():
    return "hello"


def _returns_obj():
    return thingy


def _raises():
    raise ValueError("well darn")


def _generate_stack(stack_size: int, callback: Callable, args: tuple):
    if stack_size > 0:
        return f(_generate_stack, stack_size - 1, callback, args)
    else:
        return callback(*args)


def test_stack():

    assert f(_returns) == "hello"
    assert f(f, f, f, f, f, f, f, _returns) == "hello"

    assert f(_returns_obj) is thingy

    assert _generate_stack(10, _returns_obj, ()) is thingy


def test_raise():

    with pytest.raises(ValueError):
        f(_raises)

    with pytest.raises(ValueError):
        _generate_stack(10, _raises, ())
