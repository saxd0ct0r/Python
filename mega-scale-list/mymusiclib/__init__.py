# mymusiclib/__init__.py
# Marks mymusiclib as a Python package and exposes key functions/classes.

__version__ = "0.1.0"  # Version of the music library.

from .notes import note_to_midi, midi_to_note
from .scales import Scale, Arpeggio, get_preferred_spelling
from .instrument import Instrument
from .segments import generate_segments
from .tools import generate_distribution_table, print_distribution_table