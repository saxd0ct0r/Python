# Timothy Owen
# 16 June 2025
'''
8.18 LAB: Filter and sort a list
Write a program that gets a list of integers from input, and outputs negative 
integers in descending order (highest to lowest).
    Ex: If the input is:
            10 -7 4 -39 -6 12 -2
        the output is:
            -2 -6 -7 -39 
For coding simplicity, follow every output value by a space. Do not end with newline.
'''

user_input = input().split()
numbers = [int(number) for number in user_input if int(number) < 0]

numbers.sort()
for number in numbers[::-1]:
    print(f"{number}", end=" ")
