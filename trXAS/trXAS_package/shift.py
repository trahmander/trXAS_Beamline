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
#from config import refSplines
from config import (lines, 
                    stepSize,
                    peakFindStart,
                    peakFindEnd)
###############################################################################
#finds the x-value of the peak specified around xlow and xhigh. Appends it to peaks.
def find_peak(xlow, xhigh, func):
    step = (xhigh - xlow) / stepSize
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
def get_spline(low, high, x, refY, y):
    step = (high - low) / stepSize
    line = np.linspace(low, high, step)
    refSpline = itp.interp1d(x, refY, kind='slinear')                                   #This one does linear interpolation. kinda ugly
    spline = itp.interp1d(x, y, kind = 'slinear')
    lines.append(line)
#    refSplines.append(refSpline)
    splines.append(spline)
    return refSpline
#unpacks the 2d array into 1d arrays given by the columns. uses find_peak and get_spline.
def photonE_counts_plot(dataSet, refCol, col, file):
    photonE = []
    dataSet = dataSet.T
    try:
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
        refVals = columns[refCol]
        vals = columns[col]
#        step = (highE - lowE) / stepSize
        splinE = get_spline(lowE, highE, photonE, refVals, vals)
        find_peak(peakFindStart, peakFindEnd, splinE)                                       #should not be hardcoded.
    except:
        print("Didn't load to array:\t"+file)             
    return photonE
#shifts all peaks to match the earleast peak. returns new splines. cuts the spline at the  high energy side.
def shift_spline(splineNum, refPeaks, spline, line):
#    yVals = ySpline[splineNum]( line[splineNum] )
    vals = spline[splineNum]( line[splineNum] )
    ref = np.amin( refPeaks )
    
    if np.abs(ref - refPeaks[splineNum]) < stepSize:
        return vals, line[splineNum]
    else:
        delta = peaks[splineNum] - ref
        index = int ( delta / stepSize )
        for i in range (len(vals) - index ) :
            vals[i] = vals[i+index]
        return vals[:-index], line[splineNum][:-index]

###############################################################################
#Test Functions for shift.py
###############################################################################
def test_shift():
    return
###############################################################################
if __name__ == "__main__":
    test_shift()