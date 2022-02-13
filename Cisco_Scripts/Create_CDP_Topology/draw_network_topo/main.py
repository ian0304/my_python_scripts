from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from draw_network_graph import draw_topology

def cdp_to_dict(cdp_list):
    # get cdp result from Nornir_Scrapli
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
            if value in result_dict.keys():
                break
            topology_dict[key] = value
    return topology_dict 

def main():
    nr = InitNornir(config_file="config.yaml")
    result = nr.run(task=send_command, command="show cdp neighbor | begin Device ID")
    #Change cdp result from string to list
    result_list = []
    for i in result:
        #Add local device name in the begining of device result
        result_list.append(f"{i}\n{str(result[i][0])}")
    topology_dict = cdp_to_dict(result_list)
    draw_topology(topology_dict)

if __name__ == '__main__':
    main()