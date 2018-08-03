# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 13:48:38 2018
use: stores files as arrays and adds to the lists in config. Used to do the shifting of files.
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
#From modules in trXAS_package
from config import (lines,
                    splines,
                    xOrig,
                    stepSize,
                    peakFindStart,
                    peakFindEnd)
###############################################################################
#finds the x-value of the max specified around xlow and xhigh of the ref spectrum. 
def find_peak(func):
    if peakFindEnd == "all" and peakFindStart =="all":
        nearPeak = lines[-1]
        return np.amax( func(nearPeak) )
    else:
        step = (float(peakFindEnd) - float(peakFindStart)) / stepSize
        nearPeak = np.linspace(float(peakFindStart), float(peakFindEnd), step)
    feature = func(nearPeak)
    maxVal = feature[0]  
    peak = 0
    for i in range( len(feature) ):
        if feature[i] > maxVal:
            maxVal = feature[i]
            peak = i
#    peaks.append(nearPeak[peak])           
    return nearPeak[peak]
#finds the geometric center of the ref spectrum.
def find_center(xVals, func):
    yVals = func(xVals)
    mass = simps( yVals, xVals )
    centerOfMass = simps( xVals*yVals , xVals) / mass
    return centerOfMass
#Interpolation of data. returns linear spline. Appends it to splines
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
    xOrig.append(x)
    lines.append(line)
    refSpline = colSpline[refCol]
    return refSpline
#unpacks the 2d array into 1d arrays given by the columns. uses find_peak and get_spline.
# wantSpline is true by default. If set to false, an array of the column specified by
# colIndex is returned.
def data_to_column(dataSet, colIndex, file, wantSpline=True):
    dataSet = dataSet.T
    try:
        columns = (firstColumn,
            xRefNorm, 
            xRef, 
            xPumpNorm, 
            xPump, 
            yRefNorm, 
            yRef, 
            yPumpNorm, 
            yPump, 
            xAllNorm, 
            xAll, 
            yAllNorm, 
            yAll, 
            xAllyRefNorm, 
            xAllyRef,
            yAllxRefNorm, 
            yAllxRef, 
            BCxHistNorm,  
            BCyHistNorm, 
            stsNorm, 
            BCSCNorm, 
            BCLRNorm, 
            BCxHist, 
            BCyHist, 
            sts,
            BCSC, 
            BCLR, 
            ) = dataSet
        if wantSpline:
            colData = get_spline(firstColumn, columns[1:], colIndex-1)
        else:
            colData = columns[colIndex]                                     #should not be hardcoded.
    except Exception as e:
        print("Didn't load to array:\t"+file)
        print(e)             
    return colData
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
#returns index of value closes to the literature value.
def ref_index(refFeature, litVal):
    diff = [ np.abs(ref-litVal) for  ref in refFeature  ] 
    index = diff.index( np.amin(diff) )
    return index
#returns the standard error difference between ref and vals shifted by delta
def difference_func(delta, ref, vals):
    if delta<stepSize/2 and delta> -1*stepSize/2:
        ind = 0    
    elif delta>0:
        ind = int( delta/stepSize )
        vals = [ vals[k + ind] for k in range( len(vals) - ind )  ]
    elif delta<0:
        ind = int( -1*delta/stepSize )
        #[::-1] reverses the order of the array.
        vals = [ vals[::-1][k+ ind] for k in range( len(vals) -ind)  ]
        ref = ref[::-1]        
    smaller = min( len(vals), len(ref) )
    ref = ref[:smaller]
    vals = vals[:smaller]
    diff = np.std( vals - ref ) *  np.sqrt(smaller)
    return diff
#chooses the reference with peak/center closest to the literature Value.
# if literatureVal is 0 then the earliest peak/center is taken. calculates the
# difference between all peaks/centers and the reference.
def get_deltas(refPeaks, litVal):
    if bool(litVal) :
        refIndex = ref_index(refPeaks, litVal)
        ref = refPeaks[refIndex]
    else:
        ref = np.amin(refPeaks)
    deltas=[]
    for peak in refPeaks:       
        if  peak - ref < stepSize/2.0:
            deltas.append(0.0)
        else:
            deltas.append(peak - ref)
    return deltas
#determines deltas by minimizing the error given in diff_func by taking steps of
# stepSize in config and making shifts in the interval (-bound, bound)
def diff_deltas(splineCols, lines, scanSize, refPeaks, refCol, litVal):
    refSplines = [s[refCol] for s in splineCols] 
    scanIndex=[]
    scan = 0
    for size in scanSize:
        if size !=0:
            scanIndex.append(scan)
            scan += size
        else:
            continue
    refPeaks = [refPeaks[ind] for ind in scanIndex]
    if bool(litVal):
        refIndex = ref_index(refPeaks, litVal)
        ref = refSplines[refIndex]( lines[refIndex] )
    else:
        minIndex = refPeaks.index( min(refPeaks) )
        ref = refSplines[minIndex]( lines[minIndex] )   
    deltas=[]
    bound= 0.55
    shifts = np.arange(-bound,bound, stepSize)   
    for i , spline in enumerate(refSplines):
        vals = spline( lines[i] )
        error = [difference_func(s, ref, vals) for s in shifts]
        delt = shifts[ error.index( np.amin(error) ) ]
        if np.abs(delt) == bound: # raises a warning if the smallest error corresponds to a maximum shift.
            raise RuntimeWarning("shift reached the bounds")
        for j in range( scanSize[i]  ):
            deltas.append( delt  )
    return deltas
#shifts each column by delta ammount. Also shifts more so that the reference is at the literature Value.
# if lit value is set to 0, then no additional shift occurs.
def apply_shift(delta, splineCols, lines, refPeaks, litVal):
    if bool(litVal):
        refIndex = ref_index(refPeaks, litVal)
        litDiff =  refPeaks[refIndex] - litVal
    else:
        litDiff = 0
    index = [ int( de / stepSize ) for de in delta ]
    valuesAllCol=[]
    for i, spline in enumerate( splineCols ):
        values=[]
        ind = index[i]
        if ind == 0:
            for col in spline :
                values.append( col( lines[i] ) )
            lines[i] = lines[i] - litDiff
        elif ind>0:
            for col in spline:
                val = col( lines[i] )
                val = [ val[k + ind] for k in range( len(val) - ind )  ]
#                val = val[:-ind]
                values.append(val)
            lines[i] = lines[i][:-ind] - litDiff
        else:
            ind = -1*ind
            for col in spline:
                val = col( lines[i] )
                val = [ val[::-1][k+ ind] for k in range( len(val) -ind)  ]
                values.append(val[::-1])
            lines[i] = lines[i][ind:] - litDiff
    
        valuesAllCol.append(values)
    return lines, valuesAllCol, litDiff
###############################################################################
#Test Functions for shift.py
###############################################################################
def test_shift():
    return
###############################################################################
if __name__ == "__main__":
    test_shift()