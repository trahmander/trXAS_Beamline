# -*- coding: utf-8 -*-
"""
Created on Wed Mar 21 17:32:58 2018
use: For averaging interpolations save each bunch. For averaging many bunches
     together. Also for calculating standard errors and summing errors. Also 
     used for cutting interpolated data because of shifting.
@author: 2-310-GL group
"""
###############################################################################
#Import modules
###############################################################################
#From built-in modules
import numpy as np
from matplotlib import pyplot as plt
from scipy import optimize as opt
import random
#From modules in trXAS_package
from config import stepSize
###############################################################################
#average the values from "numVals" number of interpolated data and return the 
# new line and spline values.
def average_vals(vals, lines):  
    numVals=len(vals)
    if numVals == 1:
        lineAvg = lines
        valAvg = vals
    else:
        end  = min( [len(v) for v in vals] )
        valAvg = np.zeros(end)
        lineAvg = np.zeros(end)
        for i in range( numVals ):
            val = vals[i][:end]
            line = lines[i][:end]
            for j in range( end ):
                valAvg[j] += val[j]
                lineAvg[j] += line[j]
        valAvg /= numVals
        lineAvg /= numVals
    return lineAvg, valAvg
#cuts the interpolation from the left or right depending on sign of delta.
# all interpolation data has same size after cutting.
def cut_splines(vals, deltas):
    ind = [ int(d/stepSize) for d in deltas ]
    # for delta<0, the values should shift to the right by the smallest delta.
    try:
        rightShift = np.abs( min( [i for i in ind if i<=0] ) )
    except(ValueError): # valueError occurs when there is no value <=0 in ind
        rightShift=0
    # for delta>0, the values should shift to the right by the largest delta.
    try:
        leftShift = max( [i for i in ind if i >=0] )
    except (ValueError): # valueError occurs when there is no value >=0 in ind
        leftShift=0
    vals = [ val[ rightShift : len(val) - leftShift ] for val in vals ]
    return vals
#calculates standard error of entire column based on the averages.
def standard_error(vals, lines, valAvg, lineAvg):
    yErr = np.zeros_like(valAvg)
    xErr = np.zeros_like(lineAvg)
    numVals = len(vals)
    end = min( len(v) for v in vals )
    for i in range(numVals):
        val = vals[i][:end]
        line = lines[i][:end]
        for j in range(end):
            dy = (valAvg[j] - val[j])
            yErr[j] += dy*dy
            dx = lineAvg[j] - line[j]
            xErr[j] += dx*dx
    yErr /= numVals
    yErr = np.sqrt(yErr)
    xErr /= numVals
    xErr = np.sqrt(xErr)
    return xErr, yErr
#sums errors together. norm is False be default. If set to true, the error is
# divided by the number of terms. This is used in finding standard error of 
# the files with multiple averaged bunches.
def sum_error(errs, norm=False):
    standardErr = 0
    for err in errs:
        standardErr += err*err
    standardErr = np.sqrt(standardErr)
    if norm:
        standardErr /= np.sqrt( len(errs) )
    return standardErr
#chunks a sequence into a list of tuples that are of length size. Used for 
# averaging multiple bunches together.
def chunk_list(seq, size):
    return list( zip( *[iter(seq)]*size  ) )
#Removes outliers from a data set if the ratio of the difference between the
# y value and the median to the median is greater than m. Currently unused, 
# because it was throwing out data when doing integration for a few bunches 
# around 1st bunch.
def remove_outliers(dataX,dataY, m = 2.):
    diff = np.abs(np.array(dataY) - np.median(dataY))
    mdev = np.median(diff)
    s =[ d/mdev if mdev!=0 else 0 for d in diff]
    i=0
    size = len(dataY)
    while (i < size ):
        if s[i]>=m:
            del dataY[i]
            del dataX[i]
            size-=1
        i+=1          
    return dataX, dataY
###############################################################################
#Test function for average.py
###############################################################################
def test_average():
    randomLists=[]
    for i in range(4):
        rand= [random.randint(0,100) for r in range(5) ]
        print( rand )
        chunkRand = chunk_list(rand,1)
        print( chunkRand )
        for chunk in chunkRand:
            print( str(chunk[0])+"-"+str(chunk[-1]) )
        randomLists.append( rand )
    return
if __name__ == "__main__":
    test_average()