# Timothy Owen
# 4 June 2025
'''
Complete the program by providing the additional branches for decoding other 
letters in a phone number. Try writing the program incrementally by adding one 
elif branch at a time, testing that each added branch works as intended.
'''

user_input = input("Enter phone number: ")
phone_number = ""

for character in user_input:
    if ("0" <= character <= "9") or (character == "-"):
        phone_number += character
    elif ("a" <= character <= "c") or ("A" <= character <= "C"):
        phone_number += "2"
# My code here
    elif ("d" <= character <= "f") or ("D" <= character <= "F"):
        phone_number += "3"
    elif ("g" <= character <= "i") or ("G" <= character <= "I"):
        phone_number += "4"
    elif ("j" <= character <= "l") or ("J" <= character <= "L"):
        phone_number += "5"
    elif ("m" <= character <= "o") or ("M" <= character <= "O"):
        phone_number += "6"
    elif ("p" <= character <= "s") or ("P" <= character <= "S"):
        phone_number += "7"
    elif ("t" <= character <= "v") or ("T" <= character <= "V"):
        phone_number += "8"
    elif ("w" <= character <= "z") or ("W" <= character <= "Z"):
        phone_number += "9"
# End my code
    else:
        phone_number += "?"

print(f"Numbers only: {phone_number}")