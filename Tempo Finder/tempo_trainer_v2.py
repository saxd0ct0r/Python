# Timothy Owen
# Updated February 2026
'''Tempo Trainer has two modes, targeted and untargeted. 

The untargeted mode is intended for exercises and passages that do not have a 
goal tempo. Scales, for example, can be performed at an arbitrarily high tempo, 
limited only by the user's present ability. For a first exposure, Tempo Trainer 
helps to identify the tempo quickly using a divide-and-conquer approach. 
Starting at 60 bpm, the user gives feedback on the performance success, and the 
tempo either halves or doubles; each subsequent performance changes by smaller 
increments until there is no noticeable difference. On subsequent exposures, 
the user starts at the tempo achieved on the last exposure. After the first 
performance on the current iteration, the Trainer takes the user through a 
review cycle. If the review cycle confirms the user can still perform at the 
previous level with no issues, the Trainer then guides the user through a 
challenge cycle to try for a tempo as double the previously achieved tempo.

The targeted mode is intended for exercises and passages with a pre-defined
goal tempo such as a tempo marking. The Trainer begins with a tempo about 19%
above the goal (step +4). The user begins at that tempo until the first error, 
at which point the Trainer begins using the tempo finder search pattern. If the 
user completes the passage at the slower tempo, they go back to the last error 
and attempts at a faster tempo. At the end, the user knows the most challenging
part of the passage and the tempo at which they can perform it. Further work
can be done by a) isolating the "hot spot" for special analysis and treatment,
and b) subjecting the parts before and after the "hot spot" to the same
training routine until there are no more "hot spots" to be found. Some pieces
will be very simple, while more substantial works may have many levels of "hot
spots". The management of the "hot spots" and other passages is outside the
scope of this tool.'''

import math

# Define preset tempos and step sizes in a tuple so they don't get changed
# by accident
TEMPOS = (
          30, 31.5, 33, 34.5, 36, 38, 40, 42,
          44, 46, 48, 50, 52, 54, 56, 58,
          60, 63, 66, 69, 72, 76, 80, 84,
          88, 92, 96, 100, 104, 108, 112, 116,
          120, 126, 132, 138, 144, 152, 160, 168,
          176, 184, 192, 200, 208, 216, 224, 232,
          240
          )
STEP_SIZES = (16, 8, 4, 2, 1, 1)

# Targeted mode constants
STEPS_PER_DOUBLING = 16
HEADROOM_STEPS = 4  # +19% above target (step +4)

lower_bound = TEMPOS[0]
upper_bound = TEMPOS[-1]
quit = False

# ============================================================================
# UNTARGETED MODE FUNCTIONS
# ============================================================================

def find_tempo(start_tempo = 60, initial_step_size_index = 0, start_perfect = True):

    # resolve tempo to available slots
    tempo_index = resolve_tempo(start_tempo)
    step_size_index = initial_step_size_index
    maxxed =  False
    perfect_run = start_perfect      # Used to keep track of a string of all successes
    tempo_increases = False

    while step_size_index < len(STEP_SIZES):    # Limits number of repetitions
        tempo = TEMPOS[tempo_index]
        step_size = STEP_SIZES[step_size_index]
        tempo_increases = check_success(tempo)

        if tempo_increases:
            # Check upper bound
            if tempo == upper_bound:    # You could go faster, but really?
                maxxed = True
                break

            # If the next increment in tempo goes "out of bounds", chop it in half
            # until it will no longer take you "out of bounds"
            step_size_index, step_size = check_upper_bound\
                (tempo_index, step_size_index)
            tempo_index += step_size
                    
        else:
            perfect_run = False     # Oops! Made a mistake, so no longer perfect...
            # Check lower bound
            # The logic is parallel to what happens if the tempo increases as above.
            if tempo == lower_bound:
                break

            step_size_index, step_size = check_lower_bound\
                (tempo_index, step_size_index)
            tempo_index -= step_size
                
        step_size_index += 1

    # The last repetition: success means you have reached the target, not that 
    # you should increment the tempo
    if tempo_increases and not maxxed:
        tempo_index -= 1   

    return tempo_index, perfect_run

