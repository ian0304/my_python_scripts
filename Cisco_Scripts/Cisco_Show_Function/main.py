
'''
class cisco:
    def __init__(self, description):
        self.description = description

    def route(self):
        return f'show ip route'
'''    
    



def main():
    from nornir import InitNornir
    from nornir_netmiko.tasks import netmiko_send_command
    from nornir_netmiko.tasks import netmiko_send_config
    from nornir_utils.plugins.functions import print_result
    from getpass import getpass

    #device = input("Device IP: ")
    #username = input('Username: ')
    username = 'cisco'
    password = 'cisco123'
    #password = getpass('Password: ')
    #cmd = input('Input cmd:')

    #with open('inventory/hosts.yaml', 'w') as f:
    #   yaml.dump({device:{'hostname': device}}, f, default_flow_style=False)

    # get cdp result from Nornir_Scrapli
    nr = InitNornir(config_file="config.yaml")
    nr.inventory.defaults.username = username
    nr.inventory.defaults.password = password
    result = (nr.run(netmiko_send_command, command_string="show cdp neighbor | begin Device ID"))
    result = (nr.run(netmiko_send_config, config_commands="int lo 100"))
    result = (nr.run(netmiko_send_config, config_commands=["int lo 100", "ip address 1.1.1.1 255.255.255.255"]))
    print_result(result)

if __name__ == '__main__':
    main()