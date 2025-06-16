# Timothy Owen
# 16 June 2025
'''
8.19 LAB: Middle item
Given a sorted list of integers, output "Middle item: " followed by the middle 
integer. Assume the number of integers is always odd.
    Ex: If the input is:
            2 3 4 8 11
        the output is:
            Middle item: 4
The maximum number of inputs for any test case should not exceed 9. If 
exceeded, output "Too many inputs".

Hint: First read the data into a list. Then, based on the list's size, find the 
middle item.
'''

user_input = input().split()
if len(user_input) > 9:
    print("Too many inputs")
else:
    middle_item = user_input[len(user_input) // 2]
    print(f"Middle item: {middle_item}")
