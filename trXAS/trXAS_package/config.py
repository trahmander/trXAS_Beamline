# -*- coding: utf-8 -*-
"""
Created on Wed Mar 28 16:52:45 2018
use: initializing global variables used in shift.py and main.py
@author: 2-310-GL group
"""
import os
#Enter manual  user inputsa. Should be in quotation marks.
openDirectory = os.path.normpath(os.pardir+ os.sep+ "test_data")
saveDirectory= os.path.normpath(os.pardir+os.sep+"test_data_processed")
column = "StS norm"
firstBunch = "all"
lastBunch = "all"
photonEnergyStart = "532.5"
photonEnergyEnd= "535.0"
showPlots = True
stepSize = 0.001 
#Initialize some values that are shared between the package files.
peaks = []
splines = []
lines= []
             