# Checks to see if the next step_size takes the tempo out of bounds. If so, cut 
# the step_size (increment step_size_index) and check again. Returns the new 
# step_size_index and step_size. 
def check_upper_bound(tempo_index, step_size_index):
    step_size = STEP_SIZES[step_size_index]

    next_too_high = tempo_index + step_size > len(TEMPOS) - 1
    while next_too_high and step_size_index < len(STEP_SIZES) - 1:
        step_size_index += 1
        step_size = STEP_SIZES[step_size_index]
        next_too_high = tempo_index + step_size > len(TEMPOS) - 1

    return step_size_index, step_size

# This does the same as check_upper_bound but against the lower limit.
def check_lower_bound(tempo_index, step_size_index):
    step_size = STEP_SIZES[step_size_index]

    next_too_low = tempo_index - step_size < 0
    while next_too_low and step_size_index < len(STEP_SIZES) - 1:
        step_size_index += 1
        step_size = STEP_SIZES[step_size_index]
        next_too_low = tempo_index - step_size < 0

    return step_size_index, step_size

# Gets user input about success or failure at given tempo
def check_success(tempo):
    success = None
    user_input = input(f"Attempt at {tempo}bpm. Success? (y/n; y is default): ")

    while success == None:
        if user_input.lower() == "y":
            success = True
        elif user_input.lower() == "n":
            success = False
        else:
            success = True  # default answer is 'y'; change to False for 'n'
                            # or add prompt to give specific answer, no default
    
    return success

# This function resolves the input to the index that most closely matches
def resolve_tempo(tempo):
    if tempo in TEMPOS:       # slot start tempo into preset options
        return TEMPOS.index(tempo)
    else:
        for real_tempo in TEMPOS[::-1]:  # Find the first preset that is lower
            if real_tempo < tempo:
                return TEMPOS.index(real_tempo)

# ============================================================================
# TARGETED MODE FUNCTIONS
# ============================================================================

def step_to_multiplier(step):
    """Convert step to tempo multiplier. Step 0 = target tempo (1.0)"""
    return 2 ** (step / STEPS_PER_DOUBLING)

def step_to_bpm(step, target_bpm):
    """Convert step to actual BPM. Step 0 = target BPM"""
    return round(target_bpm * step_to_multiplier(step), 1)

