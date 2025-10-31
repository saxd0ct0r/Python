import os
import csv
from collections import defaultdict

# Define parent collections with modes, intervals, and solfege at module level for reusability
collections = {
    'Major': {
        'modes': ['Ionian', 'Dorian', 'Phrygian', 'Lydian', 'Mixolydian', 'Aeolian', 'Locrian'],
        'intervals': [
            [0, 2, 4, 5, 7, 9, 11],  # Ionian
            [0, 2, 3, 5, 7, 9, 10],  # Dorian
            [0, 1, 3, 5, 7, 8, 10],  # Phrygian
            [0, 2, 4, 6, 7, 9, 11],  # Lydian
            [0, 2, 4, 5, 7, 9, 10],  # Mixolydian
            [0, 2, 3, 5, 7, 8, 10],  # Aeolian
            [0, 1, 3, 5, 6, 8, 10],  # Locrian
        ],
        'solfege': ['Do', 'Re', 'Mi', 'Fa', 'Sol', 'La', 'Ti'],
    },
    'H Minor': {
        'modes': ['Aeolian ♯7', 'Locrian ♯6', 'Ionian ♯5', 'Dorian ♯4', 'Phrygian ♯3', 'Lydian ♯2', 'Mixolydian ♯1'],
        'intervals': [
            [0, 2, 3, 5, 7, 8, 11],  # Aeolian ♯7
            [0, 1, 3, 5, 6, 9, 10],   # Locrian ♯6
            [0, 2, 4, 5, 8, 9, 11],   # Ionian ♯5
            [0, 2, 3, 6, 7, 9, 10],   # Dorian ♯4
            [0, 1, 4, 5, 7, 8, 10],   # Phrygian ♯3
            [0, 3, 4, 6, 7, 9, 11],   # Lydian ♯2
            [0, 1, 3, 4, 6, 8, 9],    # Mixolydian ♯1
        ],
        'solfege': ['La', 'Ti', 'Do', 'Re', 'Mi', 'Fa', 'Si'],
    },
    'M Minor': {
        'modes': ['Dorian ♯7', 'Phrygian ♯6', 'Lydian ♯5', 'Mixolydian ♯4', 'Aeolian ♯3', 'Locrian ♯2', 'Ionian ♯1'],
        'intervals': [
            [0, 2, 3, 5, 7, 9, 11],   # Dorian ♯7
            [0, 1, 3, 5, 7, 8, 10],   # Phrygian ♯6
            [0, 2, 4, 6, 7, 9, 11],   # Lydian ♯5
            [0, 2, 4, 5, 7, 9, 10],   # Mixolydian ♯4
            [0, 2, 3, 5, 7, 8, 10],   # Aeolian ♯3
            [0, 1, 3, 5, 6, 8, 10],   # Locrian ♯2
            [0, 1, 3, 5, 6, 8, 10],   # Ionian ♯1
        ],
        'solfege': ['Re', 'Mi', 'Fa', 'Sol', 'La', 'Ti', 'Di'],
    },
    'H Major': {
        'modes': ['Ionian ♭6', 'Dorian ♭5', 'Phrygian ♭4', 'Lydian ♭3', 'Mixolydian ♭2', 'Aeolian ♭1', 'Locrian ♭7'],
        'intervals': [
            [0, 2, 4, 5, 7, 8, 11],   # Ionian ♭6
            [0, 2, 3, 5, 6, 9, 10],   # Dorian ♭5
            [0, 1, 3, 4, 7, 8, 10],   # Phrygian ♭4
            [0, 2, 3, 6, 7, 9, 11],   # Lydian ♭3
            [0, 1, 4, 5, 7, 9, 10],   # Mixolydian ♭2
            [0, 3, 4, 6, 8, 9, 11],   # Aeolian ♭1
            [0, 1, 3, 5, 6, 8, 9],    # Locrian ♭7
        ],
        'solfege': ['Do', 'Re', 'Mi', 'Fa', 'Sol', 'Le', 'Ti'],
    },
    'Diminished': {
        'modes': ['Diminished ♮9', 'Diminished ♭9', 'Diminished ♮9', 'Diminished ♭9', 'Diminished ♮9', 'Diminished ♭9', 'Diminished ♮9', 'Diminished ♭9'],
        'intervals': [
            [0, 2, 3, 5, 6, 8, 9, 11],  # Diminished ♮9 (whole-half)
            [0, 1, 3, 4, 6, 7, 9, 10],  # Diminished ♭9 (half-whole)
            [0, 2, 3, 5, 6, 8, 9, 11],  # Diminished ♮9
            [0, 1, 3, 4, 6, 7, 9, 10],  # Diminished ♭9
            [0, 2, 3, 5, 6, 8, 9, 11],  # Diminished ♮9
            [0, 1, 3, 4, 6, 7, 9, 10],  # Diminished ♭9
            [0, 2, 3, 5, 6, 8, 9, 11],  # Diminished ♮9
            [0, 1, 3, 4, 6, 7, 9, 10],  # Diminished ♭9
        ],
        'solfege': ['Ti', 'Di', 'Re', 'Mi', 'Fa', 'Sol', 'Le', 'Li'],
    },
    'WT': {
        'modes': ['Whole-Tone', 'Whole-Tone', 'Whole-Tone', 'Whole-Tone', 'Whole-Tone', 'Whole-Tone'],
        'intervals': [
            [0, 2, 4, 6, 8, 10],  # Whole-Tone
            [0, 2, 4, 6, 8, 10],  # Whole-Tone
            [0, 2, 4, 6, 8, 10],  # Whole-Tone
            [0, 2, 4, 6, 8, 10],  # Whole-Tone
            [0, 2, 4, 6, 8, 10],  # Whole-Tone
            [0, 2, 4, 6, 8, 10],  # Whole-Tone
        ],
        'solfege': ['Fa', 'Sol', 'La', 'Ti', 'Di', 'Ri'],
    },
    'Tritone': {
        'modes': ['Tritone ♭9', 'Tritone ♯9', 'Tritone ♮9', 'Tritone ♭9', 'Tritone ♯9', 'Tritone ♮9'],
        'intervals': [
            [0, 1, 4, 6, 7, 10],  # Tritone ♭9
            [0, 3, 5, 6, 9, 11],  # Tritone ♯9
            [0, 2, 3, 6, 8, 9],   # Tritone ♮9
            [0, 1, 4, 6, 7, 10],  # Tritone ♭9
            [0, 3, 5, 6, 9, 11],  # Tritone ♯9
            [0, 2, 3, 6, 8, 9],   # Tritone ♮9
        ],
        'solfege': ['Di', 'Re', 'Fa', 'Sol', 'Le', 'Ti'],
    },
    'Maj triad': {
        'modes': ['Maj triad', 'Maj triad/3', 'Maj triad/5'],
        'intervals': [
            [0, 4, 7],  # Root position
            [0, 3, 8],  # 1st inversion (triad/3)
            [0, 5, 9],  # 2nd inversion (triad/5)
        ],
        'solfege': ['Do', 'Mi', 'Sol'],
    },
    'Min triad': {
        'modes': ['Min triad', 'Min triad/3', 'Min triad/5'],
        'intervals': [
            [0, 3, 7],  # Root position
            [0, 4, 9],  # 1st inversion (triad/3)
            [0, 5, 8],  # 2nd inversion (triad/5)
        ],
        'solfege': ['Re', 'Fa', 'La'],
    },
    'Maj7': {
        'modes': ['Maj7', 'Maj7/3', 'Maj7/5', 'Maj7/7'],
        'intervals': [
            [0, 4, 7, 11],  # Root position
            [0, 3, 7, 8],   # 1st inversion (chord/3)
            [0, 4, 5, 9],   # 2nd inversion (chord/5)
            [0, 1, 5, 8],   # 3rd inversion (chord/7)
        ],
        'solfege': ['Do', 'Mi', 'Sol', 'Ti'],
    },
    'Dom7': {
        'modes': ['Dom7', 'Dom7/3', 'Dom7/5', 'Dom7/7'],
        'intervals': [
            [0, 4, 7, 10],  # Root position
            [0, 3, 6, 8],   # 1st inversion (chord/3)
            [0, 3, 5, 9],   # 2nd inversion (chord/5)
            [0, 2, 6, 9],   # 3rd inversion (chord/7)
        ],
        'solfege': ['Sol', 'Ti', 'Re', 'Fa'],
    },
    'Min7': {
        'modes': ['Min7', 'Min7/3', 'Min7/5', 'Min7/7'],
        'intervals': [
            [0, 3, 7, 10],  # Root position
            [0, 4, 7, 9],   # 1st inversion (chord/3)
            [0, 3, 5, 8],   # 2nd inversion (chord/5)
            [0, 2, 5, 9],   # 3rd inversion (chord/7)
        ],
        'solfege': ['Re', 'Fa', 'La', 'Do'],
    },
    'Min7b5': {
        'modes': ['Min7b5', 'Min7b5/3', 'Min7b5/5', 'Min7b5/7'],
        'intervals': [
            [0, 3, 6, 10],  # Root position
            [0, 3, 7, 9],   # 1st inversion (chord/3)
            [0, 4, 6, 9],   # 2nd inversion (chord/5)
            [0, 2, 5, 8],   # 3rd inversion (chord/7)
        ],
        'solfege': ['Ti', 'Re', 'Fa', 'La'],
    },
    'Dim7': {
        'modes': ['Dim7', 'Dim7/3', 'Dim7/5', 'Dim7/7'],
        'intervals': [
            [0, 3, 6, 9],   # Root position
            [0, 3, 6, 9],   # 1st inversion (chord/3)
            [0, 3, 6, 9],   # 2nd inversion (chord/5)
            [0, 3, 6, 9],   # 3rd inversion (chord/7)
        ],
        'solfege': ['Si', 'Ti', 'Re', 'Fa'],
    },
    'Augmented': {
        'modes': ['Augmented ♭9', 'Augmented ♯9', 'Augmented ♭9', 'Augmented ♯9', 'Augmented ♭9', 'Augmented ♯9'],
        'intervals': [
            [0, 1, 4, 5, 8, 9],   # Augmented ♭9
            [0, 3, 4, 7, 8, 11],  # Augmented ♯9
            [0, 1, 4, 5, 8, 9],   # Augmented ♭9
            [0, 3, 4, 7, 8, 11],  # Augmented ♯9
            [0, 1, 4, 5, 8, 9],   # Augmented ♭9
            [0, 3, 4, 7, 8, 11],  # Augmented ♯9
        ],
        'solfege': ['Ti', 'Do', 'Ri', 'Mi', 'Sol', 'Le'],
    },
}

