# mymusiclib/notes.py
# Basic utilities for handling musical notes, including MIDI conversions with Unicode accidentals.

NOTES_SHARP = ['C', 'C\u266F', 'D', 'D\u266F', 'E', 'F', 'F\u266F', 'G', 'G\u266F', 'A', 'A\u266F', 'B']
NOTES_FLAT = ['C', 'D\u266D', 'D', 'E\u266D', 'E', 'F', 'G\u266D', 'G', 'A\u266D', 'A', 'B\u266D', 'B']

def note_to_midi(note):
    """
    Convert a note name to MIDI number.
    Handles both ASCII and Unicode accidentals, including rare enharmonics like B#, E#, Fb, Cb.
    Args:
        note (str): Note name (e.g., 'Bb3', 'B\u266D3', 'C#4', 'B#4').
    Returns:
        int: MIDI number (e.g., 58 for Bb3).
    """
    # Normalize Unicode to ASCII for lookup
    note = note.replace('\u266F', '#').replace('\u266D', 'b')
    notes = {
        'C': 0, 'B#': 0,
        'C#': 1, 'Db': 1,
        'D': 2,
        'D#': 3, 'Eb': 3,
        'E': 4, 'Fb': 4,
        'F': 5, 'E#': 5,
        'F#': 6, 'Gb': 6,
        'G': 7,
        'G#': 8, 'Ab': 8,
        'A': 9,
        'A#': 10, 'Bb': 10,
        'B': 11, 'Cb': 11
    }
    pitch_class = note[:-1]
    octave = int(note[-1])
    return notes[pitch_class] + (octave + 1) * 12

def midi_to_note(midi, prefer_sharp=True):
    """
    Convert MIDI number to note name with Unicode accidentals.
    Uses common names; rare enharmonics (B#, E#, Fb, Cb) handled in spelling logic elsewhere.
    Args:
        midi (int): MIDI number (e.g., 60 for C4).
        prefer_sharp (bool): Prefer sharps (True) or flats (False).
    Returns:
        str: Note name (e.g., 'C4', 'A\u266F3', 'B\u266D3').
    """
    pc = midi % 12
    octave = midi // 12 - 1
    names = NOTES_SHARP if prefer_sharp else NOTES_FLAT
    return f"{names[pc]}{octave}"