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
#    print(yAllNorm)
#    print (SE)
#    print(SE2)
#    print(photonE)
#    lowE = np.amin(photonE)
#    highE = np.amax(photonE)
    lowE = photonE[0]
    highE = photonE[-1]
    linE = np.linspace(lowE, highE, 1000)
#    splinE = itp.UnivariateSpline(photonE, yAllNorm, s=None, k=2)
#    splinE = itp.InterpolatedUnivariateSpline(photonE, yAllNorm)
#    splinE = itp.LSQUnivariateSpline(photonE, yAllNorm)
#    print( "photonE sorted? " + all( photonE[i] <= photonE[i+1] for i in range(len(photonE)-1) ) ) #check if list is really sorted
    splinE = itp.interp1d(photonE, yAllNorm, kind='slinear')                                   #This one does linear interpolation. kinda ugly
    figure = plt.figure(dpi=100)
    plt.plot( photonE, yAllNorm, marker= 'd', linestyle='none' )
    plt.plot( linE, splinE(linE), linewidth=1 )
    plt.show()

def main():
    dir = os.path.dirname(__file__)
    path = "trXAS data sample - date eval software/hv scans processed/0198_CuO_O_K-edge_355nm_58pc/"
    dataFiles = get_data_files(path)
    for file in dataFiles:
        dataSet = load_file(file)
        photonE_counts_plot(dataSet)
#    fileName = input("What is the file name?")
#    dir = os.path.dirname(__file__)
#    fileName = os.path.join(dir,"trXAS data sample - date eval software/hv scans processed/0198_0199_0201_0202_avg/0198_0199_0201_0202_avg_pump_17-17_minus_ref_1-16.txt")
#    fileName = "trXAS data sample - date eval software/hv scans processed/0198_CuO_O_K-edge_355nm_58pc/0198_diff_spect_pump_12-16_minus_ref_1-16_data.txt"
#    dataSet = np.loadtxt(fileName, skiprows=1)
#    print(dataSet[:,0])
#    dataSet = dataSet.tolist()
#    dataSet.sort(key= lambda x:x[0])
#    dataSet = np.array(dataSet)
 #   numColumns = dataSet.shape[1]
 #   print(numColumns)
        
#    (photonE, SEphotonE,
#        xRefNorm, SExRefNorm,
#        xRef, SExRef,
#        xPumpNorm, SExPumpNorm, 
#        xPump, SExPump,
#        yRefNorm, SEyRefNorm,
#        yRef, SEyRef,
#        yPumpNorm, SEyPumpNorm,
#        yPump, SEyPump,
#        xAllNorm, SExAllNorm,
#        xAll, SExAll,
#        yAllNorm, SEyAllNorm,
#        yAll, SEyAll,
#        xAllyRefNorm, SExAllyRefNorm,
#        xAllyRef, SExAllyRef,
#        yAllxRefNorm, SEyAllxRefNorm, 
#        yAllxRef, SEyAllxRef,
#        BCxHistNorm, SEBCxHistNorm, 
#        BCyHistNorm, SEBCyHistNorm,
#        stsNorm, SEstsNorm,
#        BCSCNorm, SEBCSCNorm, 
#        BCLRNorm, SEBCLRNorm,
#        BCxHist, SEBCxHist,
#        BCyHist, SEBCyHist,
#        sts, SEsts,
#        BCSC, SEBCSC, 
#        BCLR, SEBCLR,
#        SE, SE2) = np.loadtxt(fileName, skiprows=1, unpack=True)
#    (photonE, #SEphotonE,
#        xRefNorm, #SExRefNorm,
#        xRef, #SExRef,
#        xPumpNorm, #SExPumpNorm, 
#        xPump, #SExPump,
#        yRefNorm, #SEyRefNorm,
#        yRef, #SEyRef,
#        yPumpNorm, #SEyPumpNorm,
#        yPump, #SEyPump,
#        xAllNorm, #SExAllNorm,
#        xAll, #SExAll,
#        yAllNorm, #SEyAllNorm,
#        yAll, #SEyAll,
#        xAllyRefNorm, #SExAllyRefNorm,
#        xAllyRef, #SExAllyRef,
#        yAllxRefNorm, #SEyAllxRefNorm, 
#        yAllxRef, #SEyAllxRef,
#        BCxHistNorm, #SEBCxHistNorm, 
#        BCyHistNorm, #SEBCyHistNorm,
#        stsNorm, #SEstsNorm,
#        BCSCNorm, #SEBCSCNorm, 
#        BCLRNorm, #SEBCLRNorm,
#        BCxHist, #SEBCxHist,
#        BCyHist, #SEBCyHist,
#        sts, #SEsts,
#        BCSC, #SEBCSC, 
#        BCLR, #SEBCLR,
#        #SE, #SE2
#        ) = dataSet.T
#    print(yAllNorm)
#    print (SE)
#    print(SE2)
#    print(photonE)
#    lowE = np.amin(photonE)
#    highE = np.amax(photonE)
#    lowE = photonE[0]
#    highE = photonE[-1]
#    linE = np.linspace(lowE, highE, 1000)
#    splinE = itp.UnivariateSpline(photonE, yAllNorm, s=None, k=2)
#    splinE = itp.InterpolatedUnivariateSpline(photonE, yAllNorm)
#    splinE = itp.LSQUnivariateSpline(photonE, yAllNorm)
#    print( "photonE sorted? " + all( photonE[i] <= photonE[i+1] for i in range(len(photonE)-1) ) ) #check if list is really sorted
#    splinE = itp.interp1d(photonE, yAllNorm, kind='slinear')                                   #This one does linear interpolation. kinda ugly
#    figure = plt.figure(dpi=100)
#    plt.plot( photonE, yAllNorm, marker= 'd', linestyle='none' )
#    plt.plot( linE, splinE(linE), linewidth=1 )
#    plt.show()
    
if __name__ == "__main__":
    main()
