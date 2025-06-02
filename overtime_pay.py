# Timothy Owen
# 2 June 2025
# Encapsulates overtime pay calculation in a function

def computepay(hours, rate):
    ot_multiplyer = 1.5

    if (hours > 40):
        ot_hrs = hours - 40
        hours = 40
    else:
        ot_hrs = 0

    pay = (hours * rate) + (ot_hrs * rate * ot_multiplyer)    
    return pay

for name in ("James", "Judy" , "John"):
    hrs=float(input(f'{name}, please enter your weekly hours? '))
    rt=float(input('and your Pay Rate? '))
    print("Hours Entered: ", hrs)
    print("Rate Entered: ", rt)
    print(f"{name} receives ${computepay(hrs, rt):.2f}")
print("all done")
