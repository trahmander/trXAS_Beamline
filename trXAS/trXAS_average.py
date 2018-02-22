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
__revision__= "0"

import numpy as np
from matplotlib import pyplot as plt
from scipy import interpolate

def load_file(fileName):
    dataSet = np.loadtxt(fileName, dtype= 'float', skiprows=1)
    return dataSet
def twod_plot(x,y):
    figure = plt.figure(dpi=100)
    plt.plot(x,y, marker= 'd', linestyle='none')

def main():
#    fileName = input("What is the file name?")
    fileName = "0198_0199_0201_0202_avg_pump_17-17_minus_ref_1-16.txt"
 #   dataSet = np.loadtxt(fileName, skiprows=1)
 #   numColumns = dataSet.shape[1]
 #   print(numColumns)
    
    (photonE, SEphotonE,
        xRefNorm, SExRefNorm,
        xRef, SExRef,
        xPumpNorm, SExPumpNorm, 
        xPump, SExPump,
        yRefNorm, SEyRefNorm,
        yRef, SEyRef,
        yPumpNorm, SEyPumpNorm,
        yPump, SEyPump,
        xAllNorm, SExAllNorm,
        xAll, SExAll,
        yAllNorm, SEyAllNorm,
        yAll, SEyAll,
        xAllyRefNorm, SExAllyRefNorm,
        xAllyRef, SExAllyRef,
        yAllxRefNorm, SEyAllxRefNorm, 
        yAllxRef, SEyAllxRef,
        BCxHistNorm, SEBCxHistNorm, 
        BCyHistNorm, SEBCyHistNorm,
        stsNorm, SEstsNorm,
        BCSCNorm, SEBCSCNorm, 
        BCLRNorm, SEBCLRNorm,
        BCxHist, SEBCxHist,
        BCyHist, SEBCyHist,
        sts, SEsts,
        BCSC, SEBCSC, 
        BCLR, SEBCLR,
        SE, SE2) = np.loadtxt(fileName, skiprows=1, unpack=True)
    print(yAllNorm)
#    print (SE)
#    print(SE2)
    twod_plot(photonE, yAllNorm)
    
if __name__ == "__main__":
    main()
