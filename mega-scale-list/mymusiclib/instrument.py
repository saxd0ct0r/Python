# mymusiclib/instrument.py
# Defines a player's pitch range for an instrument, used for scale/arpeggio segment generation.

from .notes import note_to_midi, midi_to_note

class Instrument:
    """
    Represents a player's pitch range for an instrument, defined by lowest and highest playable notes.
    No transposition handling, per project requirements.
    """
    def __init__(self, name, min_note, max_note):
        """
        Initialize the instrument with a name and pitch range.
        Args:
            name (str): Instrument name (e.g., 'Alto Sax').
            min_note (str or int): Lowest playable note (e.g., 'Bb3' or MIDI 58).
            max_note (str or int): Highest playable note (e.g., 'Bb7' or MIDI 106).
        Raises:
            ValueError: If min_note > max_note or notes are invalid.
        """
        self.name = name
        # Convert to MIDI if string, else use directly
        self.min_midi = note_to_midi(min_note) if isinstance(min_note, str) else min_note
        self.max_midi = note_to_midi(max_note) if isinstance(max_note, str) else max_note
        # Validate range
        if self.min_midi > self.max_midi:
            raise ValueError(f"Min note ({min_note}) must be <= max note ({max_note})")
    
    def get_min_note(self):
        """
        Return the lowest playable note as a string.
        Returns:
            str: Note name (e.g., 'Bb3').
        """
        return midi_to_note(self.min_midi, prefer_sharp=False)  # Flats for consistency
    
    def get_max_note(self):
        """
        Return the highest playable note as a string.
        Returns:
            str: Note name (e.g., 'Bb7').
        """
        return midi_to_note(self.max_midi, prefer_sharp=False)
    
    def get_min_midi(self):
        """
        Return the lowest playable note as MIDI number.
        Returns:
            int: MIDI number (e.g., 58 for Bb3).
        """
        return self.min_midi
    
    def get_max_midi(self):
        """
        Return the highest playable note as MIDI number.
        Returns:
            int: MIDI number (e.g., 106 for Bb7).
        """
        return self.max_midi