# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 13:48:38 2018
use: load the chosen files into arrays, create linear splines and shift peaks to match.
@author: 2-310-GL group
"""
###############################################################################
#Import modules
###############################################################################
# built in modules
import sys
import numpy as np
from matplotlib import pyplot as plt
import scipy.interpolate as itp
#import global variables.
from config import peaks
from config import splines
from config import lines 
from config import stepSize
###############################################################################
#finds the x-value of the peak specified around xlow and xhigh. Appends it to peaks.

class shift_lists:
    def __init__(self):
        self.__peaks = []
        self.__splines = []
        self.__lines = []
    def get_peaks(self):
        return self.__peaks
    def get_splines(self):
        return self.__splines
    def get_lines(self):
        return self.__lines

    def set_peaks(self, peaks):
        self.__peaks = peaks
        return
    def set_splines(self, splines):
        self.__splines = splines
        return
    def set_lines(self, lines):
        self.__lines = lines
        return    

def find_peak(xlow, xhigh, step, func):
    nearPeak = np.linspace(xhigh, xlow, step)
    feature = func(nearPeak)
    maxVal = feature[0]  
    peak = 0
    for i in range( len(feature) ):
        if feature[i] > maxVal:
            maxVal = feature[i]
            peak = i
    peaks.append(nearPeak[peak])
    return 
#Interpolation of data. returns linear spline Appends it to splines
def get_spline(low, high, step, x, y):
    line = np.linspace(low, high, step)
    spline = itp.interp1d(x, y, kind='slinear')                                   #This one does linear interpolation. kinda ugly
    lines.append(line)
    splines.append(spline)
    return line, spline
#unpacks the 2d array into 1d arrays given by the columns. uses find_peak and get_spline.
def photonE_counts_plot(dataSet, col, file):
    dataSet = dataSet.T
    columns = (photonE, #SEphotonE,
        xRefNorm, #SExRefNorm,
        xRef, #SExRef,
        xPumpNorm, #SExPumpNorm, 
        xPump, #SExPump,
        yRefNorm, #SEyRefNorm,
        yRef, #SEyRef,
        yPumpNorm, #SEyPumpNorm,
        yPump, #SEyPump,
        xAllNorm, #SExAllNorm,
        xAll, #SExAll,
        yAllNorm, #SEyAllNorm,
        yAll, #SEyAll,
        xAllyRefNorm, #SExAllyRefNorm,
        xAllyRef, #SExAllyRef,
        yAllxRefNorm, #SEyAllxRefNorm, 
        yAllxRef, #SEyAllxRef,
        BCxHistNorm, #SEBCxHistNorm, 
        BCyHistNorm, #SEBCyHistNorm,
        stsNorm, #SEstsNorm,
        BCSCNorm, #SEBCSCNorm, 
        BCLRNorm, #SEBCLRNorm,
        BCxHist, #SEBCxHist,
        BCyHist, #SEBCyHist,
        sts, #SEsts,
        BCSC, #SEBCSC, 
        BCLR, #SEBCLR,
        #SE, #SE2
        ) = dataSet
    lowE = photonE[0]
    highE = photonE[-1]
    vals = columns[col]
    step = (highE - lowE) / stepSize
    linE, splinE = get_spline(lowE, highE, step, photonE, vals)
    find_peak(532, 537, step, splinE)             
    return
#shifts all peaks to match the earleast peak. returns new splines. cuts the spline at the right side.
def shift_spline(splineNum, pks, spln, lin):
    vals = spln[splineNum]( lin[splineNum] )
    ref = np.amin( pks )
    
    if np.abs(ref - pks[splineNum]) < stepSize:
        return vals, lin[splineNum]
    else:
        delta = pks[splineNum] - ref
        index = int ( delta / stepSize )
        for i in range (len(vals) - index ) :
            vals[i] = vals[i+index]
        return vals[:-index], lin[splineNum][:-index]

###############################################################################
#Test Functions for shift.py
###############################################################################
def test_shift():
    return
###############################################################################
if __name__ == "__main__":
    test_shift()