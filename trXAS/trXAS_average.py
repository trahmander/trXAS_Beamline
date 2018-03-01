# -*- coding: utf-8 -*-
"""
trXAS_average.py: Used to average the integrated trxas data for time plots.
@newfield revision: revision
"""
__author__  = "Tahiyat Rahman"
__date__    = "2018-02-21"
__credits__ = ["Johannes Mahl"]
__email__ = "trahman@lbl.gov"
__status__ = "production"
__revision__= "2"
###############################################################################
#Import modules
###############################################################################
import os
import sys
import numpy as np
from matplotlib import pyplot as plt
from scipy.interpolate import UnivariateSpline
from scipy.interpolate import InterpolatedUnivariateSpline
import scipy.interpolate as itp

def get_data_files(path):
    pathName = path
    dataFiles = os.listdir(pathName)
    dFiles = []
#    print(dataFiles)
#    print(len(dataFiles))
    for file in dataFiles:
#        print(file)
        if  file.endswith("data.txt") and not( "average" in file) :
            print(file)
            dFiles.append(pathName+file)
    return dFiles 
def load_file(fileName):
    dataSet = np.loadtxt(fileName, skiprows=1)
#    print(dataSet[:,0])
    dataSet = dataSet.tolist()
    dataSet.sort(key= lambda x:x[0])
    dataSet = np.array(dataSet)
    return dataSet
def find_peak(xlow, xhigh, step, func):
    nearPeak = np.linspace(xhigh, xlow, step)
    feature = func(nearPeak)
    maxVal = feature[0] 
    peak = nearPeak[0]
    for i in range( len(feature) ):
        if feature[i] > maxVal:
            maxVal = feature[i]
            peak = i
    return nearPeak[peak]
def get_spline(low, high, step, x, y):
    line = np.linspace(low, high, step)
#    splinE = itp.UnivariateSpline(photonE, yAllNorm, s=None, k=2)
#    splinE = itp.InterpolatedUnivariateSpline(photonE, yAllNorm)
#    splinE = itp.LSQUnivariateSpline(photonE, yAllNorm)
#    print( "photonE sorted? " + all( photonE[i] <= photonE[i+1] for i in range(len(photonE)-1) ) ) #check if list is really sorted
    spline = itp.interp1d(x, y, kind='slinear')                                   #This one does linear interpolation. kinda ugly
    return line, spline
def photonE_counts_plot(dataSet):
    (photonE, #SEphotonE,
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
        ) = dataSet.T
#    lowE = np.amin(photonE)
#    highE = np.amax(photonE)
    lowE = photonE[0]
    highE = photonE[-1]
    step = 1000
    linE, splinE = get_spline(lowE, highE, step, photonE, yAllNorm)
    firstPeak = find_peak(532, 537, 1000, splinE)             
    figure = plt.figure(dpi=100)
    plt.plot( photonE, yAllNorm, marker= 'd', linestyle='none' )
    plt.plot( linE, splinE(linE), linewidth=1 )
    plt.axvline( firstPeak, linewidth = 1 )
    plt.show()
#def shift_spline(spline, line, delta):
#    spline(line) = spline(line+delta)

#def average_splines(splineSet, line):
#    splineSum = np.zeros_like(line)
#    numSpline=0
#    for i in range( len(splineSet) ):
#        spline = splineSet[i](line)
#        splineSum = splineSum + spline
#        numSpline+=1
#    splineAvg = splineSum/numSpline
#    return splineAvg

def main():
    dir = os.path.dirname(__file__)
    path = "trXAS data sample - date eval software/hv scans processed/0198_CuO_O_K-edge_355nm_58pc/"
    dataFiles = get_data_files(path)
    for file in dataFiles:
        dataSet = load_file(file)
        photonE_counts_plot(dataSet)

    
if __name__ == "__main__":
    main()
