# Timothy Owen
# 13 June 2025
# version 0.2

low, high = "low", "high"
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

start_tempo = 88

for i in range(2 ** (len(STEP_SIZES))): # All the variants
    tempo_index = TEMPOS.index(start_tempo)
    step_size_index = 0
    step_size = STEP_SIZES[step_size_index]
    tempo = TEMPOS[tempo_index]
    
    print(f"{i}:", end=" ")
    for step_size_index in range(len(STEP_SIZES)):
        step_size = STEP_SIZES[step_size_index]
        tempo = TEMPOS[tempo_index]

        tempo_increases = True if i & (2 ** ((len(STEP_SIZES) - 1) - step_size_index)) else False
        # tempo_increases = True if input("Success? (y/n)").lower() in "yes" else False
        print(f"{tempo} {'/' if tempo_increases else '\\'}", end=" ")
        if tempo_increases:
            # for k in range(step_size_index, len(STEP_SIZES)):
            if tempo_index + step_size > len(TEMPOS) - 1:
                # print("next tempo out of range--too high")
                
                break

            tempo_index += step_size
    
        else:
            if tempo_index - step_size < 0:
                # print("next tempo out of range--too low")
                # step_size_index += 1
                break
            
            tempo_index -= step_size
    
    tempo = TEMPOS[tempo_index]

    if tempo_increases:
        tempo = TEMPOS[tempo_index - 1]

    print(tempo)
    # tempo_index = TEMPOS.index(start_tempo)


