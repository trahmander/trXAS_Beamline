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
#OpenDirectory is the name of the directory for your scans. os.pardir means
# parent directory of this file. os.sep is the "/" in linux and "\" in windows
openDirectory = os.path.normpath(os.pardir+ os.sep+ "PS_CuO_O_K-edge_nm_26pc")
#column is a list which specifies the names of the columns that the script will
#   plot if showSpline is set to True.
#transColumn references the column that the software uses to calculate transients.
#refColumn specifies the name of the column that you want to compare in order to determine the shifts
#psColumn is the column that the software looks at for phase shifter scans.
column = ["Y all norm","StS norm"]
transColumn = "StS norm"
psColumn = "StS"
refColumn = "Y all norm"
#firstBunch and lastBunch determine the earliest and latest bunches to to work with) 
#lastBunch determines the latest bunch after the pump to average. (Inclusive)
# These numbers can be negative. ie: Bunch -6 is the 6th bunch before the pump
# and Bunch 1 is the first after the pump. (There is no 0th Bunch). 
#Choose "all" to select all  bunches in your directory. If you only want to 
# look at 1 bunch. Choose that for first and last.
#averageStart and averageEnd are for averaging different bunches together. This
# must be within the range specified by firstBunch and lastBunch.
#averageBinning is the binning for avereging different bunches together.
# a binning of 2 will mean that every two consecutive bunches will be averaged.
firstBunch = "all"
lastBunch = "all"
averageStart= "1"
averageEnd = "3"
averageBinning="3"
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
#peakFindEnd is the larger energy in the window used to find pseaks for shifting.
#If the peak find window is not contained in the axis generated by the splines
# a value error will be returned.
#Choose "all" to find maximum on the entire photon energy axis. 
peakFindStart = "533" 
peakFindEnd= "537" 
#photonEnergyStart is the smaller energy in the window to do an integration.
#photonEnergyEnd os the larger energy in the window to do an integration.
#Choose "all" to integrate on the entire photon energy axis.
#integrationWindow sets the size of the box to look for zero crossings for the
# integration bounds. 
photonEnergyStart = "528.5" #aliased as xLow in main
photonEnergyEnd= "529.9" #aliased as xHigh in main
integrationWindow = 1.0
#saveSplines is set to True if you want to save the files for individual bunches.
#showSplines is set to True if you want the plots for the column you set in column.
#saveAverage is set to True if you want to save files with different bunches averaged together.
#saveOriginalX is set to True if you want to save files with the original x values
#saveTransients is set to True if you want calculate the transients for transColumn.
#savePhaseShifter is set to True if you want to calculate transients based on phase shifter scans.
#showTransients is set to True if you want the plots for the integrals for transColumn.
saveSplines = False
showSplines = False
saveAverage = False
saveOriginalX = False
saveTransients = False
savePhaseShifter = True
showTransients = True
#literaturePeakValue is a nominal value to shift the reference peak to.
#   set this to 0 if you don't want to shift to this value.
#stepSize determines how coarse the splining of your data is. Smaller stepSize is more expensive.
#offSet is how much time in nano seconds that t0 is before the first pump bunch.
literaturePeakValue = 530.1
offSet= 0.15
stepSize = 0.005
############################################################################### 
###############################################################################
#Initialize some values that are shared between the package files. It's best to
# keep these lists clear. (They should just be empty square brackets).
#splines keeps a list of all the linear interpolations for every bunch and scan.
#lines keeps a list of all the fine x-axis. Where the coarseness is determined by
# stepsize.
#xOrig stores the original photon energy values from these scans and bunches. 
#The jth x-axis of lines corresponds to the jth interpolation of splines and the 
# jth original x-axis in xOrig. If there are n bunches and m scans, then each of
# these lists has size n*m. So the lines and xOrig lists are somewhat redundant.
###############################################################################
splines = []
lines= []
xOrig= []
###############################################################################