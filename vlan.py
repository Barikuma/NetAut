from netmiko import ConnectHandler
from validate import validate_input, check_hosts
from getpass import getpass

# This function validates the VLAN ID entered by user
def validate_vlan_id(prompt=None, vlan_id=None):
    prohibited_vlan_id = [0, 1, 1002, 1003, 1004, 1005, 4095]

    while True:
        if vlan_id:
            for id in vlan_id:
                if id in prohibited_vlan_id:
                    print(f"\nNot allowed to create VLAN {vlan_id}")
                    break
            break
        else:
            try:
                # Requests the first vlan ID from the user
                vlan_id = int(input(prompt))

                # Checks if the user enter one of the default VLANs
                if vlan_id in prohibited_vlan_id:
                    print(f"\nNot allowed to create VLAN {vlan_id}")
                    continue
                # Checks if the user enters a VLAN ID greater or less than the expected
                elif vlan_id < 1 or vlan_id > 4094:
                    print("\nEnter a VLAN ID between 1 and 4094")
                    continue
                # All checks are complete and the VLAN ID is valid, break
                else:
                    break

            # If the user does not enter an integer
            except ValueError:
                print("\nInvalid input, please enter an integer.")

    return vlan_id


# This checks if the user entered numbers as vlan ID or otherwise
def valid_id():
    valid = True

    while True:
        vlans = input("\nEnter the IDs of VLANs to configure (if more than one, separate with a comma): ")

        vlans = ''.join(identifier.strip() for identifier in vlans)

        # Makes each ID entered by the user an element in a list
        vlans_ids = vlans.split(sep=',')

        # Loops through all the IDs, prompt the user if any of the IDs entered were not digits
        for id in vlans_ids:
            try:
                id = int(id)
            except ValueError:
                print(f"\n{id} is not a valid VLAN ID")
                valid = False
                break
        # Break out of the loop if the IDs are valid else continue the while loop
        if valid == True:
            break
        else:
            continue

    vlans_ids = ','.join(str(vlan_id) for vlan_id in vlans_ids)
    return [valid, vlans_ids]


# Function to prompt user for VLAN names and return the configuration commands
def get_vlan_commands(vlan_ids):
    vlan_commands = []
    for vlan_id in vlan_ids:
        vlan_name = input(f"Enter the name for VLAN {vlan_id}: ")
        vlan_commands.append(f'vlan {vlan_id}')
        vlan_commands.append(f'name {vlan_name}')
    return vlan_commands


# This function configures VLANS in a switch
def configure_vlan(username, password, hosts):
    number_of_vlans = validate_input("\nHow many VLANS do you wish to configure: ", allow_int=True)

    # This is in case the user wants to create those number of VLANS automatically with a specified increment in VLAN ID
    prompt = f"\nWould you like to configure {number_of_vlans} number of vlans automatically (Y/N)?: "
    auto_or_manual = validate_input(prompt, expected_input=['Y', 'N'])


    # If users agrees to auto configure
    if auto_or_manual == 'Y':

        vlan_id = validate_vlan_id("\nFirst VLAN ID between 2 and 4094 (0, 1, 1002, 1003, 1004, 1005, 4095 are prohibited): ")

        while True:
            # Requests the increment value from the user
            increment = validate_input("\nIncrement: ", allow_int=True)

            # Checks if increment is greater than the range of configurable VLAN IDs
            if increment <= 0 or increment > 4094:
                print("\nIncrement range is invalid")
                continue
            break

        ids = []
        # Loops for the number of VLANS entered by the user
        for _ in range(number_of_vlans):
            ids.append(str(vlan_id))

            # Increments the VLAN ID with the increment value, which serves as the new VLAN ID for the next VLAN
            vlan_id += increment

            # Check if the new VLAN ID is greater than the highest configurable ID 4094
            if vlan_id > 4094:
                print("\nCannot go beyond 4094")
                break
        command = get_vlan_commands(ids)

    # If user disagress to auto configure
    elif auto_or_manual == 'N':

        # Requests for the vlan ID and the vlan name from the user
        vid = valid_id()
        list_of_ids = vid[1]

        valid_vlan_id = validate_vlan_id(vlan_id=list_of_ids.split(sep=','))
        command = get_vlan_commands(valid_vlan_id)

    # Loop through the devices entered by the user and connect to each
    for net_device in hosts:
        device = {
            'device_type': 'cisco_ios',
            'host': net_device,
            'username': username,
            'password': password
        }

        print(f"\n Host {net_device}\n")
        with ConnectHandler(**device) as device__:
            device__.send_config_set(command)
            vlan_brief = device__.send_command("show vlan brief")

        print(f"\n{net_device}\n{vlan_brief}")

if __name__ == '__main__':

    hostnames = ['SW1', 'SW2', 'R1', 'R2']
    print("\nAvailable host devices to configure")

    for hostname in hostnames:
        print(hostname, end=' ')
    print("")

    while True:
        print(hostnames)

        valid = check_hosts(hostnames)

        if valid[0]:
            break

    # Ask user for authentication parameters
    username = input("Username: ")
    password = getpass()

    configure_vlan(username, password, valid[1])