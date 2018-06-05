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

from config import stepSize
###############################################################################
#some constants
e = np.e
pi = np.pi
def gaussian(fwhm, A=1, x0=0, B=0):
    def gaussian_func(x):
        return A*np.exp(-4*np.log(2)*(x-x0)**2/fwhm**2) + B
    return gaussian_func
def lorentzian(A, B, fwhm, x0):
    def lorentzian_func(x):
        return A*0.5*fwhm/( (x-x0)**2 + (0.5*fwhm)**2 ) + B
    return lorentzian_func
#average the values from "numVals" number of splines and return the new line and spline values.
def average_vals(vals, lines):
    valAvg = np.zeros_like(lines[0])
    lineAvg = np.zeros_like(lines[0])    
    numVals=len(vals)
    for i in range( numVals ):
        val = vals[i]
        line = lines[i]
        smaller = min(len(val), len(valAvg) )
        for j in range( smaller ):
            valAvg[j] += val[j]
            lineAvg[j] += line[j]
        valAvg = valAvg[:smaller]
        lineAvg = lineAvg[:smaller]
    valAvg /= numVals
    lineAvg /= numVals
    return lineAvg, valAvg
def cut_splines(vals, deltas):
    ind = [ int(d/stepSize) for d in deltas ]
    try:
        rightShift = np.abs( min( [i for i in ind if i<=0] ) )
    except(ValueError):
        rightShift=0
    try:
        leftShift = max( [i for i in ind if i >=0] )
    except (ValueError):
        leftShift=0
    vals = [ val[ rightShift : len(val) - leftShift ] for val in vals ]
#    lines = [ line[ rightShift : len(line) - leftShift ] for line in lines ]
    return vals
def standard_error(vals, lines, valAvg, lineAvg):
    yErr = np.zeros_like(valAvg)
    xErr = np.zeros_like(lineAvg)
    numVals = len(vals)
    for i in range(numVals):
        val = vals[i]
        line = lines[i]
        smaller = min(len(val), len(valAvg))
        for j in range(smaller):
            dy = (valAvg[j] - val[j])
            yErr[j] += dy*dy
            dx = lineAvg[j] - line[j]
            xErr[j] += dx*dx
        yErr = yErr[:smaller]
        xErr = xErr[:smaller]
    yErr /= numVals
    yErr = np.sqrt(yErr)
    xErr /= numVals
    xErr = np.sqrt(xErr)
    return xErr, yErr
def average_by_bunch(bunchNum, vals, line):
    for bunch in bunchNum:
        x=1
    return
###############################################################################
#Test function for average.py
###############################################################################
def test_average():
    randomLists=[]
    for i in range(5):
        rand= [random.randint(0,100) for r in range(10) ]
        randomLists.append( rand )
    print(randomLists)

    
#    avg = average_vals(randomLists, randomLists)
#    err = standard_error(randomLists, randomLists)
#    print(avg[0])
#    print(err[0])
    
    randomLists = np.array(randomLists)
    avg = np.mean(randomLists, axis = 1)
    err = np.std(randomLists, axis = 1)/ np.sqrt(len(randomLists[0]))
    print(avg)
    print(err)
    
    return
if __name__ == "__main__":
    test_average()