def find_tempo_targeted(target_bpm, start_measure, end_measure):
    """
    Targeted mode for pieces with a goal tempo.
    Target tempo is step 0.
    
    Returns:
        dict: {
            'hot_spot_measure': str or None,
            'hot_spot_step': int  (step number relative to target)
        }
    """
    current_step = HEADROOM_STEPS  # Start at +4 (+19%)
    current_measure = start_measure
    hot_spot_measure = None
    last_successful_step = None
    
    print(f"\n{'='*60}")
    print(f"TARGETED MODE: {start_measure} to {end_measure}")
    print(f"Target tempo: {target_bpm} BPM (step 0)")
    print(f"Starting tempo: {step_to_bpm(current_step, target_bpm)} BPM (step +{current_step}, +19%)")
    print(f"{'='*60}\n")
    
    # Start playing
    tempo = step_to_bpm(current_step, target_bpm)
    print(f"Playing from measure {current_measure} at {tempo} BPM (step {current_step:+d})")
    measure_input = input(f"  Enter measure where error occurred (or [Enter] if completed cleanly): ")
    
    if measure_input.strip() == "":
        # Completed the whole piece at +19%!
        print(f"✓ Completed entire passage at {tempo} BPM")
        return {
            'hot_spot_measure': None,
            'hot_spot_step': current_step
        }
    
    # Hit an error - this is now our hot spot candidate
    error_measure = measure_input.strip()
    print(f"✗ Error at measure {error_measure}")
    hot_spot_measure = error_measure
    current_measure = error_measure
    
    # Drop 16 steps (from +4 to -12)
    current_step -= 16
    tempo = step_to_bpm(current_step, target_bpm)
    
    print(f"Playing from measure {current_measure} at {tempo} BPM (step {current_step:+d})")
    measure_input = input(f"  Enter measure where error occurred (or [Enter] if completed cleanly): ")
    
    if measure_input.strip() != "":
        # Still erroring - search downward: -8, -4, -2, -1
        new_error = measure_input.strip()
        print(f"✗ Error at measure {new_error}")
        if new_error != hot_spot_measure:
            hot_spot_measure = new_error
            current_measure = new_error
        
        # Binary search downward: -8, -4, -2, -1
        # Pattern: -12 → -20 → -24 → -26 → -27
        for drop_amount in [8, 4, 2, 1]:
            current_step -= drop_amount
            tempo = step_to_bpm(current_step, target_bpm)
            
            print(f"Playing from measure {current_measure} at {tempo} BPM (step {current_step:+d})")
            measure_input = input(f"  Enter measure where error occurred (or [Enter] if completed cleanly): ")
            
            if measure_input.strip() == "":
                # Success! Found a playable tempo
                print(f"✓ Completed from m.{current_measure} to end")
                last_successful_step = current_step
                break
            else:
                # Still erroring - continue dropping
                error = measure_input.strip()
                print(f"✗ Error at measure {error}")
                if error != hot_spot_measure:
                    hot_spot_measure = error
                    current_measure = error
        
        if last_successful_step is None:
            # Still erroring at step -27 - needs foundational work
            hot_spot_step = current_step
            
            print(f"\n{'='*60}")
            print(f"PASSAGE TOO DIFFICULT:")
            print(f"  Still unable to complete at step {current_step:+d}")
            print(f"  This is {step_to_bpm(current_step, target_bpm)} BPM for a {target_bpm} BPM piece")
            print(f"\n  RECOMMENDATION:")
            print(f"  This passage requires foundational work on smaller chunks.")
            print(f"  Break down to even more isolated sections, potentially down")
            print(f"  to individual intervals or note transitions, before attempting")
            print(f"  this passage again.")
            print(f"{'='*60}\n")
            
            return {
                'hot_spot_measure': hot_spot_measure,
                'hot_spot_step': hot_spot_step
            }
        
        # Now search upward from the successful tempo: +4, +2, +1
        for raise_amount in [4, 2, 1]:
            current_step += raise_amount
            tempo = step_to_bpm(current_step, target_bpm)
            
            print(f"Playing from measure {current_measure} at {tempo} BPM (step {current_step:+d})")
            measure_input = input(f"  Enter measure where error occurred (or [Enter] if completed cleanly): ")
            
            if measure_input.strip() == "":
                # Success
                print(f"✓ Completed from m.{current_measure} to end")
                last_successful_step = current_step
            else:
                # Error - drop back and continue
                error = measure_input.strip()
                print(f"✗ Error at measure {error}")
                if error != hot_spot_measure:
                    hot_spot_measure = error
                    current_measure = error
                current_step -= raise_amount
        
        hot_spot_step = last_successful_step
        
    else:
        # Success at -12 - search upward: +8, +4, +2, +1
        print(f"✓ Completed from m.{current_measure} to end")
        last_successful_step = current_step
        
        for raise_amount in [8, 4, 2, 1]:
            current_step += raise_amount
            tempo = step_to_bpm(current_step, target_bpm)
            
            print(f"Playing from measure {current_measure} at {tempo} BPM (step {current_step:+d})")
            measure_input = input(f"  Enter measure where error occurred (or [Enter] if completed cleanly): ")
            
            if measure_input.strip() == "":
                # Success
                print(f"✓ Completed from m.{current_measure} to end")
                last_successful_step = current_step
            else:
                # Error - drop back and continue
                error = measure_input.strip()
                print(f"✗ Error at measure {error}")
                if error != hot_spot_measure:
                    hot_spot_measure = error
                    current_measure = error
                current_step -= raise_amount
        
        hot_spot_step = last_successful_step if last_successful_step is not None else current_step
    
    print(f"\n{'='*60}")
    print(f"HOT SPOT IDENTIFIED:")
    print(f"  Measure: {hot_spot_measure}")
    print(f"  Step: {hot_spot_step:+d}")
    print(f"  Tempo: {step_to_bpm(hot_spot_step, target_bpm)} BPM")
    print(f"{'='*60}\n")
    
    return {
        'hot_spot_measure': hot_spot_measure,
        'hot_spot_step': hot_spot_step
    }

