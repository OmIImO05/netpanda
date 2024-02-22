"""The common module contains common functions and classes used by the other modules.
"""

def hello_world():
    """Prints "Hello World!" to the console.
    """
    print("Hello World!")



def get_state_for_city(city):
    us_states = {
        "New York": "New York",
        "Los Angeles": "California",
        "Chicago": "Illinois",
        "Houston": "Texas",
        "Phoenix": "Arizona",
        "Nashville": "Tennessee",
        "Little Rock": "Arkansas",
        "Oklahoma City": "Oklahoma",
        "Indianapolis": "Indiana",
        "Columbus": "Ohio",
        "Denver": "Colorado"

    }

    return us_states.get(city, "Unknown")

def main():
    # Ask the user to input a city name
    city_name = input("Enter a city name: ")

    # Get the corresponding state
    state_name = get_state_for_city(city_name)

    # Display the result
    if state_name != "Unknown":
        print(f"The city of {city_name} is in the state of {state_name}.")
    else:
        print(f"Sorry, we don't have information for the city of {city_name}.")

if __name__ == "__main__":
    main()


