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


