# Timothy Owen
# 11 June 2025
# tempo_finder 0.1
'''Utility to guide through the range of practice tempos'''

TEMPOS = (30, 31.5, 33, 34.5, 36, 38, 40, 42,
          44, 46, 48, 50, 52, 54, 56, 58,
          60, 63, 66, 69, 72, 76, 80, 84,
          88, 92, 96, 100, 104, 108, 112, 116,
          120, 126, 132, 138, 144, 152, 160, 168,
          176, 184, 192, 200, 208, 216, 224, 232,
          240)
'''
TODO: write pseudocode for the flow of different use cases
Case 1: Working on an exercise for the first time. Unknown tempo, no fixed 
goal tempo.
Purpose: find tempo between 30 and 240 bpm at which you can play cleanly.
Algorithm:
    1. Start at 60bpm. 
        a. if successful, double the tempo (+16 steps)
        b. if failure, halve the tempo (-16 steps)
        c. step size halves (step size is 8 steps)
    2. Perform again at new tempo.
        a. if successful, increase tempo (+8/4/2/1)
        b. if failure, decrease tempo (-8/4/2/1)
        c. step size halves
        d. if step size >= 1, repeat the cycle,
            else end the cycle
    3. If all successful, increase tempo one more step and make one more attempt
    4. Record/report highest successful tempo

Case 2: Working on an exercise previously worked on. Known previous tempo, no
fixed goal tempo.
Purpose:
    1. Reinforce previous learning
    2. Detect imperfections in technique that may have crept in
 
'''