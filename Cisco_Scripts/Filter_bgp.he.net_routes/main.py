#filter dup subnet for https://bgp.he.net/
# Import necessary libraries
import re
import netaddr
from netaddr import IPNetwork

# Regular expression to find IP addresses
net_regex = re.compile('(\d{1,3}\.){3}\d{1,3}/\d{1,2}')
# Initialize empty list to store networks
net = []

# Open file and read line by line
with open('file.txt') as f:
    for line in f:
        # Search for IP addresses in each line
        net_result = net_regex.search(line)
        # If IP address is found, add it to the list
        if bool(net_result) == True:
            net.append(IPNetwork(net_result.group()))

# Merge CIDR addresses
net = netaddr.cidr_merge(net)

# Prepare the data to be written into the file
write_file = []
for line in net:
    write_file.append(str(line)+'\n')

# Open a file in write mode and write the data into it
with open('sorted.txt', 'w') as f:
    f.writelines(write_file)