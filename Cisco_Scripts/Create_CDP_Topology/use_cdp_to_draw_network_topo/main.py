def main():
    from nornir import InitNornir
    from nornir_scrapli.tasks import send_command
    from draw_network_graph import draw_topology
    from cdp_to_dict import cdp_to_dict
    nr = InitNornir(config_file="config.yaml")
    result = nr.run(task=send_command, command="show cdp neighbor | begin Device ID")
    result_list = []
    for i in result:
        result_list.append(f"{i}\n{str(result[i][0])}")
    topology_dict = cdp_to_dict(result_list)
    draw_topology(topology_dict)

if __name__ == '__main__':
    main()