from netaddr import IPAddress
import netaddr
import re


ip_regex = re.compile('(((\d+){1,3}\.){3}(\d+){1,3})\s+\d{2}:\d{2}:\d{2}\s+\w{4}\.\w{4}.\w{4}')

'''About the IP Network can be optimized by using Nornir to get it under cisco device interface config '''
arp_subnet = netaddr.IPNetwork('192.168.21.0/24')
arp_subnet_list = list(arp_subnet.iter_hosts())

with open('arp_table.txt') as f:
    for line in f:
        ip_result = ip_regex.search(line)
        if bool(ip_result) == True:
            used_ip = netaddr.IPAddress(ip_result.group())
            arp_subnet_list.remove(used_ip)
            

with open('avalible_ip.txt', 'w') as f:
    for ip in arp_subnet_list:
        f.write(f'{str(ip)}\n')
