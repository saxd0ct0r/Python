# Timothy Owen
# 6 June 2025
'''
5.19 LAB: Countdown until matching digits
Write a program that takes in an integer in the range 11-99 (inclusive) as 
input. The output of the program is a countdown starting from the input 
integer until an integer where both digits are identical.
    Ex: If the input is:
            93
        the output is:
            93
            92
            91
            90
            89
            88
    Ex: If the input is:
            11
        the output is:
            11
    Ex: If the input is:
            9
        or any value not between 11 and 99 (inclusive), the output is:
            Input must be 11-99
Use a while loop. Compare the digits; do not write a large if-else for all 
possible same-digit numbers (11, 22, 33, ..., 99), as that approach would be
cumbersome for larger ranges.
'''

number = int(input())
if 11 <= number <= 99:
    while True:
        print(number)
        if not number % 11:
            break
        else:
            number -= 1
            continue

else:
    print("Input must be 11-99")
