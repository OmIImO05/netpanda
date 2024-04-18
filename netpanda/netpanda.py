"""Main module."""

from turtle import position
import ipyleaflet
from ipyleaflet import Map, Polyline, Marker, TileLayer, LayersControl, basemaps
from ipyleaflet import Map, WidgetControl, basemaps
import ipywidgets as widgets
from panel import widget
import shapefile
import json
import geopandas as gpd
from ipyleaflet import GeoData
from shapely.geometry import Point, LineString

class Map(ipyleaflet.Map):
    def __init__(self, center=[20, 0], zoom=2, **kwargs):
        super().__init__(center=center, zoom=zoom, **kwargs)

        self.default_basemap = basemaps.OpenStreetMap.Mapnik
        self.add_layer(self.default_basemap)

        # Keep track of the current basemap layer
        self.current_basemap_layer = self.default_basemap

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
        
        
    def add_vector(self, data, name="vector_layer", **kwargs):
        """
        Add vector data to the map.

        Args:
        data (str or geopandas.GeoDataFrame): The vector data to add. This can be a file path or a GeoDataFrame.
        name (str, optional): The name of the vector layer. Defaults to "vector_layer".
        **kwargs: Additional keyword arguments for the vector layer.
        """
        import geopandas as gpd
        from ipyleaflet import Map, GeoData

        if isinstance(data, gpd.GeoDataFrame):
         geo_data = GeoData(geo_dataframe=data, name=name, **kwargs)
        elif isinstance(data, str):
         geo_data = GeoData(geo_dataframe=gpd.read_file(data), name=name, **kwargs)
        else:
            raise ValueError("Unsupported data format. Please provide a GeoDataFrame or a file path.")

    # Add the GeoData object to the map
        self.add_layer(geo_data)


    def add_image(self, url, bounds, name="image", **kwargs):
        """Adds an image overlay to the map.

        Args:
        url (str): The URL of the image.
        bounds (list): The bounds of the image.
        name (str, optional): The name of the layer. Defaults to "image".
        """
        layer = ipyleaflet.ImageOverlay(url=url, bounds=bounds, name=name, **kwargs)
        self.add_layer(layer)

    def add_raster(self, data, name="raster", zoom_to_layer=True, **kwargs):
        """Adds a raster layer to the map.

        Args:
        data (str): The path to the raster file.
        name (str, optional): The name of the layer. Defaults to "raster".
        """

        try:
           from localtileserver import TileClient, get_leaflet_tile_layer
        except ImportError:
           raise ImportError("Please install the localtileserver package.")

        client = TileClient(data)
        layer = get_leaflet_tile_layer(client, name=name, **kwargs)
        self.add_layer(layer)

        if zoom_to_layer:
           self.center = client.center()
           self.zoom = client.default_zoom

    def add_widget(self, widget, position="topright"):
        """Adds a widget to the map.

        Args:
        widget (object): The widget to be added.
        position (str, optional): The position of the widget. Defaults to "topright".
        """
        control = ipyleaflet.WidgetControl(widget=widget, position=position)
        self.add_control(control)

    def add_zoom_slider(
        self, description="Zoom level", min=0, max=24, value=10, position="topright"
    ):
        """Adds a zoom slider to the map.

        Args:
            position (str, optional): The position of the zoom slider. Defaults to "topright".
        """
        zoom_slider = widgets.IntSlider(
            description=description, min=min, max=max, value=value
        )

        control = ipyleaflet.WidgetControl(widget=zoom_slider, position=position)
        self.add(control)
        widgets.jslink((zoom_slider, "value"), (self, "zoom"))
 
    def add_opacity_slider(
            self, layer_index=-1, description="Opacity:", position="topright"
    ):
        """Adds an opacity slider for the specified layer.

        Args:
            layer (object): The layer for which to add the opacity slider.
            description (str, optional): The description of the opacity slider. Defaults to "Opacity:".
            position (str, optional): The position of the opacity slider. Defaults to "topright".

        Returns:
            None
        """
        layer = self.layers[layer_index]
        opacity_slider = widgets.FloatSlider(
            description=description, min=0, max=1, value=layer.opacity, style={"description_width": "initial"}
        )

        def update_opacity(change):
            """
            Updates the opacity of a layer based on the new value from a slider.

            This function is designed to be used as a callback for an ipywidgets slider. 
            It takes a dictionary with a "new" key representing the new value of the slider, 
            and sets the opacity of a global layer variable to this new value.

            Args:
            change (dict): A dictionary with a "new" key representing the new value of the slider.

            Returns:
                None
            """
            layer.opacity = change["new"]
            
        opacity_slider.observe(update_opacity, "value")
        
        control = ipyleaflet.WidgetControl(widget=opacity_slider, position=position)
        self.add(control)


    from ipyleaflet import TileLayer, basemaps

    def add_basemap(self, basemap_name):

        print("Trying to add new basemap:", basemap_name) 
        basemap_layer_def = getattr(basemaps, basemap_name, None)
   
        if basemap_layer_def is not None:
            new_basemap_layer = TileLayer(url=basemap_layer_def['url'], attribution=basemap_layer_def['attribution'])
            if hasattr(self, 'current_basemap_layer'):
                self.remove_layer(self.current_basemap_layer)
            self.current_basemap_layer = new_basemap_layer
            self.add_layer(new_basemap_layer)
            print("New basemap added:", basemap_name)  
        else:
            print("No basemap found with name:", basemap_name) 


    from ipywidgets import Dropdown, Button, HBox
    
    def add_basemap_gui(self, position="topright"):
        """Adds a basemap GUI to the map.

        Args:
            position (str, optional): The position of the basemap GUI. Defaults to "topright".

        Returns:
            None
        """
        basemap_selector = widgets.Dropdown(
            options=[
                ("OpenStreetMap", basemaps.OpenStreetMap.Mapnik),
                ("OpenTopoMap", "OpenTopoMap"),
                ("Esri.WorldImagery",  "Esri.WorldImagery"),
                ("CartoDB.DarkMatter", "CartoDB.DarkMatter"),
            ],
            value=self.default_basemap,
            description="Basemaps",
        )

        close_button = widgets.Button(
            icon='times', 
            layout={'width': '35px'}  
        )

        def on_basemap_change(change):
               new_basemap_name = change['new']  # Get the name of the new basemap from the change event.
               self.add_basemap(new_basemap_name)



        #def on_basemap_change(change):
            #print("Basemap change detected:", change)  # For debugging
            #new_basemap = next((item[1] for item in basemap_selector.options if item[0] == change['new']), None)
            #if new_basemap:
               #self.add_basemap(new_basemap)



        close_button = widgets.Button(
            description='Close',
            button_style='danger',        
        )


        def on_close_button_clicked(button):
            """
            Handles the event of clicking the close button on a control.

            This function is designed to be used as a callback for a button click event. 
            It takes a button instance as an argument, and calls the remove method 
            to remove a global control variable from the map.

            Args:
             button (ipywidgets.Button): The button that was clicked.

            Returns:
            None
            """

            self.remove_control(control)

        close_button.on_click(on_close_button_clicked)
        basemap_selector.observe(on_basemap_change, names='value')
        widget_box = widgets.HBox([basemap_selector, close_button])
        control = WidgetControl(widget=widget_box, position=position)
        self.add_control(control)


    def add_toolbar(self, position="topright"):
        """Adds a toolbar to the map.

        Args:
            position (str, optional): The position of the toolbar. Defaults to "topright".
        """

        padding = "0px 0px 0px 5px"  # upper, right, bottom, left

        toolbar_button = widgets.ToggleButton(
            value=False,
            tooltip="Toolbar",
            icon="wrench",
            layout=widgets.Layout(width="28px", height="28px", padding=padding),
        )

        close_button = widgets.ToggleButton(
            value=False,
            tooltip="Close the tool",
            icon="times",
            button_style="primary",
            layout=widgets.Layout(height="28px", width="28px", padding=padding),
        )

        toolbar = widgets.VBox([toolbar_button])

        def close_click(change):
            if change["new"]:
                toolbar_button.close()
                close_button.close()
                toolbar.close()

        close_button.observe(close_click, "value")

        rows = 2
        cols = 2
        grid = widgets.GridspecLayout(
            rows, cols, grid_gap="0px", layout=widgets.Layout(width="65px")
        )

        icons = ["folder-open", "map", "info", "question"]

        for i in range(rows):
            for j in range(cols):
                grid[i, j] = widgets.Button(
                    description="",
                    button_style="primary",
                    icon=icons[i * rows + j],
                    layout=widgets.Layout(width="28px", padding="0px"),
                )

        def toolbar_click(change):
            if change["new"]:
                toolbar.children = [widgets.HBox([close_button, toolbar_button]), grid]
            else:
                toolbar.children = [toolbar_button]

        toolbar_button.observe(toolbar_click, "value")
        toolbar_ctrl = WidgetControl(widget=toolbar, position="topright")
        self.add(toolbar_ctrl)

        output = widgets.Output()
        output_control = WidgetControl(widget=output, position="bottomright")
        self.add(output_control)

        def toolbar_callback(change):
            if change.icon == "folder-open":
                with output:
                    output.clear_output()
                    print(f"You can open a file")
            elif change.icon == "map":
                with output:
                    output.clear_output()
                    print(f"You can add a layer")
            else:
                with output:
                    output.clear_output()
                    print(f"Icon: {change.icon}")

        for tool in grid.children:
            tool.on_click(toolbar_callback)