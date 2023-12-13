from __future__ import annotations

from abc import ABC
from typing import Callable, Generic, Protocol, TypeVar, overload
import typing

Start = TypeVar("Start", covariant=True)
Stop = TypeVar("Stop", covariant=True)
Step = TypeVar("Step", covariant=True)

Func = TypeVar("Func", bound=Callable, covariant=True)


class MySliceA(ABC):
    ...


class MySlice(Protocol[Start, Stop, Step]):
    start: property
    stop: property
    step: property


bruh: MySlice[int, int, int] = slice(1, 2, 3)

bruh.start
