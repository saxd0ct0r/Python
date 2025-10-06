# mymusiclib/tools.py
# Utility functions for music theory tools, including table generation for scale/arpeggio pitch distributions.

from .scales import scale_types, arpeggio_types

def generate_distribution_table():
    """
    Generate a table of pitch distributions for all scales and arpeggios, using movable Do with La-based minor.
    Columns: Parent Scale, Mode, 0-12 (semitones with solfege).
    Returns:
        list: Rows as dicts with 'parent', 'mode', and pitch classes 0-12.
    """
    solfege = ['Do', 'Di/Ra', 'Re', 'Ri/Me', 'Mi', 'Fa', 'Fi/Se', 'Sol', 'Si/Le', 'La', 'Li/Te', 'Ti', 'Do']
    # Mode starting points for all collections, based on degree relative to Ionian
    mode_starts = {
        'Ionian': 0, 'Dorian': 2, 'Phrygian': 4, 'Lydian': 5, 'Mixolydian': 7, 'Aeolian': 9, 'Locrian': 11,
        'Aeolian #7': 9, 'Locrian #6': 11, 'Ionian #5': 0, 'Dorian #4': 2, 'Phrygian #3': 4, 'Lydian #2': 1, 'Mixolydian #1': 8,
        'Dorian #7': 2, 'Phrygian #6': 4, 'Lydian #5': 0, 'Mixolydian #4': 2, 'Aeolian #3': 4, 'Locrian #2': 8, 'Ionian #1': 11,
        'Ionian b6': 0, 'Dorian b5': 2, 'Phrygian b4': 4, 'Lydian b3': 10, 'Mixolydian b2': 0, 'Aeolian b1': 1, 'Locrian b7': 11,
        'Dim 0': 0, 'Dim 1': 2, 'Dim 2': 3, 'Dim 3': 5, 'Dim 4': 6, 'Dim 5': 9, 'Dim 6': 10, 'Dim 7': 11,
        'WT 0': 0, 'WT 1': 2, 'WT 2': 4, 'WT 3': 6, 'WT 4': 8, 'WT 5': 10,
        'Maj': 0, 'Maj/3': 4, 'Maj/5': 7,
        'Min': 0, 'Min/3': 3, 'Min/5': 7,
        'Maj7': 0, 'Maj7/3': 4, 'Maj7/5': 7, 'Maj7/7': 11,
        'Min7': 0, 'Min7/3': 3, 'Min7/5': 7, 'Min7/7': 10,
        'Dom7': 0, 'Dom7/3': 4, 'Dom7/5': 7, 'Dom7/7': 10,
        'HalfDim7': 0, 'HalfDim7/3': 3, 'HalfDim7/5': 6, 'HalfDim7/7': 10,
        'Dim7': 0, 'Dim7/3': 3, 'Dim7/5': 6, 'Dim7/7': 9
    }
    # Map pitch classes to solfege relative to mode start
    def get_mode_solfege(intervals, mode_index, mode_name):
        start_idx = mode_starts.get(mode_name, 0)  # Fallback to Do
        intervals = intervals[mode_index:] + intervals[:mode_index]
        pc = 0
        row = {str(i): '' for i in range(13)}
        for i in range(len(intervals) + 1):
            row[str(pc)] = solfege[start_idx % 12]
            if i < len(intervals):
                pc = (pc + intervals[i]) % 12
            start_idx += intervals[i] if i < len(intervals) else 0
        return row

    rows = []
    # Scales
    for scale_type, data in scale_types.items():
        intervals = data['intervals']
        modes = data['modes']
        for mode_index, mode_name in enumerate(modes):
            row = get_mode_solfege(intervals, mode_index, mode_name)
            row['parent'] = scale_type
            row['mode'] = mode_name
            rows.append(row)
    # Arpeggios
    for arp_type, data in arpeggio_types.items():
        intervals = data['intervals']
        modes = data['modes']
        for mode_index, mode_name in enumerate(modes):
            row = get_mode_solfege(intervals, mode_index, mode_name)
            row['parent'] = arp_type
            row['mode'] = mode_name
            rows.append(row)
    
    return rows

def print_distribution_table():
    """
    Print the distribution table in a readable format.
    """
    rows = generate_distribution_table()
    headers = ['Parent Scale', 'Mode'] + [str(i) for i in range(13)]
    print(' | '.join(headers))
    print('-' * (len(headers) * 8))
    for row in rows:
        values = [row['parent'], row['mode']] + [row[str(i)] for i in range(13)]
        print(' | '.join(values))

if __name__ == '__main__':
    print_distribution_table()