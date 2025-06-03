# Timothy Owen
# 2 June 2025
# Encapsulated function to get and validate structure of an IP address with CIDR,
# returns a list with four octets and CIDR code as ints, Ex. [192, 168, 30, 10, 24]

def get_ip_address():

    user_response = input("Enter IP/CIDR (X to exit): ")
    if user_response.lower() == "x":
        return -1
    
    ip_address = user_response.split(".")
    if len(ip_address) == 4:
        temp = ip_address[3].split("/")
        ip_address[3] = temp[0]
        cidr = temp[1]
        print(ip_address, cidr)
    else:
        print("Error")
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
            print("Invalid entry. IP address should be in form of ###.###.###.###/CIDR")
            return -1
        
    return ip_address, cidr
        
print(get_ip_address())
