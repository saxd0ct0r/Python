# Timothy Owen
# 9 Jun 2025
'''
6.26 LAB: Exact change - functions
Define a function called exact_change that takes the total change amount in 
cents and calculates the change using the fewest coins. The coin types are 
pennies, nickels, dimes, and quarters. Then write a main program that reads the 
total change amount as an integer input, calls exact_change(), and outputs the 
change, one coin type per line. Use singular and plural coin names as 
appropriate, like 1 penny vs. 2 pennies. Output "no change" if the input is 0 
or less.
    Ex: If the input is:
            0 
        (or less), the output is:
            no change
    Ex: If the input is:
            45
        the output is:
            2 dimes 
            1 quarter
Your program must define and call the following function. The function 
exact_change() should return a tuple containing num_pennies, num_nickels, 
num_dimes, and num_quarters.
def exact_change(user_total)
'''

# Define your function here
def exact_change(user_total):
    '''Calculates the fewest number of coins to equal required change'''
    pennies, nickels, dimes, quarters = 0, 0, 0, 0

    while user_total > 0:
        if user_total >= 25:
            quarters += 1
            user_total -= 25
            continue
        elif user_total >= 10:
            dimes += 1
            user_total -= 10
            continue
        elif user_total >=5:
            nickels += 1
            user_total -= 5
            continue
        elif user_total >= 1:
            pennies += 1
            user_total -= 1

    return pennies, nickels, dimes, quarters

def print_coins(number, single, plural):
    if number:
        print(f"{number}", end=" ")
        if number > 1:
            print(plural)
        else:
            print(single)

if __name__ == "__main__":
    input_val = int(input())
    num_pennies, num_nickels, num_dimes, num_quarters = exact_change(input_val)

    # Type your code here.
    if num_pennies + num_nickels + num_dimes + num_quarters <= 0:
        print("no change")

    print_coins(num_pennies, "penny", "pennies")
    print_coins(num_nickels, "nickel", "nickels")
    print_coins(num_dimes, "dime", "dimes")
    print_coins(num_quarters, "quarter", "quarters")