# ============================================================================
# MAIN MENU AND MODES
# ============================================================================

def main_menu():
    """Select between untargeted and targeted modes."""
    print("\n" + "="*60)
    print("TEMPO TRAINER")
    print("="*60)
    print("1. Untargeted mode (scales, exercises)")
    print("2. Targeted mode (pieces with goal tempo)")
    print("0. Exit")
    print("="*60)
    
    choice = input("Select mode: ")
    return choice

# Main loop
if __name__ == "__main__":
    while True:
        choice = main_menu()
        
        if choice == "0":
            break
            
        elif choice == "2":
            # TARGETED MODE
            target_bpm = None
            while target_bpm is None:
                try:
                    target_bpm = float(input("Enter target tempo (BPM): "))
                except ValueError:
                    print("Must be a number")
            
            start_measure = input("Enter start measure identifier: ")
            end_measure = input("Enter end measure identifier: ")
            
            result = find_tempo_targeted(target_bpm, start_measure, end_measure)
            
            if result['hot_spot_measure']:
                print(f"\nNext steps:")
                print(f"1. Create hot spot card for measure {result['hot_spot_measure']} at step {result['hot_spot_step']:+d}")
                print(f"2. Create child segment: {start_measure} to (measure before {result['hot_spot_measure']})")
                print(f"3. Create child segment: (measure after {result['hot_spot_measure']}) to {end_measure}")
            else:
                print(f"\n🎉 No hot spots! Piece mastered at step {result['hot_spot_step']:+d} ({step_to_bpm(result['hot_spot_step'], target_bpm)} BPM)")
                
        elif choice == "1":
            # UNTARGETED MODE
            while True:     # repeat until valid input
                first_time = False
                start_tempo = input("Enter a start tempo (30-240,"
                                    " [Enter] for first time,"
                                    " 0 to exit): ")
                if start_tempo == "":
                    first_time = True
                    break
                try:
                    start_tempo = int(start_tempo)
                    if start_tempo == 0:
                        break

                    if 30 <= start_tempo <= 240:
                        break
                    else: raise ValueError
                except ValueError:
                    print("Must be an integer (30-240)")
                    continue

            if start_tempo == 0:
                continue

            if first_time:
                tempo_index, perfect_run = find_tempo()
                if perfect_run:
                    tempo_index += 1 if check_success(TEMPOS[tempo_index + 1]) else 0
            else:
                start_tempo_index = resolve_tempo(start_tempo)
                start_tempo = TEMPOS[start_tempo_index]
                tempo_index = start_tempo_index
                first_trial_success = check_success(start_tempo)
                print("Entering review phase ('slow' practice)")
                step_size_index = 0
                step_size_index, step_size = check_lower_bound(tempo_index, step_size_index)
                if tempo_index > 0:
                    tempo_index -= step_size
                step_size_index += 1
                tempo = TEMPOS[tempo_index]
                
                tempo_index, perfect_run = find_tempo(tempo, step_size_index, first_trial_success)
                if perfect_run:
                    print("Now entering growth phase ('fast' practice)")
                    step_size_index = 1
                    tempo_index = start_tempo_index
                    tempo = TEMPOS[tempo_index]
                    growth_phase_start_success = check_success(tempo)
                    step_size_index, step_size = check_upper_bound(tempo_index,step_size_index)
                    if tempo_index < len(TEMPOS):
                        tempo_index += step_size
                    step_size_index += 1
                    tempo = TEMPOS[tempo_index]

                    tempo_index, another_perfect_run = find_tempo(
                        tempo, step_size_index, growth_phase_start_success)
                    if another_perfect_run:
                        if check_success(TEMPOS[tempo_index + 1]):
                            tempo_index += 1
                    
            print(f"Final tempo: {TEMPOS[tempo_index]}bpm")