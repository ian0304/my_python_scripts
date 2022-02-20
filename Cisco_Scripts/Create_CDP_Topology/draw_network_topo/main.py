# -*- coding: utf-8 -*-

def OrionSDK_Search(Comments):
    '''
		Comment(输入的筛选条件)
    筛选Solarwinds数据库站点信息，将设备名称和IP保存到hosts.yaml文件
    '''
    import orionsdk
    import yaml
    swis = orionsdk.SwisClient("192.168.21.39", "test", "Password01!!")
    Hosts_Result = swis.query(f"\
        SELECT Nodes.DisplayName, Nodes.IP, Nodes.NodeID \
        FROM Orion.Nodes \
        INNER JOIN Orion.NodesCustomProperties \
        ON NodesCustomProperties.NodeID=Nodes.NodeID \
        WHERE NodesCustomProperties.Comments = '{Comments}' \
            ")
    Hosts_Result = tuple(Hosts_Result.values())[0]
    to_yaml = {}
    for i in Hosts_Result:
        to_yaml[i['DisplayName']] = {'hostname':i['IP']}

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

    Comments = input('Which site your want to check (site_code): ')
    username = input('Your Username: ')
    password = getpass('Your Password: ')
    
    OrionSDK_Search(Comments)
    result_list = Nornir_show_cdp(username, password)
    topology_dict = filter_cdp_dict(result_list)
    draw_topology(topology_dict)


if __name__ == '__main__':
    main()