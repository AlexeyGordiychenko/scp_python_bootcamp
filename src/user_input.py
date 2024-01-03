def user_input(prompt, min_value, max_value):
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
