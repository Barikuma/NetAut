from netmiko import ConnectHandler
from validate import get_valid_ddn, validate_input

def configure_ip_address(username, password, hosts):
    hosts = hosts.split(sep=',')
    for net_device in hosts:
        print(net_device)
        device = {
            'device_type': 'cisco_ios',
            'host': net_device,
            'username': username,
            'password': password
        }

        try:
            # Requests for the parameters needed to be configured from the user
            interface = input("\nInterface: ")
            ip_address = get_valid_ddn()
            netmask = get_valid_ddn(subnet_mask=True)

            # The list of commands entered on the device
            commands = [
                f"interface {interface}",
                f"ip address {ip_address} {netmask}"
            ]

            turn_on_interface = validate_input(f"Turn on interface {interface} (Y/N): ", expected_input=['Y', 'N'])

            # If the user decides to turn on the interface
            if turn_on_interface == 'Y':
                commands.append("no shutdown")

            with ConnectHandler(**device) as device__:
            # Sends the set of commands to the device
                print(device__.send_config_set(commands))

                # Command to verify the ip address was configured on the interface
                interface_brief = device__.send_command("show ip interface brief")
            
            # Return the verification
            print(interface_brief)
        except Exception as e:
            print(f"Error: {e} occured while configuring device")

