
from draw_network_graph import draw_topology

def cdp_to_dict(cdp_list):
    #transfer cdp string list to {(localdevice: localinterface), (remotedevice:remoteinterface)} format
    import re
    result_dict = {}
    topology_dict = {}
    for lines in cdp_list:
        loc_dev_regex = re.compile('\S+')
        regex = re.compile('(\S+?)[\s\.][\s+\S+][\s\n]\s+(\S+\s?\S+)\s+\d+\s+[rCDBHIMPRTS ]{5}\s+(.*)')
        loc_dev_result = loc_dev_regex.search(lines)
        result = regex.findall(lines)
        for item in result:
            result_dict[(loc_dev_result.group(), ''.join(item[1].split()))] = item[0].split('.')[0], ''.join((item[2]).split()[-2:])
    for key, value in result_dict.items():
        if value in topology_dict.keys():
            pass
        topology_dict[key] = value

    return topology_dict 

def main():
    from nornir import InitNornir
    from nornir_netmiko.tasks import netmiko_send_command
    from nornir_utils.plugins.functions import print_result
    from getpass import getpass
    # get cdp result from Nornir_Scrapli
    nr = InitNornir(config_file="config.yaml")
    nr.inventory.defaults.username = str(input('Your Username: '))
    nr.inventory.defaults.password = str(getpass('Your Password: '))
    result = nr.run(netmiko_send_command, command_string="show cdp neighbor | begin Device ID")
    #Change cdp result from string to list
    result_list = []
    for i in result:
        #Add local device name in the begining of device result
        result_list.append(f"{i}\n{str(result[i][0])}")
    topology_dict = cdp_to_dict(result_list)
    draw_topology(topology_dict)

if __name__ == '__main__':
    main()