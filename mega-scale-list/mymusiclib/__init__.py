# mymusiclib/__init__.py
# Marks mymusiclib as a Python package and exposes key functions/classes.

__version__ = "0.1.1"  # Updated version after integrating tools_claude

from .notes import note_to_midi, midi_to_note
from .scales import Scale, Arpeggio, get_preferred_spelling
from .instrument import Instrument
from .tools import generate_scale_table

# Import from tools_claude
from .tools_claude import (
    collections,
    calculate_weighting_function,
    generate_modes_chart,
    generate_filtered_modes_chart,
)

# Optionally import the reordering function if you plan to use it broadly
# from .tools_claude_reorder import reorder_collections_by_weight
