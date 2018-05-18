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
import numpy as np
#from matplotlib import pyplot as plt
import scipy.interpolate as itp
from scipy.integrate import simps
import scipy.optimize as opt
#import global variables.
#from config import peaks
#from config import splines
#from config import refSplines
from config import (lines,
                    peaks,
                    splines,
                    stepSize,
                    peakFindStart,
                    peakFindEnd)
###############################################################################
#finds the x-value of the peak specified around xlow and xhigh. Appends it to peaks.
def find_peak(func):
    step = (float(peakFindEnd) - float(peakFindStart)) / stepSize
    nearPeak = np.linspace(float(peakFindStart), float(peakFindEnd), step)
    feature = func(nearPeak)
    maxVal = feature[0]  
    peak = 0
    for i in range( len(feature) ):
        if feature[i] > maxVal:
            maxVal = feature[i]
            peak = i
    peaks.append(nearPeak[peak])
    return nearPeak[peak]
def find_center(xVals, func):
#    step = (xhigh - xlow)/stepSize
#    xVals = np.linspace(xhigh, xlow, step)
    yVals = func(xVals)
    mass = simps( yVals, xVals )
    centerOfMass = simps( np.multiply(xVals, yVals) , xVals) / mass
    return centerOfMass
#Interpolation of data. returns linear spline Appends it to splines
def get_spline(x, col, refCol):
    low = x[0]
    high = x[-1]
    step = (high - low) / stepSize
    line = np.linspace(low, high, step)
#    refSpline = itp.interp1d(x, refY, kind='slinear')                                   #This one does linear interpolation. kinda ugly
    colSpline=[]
    for y in col:
        spline = itp.interp1d(x, y, kind = 'slinear')
        colSpline.append(spline)
    splines.append(colSpline)
    lines.append(line)
    refSpline = colSpline[refCol]
    return refSpline
#unpacks the 2d array into 1d arrays given by the columns. uses find_peak and get_spline.
def data_to_column(dataSet, refCol, file):
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
#        lowE = photonE[0]
#        highE = photonE[-1]
#        refVals = columns[refCol]
#        vals = columns[col]
#        step = (highE - lowE) / stepSize
        refSpline = get_spline(photonE, columns[1:], refCol-1)
#        if findPeak:
#            peakEnergy = find_peak(float(peakFindStart), float(peakFindEnd), refSpline)                                       #should not be hardcoded.
    except:
        print("Didn't load to array:\t"+file)             
    return refSpline
#shifts all peaks to match the earleast peak. returns new splines. cuts the spline at the  low energy side.
def shift_spline(splineNum, refPeaks, spline, line):
#    yVals = ySpline[splineNum]( line[splineNum] )
    vals = spline[splineNum]( line[splineNum] )
    ref = np.amin( refPeaks )
    
    if np.abs(ref - refPeaks[splineNum]) < stepSize:
        return vals, line[splineNum]
    else:
        delta = refPeaks[splineNum] - ref
        index = int ( delta / stepSize )
        for i in range (len(vals) - index ) :
            vals[i] = vals[i+index]
        return vals[:-index], line[splineNum][:-index]
def get_deltas(refPeaks):
    ref = np.amin(refPeaks)
    deltas=[]
    for peak in refPeaks:       
        if  peak - ref < stepSize/2.0:
            deltas.append(0.0)
        else:
            deltas.append(peak - ref)
    return deltas
def apply_shift(delta, splineCols, lines):
    index = [int ( de / stepSize ) for de in delta]
    valuesAllCol=[]
    for i, spline in enumerate( splineCols ):
        values=[]
        ind = index[i]
        if ind == 0:
            for col in spline :
                values.append( col( lines[i] ) )
        else:
            for col in spline:
                val = col( lines[i] )
                for k in range( len(val) - ind ):
                    val[k] = val[k+ind]
                values.append(val[:-ind])
            lines[i] = lines[i][:-ind]
    
        valuesAllCol.append(values)
    return lines, valuesAllCol

###############################################################################
#Test Functions for shift.py
###############################################################################
def test_shift():
    return
###############################################################################
if __name__ == "__main__":
    test_shift()