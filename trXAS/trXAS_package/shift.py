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
from config import rawVals
from config import rawPhotonE
from config import stepSize

#finds the x-value of the peak specified around xlow and xhigh. Appends it to peaks.
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
    return nearPeak[peak]
#Interpolation of data. returns linear spline Appends it to splines
def get_spline(low, high, step, x, y):
    line = np.linspace(low, high, step)
#    splinE = itp.UnivariateSpline(photonE, yAllNorm, s=None, k=2)
#    splinE = itp.InterpolatedUnivariateSpline(photonE, yAllNorm)
#    splinE = itp.LSQUnivariateSpline(photonE, yAllNorm)
#    print( "photonE sorted? " + all( photonE[i] <= photonE[i+1] for i in range(len(photonE)-1) ) ) #check if list is really sorted

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
    rawVals.append(vals)
    rawPhotonE.append(photonE)
    step = (highE - lowE) / stepSize
    linE, splinE = get_spline(lowE, highE, step, photonE, vals)
    firstPeak = find_peak(532, 537, step, splinE)             
    return
#shifts all peaks to match the earleast peak. returns new splines
def shift_spline(splineNum, pks, spln, lin):
    vals = spln[splineNum]( lin[splineNum] )
    ref = np.amin( pks )
    
    if ref == pks[splineNum]:
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

if __name__ == "__main__":
    test_shift()