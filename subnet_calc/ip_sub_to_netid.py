# Timothy Owen
# 3 June 2025
'''
Script to take a string of IP/CIDR and output the following:
IP address, CIDR
Subnet Mask
Network ID
1st Usable IP/Gateway
Last Usable IP
Broadcast IP
'''
null_ip = [0, 0, 0, 0] # used often enough that it deserves its own name

# Takes a string holding the IP address, returns a tuple: ([list of octets as integers], integer)
# Provides validation for input, raises ValueError with messages to help user correct input
def str_to_ip_address(str_ip_address_cidr):

    ip_address = str_ip_address_cidr.split(".")

    if len(ip_address) != 4:
        raise ValueError("Invalid input. IPv4 address must be four octets")
    
    try:
        cidr = str_ip_address_cidr.split("/")[1]    # [1] is the CIDR part, dump the rest
    except:
        raise ValueError("Invalid input. Calculator expects CIDR code after a '/'")

    ip_address[3] = ip_address[3].split("/")[0]     # Go back and get the octet without CIDR
    
    index = 0
    for octet in ip_address:
        octet = int(ip_address[index])
        if 0 <= octet <= 255:
            ip_address[index] = octet
            index += 1
        else:
            raise ValueError(f"Invalid input. IPv4 octet {ip_address[index]} outside of range 0 to 255")
        
    try:
        err_message = "Invalid input. CIDR must be an integer between 0 and 30"
        cidr = int(cidr)
        if cidr < 0 or cidr > 30:
            raise ValueError(err_message)
    except:
        raise ValueError(err_message)
        
    return ip_address, cidr

# Takes an integer for the CIDR code, returns a list of octets for the subnet mask
def cidr_to_subnet(cidr_code):
    subnet_mask = null_ip.copy()                    # Each element represents one octet
    
    for i in range(len(subnet_mask)):
        if cidr_code >= 8:                          # Only need to calculate the octet where the mask ends, so set to all bits on and go to the next
            subnet_mask[i] = 255
        elif cidr_code >= 0 :                       # This octet needs to be calculated. Formula effectively strips bits not part of the submask
            subnet_mask[i] = (256 - 2 ** (8 - cidr_code))
        else:
            subnet_mask[i] = 0                      # At this point, there are no more on bits in the submask

        cidr_code -=8                               # As each octet is processed, update cidr_code to match remaining octets

    return subnet_mask

# Takes a list of octets, integer CIDR code, returns a list of octets for the Network ID
# Calls cidr_to_subnet()
def ip_to_netID(ip_list, cidr_code):
    netID = null_ip.copy()

    subnet = cidr_to_subnet(cidr_code)
    for i in range(4):
        netID[i] = ip_list[i] & subnet[i]           # Bitwise AND for each octet
    return netID

# Takes a list of octets, returns a string IP address
def octet_list_to_ip_str(octets):
    return f"{octets[0]}.{octets[1]}.{octets[2]}.{octets[3]}"

# Takes a string in form of ##.##.##.##/##, prints list of related addresses
# Assembles returns from all the other functions
def display_ip_info(ip_string):     
    ip_address, cidr = str_to_ip_address(ip_string) # Parse and validate ip_string

    subnet = cidr_to_subnet(cidr)
    network_ID = ip_to_netID(ip_address, cidr)

    gateway = network_ID.copy()
    gateway[-1] += 1

    broadcast_mask = null_ip.copy()
    broadcast = null_ip.copy()
    for i in range(len(broadcast_mask)):
        broadcast_mask[i] = ~subnet[i] & 0xff       # Bitwise NOT
        broadcast[i] = network_ID[i] | broadcast_mask[i] # Turns on all bits of subnet range

    last_ip = broadcast.copy()
    last_ip[-1] -= 1

    print(f"Input:\t\t\t{ip_string}")
    print(f"IP address:\t\t{octet_list_to_ip_str(ip_address)}\tCIDR: {cidr}")
    print(f"Subnet mask:\t\t{octet_list_to_ip_str(subnet)}")
    print(f"Network ID:\t\t{octet_list_to_ip_str(network_ID)}")
    print(f"Gateway (1st usable):\t{octet_list_to_ip_str(gateway)}")
    print(f"Last usable:\t\t{octet_list_to_ip_str(last_ip)}")
    print(f"Broadcast:\t\t{octet_list_to_ip_str(broadcast)}")

# Endless loop as main function, takes the IP/CIDR or X/x to exit
# If there is a problem with the entry, displays error message with
# info about how to correct it.
while True:
    try:
        my_ip = input("Enter an IP address with CIDR code in form of ###.###.###.###/## (X to exit):\n")
        if my_ip.lower() == "x":
            break

        display_ip_info(my_ip)
        print()
    except ValueError as e:
        print(e)
