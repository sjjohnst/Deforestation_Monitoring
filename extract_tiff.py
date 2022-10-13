# -*- coding: utf-8 -*-
"""
Created on Thu Oct 13 11:14:12 2022

@author: Sam

Extract the Sentinel-1 data from within zip archive.
Finds the zip archive with name f
Extracts all tiff images from within the archive, but nothing else
Stores them in directory named f -> Should be changed to destination directory
"""

import zipfile

f = "S1A_IW_GRDH_1SDV_20220803T092329_20220803T092354_044386_054C05_85AD.zip"

with zipfile.ZipFile(f) as zf:
    names = zf.namelist()
    tiffs = [file for file in names if ".tiff" in file]
    # ADD: Check if previously extracted?
    for tiff in tiffs:
        zf.extract(tiff)
