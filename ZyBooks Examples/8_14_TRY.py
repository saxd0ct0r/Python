room_data = {}

input_line = input()
while input_line != "done":
    room_number, guest = input_line.split()
    room_data[int(room_number)] = guest
    input_line = input()

sorted_room_number = list(room_data.keys())
sorted_room_number.sort()
for room in sorted_room_number:
    print(f"Room number: {room}, Guest name: {room_data[room]}")