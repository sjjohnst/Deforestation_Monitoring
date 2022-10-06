"""
Created on Thu Oct  6 15:53:12 2022

@author: Sam

Get the user's area of interest
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets  import RectangleSelector


xdata = np.linspace(0,9*np.pi, num=301)
ydata = np.sin(xdata)

fig, ax = plt.subplots()
line, = ax.plot(xdata, ydata)


def line_select_callback(eclick, erelease):
    x1, y1 = eclick.xdata, eclick.ydata
    x2, y2 = erelease.xdata, erelease.ydata

    rect = plt.Rectangle( (min(x1,x2),min(y1,y2)), np.abs(x1-x2), np.abs(y1-y2) )
    ax.add_patch(rect)


rs = RectangleSelector(ax, line_select_callback,
                       useblit=False, button=[1], 
                       minspanx=5, minspany=5, spancoords='pixels', 
                       interactive=True)



plt.show()