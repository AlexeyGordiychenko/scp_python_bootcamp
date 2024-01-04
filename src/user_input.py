def user_input(prompt, min_value, max_value):
    """
    Takes user input, checks if it is within a specified range, and returns the
    value.

    :parameters:
        prompt (str): The prompt to display to the user.
        min_value (int): The minimum allowed value.
        max_value (int): The maximum allowed value.

    :returns:
        int: The user input value.
    """
    while True:
        try:
            value = int(input(f"{prompt}: "))
            if min_value <= value <= max_value:
                return value
            else:
                print(
                    f"Error! Please enter a natural number between {min_value} and {max_value}.")
        except ValueError:
            print("Error! Please enter a natural number.")
