from netmiko import ConnectHandler
from getpass import getpass
from validate import validate_input

# This function connects to the device and sends the commands
def connect(hosts, username, password, config_mode_command, priv_mode_command):

    # If the hosts parameter contains just one string, convert the string to a list
    if isinstance(hosts, str):
        hosts = [hosts]
    
    # Loop through the hosts list, connect to each device and send the command
    for host in hosts:
        device = {
            'device_type': 'cisco_ios',
            'host': host,
            'username': username,
            'password': password
        }

        # Connect, send command to device print output of show command
        with ConnectHandler(**device) as device__:
            device__.send_config_set(config_mode_command)
            show_output = device__.send_command(priv_mode_command)
        
        print(f"\nHost {host}\n{show_output}")

# This function forms the etherchannel between the switches
def etherchannel(hosts, username, password):
    interfaces = input("Interfaces: ")
    config_mode_command = [
        f"interface range {interfaces}"
    ]

    # A dictionary of the two link aggregation protocols
    protocols = {
        '1': 'PAGP',
        '2': 'LACP'
    }

    # This loop is to make sure the user enters a digit as the group number
    while True:
        group_number = input("Group number: ")
        if group_number.isdigit():
            break
        print("Enter a number please")
    
    print("\nProtcols")
    # Prints the key and values of the protocols dictionary
    for k,v in protocols.items():
        print(f"{k}. {v}")
    
    # Asks the user the protocol they wish to configure the interfaces with
    user_choice = validate_input("Protocol (Enter a number): ", ['1', '2'])

    # Loops through the list of hosts and sends the appropriate command to that host
    for host in hosts:
        if protocols[f'{user_choice}'] == protocols['1']:
            mode = validate_input(f"\nHost {host}\nMode (auto / desirable): ", expected_input=["AUTO", "DESIRABLE"])
            config_mode_command.append(f"channel-group {group_number} mode {mode.lower()}")
            config_mode_command.append("channel-protocol pagp")

        elif protocols[f'{user_choice}'] == protocols['2']:
            mode = validate_input(f"\nHost {host}\nMode (active / passive): ", expected_input=["ACTIVE", "PASSIVE"])
            config_mode_command.append(f"channel-group {group_number} mode {mode.lower()}")
            config_mode_command.append("channel-protocol lacp")
        
        priv_mode_command = "show etherchannel summary"
        connect(host, username, password, config_mode_command, priv_mode_command)


if __name__ == '__main__':
    hosts = ['AS1', 'AS2']
    username = input("Username: ")
    password = getpass()

    etherchannel(hosts, username, password)