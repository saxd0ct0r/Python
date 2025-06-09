# Timothy Owen
# 9 June 2025
'''
6.28 LAB: Output values in a list below a user defined amount - functions
Write a program that first gets a list of integers from input. The input begins 
with an integer indicating the number of integers that follows. Then, get the 
last value from the input, and output all integers less than or equal to that 
value.
    Ex: If the input is:
            5
            50
            60
            140
            200
            75
            100
        the output is:
            50
            60
            75
The 5 indicates that five integers are in the list, namely 50, 60, 140, 200, 
and 75. The 100 indicates that the program should output all integers less than 
or equal to 100, so the program outputs 50, 60, and 75.

Such functionality is common on sites like Amazon, where a user can filter 
results. Utilizing functions will help to make your main very clean and 
intuitive.

The program must define the following two functions:
def get_user_values() - read from input the size of the list, the integers in 
the list, and the threshold value. Return the list of integers and the 
threshold value.

def ints_less_than_or_equal_to_threshold(user_values, upper_threshold) - create 
a new list that contains values in user_values that are less than or equal to 
upper_threshold. Return the newly created list.
'''

# Define your functions here
def get_user_values():
    temp = int(input())
    numbers = []

    for i in range(temp):
        numbers.append(int(input()))

    threshold = int(input())

    return numbers, threshold

def ints_less_than_or_equal_to_threshold(user_values, upper_threshold):
    filtered_numbers = []

    for num in user_values:
        if num <= upper_threshold:
            filtered_numbers.append(num)

    return filtered_numbers

if __name__ == "__main__":
    user_values, upper_threshold = get_user_values()
    res_values = ints_less_than_or_equal_to_threshold(user_values,
                                                      upper_threshold)

    for value in res_values:
        print(value)
