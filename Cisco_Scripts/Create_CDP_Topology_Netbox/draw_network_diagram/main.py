# -*- coding: utf-8 -*-

def Netbox_Search(devrole, sitecode):
    import yaml
    import pynetbox
    nb = pynetbox.api(
        'http://192.168.21.22',
        threading=True,
        #private_key_file='/path/to/private-key.pem',
        token='eeba2c3f126b3deccaedd1c1e593974c8710ac44'
    )
    #filter devices based on role 'backbone'
    devices = nb.dcim.devices.filter(role=devrole)
    
    to_yaml = {}
    for device in devices:
        #filter device based on site 'My_Lab'
        if str(device.site) == sitecode:
            to_yaml[str(device)] = {'hostname':(str(device.primary_ip4)).split('/')[0]}
            
    with open('inventory/hosts.yaml', 'w') as f:
        yaml.dump(to_yaml, f, default_flow_style=False)
        
    if bool(to_yaml) == True:
        print("Hosts.yaml is ready to use!")
    else:
        print("No device has been found!")

    return   



def Nornir_show_cdp(username, password):
    '''
    username(网络设备的用户名)
    password(网络设备的密码)
    用Nornir连接网络设备获取cdp信息并返回一个list列表
    '''
    from nornir import InitNornir
    from nornir_netmiko.tasks import netmiko_send_command
    nr = InitNornir(config_file="config.yaml")
    nr.inventory.defaults.username = username
    nr.inventory.defaults.password = password
    result = nr.run(netmiko_send_command, command_string="show cdp neighbor | begin Device ID")
    result_list = []
    for i in result:
        result_list.append(f"{i}\n{str(result[i][0])}")
    return result_list


def filter_cdp_dict(result_list):
    '''
    result_list(从def Nornir_show_cdp返回的cdp信息列表)
    用正则表达式筛选出本地设备名称,本地设备接口,远端设备名称,远端设备接口
    并保存为可以被 draw_topology()处理的字典
    '''
    import re
    result_dict = {}
    topology_dict = {}
    for lines in result_list:
        loc_dev_regex = re.compile('\S+')
        regex = re.compile('(\S+)\s+(\S+\s?\S+)\s+\d+\s+[rCDBHIMPRTS ]{5}\s+(.*)')
        loc_dev_result = loc_dev_regex.search(lines)
        result = regex.findall(lines)
        for item in result:
            result_dict[(loc_dev_result.group(), ''.join(item[1].split()))] = item[0].split('.')[0], ''.join((item[2]).split()[-2:])
    
    topology_dict = {}
    for key, value in result_dict.items():
        if value in topology_dict.keys():
            pass
        else:
            topology_dict[key] = value
    return topology_dict


def main():
    from draw_network_graph import draw_topology
    from getpass import getpass

    devrole = input('What kind of device do you want to connect: ')
    sitecode = input('Which site your want to check (site_code): ')
    username = input('Your Username: ')
    password = getpass('Your Password: ')
    
    Netbox_Search(devrole, sitecode)
    result_list = Nornir_show_cdp(username, password)
    topology_dict = filter_cdp_dict(result_list)
    draw_topology(topology_dict)


if __name__ == '__main__':
    main()