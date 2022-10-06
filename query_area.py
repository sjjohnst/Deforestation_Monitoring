"""
Created on Thu Oct  6 15:53:12 2022

@author: Sam

Get the user's area of interest
"""

import folium
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    start_coords = (-14.235004, -51.92528)
    folium_map = folium.Map(location=start_coords, zoom_start=5)
    return folium_map._repr_html_()


if __name__ == '__main__':
    app.run(debug=False)