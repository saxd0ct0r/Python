# Timothy Owen
# 11 June 2025
# ZyBooks 8.5.1

num_lines = int(input())
vals_2d = []
for row_index in range(num_lines):
    row_elements = []
    for x in input().split():
        row_elements.append(int(x))
    vals_2d.append(row_elements)

new_vals_2d = ""
for row in vals_2d:
    new_row = []
    for val in row:
        new_row.append(str(val))
    new_vals_2d += ",".join(new_row)
    new_vals_2d += "\n"
    
print(new_vals_2d, end="")

    