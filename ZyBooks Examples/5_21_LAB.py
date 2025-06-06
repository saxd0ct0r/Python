# Timothy Owen
# 6 June 2025
'''
5.21 LAB: Smallest and largest numbers in a list
Write a program that reads a list of integers into a list as long as the 
integers are greater than zero, then outputs the smallest and largest integers 
in the list.
    Ex: If the input is:
            10
            5
            3
            21
            2
            -6
        the output is:
            2 and 21
You can assume that the list of integers will have at least 2 values.
'''
smallest = 0
user_input = 1
while user_input > 0:
    user_input = int(input())
    if user_input < 0:
        break
    if smallest == 0:
        smallest = user_input
        largest = user_input
        continue
    smallest = smallest if smallest < user_input else user_input
    largest = user_input if user_input > largest else largest

print(f"{smallest} and {largest}")

