"""
Different timbres
"""

from typing import Iterable
from .basic import sine, square, triangle, stack, scale
from .type import Frequency, Audio, Timbre


def sine_timbre() -> Timbre:
    """
    Returns a timbre that uses sine waves.
    """
    return sine


def square_timbre() -> Timbre:
    """
    Returns a timbre that uses square waves.
    """
    return square


def triangle_timbre() -> Timbre:
    """
    Returns a timbre that uses triangle waves.
    """
    return triangle


def piano(overtunes_multiplier: Iterable[float]) -> Timbre:
    """
    Returns a timbre that sounds like a piano.
    It has overtones proportional to base frequency for n in overtunes_multiplier.

    Note: overtunes_multiplier[0] should be 1 in most cases in order to preserve base frequency loudness.
    """

    def _piano(hz: Frequency) -> Audio:
        overtune_waves = []
        for i, multiplier in enumerate(overtunes_multiplier):
            overtune_waves.append(scale(sine(hz * i), multiplier))
        return stack(*overtune_waves)

    return _piano


def default_piano() -> Timbre:
    """
    Returns a timbre that sounds like a piano.
    """
    return piano([1, 0.5, 0.25, 0.125, 0.0625, 0.03125, 0.15625, 0.078125])
