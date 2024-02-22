"""The common module contains common functions and classes used by the other modules.
"""

def hello_world():
    """Prints "Hello World!" to the console.
    """
    print("Hello World!")


import random

def random_number_in_range(start, end):
    return random.randint(start, end)
result = random_number_in_range(1, 10)
print(result)



def get_state_for_city(city):
    us_states = {
        "New York": "New York",
        "Los Angeles": "California",
        "Chicago": "Illinois",
        "Houston": "Texas",
        "Phoenix": "Arizona",
        "Nashville": "Tennessee",
        "Denver": "Colorado"
    }

    return us_states.get(city, "Unknown")


def get_and_print_city_state():
    city_name = input("Enter a city name: ")
    state_name = get_state_for_city(city_name)

    if state_name != "Unknown":
        print(f"The city of {city_name} is in the state of {state_name}.")
    else:
        print(f"Sorry, we don't have information for the city of {city_name}.")
