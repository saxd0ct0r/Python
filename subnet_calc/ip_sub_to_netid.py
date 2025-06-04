# Timothy Owen
# 3 June 2025
'''
Script to take string of IP/CIDR and output the following:
IP address, CIDR
Subnet Mask
Network ID
1st Usable IP/Gateway
Last Usable IP
Broadcast IP
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

my_ip = "192.168.40.39/26"

ip_address, cidr = str_to_ip_address(my_ip)
subnet = cidr_to_subnet(cidr)
network_ID = ip_to_netID(ip_address, cidr)

gateway = network_ID.copy()
gateway[-1] += 1

broadcast_mask = null_ip.copy()
broadcast = null_ip.copy()
for i in range(len(broadcast_mask)):
    broadcast_mask[i] = ~subnet[i] & 0xff
    broadcast[i] = network_ID[i] | broadcast_mask[i]

last_ip = broadcast.copy()
last_ip[-1] -= 1

print(f"Input:\t\t\t{my_ip}")
print(f"IP address:\t\t{octet_list_to_ip_str(ip_address)}\tCIDR: {cidr}")
print(f"Subnet mask:\t\t{octet_list_to_ip_str(subnet)}")
print(f"Network ID:\t\t{octet_list_to_ip_str(network_ID)}")
print(f"Gateway (1st usable):\t{octet_list_to_ip_str(gateway)}")
print(f"Last usable:\t\t{octet_list_to_ip_str(last_ip)}")
print(f"Broadcast:\t\t{octet_list_to_ip_str(broadcast)}")


