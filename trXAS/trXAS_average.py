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
__revision__= "5"
###############################################################################
#Import modules
###############################################################################
import os
import sys
import numpy as np
import itertools as iter
from matplotlib import pyplot as plt
#from scipy.interpolate import UnivariateSpline
#from scipy.interpolate import InterpolatedUnivariateSpline
import scipy.interpolate as itp

peaks = []
peakAvgs = []
splines = []
lines= []
peaksAll=[]
splinesAll=[]
linesAll=[]
stepSize = 0.001


def user_inputs():
    print("This software is used for averaging spectral distributions :)")
    directory = input("Please enter the directory that you wish to send data.")
    print("Which column do you want to look at?")
    col = {"0a":photonE, "0b":SEphotonE,
        "1a":xRefNorm, "1b":SExRefNorm,
        "1c":xRef, "1d":SExRef,
        "2a":xPumpNorm, "2b":SExPumpNorm, 
        "2c":xPump, "2d":SExPump,
        "3a":yRefNorm, "3b":SEyRefNorm,
        "3c":yRef,"3d":SEyRef,
        "4a":yPumpNorm, "4b":SEyPumpNorm,
        "4c":yPump, "4d":SEyPump,
        "5a":xAllNorm, "5b":SExAllNorm,
        "5c":xAll, "5d":SExAll,
        "6a":yAllNorm, "6b":SEyAllNorm,
        "6c":yAll, "6d":SEyAll,
        "7a":xAllyRefNorm, "7b":SExAllyRefNorm,
        "7c":xAllyRef, "7d":SExAllyRef,
        "8a":yAllxRefNorm, "8b":SEyAllxRefNorm, 
        "8c":yAllxRef, "8d":SEyAllxRef,
        "9a":BCxHistNorm, "9b":SEBCxHistNorm, 
        "10a":BCyHistNorm, "10b":SEBCyHistNorm,
        "11a":stsNorm, "11b":SEstsNorm,
        "12a":BCSCNorm, "12b":SEBCSCNorm, 
        "13a":BCLRNorm, "13b":SEBCLRNorm,
        "9c":BCxHist, "9d":SEBCxHist,
        "10c":BCyHist, "10d":SEBCyHist,
        "11c":sts, "11d":SEsts,
        "12c":BCSC, "12d":SEBCSC, 
        "13c":BCLR, "13d":SEBCLR,}
    print("Choose which column from this table")
    column = input("1:\t X Reference\n"+
              "2:\t X Pump\n"+
              "3:\t Y Reference\n"+
              "4:\t Y Pump\n"+
              "5:\t X All\n"+
              "6:\t Y All\n"+
              "7:\t X All Y Reference\n"+
              "8:\t Y All X Reference\n"+
              "9:\t BC X Histogram\n"+
              "10:\t BC Y Histogram\n"+
              "11:\t STS\n"+
              "12:\t X BCSC\n"+
              "13:\t BCLR\n")
    column += input("a: Normalized \t b: Standard Error of Normalized \t" +
                    "c: Non-Normalized \t d: Standard Error of Unormalized ")
    return

def get_data_files(path):
    pathName = path
    dataFiles = os.listdir(pathName)
    dFiles = []    
    for file in dataFiles:
        if  file.endswith("data.txt") and not( "average" in file) :
#            print(file)
            dFiles.append(os.path.join(pathName,file))
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
    peak = 0
    for i in range( len(feature) ):
        if feature[i] > maxVal:
            maxVal = feature[i]
            peak = i
    peaks.append(nearPeak[peak])
    return nearPeak[peak]
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
def photonE_counts_plot(dataSet, file):
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
    step = (highE - lowE) / stepSize
    linE, splinE = get_spline(lowE, highE, step, photonE, stsNorm)
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
#def calc_step_size(vals):
#    pairs =  list ( iter.combinations(vals, 2) )
#    diff = [p[1] - p[0] for p in pairs]
#    diff = np.abs(diff)
#    step = round (np.amin(diff)/2, -3)
#    return step
    
        

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
#    dir = os.path.dirname(__file__)
#    paths = ["trXAS data sample - date eval software/hv scans processed/0198_CuO_O_K-edge_355nm_58pc/",
#             "trXAS data sample - date eval software/hv scans processed/0199_CuO_O_K-edge_355nm_58pc/",
#             "trXAS data sample - date eval software/hv scans processed/0201_CuO_O_K-edge_355nm_58pc/",
#             "trXAS data sample - date eval software/hv scans processed/0202_CuO_O_K-edge_355nm_58pc/"]
#    path = "trXAS data sample - date eval software/hv scans processed/0198_CuO_O_K-edge_355nm_58pc/"
    direct ="trXAS data sample - date eval software/hv scans processed/"
    paths = os.listdir(direct)
    for i in range( len(paths) ):
        paths[i] = os.path.join(direct, paths[i])
    for path in paths:
         if "avg" in path:
            paths.remove(path)
    for j in range( len(paths) ) :
        path = paths[j]
        dataFiles = get_data_files(path)
        fig = plt.figure(dpi=100)
        plt.title(path)
        for i in range(len(dataFiles)):
            file = dataFiles[i]
            dataSet = load_file(file)
            photonE_counts_plot(dataSet, file)
        
            shiftedVals, shiftedLine = shift_spline(i, peaks, splines, lines)
            plt.plot(shiftedLine, shiftedVals, linewidth=1)
        
        print( peaks )
        print( set(peaks) )
        peakAvgs.append( np.average(peaks) )
        
        peaksAll.extend(peaks)
        splinesAll.extend(splines)
        linesAll.extend(lines)
        peaks.clear()
        splines.clear()
        lines.clear()
    print( peakAvgs )
    
    
#    print( splines[0](lines[0]) )
#    print( shiftedVals )
#    for i in range ( len(splines) ) :
#        shiftedVals, shiftedLine = shift_spline(i)
#        fig = plt.figure(dpi=100)
#        plt.plot(shiftedLine, shiftedVals, linewidth=1, color='b')
#        plt.plot(lines[i], splines[i](lines[i]), linewidth=1,  color='g')
    fig = plt.figure(dpi=200)
    plt.title("All shifted splines")
    for i in range ( len(splinesAll) ) :
        shiftedVals, shiftedLine = shift_spline(i, peaksAll, splinesAll, linesAll)
        plt.plot(shiftedLine, shiftedVals, linewidth=1)

    



    
    
if __name__ == "__main__":
    main()
