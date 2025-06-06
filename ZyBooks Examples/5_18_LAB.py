# Timothy Owen
# 6 June 2025
'''
5.18 LAB: Print string in reverse
Write a program that takes in a line of text as input, and outputs that line of 
text in reverse. The program repeats, ending when the user enters "Done", 
"done", or "d" for the line of text.
    Ex: If the input is:
            Hello there
            Hey
            done
        then the output is:

            ereht olleH
            yeH
'''

def reverse_string(s):
    reversed_string = ""
    for i in range(len(s) - 1, -1, -1):
        reversed_string += s[i]

    return reversed_string

entries = []
while True:
    user_input = input()
    if user_input in ["Done", "done", "d"]:
        break

    entries.append(user_input)

for entry in entries:
    print(reverse_string(entry))