# Define priority order for collections
collection_priorities = [
    'Major', 'H Minor', 'M Minor', 'H Major', 'Diminished', 'WT', 'Tritone', 'Augmented',
    'Maj triad', 'Min triad', 'Maj7', 'Dom7', 'Min7', 'Min7b5', 'Dim7'
]

# Define priority order for Secondary Mode retention
mode_priorities = {
    'Major': ['Lydian', 'Ionian', 'Mixolydian', 'Dorian', 'Aeolian', 'Phrygian', 'Locrian'],
    'H Minor': ['Lydian ♯2', 'Aeolian ♯7', 'Ionian ♯5', 'Dorian ♯4', 'Locrian ♯6', 'Phrygian ♯3', 'Mixolydian ♯1'],
    'M Minor': ['Lydian ♯5', 'Dorian ♯7', 'Mixolydian ♯4', 'Aeolian ♯3', 'Phrygian ♯6', 'Locrian ♯2', 'Ionian ♯1'],
    'H Major': ['Aeolian ♭1', 'Lydian ♭3', 'Ionian ♭6', 'Mixolydian ♭2', 'Dorian ♭5', 'Phrygian ♭4', 'Locrian ♭7'],
    'Diminished': ['Diminished ♮9', 'Diminished ♮9', 'Diminished ♮9', 'Diminished ♮9', 'Diminished ♭9', 'Diminished ♭9', 'Diminished ♭9', 'Diminished ♭9'],
    'WT': ['Whole-Tone', 'Whole-Tone', 'Whole-Tone', 'Whole-Tone', 'Whole-Tone', 'Whole-Tone'],
    'Maj triad': ['Maj triad/5', 'Maj triad/3', 'Maj triad'],
    'Min triad': ['Min triad/3', 'Min triad/5', 'Min triad'],
    'Maj7': ['Maj7', 'Maj7/5', 'Maj7/3', 'Maj7/7'],
    'Dom7': ['Dom7', 'Dom7/7', 'Dom7/5', 'Dom7/3'],
    'Min7': ['Min7', 'Min7/3', 'Min7/7', 'Min7/5'],
    'Min7b5': ['Min7b5', 'Min7b5/3', 'Min7b5/5', 'Min7b5/7'],
    'Dim7': ['Dim7', 'Dim7/3', 'Dim7/5', 'Dim7/7'],
    'Tritone': ['Tritone ♯9', 'Tritone ♯9', 'Tritone ♭9', 'Tritone ♭9', 'Tritone ♮9', 'Tritone ♮9'],
    'Augmented': ['Augmented ♯9', 'Augmented ♯9', 'Augmented ♯9', 'Augmented ♭9', 'Augmented ♭9', 'Augmented ♭9'],
}

