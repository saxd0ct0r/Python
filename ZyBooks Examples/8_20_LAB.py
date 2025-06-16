# Timothy Owen
# 16 June 2025
'''
8.20 LAB: Elements in a range
Write a program that first gets a list of integers from input. That list is 
followed by two more integers representing lower and upper bounds of a range. 
Your program should output all integers from the list that are within that 
range (inclusive of the bounds).
    Ex: If the input is:
            25 51 0 200 33
            0 50
        the output is:
            25,0,33,
The bounds are 0-50, so 51 and 200 are out of range and thus not output.

For coding simplicity, follow each output integer by a comma, even the last 
one. Do not end with newline.
'''

user_input = input().split()
user_input = [int(number) for number in user_input]

user_range = input().split()
user_range = [int(number) for number in user_range]
upper_bound = max(user_range)
lower_bound = min(user_range)

in_bounds = [number for number in user_input if lower_bound <= number <= upper_bound]
for number in in_bounds:
    print(number, end=",")
    