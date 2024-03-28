"""Main module."""


import ipyleaflet
from ipyleaflet import Map, Marker, Polyline, LayersControl, TileLayer, basemaps

class AirplaneRouteMap(Map):
    def __init__(self, center=[20, 0], zoom=2, **kwargs):
        
        super().__init__(center=center, zoom=zoom, basemap=basemaps.NASAGIBS.ViirsEarthAtNight2012, **kwargs)
        self.routes = []  # Initialize an empty list to store routes
        self.add_control(LayersControl())  # Add layer control automatically

    def add_route(self, start, end, color="blue", weight=2):
        """
        Adds a route to the routes list. Routes will be drawn when draw_routes is called.
        
        Parameters:
            start (tuple): The starting point of the route as (latitude, longitude).
            end (tuple): The ending point of the route as (latitude, longitude).
            color (str): The color of the route line. Default is blue.
            weight (int): The thickness of the route line. Default is 2.
        """
        line = Polyline(locations=[start, end], color=color, fill=False, weight=weight)
        self.routes.append(line)
    
    def draw_routes(self):
        """
        Draws all routes stored in the routes list on the map.
        """
        for route in self.routes:
            self.add_layer(route)

    def add_marker(self, location, title=""):
        """
        Adds a marker to the map.
        
        Parameters:
            location (tuple): The location of the marker as (latitude, longitude).
            title (str): A tooltip title for the marker.
        """
        marker = Marker(location=location, draggable=False, title=title)
        self.add_layer(marker)

    def add_custom_tile_layer(self, url, name, attribution):
        """
        Adds a custom tile layer to the map.
        
        Parameters:
            url (str): The URL template for the tiles.
            name (str): The name of the layer.
            attribution (str): The attribution text for the layer.
        """
        layer = TileLayer(url=url, name=name, attribution=attribution)
        self.add_layer(layer)
