#filter dup subnet for https://bgp.he.net/
import re
import netaddr
from netaddr import IPNetwork

net_regex = re.compile('(\d{1,3}\.){3}\d{1,3}/\d{1,2}')
net = []
with open('file.txt') as f:
    for line in f:
        net_result = net_regex.search(line)
        if bool(net_result) == True:
            net.append(IPNetwork(net_result.group()))

net = netaddr.cidr_merge(net)

write_file = []
for line in net:
    write_file.append(str(line)+'\n')

with open('sorted.txt', 'w') as f:
    f.writelines(write_file)