# -*- coding: utf-8 -*-
"""
Created on Fri Oct 14 12:12:28 2022

@author: Sam

Functions that handle queries to Copernicus data store, as well as associated
processing of results (filtering).
"""

from sentinelsat import SentinelAPI, read_geojson, geojson_towkt
import geopandas as gpd
import shapely
from datetime import date
import re


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
                             date=(last_date, date.today()))
    
    # Convert to dataframe, and then sort by ingestion date
    products_df = api.to_dataframe(products)
    products_df = products_df.sort_values('ingestiondate', ascending=False)
    
    # Add in a column with rounded footprint values
    products_df['rounded_footprint'] = products_df.footprint.apply(lambda x: re.sub(simpledex, mround, x))
    
    # Now filter out all duplicate rounded footprints, keeping the first seen 
    # (which will have most recent date due to sort)
    products_df = products_df.drop_duplicates(subset=['rounded_footprint'], keep='first')
    
    # Finally return all the footprints
    return products_df.footprint