def calculate_weighting_function(pitch_classes, start_column=None):
    """
    Calculate a 13-digit weighting function for a list of pitch classes.
    Left-most digit is count of PCs in [12,12], next is [11,12], ..., right-most is [0,12].
    If start_column is specified, counts PCs in [i,12] for i from 12 to start_column,
    padding left with 9s to maintain 13 digits.
    
    Args:
        pitch_classes: List of pitch classes (0-11).
        start_column: Starting pitch class for filtering (default None for full range).
    
    Returns:
        13-digit string representing the weighting function.
    """
    pitch_classes = sorted(set([pc % 12 for pc in pitch_classes]))  # Normalize to 0-11, remove duplicates
    weights = []
    if start_column is None:
        # Full range: i from 12 to 0
        for i in range(12, -1, -1):
            count = sum(1 for pc in pitch_classes if pc >= i or pc == 0)  # Include PC 0 (12)
            weights.append(count)
    else:
        # Filtered range: i from 12 to start_column
        for i in range(12, start_column - 1, -1):
            count = sum(1 for pc in pitch_classes if pc >= i or pc == 0)  # Include PC 0 (12)
            weights.append(count)
        # Pad left with 9s to reach 13 digits
        weights = [9] * (13 - len(weights)) + weights
    return ''.join(str(w) for w in weights)

