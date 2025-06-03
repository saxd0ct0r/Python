# Timothy Owen
# 2 June 2025
# Encapsulated function to get and validate structure of an IP address with CIDR,
# returns a list with four octets and CIDR code as ints, Ex. [192, 168, 30, 10, 24]

def get_ip_address():
    while True:
        user_response = input("Enter IP/CIDR (X to exit): ")
        if user_response.lower() == "x":
            return -1
        
        ip_address = user_response.split(".")
        if len(ip_address) == 4:
            temp = ip_address[len(ip_address) - 1].split("/")
            ip_address[len(ip_address) - 1] = temp[0]
            cidr = temp[1]
            print(ip_address, cidr)
        else:
            print("Error")
            return -1
        

get_ip_address()
