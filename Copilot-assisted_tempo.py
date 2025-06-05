# Script Idea: Logarithmic Tempo Selection for Scale Practice

## Python Implementation: Logarithmic Tempo Selection

Below is a Python script that guides you through the tempo selection process using traditional metronome markings as logarithmic steps.

```python
# Traditional metronome markings (approximate logarithmic progression)
METRONOME_MARKINGS = [
    40, 42, 44, 46, 48, 50, 52, 54, 56, 58, 60, 63, 66, 69, 72, 76, 80, 84, 88, 92, 96, 100, 104, 108, 112, 116, 120,
    126, 132, 138, 144, 152, 160, 168, 176, 184, 192, 200, 208, 216, 224, 232, 240
]

def find_nearest_marking(bpm):
    return min(METRONOME_MARKINGS, key=lambda x: abs(x - bpm))

def get_index(bpm):
    return METRONOME_MARKINGS.index(find_nearest_marking(bpm))

def logarithmic_search(start_idx, end_idx, success_callback):
    step = abs(end_idx - start_idx) // 2
    current_idx = start_idx
    history = []
    while step > 0:
        next_idx = current_idx + step if end_idx > start_idx else current_idx - step
        next_idx = max(0, min(next_idx, len(METRONOME_MARKINGS) - 1))
        bpm = METRONOME_MARKINGS[next_idx]
        success = success_callback(bpm)
        history.append((bpm, success))
        if success:
            current_idx = next_idx
        step //= 2
    return METRONOME_MARKINGS[current_idx], history

def tempo_selection(first_time=True, last_success_bpm=60, success_callback=None):
    if first_time:
        print("First-time scale practice:")
        start_idx = get_index(60)
        end_idx = get_index(240)
        max_bpm, history = logarithmic_search(start_idx, end_idx, success_callback)
        if all(success for _, success in history):
            if success_callback(240):
                print("Final performance at 240 BPM successful!")
                max_bpm = 240
        print(f"Your maximum clean tempo: {max_bpm} BPM")
    else:
        print("Subsequent scale practice:")
        start_idx = get_index(last_success_bpm)
        if success_callback(last_success_bpm):
            # Try slower tempos
            min_idx = 0
            _, history = logarithmic_search(start_idx, min_idx, success_callback)
            if all(success for _, success in history):
                # Try higher tempos
                max_idx = min(start_idx + 16, len(METRONOME_MARKINGS) - 1)
                max_bpm, history_high = logarithmic_search(start_idx, max_idx, success_callback)
                if all(success for _, success in history_high):
                    if success_callback(METRONOME_MARKINGS[max_idx]):
                        print(f"Final performance at {METRONOME_MARKINGS[max_idx]} BPM successful!")
                        max_bpm = METRONOME_MARKINGS[max_idx]
            print(f"Your reinforced or new maximum tempo: {max_bpm} BPM")
        else:
            # Try lower tempos
            min_idx = 0
            max_bpm, _ = logarithmic_search(start_idx, min_idx, success_callback)
            print(f"Adjusted to lower tempo: {max_bpm} BPM")

# Example usage:
# Replace the following with your own logic for determining success at a given BPM.
def user_success_callback(bpm):
    print(f"Try playing at {bpm} BPM. Were you successful? (y/n): ", end="")
    return input().strip().lower() == 'y'

# Uncomment to run:
# tempo_selection(first_time=True, success_callback=user_success_callback)
```

This script uses traditional metronome markings to approximate logarithmic tempo steps. The `success_callback` function should be implemented to interactively or programmatically determine if you were successful at each tempo.