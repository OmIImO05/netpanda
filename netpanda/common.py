"""The common module contains common functions and classes used by the other modules.
"""

def hello_world():
    """Prints "Hello World!" to the console.
    """
    print("Hello World!")


from geopy.geocoders import Nominatim

def get_coordinates(city, state):
    geolocator = Nominatim(user_agent="my_geocoder")
    location = geolocator.geocode(f"{city}, {state}")
    if location:
        return location.latitude, location.longitude
    else:
        return None

# Example usage for cities in Tennessee
cities_in_tennessee = ["Nashville", "Memphis", "Knoxville", "Chattanooga", "Clarksville"]

for city in cities_in_tennessee:
    coordinates = get_coordinates(city, "Tennessee")
    
    if coordinates:
        lat, lon = coordinates
        print(f"{city}: Latitude {lat}, Longitude {lon}")
    else:
        print(f"Could not retrieve coordinates for {city}")

