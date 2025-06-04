# Timothy Owen
# 29 May 2025
'''
Given a starting tempo, this algorithm guides the user through a sequence
of slower tempos to reinforce the learning of fingering patterns and musical
passages. Based loosely on the principle of the binary search, it rapidly
converges on the tempo at which the user is able to perform with good
technique in O = log(n) time.
'''

# returns the index of the tuple element closest numerically to the target
def find_nearest_index(tup, target):
    if not tup:
        raise ValueError("Tuple is empty")
    return min(range(len(tup)), key=lambda i: abs(tup[i] - target))

def find_tempo(tempo_index, step):
    temp_index =  tempo_index

    while step > 0:
        step //= 2
        user_input = ""

        print(f"Next tempo: {tempos_bpm[temp_index]}")
        while user_input == "":
            user_input = input("Success [y/n]? ")
            if user_input.lower() == "y":
                temp_index += max(step, 1)
            elif user_input.lower() == "n":
                temp_index -= max(step, 1)
            else:
                print("Please give a valid [y/n] response")
                user_input = ""

    return temp_index

tempos_bpm = (30, 31.5, 33, 34.5, 36, 38, 40, 42,
              44, 46, 48, 50, 52, 54, 56, 58,
              60, 63, 66, 69, 72, 76, 80, 84,
              88, 92, 96, 100, 104, 108, 112, 116,
              120, 126, 132, 138, 144, 152, 160, 168,
              176, 184, 192, 200, 208, 216, 224, 232,
              240)
# print(tempos_bpm[0])
# # TEST
# start_tempo = 67.9
# print(f"Start Tempo Input: {start_tempo}\t", end = "")
# print(f"Processed Start Tempo: {tempos_bpm[find_nearest_index(tempos_bpm, start_tempo)]}")

user_input = ""
start_tempo = 0
index = 0

while True:
    user_input = input("Enter a starting tempo (X to exit): ")
    if user_input == "":
        start_tempo = 60
        index = find_nearest_index(tempos_bpm, 60)
        break
    if user_input.lower() == "x":
        quit = True
        break

    try:
        start_tempo = float(user_input)
    except:
        print(f"Sorry, {user_input} doesn't work as a tempo.")
        print("Try an number between 30 and 240 this time.")
        continue

    if 30 <= start_tempo <= 240:
        index = find_nearest_index(tempos_bpm, start_tempo)
        start_tempo = tempos_bpm[index]
        break

    print("Try a value between 30 and 240.")

print(f"Starting at tempo {start_tempo}bpm")
input("Press Enter to continue")
step_size = 16

while index < step_size:
    step_size //= 2

index -= step_size

index = find_tempo(index, step_size)
index = find_tempo(index, 1)

if tempos_bpm[index] == start_tempo:
    print("Great job! Let's try increasing the tempo")
    index = find_tempo(index + 8, 8)
    index = find_tempo(index, 1)
else:
    print("Let's adjust our expectations for next time.")

end_tempo = tempos_bpm[index]
print(f"Final tempo: {end_tempo}bpm")
