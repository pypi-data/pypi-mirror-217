"""
AnyMusic is a collection of tools to create theoretically any music from the very basics of sine
waves.
"""

from .basic import sine, square, triangle, stack, scale, composition, from_to, shift
from .scale import really_generic_scale_system, traditional_scale_system
from .timbre import sine_timbre, square_timbre, triangle_timbre, piano, default_piano
from .type import Audio, ScaleSystem, Frequency, Octave, Semitone, Time
from .wave import write_file, read_file

__version__ = "0.0.0"
