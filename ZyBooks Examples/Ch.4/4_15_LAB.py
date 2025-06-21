# Timothy Owen
# 30 May 2025
'''ZyLab Exercise 4.15.1: LAB: Smallest number
Write a program whose inputs are three integers, and whose output is the
smallest of the three values.
'''

user_nums = []

for i in range(3):
    user_nums.append(int(input()))

print(min(user_nums))