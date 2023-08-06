"""
Contains basic functions for generating sound waves.
"""

import math
import functools
from typing import Callable, TypeVar

from .type import Audio, Frequency, Time


R = TypeVar("R")
S = TypeVar("S")
T = TypeVar("T")


def sine(hz: Frequency) -> Audio:
    """
    Returns a sine wave of the given frequency.
    """
    return lambda t: math.sin(t * hz * math.pi * 2)


def square(hz: Frequency) -> Audio:
    """
    Returns a square wave of the given frequency.
    """
    return lambda t: 1 if math.sin(t * hz * math.pi * 2) > 0 else -1


def triangle(hz: Frequency) -> Audio:
    """
    Returns a triangle wave of the given frequency.
    """
    return lambda t: 1 - abs((t * hz * 2) % 2 - 1) * 2


def stack(*fs: Audio) -> Audio:
    """
    Returns sum of the given functions.
    """
    return lambda t: functools.reduce(lambda x, y: x + y, [f(t) for f in fs])


def scale(f: Audio, factor: float) -> Audio:
    """
    Returns a scaled version of the given function.
    """
    return lambda t: f(t) * factor


def composition(f: Callable[[S], T], g: Callable[[R], S]) -> Callable[[R], T]:
    """
    Returns the composition of the given functions, that is, f(g(x)).
    """
    return lambda t: f(g(t))


def from_to(f: Audio, start: Time, end: Time) -> Audio:
    """
    Returns a function that is 0 before start and after end.
    """
    return lambda t: f(t) if start <= t <= end else 0


def shift(f: Audio, offset: Time) -> Audio:
    """
    Returns a function that is shifted by the given offset.
    """
    return lambda t: f(t - offset)
