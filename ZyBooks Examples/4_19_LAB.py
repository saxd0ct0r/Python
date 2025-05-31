# Timothy Owen
# 30 May 2025
# ZyLabs Exercise

input_year = int(input())

# is_leap_year = True if (
#     input_year % 4 == 0 and not input_year % 100 == 0
# ) or (input_year % 400 == 0) else False

result = "leap year" if (
    not input_year % 4 and input_year % 100
) or (
    not input_year % 400
) else "not a leap year"

print(input_year, "-", result)