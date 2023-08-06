"""
Make human-recognizable regular sounds.
"""

from .type import ScaleSystem, Frequency


def really_generic_scale_system(base_freq: Frequency, base: float, eqtm: float) -> ScaleSystem:
    """
    Traditional music scale systems use C * 2^( a + b * 1/12 ) as the frequency where it is the a * 12 + b semitones
    above the base frequency.
    However it can be further generalized to C * BASE^( a + b * EQTM ) where EQTM is the equal temperament.

    For example, for a 24-EDO scale, BASE is 2 and EQTM is 1/24.
    """
    return lambda a, b: base_freq * (base ** (a + b * eqtm))


def traditional_scale_system() -> ScaleSystem:
    """
    Returns the traditional equal temperament scale system.
    """
    # Starting from C0, the base frequency is 16.3 Hz.
    return really_generic_scale_system(16.3, 2, 1 / 12)
