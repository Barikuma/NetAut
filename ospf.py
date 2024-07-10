from netmiko import ConnectHandler
from validate import get_valid_ddn, validate_input, get_hostname
from getpass import getpass

# This function checks if there are OSPF processes currently running on the device
def running_process(device):
    ospf_process = device.send_command("show running-config | section ospf")

    # If router ospf is in the output of the command
    if "router ospf" in ospf_process:
        return True
    return False

# This function is used to configure OSPF router ID, networks and passive interfaces
def configure_parameters(device, process_id):
    configure_router_id = validate_input("Will you like to configure Router ID (Y/N): ", expected_input=['Y', 'N'])

    commands = [f"router ospf {process_id}"]

    # If the user decides to configure a router ID, append the ID to the commands list
    if configure_router_id == 'Y':
        router_id = get_valid_ddn("Enter Router ID: ")
        commands.append(router_id)
    elif configure_router_id == 'N':
        print("Exiting router ID configuration...")

    configure_networks = validate_input("Will you like to configure networks (Y/N): ", expected_input=['Y', 'N'])

    # If the user decides to add a network to the OSPF process
    if configure_networks == 'Y':
        done = False
        
        # Requests for OSPF network until the user decides to stop
        while True:
            network_id = get_valid_ddn("Network ID: ")
            wildcard_mask = get_valid_ddn("WIldcard mask: ", wildcard_mask=True)

            # This loop validates the area number entered by the user
            while True:
                try:
                    area = int(input("Area: "))

                    # If the area number entered by the user is within the valid range
                    if 0 <= area <= 4294967295:
                        break
                    print("Area number must be between 0 - 4294967295")

                # If the user enter a non-digit
                except TypeError:
                    print("Area should be a number")

            # Append the command to the list of commands
            commands.append(f"network {network_id} {wildcard_mask} area {str(area)}")
            
            # Prompt the user asking if they are done
            done = validate_input("Done?(Y/N): ", expected_input=['Y', 'N'])

            # If the user decides to stop
            if done == 'Y':
                break
    elif configure_networks == 'N':
        print("Exiting network configuration...")

    passive_interface = validate_input("Will you like to configure passive interfaces (Y/N): ", expected_input=['Y', 'N'])

    # If the user decides to configure a passive interface
    if passive_interface == 'Y':
        interfaces = input("Enter interface (if more than one, separate with a comma): ")
        strip_spaces = ''.join(inter.strip() for inter in interfaces)
        interfaces = strip_spaces.split(sep=',')

        # Append the command for all passive interfaces to the list of commands
        for interface in interfaces:
            commands.append(f"passive-interface {interface}")
    elif passive_interface =='N':
        print("Exiting passive interface configuration...")
    
    # Checks if the user chose to configure a parameter
    if len(commands) > 1:
        device.send_config_set(commands)
    
    # The output of the show command
    show_ospf_process = device.send_command("show running-config | sectio ospf")

    print(f"\nHost {get_hostname(device)}\n{show_ospf_process}")
            




def configure_ospf_process(device):

    process_check = running_process(device)

    if not process_check:
        # Prompt the user, asking if they'll like to configure a process
        config_ospf = validate_input("\nNo OSPF process running, would you like to configure one (Y/N)?: ", expected_input=['Y', 'N'])

        if config_ospf == 'Y':
            while True:
                # Prompt the user asking for the process ID of the ospf process
                process_id = validate_input("\nProcess ID: ", allow_int=True)

                # If the process ID entered by the user is within the range of allowed proces IDs
                if process_id >= 1 and process_id <= 65535:
                    break
                else:
                    print("\nEnter a number between 1 and 65535")
            configure_parameters(device, str(process_id))
        elif config_ospf == 'N':
            print("Exiting OSPF configuration...")
    

    

if __name__ == '__main__':
    hostnames = ['SW1', 'SW2', 'R1', 'R2']

    print("\nAvailable host devices to configure")
    for hostname in hostnames:
        print(hostname, end=' ')
    print("")

    while True:
        # Accepts input from the user
        host_to_configure = input("Hosts to configure (if more than one, separate with a comma): ").upper()

        # Strips off spaces after a comma in the user input
        strip_spaces = ''.join(s.strip() for s in host_to_configure)

        # Adds each separated value in stri_spaces to a list
        host_to_configure = strip_spaces.split(sep=',')

        valid_hosts = True
        unavailable_hosts = []

        # Loops through the hosts entered by the user and appends any unavailable host entered by the user to a list
        for host in host_to_configure:
            if not host in hostnames:
                unavailable_hosts.append(host)

        # If there unavailable hosts, prompt the user and set valid_hosts to false
        if unavailable_hosts:
            if len(unavailable_hosts) > 1:
                print(f"Hosts", *unavailable_hosts, "is not in the list of available devices")
            else:
                print(f"Host", *unavailable_hosts, "is not in the list of available devices")
            valid_hosts = False
        
        # If the hosts entered by the user is valid, break out of the while loop
        if valid_hosts:
            break
    
    # Ask user for authentication parameters
    username = input("Username: ")
    password = getpass()

    # Loop through the devices entered by the user and connect to each
    for net_device in host_to_configure:
        device = {
            'device_type': 'cisco_ios',
            'host': net_device,
            'username': username,
            'password': password
        }

        with ConnectHandler(**device) as device__:
            configure_ospf_process(device__)