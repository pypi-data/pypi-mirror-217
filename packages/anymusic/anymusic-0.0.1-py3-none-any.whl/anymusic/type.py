"""
Common types.
"""

from typing import Callable

Time = float  # In seconds
Frequency = float  # In Hz
Octave = int  # In octaves (but not necessarily the traditional 12-EDO)
Semitone = int  # In semitones, [0, x-EDO]

# Time |-> Amplitude
# Where Time is in seconds and Amplitude is in [-1, 1]
Audio = Callable[[Time], Frequency]

# Octaves, Semitones |-> Frequency
# Where Octaves is the number of octaves above the base frequency and Semitones is the number of semitones above the
# current octave.
ScaleSystem = Callable[[Octave, Semitone], Frequency]

# Frequency |-> Sec2Amp
# Where Frequency is the base frequency of the wave.
Timbre = Callable[[Frequency], Audio]
