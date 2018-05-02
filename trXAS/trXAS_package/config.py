# -*- coding: utf-8 -*-
"""
Created on Wed Mar 28 16:52:45 2018
use: initializing global variables used in shift.py and main.py
@author: 2-310-GL group
"""
import os
#Enter manual  user inputsa. Should be in quotation marks.
openDirectory = os.path.normpath(os.pardir+ os.sep+ "test_data_bunchbybunch")
saveDirectory= os.path.normpath(os.pardir+os.sep+"test_saves")
column = "StS norm"
refColumn = "Y all norm"
firstBunch = "1"
lastBunch = "1"
photonEnergyStart = "all"
photonEnergyEnd= "all"
showSplines = False
showIntegrals = True
stepSize = 0.001 
#Initialize some values that are shared between the package files.
peaks = []
splines = []
refSplines = []
lines= []