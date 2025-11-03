# mymusiclib/scales.py
# Core module for handling musical collections (scales, arpeggios, etc.).
# Provides generation (MIDI notes) and spelling logic for well-formed note names.

from .notes import note_to_midi, midi_to_note

# Define letter names for scale/arpeggio spelling (A-G cycle).
letters = 'ABCDEFG'

# Map base pitch classes (no accidentals) to MIDI pitch classes (C=0, ..., B=11).
base_pc = {'A': 9, 'B': 11, 'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7}

# Map MIDI pitch classes (0-11) to possible note names (e.g., 1 -> ['C#', 'Db']).
pc_to_names = {}
for l in letters:
    for acc in [-1, 0, 1]:  # -1=flat, 0=natural, 1=sharp
        pc = (base_pc[l] + acc) % 12
        name = l + ('#' if acc == 1 else 'b' if acc == -1 else '')
        pc_to_names.setdefault(pc, []).append(name)

# Define scale types with intervals, mode names, and number of notes.
# Intervals are semitone steps between notes (e.g., Major: [2,2,1,2,2,2,1]).
# Modes follow custom nomenclature (e.g., Aeolian #7 for Harmonic Minor).
scale_types = {
    'Major': {
        'intervals': [2, 2, 1, 2, 2, 2, 1],
        'modes': ['Ionian', 'Dorian', 'Phrygian', 'Lydian', 'Mixolydian', 'Aeolian', 'Locrian'],
        'num_notes': 7
    },
    'Harmonic Minor': {
        'intervals': [2, 1, 2, 2, 1, 3, 1],
        'modes': ['Aeolian #7', 'Locrian #6', 'Ionian #5', 'Dorian #4', 'Phrygian #3', 'Lydian #2', 'Mixolydian #1'],
        'num_notes': 7
    },
    'Melodic Minor': {
        'intervals': [2, 1, 2, 2, 2, 2, 1],
        'modes': ['Dorian #7', 'Phrygian #6', 'Lydian #5', 'Mixolydian #4', 'Aeolian #3', 'Locrian #2', 'Ionian #1'],
        'num_notes': 7
    },
    'Major b6': {
        'intervals': [2, 2, 1, 2, 1, 3, 1],
        'modes': ['Ionian b6', 'Dorian b5', 'Phrygian b4', 'Lydian b3', 'Mixolydian b2', 'Aeolian b1', 'Locrian b7'],
        'num_notes': 7
    },
    'Diminished': {
        'intervals': [2, 1, 2, 1, 2, 1, 2, 1],
        'modes': [f'Dim {i}' for i in range(8)],
        'num_notes': 8
    },
    'Whole-Tone': {
        'intervals': [2, 2, 2, 2, 2, 2],
        'modes': [f'WT {i}' for i in range(6)],
        'num_notes': 6
    }
}

# Define arpeggio types with intervals, mode names (for inversions), and number of notes.
# Intervals are semitone steps between chord tones (e.g., Major 7: [4,3,4]).
# Modes represent inversions (e.g., 'Maj7/3' for first inversion).
arpeggio_types = {
    'Major triad': {
        'intervals': [4, 3],
        'modes': ['Maj', 'Maj/3', 'Maj/5'],
        'num_notes': 3
    },
    'Minor triad': {
        'intervals': [3, 4],
        'modes': ['Min', 'Min/3', 'Min/5'],
        'num_notes': 3
    },
    'Major 7': {
        'intervals': [4, 3, 4],
        'modes': ['Maj7', 'Maj7/3', 'Maj7/5', 'Maj7/7'],
        'num_notes': 4
    },
    'Minor 7': {
        'intervals': [3, 4, 3],
        'modes': ['Min7', 'Min7/3', 'Min7/5', 'Min7/7'],
        'num_notes': 4
    },
    'Dominant 7': {
        'intervals': [4, 3, 3],
        'modes': ['Dom7', 'Dom7/3', 'Dom7/5', 'Dom7/7'],
        'num_notes': 4
    },
    'Half-Diminished 7': {
        'intervals': [3, 3, 4],
        'modes': ['HalfDim7', 'HalfDim7/3', 'HalfDim7/5', 'HalfDim7/7'],
        'num_notes': 4
    },
    'Diminished 7': {
        'intervals': [3, 3, 3],
        'modes': ['Dim7', 'Dim7/3', 'Dim7/5', 'Dim7/7'],
        'num_notes': 4
    }
}

def replace_accidentals(name):
    """
    Replace ASCII accidentals with Unicode symbols for display.
    Args:
        name (str): Note name with ASCII accidental (e.g., 'C#', 'Db').
    Returns:
        str: Note name with Unicode accidental (e.g., 'C\u266F', 'D\u266D').
    """
    return name.replace('#', '\u266F').replace('b', '\u266D')

def get_preferred_spelling(collection_type, mode_index, root_pc):
    """
    Generate well-formed note names for a scale or arpeggio starting at root_pc.
    Rules: One letter per note, no double accidentals, prefer flats unless forced, late duplicates for Dim7.
    Args:
        collection_type (str): Scale or arpeggio name (e.g., 'Major', 'Major 7').
        mode_index (int): Mode/inversion index (0 for root position/mode).
        root_pc (int): Root pitch class (0-11).
    Returns:
        list: Note names with Unicode accidentals (e.g., ['C', 'D', 'E', ...] or ['C', 'E', 'G', 'B']) or None if invalid.
    """
    if collection_type in scale_types:
        d = scale_types[collection_type]
        letter_step = 1
    elif collection_type in arpeggio_types:
        d = arpeggio_types[collection_type]
        letter_step = 2
    else:
        return None
    full_intervals = d['intervals']
    num_notes = d['num_notes']
    # Rotate intervals for the mode/inversion.
    intervals = full_intervals[mode_index:] + full_intervals[:mode_index]
    valid_spellings = []
    # Try each possible root name for the root pitch class.
    for root_name in pc_to_names.get(root_pc, []):
        root_letter = root_name[0]
        root_index = letters.index(root_letter)
        good = True
        names = []
        sharps = 0
        flats = 0
        # Build note names, ensuring one letter per note and no double accidentals.
        for j in range(num_notes):
            letter = letters[(root_index + letter_step * j) % 7]
            cum = sum(intervals[0:j])  # Cumulative semitones from root.
            pc_j = (root_pc + cum) % 12
            base = base_pc[letter]
            acc_j = (pc_j - base) % 12
            if acc_j > 6: acc_j -= 12  # Normalize to smallest accidental.
            if abs(acc_j) > 1:  # No double sharps/flats.
                good = False
                break
            name_j = letter + ('#' if acc_j == 1 else 'b' if acc_j == -1 else '')
            names.append(replace_accidentals(name_j))
            if acc_j == 1:
                sharps += 1
            elif acc_j == -1:
                flats += 1
        if good:
            # Store valid spelling with accidental counts and first letter index for sorting.
            valid_spellings.append({
                'names': names,
                'num_acc': sharps + flats,
                'num_flats': flats,
                'first_letter_idx': root_index
            })
    if not valid_spellings:
        return None
    # Prefer spelling: fewest accidentals, most flats, later first letter for Dim7 (e.g., C over B#).
    valid_spellings.sort(key=lambda s: (
        s['num_acc'],
        -s['num_flats'],
        -s['first_letter_idx'] if collection_type == 'Diminished 7' else s['first_letter_idx']
    ))
    return valid_spellings[0]['names']

class Scale:
    """
    Represents a musical scale or mode, generating MIDI notes.
    Supports all scale types and their modes (e.g., Major, Dorian).
    """
    def __init__(self, collection_type, root, mode_index=0):
        """
        Initialize a scale.
        Args:
            collection_type (str): Scale name (e.g., 'Major').
            root (str or int): Root note (e.g., 'C4' or MIDI 60).
            mode_index (int): Mode index (0 for root mode).
        Raises:
            ValueError: If collection_type is not a valid scale.
        """
        if collection_type not in scale_types:
            raise ValueError(f"Unknown scale type: {collection_type}")
        self.collection_type = collection_type
        # Convert root to MIDI if string (e.g., 'C4' -> 60).
        self.root_midi = note_to_midi(root) if isinstance(root, str) else root
        self.mode_index = mode_index
        self.intervals = scale_types[collection_type]['intervals']
        self.modes = scale_types[collection_type]['modes']
        self.num_notes = scale_types[collection_type]['num_notes']

    def generate(self, num_notes=None):
        """
        Generate MIDI notes for the scale/mode.
        Args:
            num_notes (int, optional): Number of notes to generate (default: full scale).
        Returns:
            list: MIDI note numbers (e.g., [60, 62, 64, ...] for C Major).
        Raises:
            ValueError: If num_notes exceeds scale size.
        """
        if num_notes is None:
            num_notes = self.num_notes
        if num_notes > self.num_notes:
            raise ValueError(f"Requested {num_notes} notes, but scale has only {self.num_notes}")
        # Rotate intervals for the mode.
        intervals = self.intervals[self.mode_index:] + self.intervals[:self.mode_index]
        midis = [self.root_midi]
        # Build MIDI sequence by adding intervals.
        for i in range(num_notes - 1):
            midis.append(midis[-1] + intervals[i % len(intervals)])
        return midis

    def get_mode_name(self):
        """
        Return the name of the current mode.
        Returns:
            str: Mode name (e.g., 'Ionian', 'Dorian #7').
        """
        return self.modes[self.mode_index]

class Arpeggio:
    """
    Represents a chord arpeggio, generating MIDI notes for root position or inversions.
    Supports triads and seventh chords with inversions treated as modes.
    """
    def __init__(self, collection_type, root, inversion_index=0):
        """
        Initialize an arpeggio.
        Args:
            collection_type (str): Arpeggio name (e.g., 'Major 7').
            root (str or int): Root note (e.g., 'C4' or MIDI 60).
            inversion_index (int): Inversion index (0 for root position).
        Raises:
            ValueError: If collection_type is not a valid arpeggio.
        """
        if collection_type not in arpeggio_types:
            raise ValueError(f"Unknown arpeggio type: {collection_type}")
        self.collection_type = collection_type
        # Convert root to MIDI if string (e.g., 'C4' -> 60).
        self.root_midi = note_to_midi(root) if isinstance(root, str) else root
        self.inversion_index = inversion_index
        self.intervals = arpeggio_types[collection_type]['intervals']
        # Add closing interval to make cyclical (sum to 12 for proper inversion rotation).
        self.cycle_intervals = self.intervals + [12 - sum(self.intervals)]
        self.modes = arpeggio_types[collection_type]['modes']
        self.num_notes = arpeggio_types[collection_type]['num_notes']

    def generate(self, num_notes=None):
        """
        Generate MIDI notes for the arpeggio/inversion.
        Args:
            num_notes (int, optional): Number of notes to generate (default: full arpeggio).
        Returns:
            list: MIDI note numbers (e.g., [60, 64, 67, 71] for C Maj7).
        Raises:
            ValueError: If num_notes exceeds arpeggio size.
        """
        if num_notes is None:
            num_notes = self.num_notes
        if num_notes > self.num_notes:
            raise ValueError(f"Requested {num_notes} notes, but arpeggio has only {self.num_notes}")
        # Rotate cycle intervals for the inversion.
        intervals = self.cycle_intervals[self.inversion_index:] + self.cycle_intervals[:self.inversion_index]
        midis = [self.root_midi]
        # Build MIDI sequence by adding intervals (up to num_notes-1 steps).
        for i in range(num_notes - 1):
            midis.append(midis[-1] + intervals[i])
        return midis

    def get_inversion_name(self):
        """
        Return the name of the current inversion.
        Returns:
            str: Inversion name (e.g., 'Maj7', 'Maj7/3').
        """
        return self.modes[self.inversion_index]