def generate_modes_chart():
    """
    Generate a Markdown chart for all modes, sorted by weighting function in descending order.
    """
    # Generate rows with weighting functions
    rows = []
    for collection, data in collections.items():
        for mode_idx, mode in enumerate(data['modes']):
            # Get pitch classes and solfege for this mode
            pcs = data['intervals'][mode_idx]
            solfege = data['solfege']
            # Create pitch class row with solfege
            pc_row = [''] * 13  # Columns 0 to 12
            for i, pc in enumerate(pcs):
                pc_row[pc] = solfege[mode_idx + i] if mode_idx + i < len(solfege) else solfege[mode_idx + i - len(solfege)]
            pc_row[12] = solfege[mode_idx]  # Octave doubling
            # Calculate weighting function (full range)
            weight = calculate_weighting_function(pcs)
            # Store row with weight for sorting
            row = f"| {collection:<12} | {mode:<16} | {' | '.join(f'{x:^3}' for x in pc_row)} | {weight:<13} |"
            rows.append((int(weight), row))

    # Sort rows by weighting function in descending order
    rows.sort(key=lambda x: x[0], reverse=True)

    # Generate Markdown table
    header = "| Collection   | Mode             | " + " | ".join(f"PC{i:^3}" for i in range(13)) + " | Weighting     |\n"
    header += "|:-------------|:-----------------|" + "|".join(":---:" for _ in range(13)) + "|:--------------|\n"

    # Write to Markdown file
    with open('Modes_Pitch_Classes_Chart.md', 'w', encoding='utf-8') as f:
        f.write("# Modes Pitch Classes Chart\n\n")
        f.write(header)
        f.write('\n'.join(row[1] for row in rows))
        f.write("\n\n**Notes:**\n")
        f.write("- Pitch classes (0–12) show the solfege syllable if present in the mode, relative to the mode's root as pitch class 0; empty if not present. PC 12 doubles the octave.\n")
        f.write("- Solfege is fixed relative to the parent scale or chord's tonic: Major (Do as Ionian root), H Minor (La as Aeolian ♯7 root, with Si as raised 7th), M Minor (Re as Dorian ♯7 root, with Di as raised 7th), H Major (Do as Ionian ♭6 root, with Le as lowered 6th), Diminished (Ti as Diminished ♮9 root, with Di, Le, Li as chromatic alterations), WT (Fa as Whole-Tone root, with Di and Ri as chromatic alterations), Tritone (Di as Tritone ♭9 root, with Di, Re, Fa, Sol, Le, Ti), Maj triad/Maj7 (Do as root), Min triad/Min7 (Re as root), Dom7 (Sol as root), Min7b5 (Ti as root), Dim7 (Si as root, with Si, Ti, Re, Fa), Augmented (Ti as Augmented ♭9 root, with Ti, Do, Ri, Mi, Sol, Le).\n")
        f.write("- Weighting Function is a 13-digit integer prioritizing density towards higher pitch classes, with left-most digit as count of PC 12, next as PCs 11–12, ..., right-most as 0–12, sorted in descending order.\n")
        f.write("- Chord inversions are named as triad/3 (1st inversion), triad/5 (2nd inversion) for triads, and chord/3, chord/5, chord/7 for seventh chords.\n")
        f.write("- Tritone scale is a hexachord [0, 1, 4, 6, 7, 10], a composite of two major triads a tritone apart, with modes named ♭9 (first interval half step), ♮9 (whole step), ♯9 (minor third).\n")
        f.write("- Augmented scale is a hexachord [0, 1, 4, 5, 8, 9], a composite of two augmented triads a half step apart or three major triads a major third apart with one shared pitch each, with modes named ♭9 (first interval half step) or ♯9 (minor third).\n")

