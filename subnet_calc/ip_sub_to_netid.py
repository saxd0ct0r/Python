# Timothy Owen
# 3 June 2025
'''
Script to take string of IP/CIDR, parse it, calculate subnet, and filter
Network ID.
'''
null_ip = [0, 0, 0, 0]

def str_to_ip_address(str_ip_address_cidr):

# parse string into octets and CIDR
    ip_address = str_ip_address_cidr.split(".")
    cidr = str_ip_address_cidr.split("/")[1]

    if len(ip_address) == 4:
        ip_address[3] = ip_address[3].split("/")[0]
        # print(ip_address, cidr)
    else:
        return -1
    
    index = 0
    for octet in ip_address:
        try:
            octet = int(ip_address[index])
            if 0 <= octet <= 255:
                ip_address[index] = octet
                index += 1
            else:
                return -1
        except:
            return -1
        
    try:
        cidr = int(cidr)
        if cidr < 0 or cidr > 30:
            return -1
    except:
        return -1
        
    return ip_address, cidr

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

    return subnet_mask

def ip_to_netID(ip_list, cidr_code):
    netID = [0, 0, 0, 0]

    subnet = cidr_to_subnet(cidr_code)
    for i in range(4):
        netID[i] = ip_list[i] & subnet[i]
    return netID

def octet_list_to_ip_str(octets):
    return f"{octets[0]}.{octets[1]}.{octets[2]}.{octets[3]}"

my_ip = "10.47.182.99/27"
ip_address, cidr = str_to_ip_address(my_ip)
print(f"IP address: {ip_address}, CIDR: {cidr}")


subnet = cidr_to_subnet(cidr)
print(f"Subnet mask: {subnet}")
network_ID = ip_to_netID(ip_address, cidr)
print(f"Network ID: {network_ID[0]}.{network_ID[1]}.{network_ID[2]}.{network_ID[3]}")
gateway = network_ID.copy()
gateway[-1] += 1
print(f"Gateway (1st usable): {gateway[0]}.{gateway[1]}.{gateway[2]}.{gateway[3]}")

broadcast_mask = null_ip.copy()
broadcast = null_ip.copy()
for i in range(len(broadcast_mask)):
    broadcast_mask[i] = ~subnet[i] & 0xff
    broadcast[i] = network_ID[i] | broadcast_mask[i]

last_ip = broadcast.copy()
last_ip[-1] -= 1
print(f"Last usable: {last_ip[0]}.{last_ip[1]}.{last_ip[2]}.{last_ip[3]}")
print(f"Broadcast: {broadcast[0]}.{broadcast[1]}.{broadcast[2]}.{broadcast[3]}")


