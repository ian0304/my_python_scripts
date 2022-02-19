
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
        else:
            topology_dict[key] = value

    return topology_dict 

def main():
    from nornir import InitNornir
    from nornir_netmiko.tasks import netmiko_send_command
    from nornir_utils.plugins.functions import print_result
    from getpass import getpass
    from nornir.core.inventory import Hosts 
    import yaml

    import sys
    from pprint import pp
    try:
        import orionsdk
    except ImportError:
        print("Module orionsdk needs to be installed")
        print("pip install orionsdk")
        sys.exit()

    #SwicClient("ServerIP/Name", "Username", "Password")
    swis = orionsdk.SwisClient("192.168.21.39", "test", "Password01!!")
    Comments = str(input('Which site your want to check (site_code): ')).upper()
    #Get Hostname/ IP / information  from Orion.Nodes filter by Comments
    NodeID = tuple((swis.query(f"SELECT NodeID FROM Orion.NodesCustomProperties WHERE Comments='{Comments}'")).values())[0]
    NodeID_Items = tuple(i['NodeID'] for i in NodeID)
    Host_IP_lst = tuple((swis.query(f"SELECT DisplayName, IP FROM Orion.Nodes WHERE NodeID IN {NodeID_Items} ")).values())[0]
    
    to_yaml = {}
    for i in Host_IP_lst:
        to_yaml[i['DisplayName']] = {'hostname':i['IP']}
        
    with open('inventory/hosts.yaml', 'w') as f:
        yaml.dump(to_yaml, f, default_flow_style=False)

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