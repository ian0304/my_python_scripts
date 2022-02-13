def cdp_to_dict(cdp_list):
    import re
    from pprint import pp
    result_dict = {}
    topology_dict = {}
    pp(cdp_list)
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