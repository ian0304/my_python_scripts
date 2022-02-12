from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from nornir_utils.plugins.functions import print_result
from draw_network_graph import draw_topology

def cdp_value(result_list):
    import re
    result_dict = {}
    topology_dict = {}
    for lines in result_list:
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



nr = InitNornir(config_file="config.yaml")
result = nr.run(task=send_command, command="show cdp neighbor | begin Device ID")
result_list = []
for i in result:
    result_list.append(f"{i}\n{str(result[i][0])}")


topology_dict = cdp_value(result_list)
draw_topology(topology_dict)