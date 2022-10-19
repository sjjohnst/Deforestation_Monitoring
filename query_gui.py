"""
Created on Thu Oct  6 15:53:12 2022

@author: Sam

Get the user's area of interest
"""

import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Polygon
from matplotlib.widgets  import RectangleSelector
import re
from sentinelsat import SentinelAPI
from datetime import date

simpledex = re.compile(r"\d*\.\d+")
def mround(match):
    return "{:.0f}".format(float(match.group()))


# Takes as input an area of interest, in WKT format, as well as last observed date
# Queries the copernicus hub for all intersection obervations ingested since
# last observation date
# TEMPORARY: Return all the geometries of retrieved images
def queryGRD(aoi, last_date):
    
    
    api = SentinelAPI("sjjohnst", "Atmosphere1806.")
    
    # Query copernicus
    products = api.query(aoi,
                             producttype='GRD',
                             platformname='Sentinel-1',
                             orbitdirection='DESCENDING',
                             date=(last_date, date.today()))
    
    # Convert to dataframe, and then sort by ingestion date
    products_df = api.to_dataframe(products)
    if products_df.empty is True:
        return []
    products_df = products_df.sort_values('ingestiondate', ascending=False)
    
    # Add in a column with rounded footprint values
    products_df['rounded_footprint'] = products_df.footprint.apply(lambda x: re.sub(simpledex, mround, x))
    
    # Now filter out all duplicate rounded footprints, keeping the first seen 
    # (which will have most recent date due to sort)
    products_df = products_df.drop_duplicates(subset=['rounded_footprint'], keep='first')
    
    # Finally return all the footprints
    return products_df.footprint


world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
brazil = world[world.name == "Brazil"]
# manaus = gpd.read_file('manaus.geojson')

fig, ax = plt.subplots()
world.plot(ax=ax)
brazil.plot(ax=ax, color='green')
# manaus.plot(ax=ax, color='yellow', alpha=0.5)

ax.set_xlim((-80, -30))
ax.set_ylim((-40, 10))

    
# Function to be executed after selection
def onselect_function(eclick, erelease):
   
    # Obtain (xmin, xmax, ymin, ymax) values
    # for rectangle selector box using extent attribute.
    extent = rect_selector.extents
    topleft = [extent[0], extent[2]]
    topright = [extent[1], extent[2]]
    botleft = [extent[0], extent[3]]
    botright = [extent[1], extent[3]]
    
    # print(rect_selector.geometry)
    
    poly = Polygon([topleft, topright, botright, botleft])
    # print(poly.wkt)
    
    products_footprint = queryGRD(poly.wkt, date(2022,9,1))
    print(len(products_footprint))
    gpd_footprints = gpd.GeoSeries.from_wkt([*products_footprint])
    gpd_query = gpd.GeoSeries.from_wkt([poly.wkt])
    gpd_footprints.boundary.plot(ax=ax, color='blue', alpha=0.3)
    gpd_query.plot(ax=ax, color='red', alpha=0.3)


rect_selector = RectangleSelector(
    ax, onselect_function, drawtype='box', button=[1])

plt.show()