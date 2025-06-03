# Timothy Owen
# 2 June 2025
# Encapsulated function to get and validate structure of an IP address with CIDR,
# returns a list with four octets and CIDR code as ints, Ex. [192, 168, 30, 10, 24]

def get_ip_address():

    user_response = input("Enter IP/CIDR (X to exit): ")
    if user_response.lower() == "x":
        return 0
    
    ip_address = user_response.split(".")
    cidr = user_response.split("/")[1]

    if len(ip_address) == 4:
        ip_address[3] = ip_address[3].split("/")[0]
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
                raise ValueError("Invalid entry. IP address octets must be integers"
                                "from 0 to 255")
        except:
            return -1
        
    try:
        cidr = int(cidr)
        if cidr < 0 or cidr > 30:
            raise ValueError("Invalid entry. CIDR must be an integer from 0 to 30")
    except:
        return -1
        
    return ip_address, cidr
        
print(get_ip_address())
