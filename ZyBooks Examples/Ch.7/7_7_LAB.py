# Timothy Owen
# 16 June 2025
'''
7.7 LAB: Count characters
Write a program whose input is a string which contains a character and a 
phrase, and whose output indicates the number of times the character appears in 
the phrase. The output should include the input character and use the plural 
form, n's, if the number of times the characters appears is not exactly 1.
    Ex: If the input is:
            n Monday
        the output is:
            1 n
    Ex: If the input is:
            z Today is Monday
        the output is:
            0 z's
    Ex: If the input is:
            n It's a sunny day
        the output is:
            2 n's
Case matters. n is different than N.
    Ex: If the input is:
            n Nobody
        the output is:
            0 n's
'''
user_input = input()
letter = user_input[0]
user_string = user_input[2:]
number = user_string.count(letter)
plural_ending = "'s" if number != 1 else ""
print(f"{number} {letter}{plural_ending}")
