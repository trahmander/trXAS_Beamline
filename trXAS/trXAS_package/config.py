# -*- coding: utf-8 -*-
"""
Created on Wed Mar 28 16:52:45 2018
use: initializing global variables used in shift.py and main.py
@author: 2-310-GL group
"""
import os
###############################################################################
#Enter manual  user inputs.
###############################################################################
#OpenDirectory is the name of the directory for your scans.
#SaveDirectory is the name of the directory to save the averages in.
openDirectory = os.path.normpath(os.pardir+ os.sep+ "CuO_O_K-edge_532nm_14pc")
saveDirectory= os.path.normpath(os.pardir+os.sep+"test_saves")
#column specifies the name of the column that you want to plot as a function of photon energy.
#refColumn specifies the name of the column that you want to compare in order to determine the shifts
column = ["StS norm"]
transColumn = "StS norm"
refColumn = "Y all norm"
#firstBunch determines the the earliest bunch before the pump to average. (Inclusive) 
#lastBunch determines the latest bunch after the pump to average. (Inclusive)
# These numbers can be negative. ie: Bunch -6 is the 6th bunch before the pump
# and Bunch 1 is the pump. (There is no 0th Bunch). Choose "all" to select all 
# bunches in your directory. If you only want to look at 1 bunch. Choose that for 
# for both values. ie: firstBunch = "7", lastBunch = "7" would look at just the 
# 7th bunch after time 0.
firstBunch = "all"
lastBunch = "all"
#These are the different options for the shifting method. Exactly one should be True.
#ShiftNone means that that the spectra will remain unchanged. This is good for making
#   initial guesses for peakFindStart and peakFindEnd 
#Shift peak, matches the maximum in the range specified by peakFindStart and peakFindEnd.
#shiftCenter matches the geometric center of the curves.
#shiftMinimize tries to minimize the difference in the spectra as a function of the shift.
shiftNone = False
shiftPeak = False
shiftCenter = False
shiftMinimize = True
#peakFindStart is the smaller energy in the window used to find peaks for shifting.
#peakFindEnd is the larger energy in the window used to find peaks for shifting.
#Choose "all" to integrate on the entire photon energy axis. 
peakFindStart = "533"
peakFindEnd= "537"
#photonEnergyStart is the smaller energy in the window to do an integration.
#photonEnergyEnd os the larger energy in the window to do an integration.
#Choose "all" to integrate on the entire photon energy axis. 
photonEnergyStart = "535.0"
photonEnergyEnd= "535.9"
#saveSplines is set to True if you want to calculate to save the shifted Splines.
#showSplines is set to True if you want the plots for the column you set in column.
#saveTransients is set to True if you want calculate the transients for transColumn.
#showTransients is set to True if you want the plots for the integrals for transColumn.
saveSplines = False
showSplines = False
saveTransients = True
showTransients = True
phaseShifter = False
#stepSize determines how coarse the splining of your data is. Smaller stepSize is more expensive.
#offSet is how much time in nano seconds that t0 is after the reference bunch. 
#Example: if t0 is 150ps before the first bunch then offset would be 2  - 0.15 = 1.85
offSet= 1.85
stepSize = 0.005
############################################################################### 
###############################################################################
#Initialize some values that are shared between the package files. It's best to
# keep these lists clear. (They should just be empty brackets).
###############################################################################
#peaks = []
splines = []
lines= []
###############################################################################