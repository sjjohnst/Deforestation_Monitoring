"""
Created on Thu Oct  6 15:53:12 2022

@author: Sam

Get the user's area of interest
"""

import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Polygon
from matplotlib.widgets  import RectangleSelector
from datetime import date
from query_sentinelsat import queryGRD


fig = plt.figure()
ax = fig.add_subplot(1,1,1)

ax.set_xlim((-80, -30))
ax.set_ylim((-40, 10))

world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
brazil = world[world.name == "Brazil"]

world.plot(ax=ax)
brazil.plot(ax=ax, color='green')

# Function to be executed after selection
def onselect_function(eclick, erelease):
    pass


# Driver function for handling MPL events
def show_footprint(event):
    # print("Key Pressed")
    if event.key == 't': 
        # Query copernicus for data and then display footprints found
        
        print("Query Copernicus")
        # Obtain (xmin, xmax, ymin, ymax) values
        # for rectangle selector box using extent attribute.
        extent = rect_selector.extents
        topleft = [extent[0], extent[2]]
        topright = [extent[1], extent[2]]
        botleft = [extent[0], extent[3]]
        botright = [extent[1], extent[3]]
        
        query_area = Polygon([topleft, topright, botright, botleft])   
        products_footprint = queryGRD(query_area.wkt, date(2022,9,1))
        # print(query_area, len(products_footprint))
        
        print("Display Footprints")
        gpd_footprints = gpd.GeoSeries.from_wkt([*products_footprint])
        gpd_query = gpd.GeoSeries.from_wkt([query_area.wkt])
        gpd_footprints.boundary.plot(ax=ax, color='blue', alpha=0.3)
        gpd_query.plot(ax=ax, color='red', alpha=0.3)
    

rect_selector = RectangleSelector(
    ax, onselect_function, button=[1], interactive=True)

fig.canvas.mpl_connect('key_press_event', show_footprint)

plt.show()