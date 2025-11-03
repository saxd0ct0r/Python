class Pitch:
    """Represents a musical pitch with explicit spelling (letter, accidental, octave)."""
    
    # Class constants
    LETTERS = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
    LETTER_TO_SEMITONE = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
    
    # Unicode accidentals
    ACCIDENTAL_SYMBOLS = {
        -2: '𝄫',  # double flat
        -1: '♭',
         0: '♮',
         1: '♯',
         2: '𝄪'   # double sharp
    }
    
    def __init__(self, letter, accidental, octave):
        """
        Create a pitch with explicit spelling.
        
        Args:
            letter: 'A' through 'G'
            accidental: -2 (double flat) through 2 (double sharp)
            octave: integer (MIDI octave numbering, where C4 = middle C)
        """
        if letter not in self.LETTERS:
            raise ValueError(f"Letter must be one of {self.LETTERS}")
        if not -2 <= accidental <= 2:
            raise ValueError("Accidental must be between -2 and 2")
        
        self.letter = letter
        self.accidental = accidental
        self.octave = octave
        self._midi_cache = None
    
    def to_midi(self):
        """Convert to MIDI number (C4 = 60)."""
        if self._midi_cache is None:
            semitone = self.LETTER_TO_SEMITONE[self.letter]
            self._midi_cache = (self.octave + 1) * 12 + semitone + self.accidental
        return self._midi_cache
    
    @classmethod
    def from_midi(cls, midi_number, letter=None, accidental=None):
        """
        Create Pitch from MIDI number with specified spelling.
        
        If letter/accidental not specified, defaults to sharp spelling for black keys.
        """
        octave = (midi_number // 12) - 1
        pitch_class = midi_number % 12
        
        if letter is not None and accidental is not None:
            # Validate that the spelling matches the MIDI number
            test_pitch = cls(letter, accidental, octave)
            if test_pitch.to_midi() != midi_number:
                raise ValueError(f"Spelling {letter}{accidental} doesn't match MIDI {midi_number}")
            return test_pitch
        
        # Default spelling (sharps for black keys)
        natural_notes = {0: 'C', 2: 'D', 4: 'E', 5: 'F', 7: 'G', 9: 'A', 11: 'B'}
        if pitch_class in natural_notes:
            return cls(natural_notes[pitch_class], 0, octave)
        
        # Black keys - default to sharp
        sharp_notes = {1: ('C', 1), 3: ('D', 1), 6: ('F', 1), 8: ('G', 1), 10: ('A', 1)}
        letter, acc = sharp_notes[pitch_class]
        return cls(letter, acc, octave)
    
    def __str__(self):
        """Return formatted string with Unicode accidentals."""
        if self.accidental == 0:
            return f"{self.letter}{self.octave}"
        else:
            acc_symbol = self.ACCIDENTAL_SYMBOLS[self.accidental]
            return f"{self.letter}{acc_symbol}{self.octave}"
    
    def __repr__(self):
        return f"Pitch('{self.letter}', {self.accidental}, {self.octave})"
    
    def __eq__(self, other):
        """Pitches are equal if they have the same spelling (not just same MIDI)."""
        if not isinstance(other, Pitch):
            return False
        return (self.letter == other.letter and 
                self.accidental == other.accidental and 
                self.octave == other.octave)
    
    def __hash__(self):
        return hash((self.letter, self.accidental, self.octave))
    
    def midi_equal(self, other):
        """Check if two pitches sound the same (enharmonic equivalents)."""
        return self.to_midi() == other.to_midi()
    
    def __lt__(self, other):
        """Compare pitches by MIDI number."""
        return self.to_midi() < other.to_midi()
    
# Test the Pitch class

def test_pitch_basic():
    """Test basic pitch creation and string representation."""
    print("=== Test Basic Pitch Creation ===")
    
    # Natural note
    c4 = Pitch('C', 0, 4)
    print(f"C natural 4: {c4}")  # Should be: C4
    print(f"MIDI: {c4.to_midi()}")  # Should be: 60
    
    # Sharp
    c_sharp4 = Pitch('C', 1, 4)
    print(f"C sharp 4: {c_sharp4}")  # Should be: C♯4
    print(f"MIDI: {c_sharp4.to_midi()}")  # Should be: 61
    
    # Flat
    d_flat4 = Pitch('D', -1, 4)
    print(f"D flat 4: {d_flat4}")  # Should be: D♭4
    print(f"MIDI: {d_flat4.to_midi()}")  # Should be: 61
    
    # Double sharp
    c_double_sharp4 = Pitch('C', 2, 4)
    print(f"C double sharp 4: {c_double_sharp4}")  # Should be: C𝄪4
    print(f"MIDI: {c_double_sharp4.to_midi()}")  # Should be: 62
    
    print()

def test_enharmonic_equivalents():
    """Test that enharmonic equivalents have same MIDI but different spelling."""
    print("=== Test Enharmonic Equivalents ===")
    
    c_sharp4 = Pitch('C', 1, 4)
    d_flat4 = Pitch('D', -1, 4)
    
    print(f"{c_sharp4} and {d_flat4}")
    print(f"Same MIDI? {c_sharp4.midi_equal(d_flat4)}")  # Should be: True
    print(f"Equal spelling? {c_sharp4 == d_flat4}")  # Should be: False
    print()

def test_from_midi():
    """Test creating pitches from MIDI numbers."""
    print("=== Test from_midi() ===")
    
    # Natural note
    pitch1 = Pitch.from_midi(60)
    print(f"MIDI 60 (default): {pitch1}")  # Should be: C4
    
    # Black key (default to sharp)
    pitch2 = Pitch.from_midi(61)
    print(f"MIDI 61 (default): {pitch2}")  # Should be: C♯4
    
    # Specify spelling as flat
    pitch3 = Pitch.from_midi(61, 'D', -1)
    print(f"MIDI 61 (as D♭): {pitch3}")  # Should be: D♭4
    
    print()

def test_comparison():
    """Test pitch comparison."""
    print("=== Test Comparison ===")
    
    bb3 = Pitch('B', -1, 3)
    c4 = Pitch('C', 0, 4)
    db4 = Pitch('D', -1, 4)
    
    print(f"{bb3} < {c4}? {bb3 < c4}")  # Should be: True
    print(f"{c4} < {db4}? {c4 < db4}")  # Should be: True
    print(f"{bb3} < {db4}? {bb3 < db4}")  # Should be: True
    
    # Sort a list of pitches
    pitches = [db4, bb3, c4]
    pitches.sort()
    print(f"Sorted: {[str(p) for p in pitches]}")  # Should be: ['B♭3', 'C4', 'D♭4']
    
    print()

def test_alto_sax_range():
    """Test creating pitches for alto saxophone range (your example)."""
    print("=== Test Alto Sax Range ===")
    
    # Your examples from the weighting discussion
    bb3 = Pitch('B', -1, 3)
    c4 = Pitch('C', 0, 4)
    db4 = Pitch('D', -1, 4)
    cb4 = Pitch('C', -1, 4)
    
    print(f"First segment: {bb3}, {c4}, {db4}")
    print(f"Second segment: {bb3}, {cb4}, {db4}")
    print(f"MIDI numbers: {bb3.to_midi()}, {c4.to_midi()}, {db4.to_midi()}")
    print(f"C♮4 and C♭4 same MIDI? {c4.midi_equal(cb4)}")  # Should be: False
    
    print()

def test_invalid_input():
    """Test error handling."""
    print("=== Test Invalid Input ===")
    
    try:
        bad_pitch = Pitch('H', 0, 4)  # Invalid letter
        print("ERROR: Should have raised ValueError")
    except ValueError as e:
        print(f"Caught expected error: {e}")
    
    try:
        bad_pitch = Pitch('C', 3, 4)  # Invalid accidental
        print("ERROR: Should have raised ValueError")
    except ValueError as e:
        print(f"Caught expected error: {e}")
    
    try:
        # Wrong spelling for MIDI number
        bad_pitch = Pitch.from_midi(60, 'D', -1)  # D♭ is MIDI 61, not 60
        print("ERROR: Should have raised ValueError")
    except ValueError as e:
        print(f"Caught expected error: {e}")
    
    print()

# Run all tests
if __name__ == "__main__":
    test_pitch_basic()
    test_enharmonic_equivalents()
    test_from_midi()
    test_comparison()
    test_alto_sax_range()
    test_invalid_input()
    print("=== All tests complete ===")