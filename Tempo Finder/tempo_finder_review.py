# Timothy Owen
# 23 June 2025
# version 0.2

# low, high = "low", "high"
# define preset tempos and step sizes in a tuple so they don't get changed
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
lower_bound = TEMPOS[0]
upper_bound = TEMPOS[-1]
quit = False

def find_tempo(start_tempo = 60, first_time = True, start_perfect = True):

    # print(f"Starting tempo: ~{start_tempo}\n")

    if start_tempo in TEMPOS:       # slot start tempo into preset options
        pass
    else:
        for tempo in TEMPOS[::-1]:  # Find the first preset that is lower
            if tempo < start_tempo:
                start_tempo = tempo
                break
    
    tempo_index = TEMPOS.index(start_tempo)
    step_size_index = 0

    maxxed =  False
    perfect_run = start_perfect      # Used to keep track of a string of all successes
    
    while step_size_index < len(STEP_SIZES):    # Limits number of repetitions
        tempo = TEMPOS[tempo_index]
        step_size = STEP_SIZES[step_size_index]
        tempo_increases = check_success(tempo)

        if tempo_increases:
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
    
    # tempo = TEMPOS[tempo_index]
    if tempo_increases and not maxxed:
        # tempo = TEMPOS[tempo_index - 1]
        tempo_index -= 1

    # # If it was a perfect run, you get one more shot that will end up potentially
    # # quadrupling the tempo.
    # if perfect_run and not maxxed:
    #     tempo = TEMPOS[tempo_index]
    #     print(f"All successes. Try at {tempo}")
    
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

def check_success(tempo):
    success = None
    user_input = input(f"Attempt at {tempo}bpm. Success? (y/n is default): ")

    while success == None:
        if user_input.lower() == "y":
            success = True
        else:
            success = False
    
    return success

while True:     # Main loop, keep running until user chooses to exit
    while True: # repeat until valid input
        try:
            first_time = False
            start_tempo = input("Enter a start tempo (30-240,"
                                " [Enter] for first time,"
                                " 0 to exit): ")
            if start_tempo == "":
                first_time = True
                break

            start_tempo = int(start_tempo)
            if start_tempo == 0:
                quit = True
                break

            if 30 <= start_tempo <= 240:
                break
            else: raise ValueError
        except ValueError:
            print("Must be an integer (30-240)")
            continue

    if quit:
        break

    if first_time:
        tempo_index, perfect_run = find_tempo()
        print(TEMPOS[tempo_index])
    else:
        # TODO play at start_tempo, note success or failure
        print("Review at starting tempo first")
        print(find_tempo(start_tempo / 2))
        # find tempo starting from 1/2 of start_tempo
