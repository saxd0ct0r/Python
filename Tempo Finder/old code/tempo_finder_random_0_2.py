# Timothy Owen
# 19 June 2025
# version 0.2

import random

low, high = "low", "high"
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
quit = False

while True:     # Main loop, keep running with user-selected starting tempo
    start_tempo = input("Enter 0 to exit: ")
    if start_tempo == "0":
        break

    start_tempo = random.randint(44, 176)
    print(f"Starting tempo: ~{start_tempo}\n")

    if start_tempo not in TEMPOS:   # slot start tempo into preset options
        for tempo in TEMPOS[::-1]:  # Find the first preset that is lower
            if tempo < start_tempo:
                start_tempo = tempo
                print(f"Closest match is {start_tempo}\n")
                break
    
    target_tempo = TEMPOS[random.randrange(len(TEMPOS))]
    print(f"Target tempo: {target_tempo}\n")

    start_tempo_index = TEMPOS.index(start_tempo)
    lower_bound = TEMPOS[0]
    upper_bound = TEMPOS[-1]

    tempo_index = start_tempo_index
    step_size_index = 0

    maxxed =  False
    perfect_run = True      # Used to keep track of a string of all successes
    
    while step_size_index < len(STEP_SIZES):    # Limits number of repetitions
        tempo = TEMPOS[tempo_index]
        step_size = STEP_SIZES[step_size_index]

        tempo_increases = True if tempo <= target_tempo else False
        print(f"{tempo}", end=" ")

        if tempo_increases:
            if tempo == upper_bound:    # You could go faster, but really?
                print("Max Out. Good job!")
                maxxed = True
                break

            # If the next increment in tempo goes "out of bounds", chop it in half
            # until it will no longer take you "out of bounds"
            next_too_high = tempo_index + step_size > len(TEMPOS) - 1
            while next_too_high and step_size_index < len(STEP_SIZES) - 1:
                step_size_index += 1
                step_size = STEP_SIZES[step_size_index]
                next_too_high = tempo_index + step_size > len(TEMPOS) - 1

            if not next_too_high:   # This if condition could probably go...
                tempo_index += step_size
                    
        else:
            perfect_run = False     # Oops! Made a mistake, so no longer perfect...
            # The logic is parallel to what happens if the tempo increases as above.
            if tempo == lower_bound:
                print("Smaller chunks.")
                break

            next_too_low = tempo_index - step_size < 0
            while next_too_low and step_size_index < len(STEP_SIZES) - 1:
                step_size_index += 1
                step_size = STEP_SIZES[step_size_index]
                next_too_low = tempo_index - step_size < 0

            if not next_too_low:
                tempo_index -= step_size
                
        step_size_index += 1
                
        # indicates the simulated success/failure of the previous trail
        print(f"{'S' if tempo_increases else 'F'}", end=" ")
    
    tempo = TEMPOS[tempo_index]

    if tempo_increases and not maxxed:
        tempo = TEMPOS[tempo_index - 1]

    print(tempo)
    # If it was a perfect run, you get one more shot that will end up potentially
    # quadrupling the tempo.
    if perfect_run and not maxxed:
        tempo = TEMPOS[tempo_index]
        print(f"All successes. Try at {tempo}")