def generate_filtered_modes_chart(start_column=9, min_pcs=3):
    """
    Generate a filtered Markdown chart for modes with at least min_pcs pitch classes
    in the range [start_column, 12], sorted by weighting function in descending order.
    Includes a Secondary Mode column indicating the mode whose solfege sequence matches
    the solfege syllables in PCs [start_column, 12]. Non-included PC columns (0 to start_column-1)
    are obscured with 'xxx'. For duplicate weighting function values, retains the mode with
    the highest priority based on collection priority, then Secondary Mode priority.
    
    Args:
        start_column (int): Starting pitch class column (0-11) for filtering (default 9).
        min_pcs (int): Minimum number of pitch classes required in [start_column, 12] (default 3).
    """
    if start_column < 0 or start_column > 11:
        raise ValueError("start_column must be between 0 and 11")
    if min_pcs < 1:
        raise ValueError("min_pcs must be at least 1")

    # Generate rows with weighting functions and filter by PC count
    rows = []
    for collection, data in collections.items():
        for mode_idx, mode in enumerate(data['modes']):
            # Get pitch classes and solfege for this mode
            pcs = data['intervals'][mode_idx]
            solfege = data['solfege']
            # Create pitch class row with solfege
            pc_row = ['xxx'] * start_column + [''] * (13 - start_column)  # Obscure columns 0 to start_column-1
            for i, pc in enumerate(pcs):
                if pc >= start_column:
                    pc_row[pc] = solfege[mode_idx + i] if mode_idx + i < len(solfege) else solfege[mode_idx + i - len(solfege)]
            pc_row[12] = solfege[mode_idx]  # Octave doubling
            # Count non-empty PCs in the range [start_column, 12]
            pc_count = sum(1 for pc in range(start_column, 13) if pc_row[pc])
            if pc_count >= min_pcs:
                # Calculate weighting function for filtered range
                weight = calculate_weighting_function(pcs, start_column=start_column)
                # Extract solfege syllables in the filtered range in mode order
                filter_pcs = [pc for pc in pcs + [12] if pc >= start_column]
                filter_solfege = [pc_row[pc] for pc in filter_pcs]
                # Find Secondary Mode: mode whose solfege sequence starts with filter_solfege
                secondary_mode = "None"
                for other_idx, other_mode in enumerate(data['modes']):
                    # For start_column=0 in non-symmetric collections, set to None if same mode
                    if start_column == 0 and other_mode == mode and collection not in ['Diminished', 'WT', 'Augmented']:
                        continue
                    # Generate full solfege sequence for the other mode
                    other_pcs = data['intervals'][other_idx]
                    other_solfege = []
                    for i in range(len(other_pcs)):
                        other_solfege.append(solfege[other_idx + i] if other_idx + i < len(solfege) else solfege[other_idx + i - len(solfege)])
                    other_solfege.append(solfege[other_idx])  # Octave doubling
                    # Check if filter_solfege is a prefix of other_solfege
                    if len(other_solfege) >= len(filter_solfege) and other_solfege[:len(filter_solfege)] == filter_solfege:
                        secondary_mode = other_mode
                        break
                # Store row with weight, collection, secondary mode, and row for priority sorting
                row = f"| {collection:<12} | {mode:<16} | {' | '.join(f'{x:^3}' for x in pc_row)} | {secondary_mode:<16} | {weight:<13} |"
                rows.append((int(weight), collection, secondary_mode, row))

    # Group rows by weighting function and filter duplicates
    grouped_rows = defaultdict(list)
    for weight, collection, secondary_mode, row in rows:
        grouped_rows[weight].append((collection, secondary_mode, row))

    filtered_rows = []
    for weight, group in grouped_rows.items():
        if len(group) == 1:
            # No duplicates, keep the row
            filtered_rows.append((weight, group[0][2]))
        else:
            # Duplicates exist, select the row with highest priority (collection, then Secondary Mode)
            highest_priority_row = min(
                group,
                key=lambda x: (
                    collection_priorities.index(x[0]),
                    mode_priorities[x[0]].index(x[1]) if x[1] in mode_priorities[x[0]] else float('inf')
                )
            )
            filtered_rows.append((weight, highest_priority_row[2]))

    # Sort rows by weighting function in descending order
    filtered_rows.sort(key=lambda x: x[0], reverse=True)

    # Generate Markdown table
    header = "| Collection   | Mode             | " + " | ".join(f"PC{i:^3}" for i in range(13)) + " | Sec. Mode        | Weighting     |\n"
    header += "|:-------------|:-----------------|" + "|".join(":---:" for _ in range(13)) + "|:-----------------|:--------------|\n"

    # Write to Markdown file
    output_file = f"Filtered_Modes_Pitch_Classes_Chart_{start_column}_to_12.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"# Filtered Modes Pitch Classes Chart (PCs {start_column}–12, Minimum {min_pcs} PCs)\n\n")
        f.write(header)
        if filtered_rows:
            f.write('\n'.join(row[1] for row in filtered_rows))
        else:
            f.write("No modes meet the filtering criteria.\n")
        f.write("\n\n**Notes:**\n")
        f.write(f"- Filtered for modes with at least {min_pcs} pitch classes in the range PCs {start_column}–12. Non-included columns (0–{start_column-1}) are obscured with 'xxx'.\n")
        f.write(f"- For duplicate weighting function values, retains the mode with the highest priority based on collection priority (Major > H Minor > M Minor > H Major > Diminished > WT > Tritone > Augmented > Maj triad > Min triad > Maj7 > Dom7 > Min7 > Min7b5 > Dim7), then Secondary Mode priority within the collection.\n")
        f.write(f"- Pitch classes (0–12) show the solfege syllable if present in the mode, relative to the mode's root as pitch class 0; empty if not present. PC 12 doubles the octave.\n")
        f.write(f"- Secondary Mode is the mode from the same parent collection whose solfege sequence, starting from its root, matches the solfege syllables in PCs {start_column}–12 in order. For start_column=0 in non-symmetric collections, the Secondary Mode is 'None' if it would be the same mode.\n")
        f.write(f"- Solfege is fixed relative to the parent scale or chord's tonic: Major (Do as Ionian root), H Minor (La as Aeolian ♯7 root, with Si as raised 7th), M Minor (Re as Dorian ♯7 root, with Di as raised 7th), H Major (Do as Ionian ♭6 root, with Le as lowered 6th), Diminished (Ti as Diminished ♮9 root, with Di, Le, Li as chromatic alterations), WT (Fa as Whole-Tone root, with Di and Ri as chromatic alterations), Tritone (Di as Tritone ♭9 root, with Di, Re, Fa, Sol, Le, Ti), Maj triad/Maj7 (Do as root), Min triad/Min7 (Re as root), Dom7 (Sol as root), Min7b5 (Ti as root), Dim7 (Si as root, with Si, Ti, Re, Fa), Augmented (Ti as Augmented ♭9 root, with Ti, Do, Ri, Mi, Sol, Le).\n")
        f.write(f"- Weighting Function is a 13-digit integer prioritizing density towards higher pitch classes in the range {start_column}–12, with left-most digit as count of PC 12, next as PCs {start_column}–12, ..., padded left with 9s to maintain 13 digits.\n")
        f.write(f"- Chord inversions are named as triad/3 (1st inversion), triad/5 (2nd inversion) for triads, and chord/3, chord/5, chord/7 for seventh chords.\n")
        f.write(f"- Tritone scale is a hexachord [0, 1, 4, 6, 7, 10], a composite of two major triads a tritone apart, with modes named ♭9 (first interval half step), ♮9 (whole step), ♯9 (minor third).\n")
        f.write(f"- Augmented scale is a hexachord [0, 1, 4, 5, 8, 9], a composite of two augmented triads a half step apart or three major triads a major third apart with one shared pitch each, with modes named ♭9 (first interval half step) or ♯9 (minor third).\n")

