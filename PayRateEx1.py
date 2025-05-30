# Timothy Owen
# 28 May 2025
# Calculates weekly pay from hours and rate, with overtime

ot_multiplyer = 1.5
hours = -1
while (hours == -1):
    try:
        hours = float(input("Enter Hours: "))
    except:
        print("Error, please enter numeric input")
        hours = -1

rate = -1
while (rate == -1):
    try:
        rate = float(input("Enter Rate: "))
    except:
        print("Error, please enter numeric input")
        rate = -1

if (hours > 40):
    ot_hrs = hours - 40
    hours = 40
else:
    ot_hrs = 0

pay = hours * rate + (ot_hrs * rate * ot_multiplyer)
print(f"\nPay: ${pay:,.2f}")