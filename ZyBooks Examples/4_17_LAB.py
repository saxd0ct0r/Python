# Timothy Owen
# 30 May 2025
'''ZyLabs Exercise 4.17.1: LAB: Seasons
Write a program that takes a date as input and outputs the date's season in the
northern hemisphere. The input is a string to represent the month and an int to
represent the day.
    Ex: If the input is:
            April
            11
        the output is:
            Spring
In addition, check if the string and int are valid (an actual month and day).
    Ex: If the input is:
            Blue
            65
        the output is:
            Invalid 
The dates for each season in the northern hemisphere are:
    Spring: March 20 - June 20
    Summer: June 21 - September 21
    Autumn: September 22 - December 20
    Winter: December 21 - March 19
'''

input_month = input()
input_day = int(input())

# Brute Force Method
#
# if (
#     input_month == "March" and 20 <= input_day <=31) or (
#     input_month == "April" and 1 <= input_day <= 30) or (
#     input_month == "May" and 1 <= input_day <= 31) or (
#     input_month == "June" and 1 <= input_day <=20
# ):
#     print("Spring")
# elif (
#     input_month == "June" and 21 <= input_day <=30) or (
#     input_month == "July" and 1 <= input_day <= 31) or (
#     input_month == "August" and 1 <= input_day <= 31) or (
#     input_month == "September" and 1 <= input_day <=21
# ):
#     print("Summer")
# elif (
#     input_month == "September" and 22 <= input_day <=30) or (
#     input_month == "October" and 1 <= input_day <= 31) or (
#     input_month == "November" and 1 <= input_day <= 30) or (
#     input_month == "December" and 1 <= input_day <=20
# ):
#     print("Autumn")
# elif (
#     input_month == "December" and 21 <= input_day <=31) or (
#     input_month == "January" and 1 <= input_day <= 31) or (
#     input_month == "February" and 1 <= input_day <= 29) or (
#     input_month == "March" and 1 <= input_day <= 19
# ):
#     print("Winter")
# else:
#     print("Invalid")

# Each season defined in a dictionary. Key is name of month, value is a list
# with first and last day
spring_dates = {"March": [20, 31,],
                "April": [1, 30],
                "May": [1, 31],
                "June": [1, 20]}

summer_dates = {"June": [21, 30],
                "July": [1, 31],
                "August": [1, 31],
                "September": [1, 21]}

autumn_dates = {"September": [22, 30],
                "October": [1, 31],
                "November": [1, 30],
                "December": [1, 20]}

winter_dates = {"December": [21, 31],
                "January": [1, 31],
                "February": [1, 29],
                "March": [1,19]}

if (input_month in spring_dates) and (
    spring_dates[input_month] [0] <= input_day <= spring_dates[input_month] [1]):
    print("Spring")
elif (input_month in summer_dates) and (
    summer_dates[input_month] [0] <= input_day <= summer_dates[input_month] [1]):
    print("Summer")
elif (input_month in autumn_dates) and (
    autumn_dates[input_month] [0] <= input_day <= autumn_dates[input_month] [1]):
    print("Autumn")
elif (input_month in winter_dates) and (
    winter_dates[input_month] [0] <= input_day <= winter_dates[input_month] [1]):
    print("Winter")
else:
    print("Invalid")