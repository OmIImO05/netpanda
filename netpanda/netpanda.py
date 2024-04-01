"""Main module."""

import ipyleaflet
from ipyleaflet import Map, Polyline, Marker, TileLayer, LayersControl, basemaps
import shapefile
import json

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
            weight (int): The thickness of the route line. Default is saved 2.
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

    def add_basemap_viirs_earth_at_night(self):
        """
        Adds NASAGIBS.ViirsEarthAtNight2012 basemap to the current map.
        """
        basemap_url = basemaps.NASAGIBS.ViirsEarthAtNight2012.build_url()
        attribution = "Tiles by NASA Earth Observations (NEO). Data by NGDC, NASA, UMD, NGA, NOAA, USGS, NPS, Census"
        self.add_custom_tile_layer(basemap_url, "Viirs Earth At Night 2012", attribution)


    def add_geojson(self, data, name="geojson", **kwargs):
        """
        Adds a GeoJSON layer to the map.

        Args:
            data (str | dict): The GeoJSON data as a string, a dictionary, or an HTTP URL.
            name (str, optional): The name of the layer. Defaults to "geojson".
        """
        # Check if the data is a URL
        if data.startswith("http"):
            # If it's a URL, fetch the GeoJSON data from the URL
            response = requests.get(data)
            data = response.json()
        # If data is a string, assume it's a local file path
        elif isinstance(data, str):
            # If it's a local file path, open and read the GeoJSON file
            with open(data) as f:
                data = json.load(f)

        if "style" not in kwargs:
            kwargs["style"] = {"color": "yellow", "weight": 1, "fillOpacity": 0}

        if "hover_style" not in kwargs:
            kwargs["hover_style"] = {"fillColor": "#00FFFF", "fillOpacity": 0.5}

        # Add GeoJSON layer with provided name and additional keyword arguments
        layer = ipyleaflet.GeoJSON(data=data, name=name, **kwargs)
        self.add_layer(layer)

        
    def add_shp(self, data, name="shp", **kwargs):
        """
        Adds a shapefile to the current map.

        Args:
            data (str or dict): The path to the shapefile as a string or an HTTP URL to a shapefile in a zip file.
            name (str, optional): The name of the layer. Defaults to "shp".
            **kwargs: Arbitrary keyword arguments.

        Raises:
            TypeError: If the data is neither a string nor an HTTP URL to a shapefile in a zip file.

        Returns:
            None
        """
        
        # Check if the data is an HTTP URL
        if data.startswith("http"):
            # If it's an HTTP URL, fetch the zip file
            response = requests.get(data)
            with zipfile.ZipFile(io.BytesIO(response.content), 'r') as z:
                # Extract the shapefile contents from the zip file
                shp_files = [name for name in z.namelist() if name.endswith('.shp')]
                if len(shp_files) == 0:
                    raise ValueError("No shapefile (.shp) found in the zip file.")
                shp_filename = shp_files[0]  # Assuming there's only one shapefile in the zip file
                with z.open(shp_filename) as shp_file:
                    # Convert the shapefile contents to GeoJSON format
                    shp_reader = shapefile.Reader(shp_file)
                    data = shp_reader.__geo_interface__
    
        elif isinstance(data, str):
            # If it's a local file path, open and read the shapefile
            with shapefile.Reader(data) as shp:
                data = shp.__geo_interface__
        else:
            raise TypeError("Data must be a string representing a file path or an HTTP URL to a shapefile in a zip file.")

        # Add GeoJSON layer with provided name and additional keyword arguments
