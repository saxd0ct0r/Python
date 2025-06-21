# Timothy Owen
# 16 June 2025
'''
7.6 LAB: Name format
Many documents use a specific format for a person's name. Write a program that 
reads a person's name in the following format:
    firstName middleName lastName (in one line)
and outputs the person's name in the following format:
    lastName, firstInitial.middleInitial.

    Ex: If the input is:
            Pat Silly Doe
        the output is:
            Doe, P.S.
        If the input has the following format:
            firstName lastName (in one line)
        the output is:
            lastName, firstInitial.

    Ex: If the input is:
            Julia Clark
        the output is:
            Clark, J.
'''

names = input().split()
last_name = names.pop()
initials = ""

for name in names:
    initials = initials + name[0] + "."

print(f"{last_name}, {initials}")