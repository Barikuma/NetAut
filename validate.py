from getpass import getpass
from netmiko import ConnectHandler

def get_valid_ddn(prompt=None, subnet_mask=False, wildcard_mask=False):
    
    while True:

        # If subnet mask is set to true
        if subnet_mask:

            # List of allowed octet values
            allowed = [0, 128, 192, 224, 240, 248, 252, 254, 255]

            # Will be used to check if a subnet mask is valid
            valid = True

            while True:

                # Request for subnet mask
                netmask = input(f"{prompt}")

                # Separate the string entered by the user, add each value to a list
                check_mask = netmask.split(sep='.')

                # Check if the values are up to 4
                if len(check_mask) != 4:
                    print("Subnet mask must be 4 DDN separated values")
                    valid = False
                    continue

                # Check if the value of the first octet is zero
                if int(check_mask[0]) == 0:
                    print("Subnet mask cannot start with a zero")
                    valid = False
                    continue
                
                # Index variable
                i = 0

                for i in range(4):

                    # If the value at the current index is an allowed value
                    if int(check_mask[i]) in allowed:

                        # If the value is 255, set valid to true and return to the top of the for loop
                        if int(check_mask[i]) == 255:
                            valid = True
                            continue

                         # If the value is an allowed value that is not 255, call the mask check function
                        else:
                            valid = mask_check(check_mask, i, subnet=True)

                            # If the function call returns a False break
                            if valid == False:
                                break

                    # if the value at the current index is not an allowed value
                    else:
                        print(f"{check_mask[i]} is not in the list of allowed values for a subnet mask")
                        valid = False
                        break
                
                 # If the final value of valid after the for loop is true, return the subnet mask entered by the user
                if valid:
                    return netmask
        
        # If wildcard mask is set to true
        elif wildcard_mask:

            # The allowed values an octet in a wildcard mask can have
            allowed = [0, 1, 3, 7, 15, 31, 63, 127, 255]

            # Will be used to check if a wildcard mask is valid
            valid = True

            while True:

                # Request the wildcard mask from the user
                wildcard_mask = input(f"{prompt}")

                # Make each octet an element of a list
                check_wildcard_mask = wildcard_mask.split(sep='.')

                # Check if there are 4 octets. If not prompt the user, set valid to false and return to the top of the loop
                if len(check_wildcard_mask) != 4:
                    print("Wildcard mask must be 4 DDN separated values")
                    valid = False
                    continue
                
                # Used to loop through the list check_wildcard_mask
                i = 0

                for i in range(4):

                    # Check if the value at the current index is an allowed value
                    if int(check_wildcard_mask[i]) in allowed:

                        # If the value is 0, set valid to true and return to the top of the for loop
                        if int(check_wildcard_mask[i]) == 0:
                            valid = True
                            continue

                        # If the value is an allowed value that is not 0, call the mask check function
                        else:
                            valid = mask_check(check_wildcard_mask, i, wildcard=True)

                            # If the function call returns a False break
                            if valid == False:
                                break

                    # if the value at the current index is not an allowed value
                    else:
                        print(f"{check_wildcard_mask[i]} is not an allowed octet value")
                        valid = False
                        break

                # If the final value of valid after the for loop is true, return the wildcard mask entered by the user
                if valid:
                    return wildcard_mask

        # If neither subnet_mask and wildcard_mask is set to true, this block runs. This block of code configures an IP address
        else:

            # Requests the user to input an IP address
            ip_address = input(f"{prompt}")

            # Splits each octet in the router ID and stores it as an element in a list
            ip_address_check = ip_address.split(sep='.')
            
            # Checks if the length of the values entered in the list is equal to 4.
            # If not, it prompts the user and goes to the beginning of the loop
            if len(ip_address_check) != 4:
                print("\nMust be 4 DDN separated values")
                continue

            # Checks if the first octet is a 0. If it is, it prompts the user and goes to the beginning of the loop
            if ip_address_check[0] == '0':
                print("\nIP address cannot start with a zero")
                continue
            
            # Will be used to check if the IP address entered by the user is valid
            valid = True

            # Loops through the elements in the list
            for octet in ip_address_check:
                
                # Checks if an octet is not a digit. If not, it sets Valid to False and breaks out of the for loop
                if not octet.isdigit():
                    print("\nIP address cannot have a non digit")
                    valid = False
                    break

                # Checks if the value of an octet is between 0 and 255. If not, it sets Valid to False and breaks out of the for loop
                if int(octet) < 0 or int(octet) > 255:
                    print("\nOctet value must be between 0 and 255")
                    valid = False
                    break
            
            # Checks if valid is set to true. If not, it runs from the beginning of the loop again
            if valid:
                return ip_address


# This function is used to run the check for either wildcard mask or sunbet mask.
# It runs the check for the remaining elements in the list after the current element.
def mask_check(mask, index, subnet=False, wildcard=False):
    valid = True

    # The index value of the next element
    i = index + 1
    
    # If the index is <= 3 which is the highest index of the list
    if i <= 3:

        # While the index is less than 3, run the loop and increment the index by 1
        while i <= 3:

            # If the subnet argument is set to true
            if subnet:

                # If the value at index i is not 0, inform the user, set valid to false and break out of while loop
                if int(mask[i]) != 0:
                    print(f"Invalid subnet mask. Cannot have a non-zero after {int(mask[index])}")
                    valid = False
                    break
                # If the value at the current index is 0, increment i by 1, set valid to true and continue the while loop
                else:
                    i += 1
                    valid = True
                    continue

            # If the wildcard argument is set to true
            elif wildcard:

                # If the value at index i is not 255, inform the user, set valid to false and break out of while loop
                if int(mask[i]) != 255:
                    print(f"Cannot have a value that isn't 255 after {mask[index]}")
                    valid = False
                    break

                # If the value at the current index is 255, increment i by 1, set valid to true and continue the while loop
                else:
                    i += 1
                    valid = True
                    continue
    # This checks if the new index is 4 valis is True. New index can only be 4 if the current index is 3 (which is the index of the last element)
    elif i == 4:
        valid = True
    
    # Returns valid
    return valid



# This function checks if the user inputs an integer when requested to
def validate_input(prompt, expected_input=None, allow_int=False):

    if expected_input == None:
        expected_input = []

    # Loops till the user's input passes check
    while True:
        value = input(prompt).strip().upper()
        try:
            # If a digit is required and the user inputs a digit, return it
            if value.isdigit() and allow_int:
                return int(value)
            
            # If the user inputs an expected value, return it
            if value in expected_input:
                return value

            # Checks if an expected input and an integer is required and the user fails to provide a valid one of both
            if expected_input and allow_int:
                raise ValueError(f"\nInvalid input. Please enter one of {expected_input} or an integer.")
            
            # If an integer is requried and the user enters something other than an integer
            elif allow_int:
                raise ValueError("\nInvalid input. Please enter an integer.")
            
            # If only the expected input is required and the user enters something else
            elif expected_input:
                raise ValueError(f"\nInvalid input. Please enter one of {expected_input}.")

        except ValueError as ve:
            print(ve)


# This function is used to get the hostname of the device
def get_hostname(device):
    output = device.send_command("show start | include hostname").split()
    hostname = output[1]
    return hostname

# This function checks if the user requested to configure hosts that are available to be configured
def check_hosts(hostnames):
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
        return [True, host_to_configure]




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