def generate_stacked_tables(min_start_column=0, min_pcs=3):
    """
    Generate a single CSV table combining filtered modes for start_column from 9 to min_start_column,
    with at least min_pcs pitch classes in the range [start_column, 12], sorted by weighting
    function in descending order. Includes a single header row, a Secondary Mode column, and
    obscures non-included PC columns with 'xxx'. For duplicate weighting function values,
    retains the mode with the highest priority based on collection priority, then Secondary Mode
    priority.
    
    Args:
        min_start_column (int): The lowest start_column to include (widest subtable, default 0).
        min_pcs (int): Minimum number of pitch classes required in [start_column, 12] (default 3).
    """
    if min_pcs < 1:
        raise ValueError("min_pcs must be at least 1")
    if min_start_column < 0 or min_start_column > 9:
        raise ValueError("min_start_column must be between 0 and 9")

    # Generate rows for all start_columns
    all_rows = []
    for start_column in range(9, min_start_column - 1, -1):  # From 9 to min_start_column
        for collection, data in collections.items():
            for mode_idx, mode in enumerate(data['modes']):
                # Get pitch classes and solfege for this mode
                pcs = data['intervals'][mode_idx]
                solfege = data['solfege']
                # Create pitch class row with solfege
                pc_row = ['xxx'] * start_column + [''] * (13 - start_column)  # Obscure columns 0 to start_column-1
                for i, pc in enumerate(pcs):
                    if pc >= start_column:
                        pc_row[pc] = solfege[mode_idx + i] if mode_idx + i < len(solfege) else solfege[mode_idx + i - len(solfege)]
                pc_row[12] = solfege[mode_idx]  # Octave doubling
                # Count non-empty PCs in the range [start_column, 12]
                pc_count = sum(1 for pc in range(start_column, 13) if pc_row[pc])
                if pc_count >= min_pcs:
                    # Calculate weighting function for filtered range
                    weight = calculate_weighting_function(pcs, start_column=start_column)
                    # Extract solfege syllables in the filtered range in mode order
                    filter_pcs = [pc for pc in pcs + [12] if pc >= start_column]
                    filter_solfege = [pc_row[pc] for pc in filter_pcs]
                    # Find Secondary Mode: mode whose solfege sequence starts with filter_solfege
                    secondary_mode = "None"
                    for other_idx, other_mode in enumerate(data['modes']):
                        # For start_column=0 in non-symmetric collections, set to None if same mode
                        if start_column == 0 and other_mode == mode and collection not in ['Diminished', 'WT', 'Augmented']:
                            continue
                        # Generate full solfege sequence for the other mode
                        other_pcs = data['intervals'][other_idx]
                        other_solfege = []
                        for i in range(len(other_pcs)):
                            other_solfege.append(solfege[other_idx + i] if other_idx + i < len(solfege) else solfege[other_idx + i - len(solfege)])
                        other_solfege.append(solfege[other_idx])  # Octave doubling
                        # Check if filter_solfege is a prefix of other_solfege
                        if len(other_solfege) >= len(filter_solfege) and other_solfege[:len(filter_solfege)] == filter_solfege:
                            secondary_mode = other_mode
                            break
                    # Store row as CSV-compatible list
                    csv_row = [collection, mode] + pc_row + [secondary_mode, weight]
                    all_rows.append((int(weight), collection, secondary_mode, csv_row))

    # Group rows by weighting function and filter duplicates
    grouped_rows = defaultdict(list)
    for weight, collection, secondary_mode, csv_row in all_rows:
        grouped_rows[weight].append((collection, secondary_mode, csv_row))

    filtered_rows = []
    for weight, group in grouped_rows.items():
        if len(group) == 1:
            # No duplicates, keep the row
            filtered_rows.append((weight, group[0][2]))
        else:
            # Duplicates exist, select the row with highest priority (collection, then Secondary Mode)
            highest_priority_row = min(
                group,
                key=lambda x: (
                    collection_priorities.index(x[0]),
                    mode_priorities[x[0]].index(x[1]) if x[1] in mode_priorities[x[0]] else float('inf')
                )
            )
            filtered_rows.append((weight, highest_priority_row[2]))

    # Sort rows by weighting function in descending order
    filtered_rows.sort(key=lambda x: x[0], reverse=True)

    # Generate CSV table
    header = ['Collection', 'Mode'] + [f'PC{i}' for i in range(13)] + ['Secondary Mode', 'Weighting Function']

    # Write to CSV file
    with open('Stacked_Filtered_Modes_Pitch_Classes_Chart.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for weight, csv_row in filtered_rows:
            writer.writerow(csv_row)

if __name__ == "__main__":
    generate_modes_chart()
    generate_filtered_modes_chart()
    generate_stacked_tables()