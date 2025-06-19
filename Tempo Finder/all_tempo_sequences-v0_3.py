# Timothy Owen
# 13 June 2025
# version 0.2

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
    while True: # repeat until valid input
        try:
            start_tempo = int(input("Enter a start tempo (30-240, 0 to exit): "))
            if start_tempo == 0:
                quit = True
                break

            if 30 <= start_tempo <= 240:
                break
            else: raise ValueError
        except:
            print("Must be an integer (30-240)")
            continue

    if quit:
        break
    
    if start_tempo not in TEMPOS:   # slot start tempo into preset options
        for tempo in TEMPOS[::-1]:  # Find the first preset that is lower
            if tempo < start_tempo:
                start_tempo = tempo
                print(f"Closest match is {start_tempo}\n")
                break
    
    start_tempo_index = TEMPOS.index(start_tempo)
    lower_bound = TEMPOS[0]
    upper_bound = TEMPOS[-1]

    for i in range(2 ** (len(STEP_SIZES))): # All the variants
        tempo_index = start_tempo_index
        step_size_index = 0

        maxxed =  False
        perfect_run = True
        
        print(f"{i}:", end=" ")

        while step_size_index < len(STEP_SIZES):
            tempo = TEMPOS[tempo_index]
            step_size = STEP_SIZES[step_size_index]

            # Using binary mask to represent going up or down in tempo to
            # converge on target tempo.
            mask_for_step_sizes = 2 ** ((len(STEP_SIZES) - 1) - step_size_index)
            tempo_increases = True if i & mask_for_step_sizes else False
            print(f"{tempo}", end=" ")

            if tempo_increases:
                if tempo == upper_bound:
                    print("Max Out. Good job!")
                    maxxed = True
                    break

                next_too_high = tempo_index + step_size > len(TEMPOS) - 1
                while next_too_high and step_size_index < len(STEP_SIZES) - 1:
                    step_size_index += 1
                    step_size = STEP_SIZES[step_size_index]
                    next_too_high = tempo_index + step_size > len(TEMPOS) - 1

                if not next_too_high:
                    tempo_index += step_size
                        
            else:
                perfect_run = False
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
                    
            print(f"{'S' if tempo_increases else 'F'}", end=" ")
        
        tempo = TEMPOS[tempo_index]

        if tempo_increases and not maxxed:
            tempo = TEMPOS[tempo_index - 1]

        print(tempo)
        if perfect_run and not maxxed:
            tempo = TEMPOS[tempo_index]
            print(f"All successes. Try at {tempo}")
        # tempo_index = TEMPOS.index(start_tempo)


