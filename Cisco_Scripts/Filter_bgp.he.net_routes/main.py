#filter dup subnet for https://bgp.he.net/
import re
import ipaddress
import copy
from pprint import pp

net_regex = re.compile('(\d{1,3}\.){3}\d{1,3}/\d{1,2}')
net = set()
with open('file.txt') as f:
    for line in f:
        net_result = net_regex.search(line)
        if bool(net_result) == True:
            net.add(ipaddress.ip_network(net_result.group()))

new_net = copy.copy(net)

while bool(net) == True:
    a = net.pop()
    for b in net:
        if a.supernet_of(b):
            new_net.remove(b)
        elif b.supernet_of(a):
            new_net.remove(a)

sorted_net = sorted(new_net)
write_file = []
for line in sorted_net:
    write_file.append(str(line)+'\n')

with open('sorted.txt', 'w') as f:
    f.writelines(write_file)