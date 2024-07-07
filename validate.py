# This function is used to validate and return a DDN number entered by a user.
def get_valid_ddn(prompt):
    
    # This loop validates the router ID entered by the user
    while True:
        ddn_number = input(prompt)

        # Splits each octet in the router ID and stores it as an element in a list
        ddn_check = ddn_number.split(sep='.')
        
        # Checks if the length of the values entered in the list is equal to 4.
        # If not, it prompts the user and goes to the beginning of the loop
        if len(ddn_check) != 4:
            print("\nMust be 4 DDN separated values")
            continue

        # Checks if the first octet is a 0. If it is, it prompts the user and goes to the beginning of the loop
        if ddn_check[0] == '0':
            print("\nCannot start with a zero")
            continue
        
        valid = True

        # Loops through the elements in the list
        for octet in ddn_check:
            
            # Checks if an octet is not a digit. If not, it sets Valid to False and breaks out of the for loop
            if not octet.isdigit():
                print("\nCannot have a non digit")
                valid = False
                break

            # Checks if the value of an octet is between 0 and 255. If not, it sets Valid to False and breaks out of the for loop
            if int(octet) < 0 or int(octet) > 255:
                print("\nOctet value must be between 0 and 255")
                valid = False
                break
        
        # Checks if valid is set to true. If not, it runs from the beginning of the loop again
        if valid:
            return ddn_number

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
