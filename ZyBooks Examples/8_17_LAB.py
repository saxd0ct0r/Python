# Timothy Owen
# 16 June 2025
'''
8.17 LAB: Varied amount of input data
Statistics are often calculated with varying amounts of input data. Write a 
program that takes any number of non-negative floating-point numbers as input, 
and outputs the max and average, respectively.

Output the max and average with two digits after the decimal point.
    Ex: If the input is:
            14.25 25 0 5.75
        the output is:
            25.00 11.25
'''
user_inputs = input().split()
for i, number in enumerate(user_inputs):
    user_inputs[i] = float(number)

max_number = max(user_inputs)
average = sum(user_inputs) / len(user_inputs)
print(f"{max_number:.2f} {average:.2f}")
