import csv

# MIDI helpers
def note_to_midi(note):
  notes = {'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3, 'E': 4, 'F': 5, 'F#': 6, 'Gb': 6, 'G': 7, 'G#': 8, 'Ab': 8, 'A': 9, 'A#': 10, 'Bb': 10, 'B': 11}
  pitch_class = note[:-1]
  octave = int(note[-1])
  return notes[pitch_class] + (octave + 1) * 12

def midi_to_note_base(midi):
  pc = midi % 12
  octave = midi // 12 - 1
  return f'C{octave}'  # Stub, used only if needed

# Unicode for accidentals
def replace_acc(name):
  return name.replace('#', '♯').replace('b', '♭')

# Spelling system
letters = 'ABCDEFG'
base_pc = {'A':9, 'B':11, 'C':0, 'D':2, 'E':4, 'F':5, 'G':7}
pc_to_names = {}
for l in letters:
  for acc in [-1,0,1]:
    pc = (base_pc[l] + acc) % 12
    name = l + ('#' if acc==1 else 'b' if acc==-1 else '')
    pc_to_names.setdefault(pc, []).append(name)

def get_preferred_spelling(scale_type, mode_index, root_pc):
  if scale_type in scale_types:
    full_intervals = scale_types[scale_type]['intervals']
    num_notes = scale_types[scale_type]['num_notes']
  else:
    return None
  intervals = full_intervals[mode_index:] + full_intervals[:mode_index]
  valid_spellings = []
  for root_name in pc_to_names.get(root_pc, []):
    root_letter = root_name[0]
    root_index = letters.index(root_letter)
    good = True
    names = []
    sharps = 0
    flats = 0
    for j in range(num_notes):
      letter = letters[(root_index + j) % 7]
      cum = sum(intervals[0:j])
      pc_j = (root_pc + cum) % 12
      base = base_pc[letter]
      acc_j = (pc_j - base) % 12
      if acc_j > 6: acc_j -= 12
      if abs(acc_j) > 1:
        good = False
        break
      name_j = letter + ('#' if acc_j==1 else 'b' if acc_j==-1 else '')
      names.append(name_j)
      if acc_j == 1:
        sharps += 1
      elif acc_j == -1:
        flats += 1
    if good:
      valid_spellings.append({'names': names, 'num_acc': sharps + flats, 'num_flats': flats})
  if not valid_spellings:
    return None
  valid_spellings.sort(key=lambda s: (s['num_acc'], -s['num_flats']))
  return valid_spellings[0]['names']

# Scale and arpeggio types
scale_types = {
  'Major': {'intervals': [2,2,1,2,2,2,1], 'modes': ['Ionian', 'Dorian', 'Phrygian', 'Lydian', 'Mixolydian', 'Aeolian', 'Locrian'], 'num_notes':7},
  'Harmonic Minor': {'intervals': [2,1,2,2,1,3,1], 'modes': ['Aeolian #7', 'Locrian #6', 'Ionian #5', 'Dorian #4', 'Phrygian #3', 'Lydian #2', 'Mixolydian #1'], 'num_notes':7},
  'Melodic Minor': {'intervals': [2,1,2,2,2,2,1], 'modes': ['Dorian #7', 'Phrygian #6', 'Lydian #5', 'Mixolydian #4', 'Aeolian #3', 'Locrian #2', 'Ionian #1'], 'num_notes':7},
  'Major b6': {'intervals': [2,2,1,2,1,3,1], 'modes': ['Ionian b6', 'Dorian b5', 'Phrygian b4', 'Lydian b3', 'Mixolydian b2', 'Aeolian b1', 'Locrian b7'], 'num_notes':7},
  # Stub for now
  'Diminished': {'intervals': [2,1,2,1,2,1,2,1], 'modes': [f'Dim {i}' for i in range(8)], 'num_notes':8},
  'Whole-Tone': {'intervals': [2,2,2,2,2,2], 'modes': [f'WT {i}' for i in range(6)], 'num_notes':6},
}

arpeggio_types = {
  'Maj7': {'intervals': [4,3,4], 'modes': ['Maj7', 'Maj7/3', 'Maj7/5', 'Maj7/7'], 'num_notes':4},
  'Min7': {'intervals': [3,4,3], 'modes': ['Min7', 'Min7/3', 'Min7/5', 'Min7/7'], 'num_notes':4},
  'Dom7': {'intervals': [4,3,3], 'modes': ['Dom7', 'Dom7/3', 'Dom7/5', 'Dom7/7'], 'num_notes':4},
  'HalfDim7': {'intervals': [3,3,4], 'modes': ['HalfDim7', 'HalfDim7/3', 'HalfDim7/5', 'HalfDim7/7'], 'num_notes':4},
  'Dim7': {'intervals': [3,3,3], 'modes': ['Dim7', 'Dim7/3', 'Dim7/5', 'Dim7/7'], 'num_notes':4},
  'Major triad': {'intervals': [4,3], 'modes': ['Maj', 'Maj/3', 'Maj/5'], 'num_notes':3},
  'Minor triad': {'intervals': [3,4], 'modes': ['Min', 'Min/3', 'Min/5'], 'num_notes':3},
}

# Include or exclude, e.g., select = ['Major', 'Harmonic Minor', 'Maj7', 'Min7'] etc.
select_types = list(scale_types.keys()) + list(arpeggio_types.keys())

def generate_weight_vector(midis):
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
    vector = [count] + vector  # Prepend for larger r left
  return vector

class Instrument:
  def __init__(self, name, min_note, max_note, transposition=0):
    self.name = name
    self.min_midi = note_to_midi(min_note)
    self.max_midi = note_to_midi(max_note)
    self.transposition = transposition  # Apply if needed, for now concert

def generate_practice_segments(instrument, select_types, min_len=3):
  all_segments = []
  seen_note_sets = set()
  current_upper = instrument.min_midi + 2  # Start low
  while current_upper <= instrument.max_midi:
    batch = []
    seen_in_batch = set()
    for t in select_types:
      if t in scale_types:
        d = scale_types[t]
      elif t in arpeggio_types:
        d = arpeggio_types[t]
      else:
        continue
      num_notes = d['num_notes']
      modes = d['modes']
      full_intervals = d['intervals']
      for mode_index in range(num_notes - 1, -1, -1):  # Higher first for preference
        intervals = full_intervals[mode_index:] + full_intervals[:mode_index]
        for L in range(min_len, num_notes + 1):
          for start_degree in range(num_notes):
            # Compute segment intervals
            seg_inter = [intervals[(start_degree + j) % num_notes] for j in range(L - 1)]
            # Build midis backward from upper
            midis = [current_upper]
            for j in range(L - 1):
              b_int = intervals[(start_degree + L - 2 - j) % num_notes]
              next_low = midis[-1] - b_int
              midis.append(next_low)
            midis = midis[::-1]
            if min(midis) < instrument.min_midi or midis[-1] != current_upper or len(set(midis)) != L or midis != sorted(midis):
              continue
            # Get root_pc
            cum_to_start = sum(intervals[0:start_degree]) % 12
            root_pc = (midis[0] % 12 - cum_to_start) % 12
            full_names = get_preferred_spelling(t, mode_index, root_pc)
            if not full_names:
              continue
            # Segment names
            seg_names = []
            for j in range(L):
              full_d = (start_degree + j) % num_notes
              seg_names.append(full_names[full_d])
            # Full notes with octave
            note_strs = []
            for j in range(L):
              octave = midis[j] // 12 - 1
              note_strs.append(replace_acc(seg_names[j] + str(octave)))
            # Name from bottom
            new_mode_index = (mode_index + start_degree) % num_notes
            mode_name = modes[new_mode_index]
            if t in arpeggio_types:
              # For arpeggio, root midi = midis[0] - sum(intervals[0:start_degree])
              cum = sum(intervals[0:start_degree])
              root_midi = midis[0] - cum
              root_oct = root_midi // 12 - 1
              root_name = replace_acc(full_names[0] + str(root_oct))
              bass = note_strs[0]
              entry = f"{root_name} {mode_name}"
              if start_degree > 0:
                entry += f" / {bass}"
            else:
              root_name = note_strs[0].split(' from')[0]  # Already with acc
              entry = f"{root_name} {mode_name} from {note_strs[0]} to {note_strs[-1]}"
            # Weight
            vector = generate_weight_vector(midis)
            note_set = frozenset(midis)
            if note_set not in seen_in_batch:
              seen_in_batch.add(note_set)
              batch.append({'entry': entry, 'vector': vector, 'notes': ' '.join(note_strs)})
    if batch:
      # Sort batch by vector descending (lex tuple)
      batch.sort(key=lambda s: tuple(s['vector']), reverse=True)
      all_segments.extend(batch)
      seen_note_sets.update(frozenset(item['notes'].split()) for item in batch)  # Update global seen if needed, but since incremental, no need for global filter
    current_upper += 1
  return all_segments

# Example
alto_sax = Instrument('Alto Sax', 'Bb3', 'Bb7', transposition=-9)  # Written range

segments = generate_practice_segments(alto_sax, select_types)

# Output
for seg in segments:
  print(seg['entry'])

with open('practice_segments.csv', 'w', newline='') as f:
  writer = csv.writer(f)
  writer.writerow(['Entry'])
  for seg in segments:
    writer.writerow([seg['entry']])