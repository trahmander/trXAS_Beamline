# -*- coding: utf-8 -*-
"""
Created on Wed Mar 21 17:32:58 2018
use: For averaging splines together.
@author: 2-310-GL group
"""
###############################################################################
#Import modules
###############################################################################
import numpy as np
from matplotlib import pyplot as plt
from scipy import optimize as opt
import random
###############################################################################
#some constants
e = np.e
pi = np.pi
def gaussian(fwhm, A=1, x0=0, B=0):
    def gaussian_func(x):
        return A*np.exp(-4*np.log(2)*(x-x0)**2/fwhm**2) + B
    return gaussian_func
def lorentzian(A, fwhm, x_0):
    def lorentzian_func(x):
        return A*0.5*fwhm/( (x-x0)**2 + (0.5*fwhm)**2 ) + B
    return lorentzian_func
#average the values from two splines and return the new line and spline values.
def average_vals(vals, line):
    valSum = np.zeros_like(line)
 
    numVals=len(vals)
    for i in range( numVals ):
        val = vals[i]
        smaller = min(len(val), len(valSum) )
        for j in range( smaller ):
            valSum[j] = valSum[j] + val[j]
        valSum = valSum[:smaller]
        line = line[:smaller]
    valAvg = valSum/numVals
    return valAvg, line
###############################################################################
#Test function for average.py
###############################################################################
def test_average():
    x_vals = np.linspace(-pi, pi, 1001)
    y_vals = np.array( [ ( gaussian(fwhm=0.4)(x) + random.randrange(0, 0.3, 0.05) ) for x in x_vals ] )
    plt.plot(x_vals, y_vals) 
    plt.show()
    return
if __name__ == "__main__":
    test_average()