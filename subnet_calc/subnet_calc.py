# Timothy Owen
# 29 May 2025
# Calculates subnet mask from CIDR code

# cidr_to_subnet does the heavy lifting

def cidr_to_subnet(cidr_code):
    subnet_mask = [0, 0, 0, 0]                                                      # Each element represents one octet
    
    for i in range(len(subnet_mask)):
        if cidr_code >= 8:                                                          # Only need to calculate the octet where the mask ends, so set to all bits on and go to the next
            subnet_mask[i] = 255
        elif cidr_code >= 0 :                                                       # This octet needs to be calculated. Formula effectively strips bits not part of the submask
            subnet_mask[i] = (256 - 2 ** (8 - cidr_code))
        else:
            subnet_mask[i] = 0                                                      # At this point, there are no more on bits in the submask

        cidr_code -=8                                                               # As each octet is processed, update cidr_code to match remaining octets

    return f"{subnet_mask[0]}.{subnet_mask[1]}.{subnet_mask[2]}.{subnet_mask[3]}"   # Yields subnet mask as a string

# Prompt user to enter a valid CIDR code (0 - 30) or exit (-1)

def get_cidr():
    while True:
        user_response = input("Enter CIDR code (X to exit): ")
        if user_response.lower() == "x":
            return -1
        
        try:
            cidr = int(user_response)
        except:
            print("Invalid response. CIDR code is an integer (0-30) following the slash.")
            continue
            
        if 0 <= cidr < 31:
            break

        print("Invalid response. CIDR code is an integer (0-30)")

    return cidr

# Main loop: prompt for CIDR, then output the subnet mask

while True:
    cidr = get_cidr()
    if cidr == -1:
        break
    subnet = cidr_to_subnet(cidr)
    print(f"{subnet} for CIDR of /{cidr}")

# # print all subnet masks
# for i in range(31):
#     print(f"{cidr_to_subnet(i)} for CIDR of /{i}")

   
