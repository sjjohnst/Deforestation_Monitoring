"""
Created on Thu Oct  6 15:53:12 2022

@author: Sam

Get the user's area of interest
"""

import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets  import RectangleSelector

world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
brazil = world[world.name == "Brazil"]
# manaus = gpd.read_file('manaus.geojson')

fig, ax = plt.subplots()
world.plot(ax=ax)
brazil.plot(ax=ax, color='green')
# manaus.plot(ax=ax, color='yellow', alpha=0.5)

ax.set_xlim((-80, -30))
ax.set_ylim((-40, 10))

def line_select_callback(eclick, erelease):
    x1, y1 = eclick.xdata, eclick.ydata
    x2, y2 = erelease.xdata, erelease.ydata

    rect = plt.Rectangle( (min(x1,x2),min(y1,y2)), np.abs(x1-x2), np.abs(y1-y2) )
    ax.add_patch(rect)
    
# Function to be executed after selection
def onselect_function(eclick, erelease):
   
    # Obtain (xmin, xmax, ymin, ymax) values
    # for rectangle selector box using extent attribute.
    extent = rect_selector.extents
    print("Extents: ", extent)
 
    # Zoom the selected part
    # Set xlim range for plot as xmin to xmax
    # of rectangle selector box.
    # plt.xlim(extent[0], extent[1])
     
    # Set ylim range for plot as ymin to ymax
    # of rectangle selector box.
    # plt.ylim(extent[2], extent[3])


# rs = RectangleSelector(ax, line_select_callback,
#                        useblit=False, button=[1], 
#                        minspanx=5, minspany=5, spancoords='pixels', 
#                        interactive=True)

rect_selector = RectangleSelector(
    ax, onselect_function, drawtype='box', button=[1])

plt.show()