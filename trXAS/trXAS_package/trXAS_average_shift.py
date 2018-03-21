# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 13:48:38 2018

@author: 2-310-GL group
"""
import os
import sys
import numpy as np
import itertools as iter
from matplotlib import pyplot as plt
#from scipy.interpolate import UnivariateSpline
#from scipy.interpolate import InterpolatedUnivariateSpline
import scipy.interpolate as itp

from trXAS_average_load_files import get_data_files as get_data_files
from trXAS_average_load_files import load_file as load_file

peaks = []
peakAvgs = []
splines = []
lines= []
peaksAll=[]
splinesAll=[]
linesAll=[]
stepSize = 0.001

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
#Interpolation of data.
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
#    lowE = np.amin(photonE)
#    highE = np.amax(photonE)
    lowE = photonE[0]
    highE = photonE[-1]
    vals = columns[col]
    step = (highE - lowE) / stepSize
    linE, splinE = get_spline(lowE, highE, step, photonE, vals)
    firstPeak = find_peak(532, 537, step, splinE)             
#    figure = plt.figure(dpi=100)
#    plt.title("File: "+str(file))
#    plt.plot( photonE, yAllNorm, marker= 'd', linestyle='none' )
#    plt.plot( linE, splinE(linE), linewidth=1 )
#    plt.axvline( firstPeak, linewidth = 1 )
#    plt.show()
# NEEDS WORK. Find a way to convert peak difference into iter difference
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


def test_shift():
    return

if __name__ == "__main__":
    test_shift()