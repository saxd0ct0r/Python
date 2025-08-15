# Timothy Owen
# 14 Aug 2025
'''
Calculates the total VA disability rating from individual claims
'''

ability = 1
total_disability = 0
display_disability = 0

while True:
    user_input = input("Enter a Disability Factor (X to exit): ")
    if user_input.lower() == "x":
        break
    disability_factor = 1 - (int(user_input) / 100)
    ability *= disability_factor
    total_disability = 1 - ability
    display_disability = round(total_disability, 1) * 100
    print(f"Raw disability is {(total_disability * 100):.1f}%")

print(f"Your final disability rating should be {int(display_disability)}%")

