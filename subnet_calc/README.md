This simple utility takes an IPv4 address with CIDR extension, parses it, and returns a report of the subnet mask,
network ID, first and last usable, and broadcast addresses.

You can see in this folder the iterative process I used. 'get_ip.py' was my first effort to encapsulate the input
and validation of the IP address. 'subnet_calc.py' was basically an attempt to do some processing on that input.
'ip_sub_to_netid.py' is the more or less final version with an accompanying screenshot of it's output.
