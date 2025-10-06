# mymusiclib/segments.py
# Generates ordered scale and arpeggio segments for practice, tailored to a player's range.

from .scales import Scale, Arpeggio, get_preferred_spelling, scale_types, arpeggio_types, replace_accidentals
from .instrument import Instrument

def generate_weight_vector(midis):
    """
    Compute weight vector for a segment, counting notes in shrinking ranges from the top.
    E.g., [Bb3, C4, Db4] (MIDI [58, 60, 61]) → [3,2,2,1] for ranges of 1,2,3,4 semitones.
    Args:
        midis (list): MIDI numbers of the segment, sorted ascending.
    Returns:
        list: Weight vector, with larger ranges on the left.
    """
    if not midis:
        return []
    midis = sorted(midis)
    max_m = midis[-1]
    min_m = midis[0]
    span = max_m - min_m + 1
    vector = []
    for r in range(1, span + 1):
        w_min = max_m - r + 1
        count = sum(w_min <= m <= max_m for m in midis)
        vector = [count] + vector  # Prepend for larger ranges left
    return vector

def generate_segments(instrument, selected_collections, min_len=3):
    """
    Generate ordered list of scale/arpeggio segments within the player's range.
    Segments are sorted by expanding range, then by weight vector descending, preferring lower mode indices (e.g., Dorian over Aeolian).
    Args:
        instrument (Instrument): Player's instrument with min/max MIDI range.
        selected_collections (list): List of scale/arpeggio types (e.g., ['Major', 'Major 7']).
        min_len (int): Minimum segment length (e.g., 3 notes).
    Returns:
        list: Segments as dicts with 'entry' (name), 'notes' (note names), and 'vector' (weight).
    """
    all_segments = []
    current_upper = instrument.get_min_midi() + min_len - 1  # Start with smallest range

    while current_upper <= instrument.get_max_midi():
        batch = []
        seen_note_sets = set()
        # Iterate over selected scales and arpeggios
        for collection_type in selected_collections:
            if collection_type in scale_types:
                d = scale_types[collection_type]
                cls = Scale
            elif collection_type in arpeggio_types:
                d = arpeggio_types[collection_type]
                cls = Arpeggio
            else:
                continue
            num_notes = d['num_notes']
            modes = d['modes']
            full_intervals = d['intervals']
            if cls == Arpeggio:
                full_intervals = full_intervals + [12 - sum(full_intervals)]  # Cyclical for inversions
            # Try each mode/inversion, starting with lower indices for Dorian/Phrygian preference
            for mode_index in range(num_notes):
                intervals = full_intervals[mode_index:] + full_intervals[:mode_index]
                for length in range(min_len, num_notes + 1):
                    for start_degree in range(num_notes):
                        # Generate segment MIDI notes backward from current_upper
                        midis = [current_upper]
                        for j in range(length - 1):
                            b_int = intervals[(start_degree + length - 2 - j) % len(intervals)]
                            next_low = midis[-1] - b_int
                            midis.append(next_low)
                        midis = midis[::-1]  # Reverse to ascending
                        # Filter: within range, correct upper note, unique notes, ascending
                        if (min(midis) < instrument.get_min_midi() or
                            midis[-1] != current_upper or
                            len(set(midis)) != length or
                            midis != sorted(midis)):
                            continue
                        # Get root pitch class
                        cum_to_start = sum(intervals[0:start_degree]) % 12
                        root_pc = (midis[0] % 12 - cum_to_start) % 12
                        # Get note names with proper spelling
                        full_names = get_preferred_spelling(collection_type, mode_index, root_pc)
                        if not full_names:
                            continue
                        seg_names = [full_names[(start_degree + j) % num_notes] for j in range(length)]
                        note_strs = []
                        for j, midi in enumerate(midis):
                            octave = midi // 12 - 1
                            note_strs.append(replace_accidentals(f"{seg_names[j]}{octave}"))
                        # Construct entry name
                        new_mode_index = (mode_index + start_degree) % num_notes
                        mode_name = modes[new_mode_index]
                        if collection_type in arpeggio_types:
                            cum = sum(intervals[0:start_degree])
                            root_midi = midis[0] - cum
                            root_oct = root_midi // 12 - 1
                            root_name = replace_accidentals(f"{full_names[0]}{root_oct}")
                            entry = f"{root_name} {mode_name} from {note_strs[0]} to {note_strs[-1]}"
                        else:
                            root_name = note_strs[0].split(' from')[0]
                            entry = f"{root_name} {mode_name} from {note_strs[0]} to {note_strs[-1]}"
                        # Compute weight vector
                        vector = generate_weight_vector(midis)
                        note_set = frozenset(midis)
                        batch.append({
                            'entry': entry,
                            'notes': ' '.join(note_strs),
                            'vector': vector,
                            'note_set': note_set,
                            'mode_index': new_mode_index
                        })
        # Filter duplicates and sort by weight vector, then lower mode_index for Dorian/Phrygian
        unique_batch = []
        seen_note_sets = set()
        for seg in sorted(batch, key=lambda s: (tuple(s['vector']), s['mode_index'])):
            if seg['note_set'] not in seen_note_sets:
                seen_note_sets.add(seg['note_set'])
                unique_batch.append({
                    'entry': seg['entry'],
                    'notes': seg['notes'],
                    'vector': seg['vector']
                })
        if unique_batch:
            all_segments.extend(unique_batch)
        current_upper += 1
    return all_segments