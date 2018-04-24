#!/usr/bin/env python
###############################################################################
#Import modules
###############################################################################
from scipy.integrate import simps, romb, trapz, cumtrapz
import random
import numpy as np
from matplotlib import pyplot as plt
from config import stepSize
###############################################################################
def find_nearest_index(xVals, x):
    x = float( x )
    index=0
    diff = np.abs( xVals - x ) 
    diffMin =diff[0]
    for i in range( len(xVals) ):
        if diff[i] < diffMin:
            diffMin = diff[i]
            index=i
    return index
# resturns the first index which is closest to xLow and the first index closest to xHigh
def find_nearest_bounds(xVals, xLow, xHigh):
    if xLow  == "all" :
        xHigh = " "
        low = 0
        high = len(xVals)
    else:
        low = find_nearest_index(xVals, xLow)
        high = find_nearest_index(xVals, xHigh)
    return low, high
# integrates yVals over a given region in xVals
def def_integral(xVals, yVals, xLow, xHigh):
    low, high = find_nearest_bounds(xVals, xLow, xHigh)
    yInterval = yVals[low:high]
    xInterval = xVals[low:high]
    integral = simps(yInterval, xInterval )
    return integral
# removes duplicates in list while preserving order.
def remove_dup(seq):
	seen = set()
	seen_add = seen.add
	return [x for x in seq if not( x in seen or seen_add(x) )]
# averages the integrals if their bunches after the laser are the same. Only references last bunch
# forexample file with bunches 17-25 is weighted the same as one from 20-25. 
def average_integrals(bunchNum, integrals):
	i=0
	stop= len(bunchNum)
	integralsAverage = []
	while (i < stop):
		bunch = bunchNum[i]
		Int = integrals[i]
		indices = [j for j, x in enumerate(bunchNum) if x == bunch ]
		Int = np.average( [integrals[j] for j in indices] )
		integralsAverage.append(Int)
		i+=1
	integrals = remove_dup(integralsAverage)
	bunchNum = remove_dup(bunchNum)
	return bunchNum, integrals
###############################################################################
#Test function for integrate.py
###############################################################################
def test_integrate():
	xVals = np.linspace(0, 4*np.pi,1001)
	yVals = np.cos(xVals)
	yVals = np.exp(2.0*xVals)
	yInt = [ 2.0 + simps( yVals[:i+1], xVals[:i+1] ) for i in range(len(xVals)) ]
	yPred = np.sin(xVals)
	yPred = 0.5*yVals

	plt.plot(xVals,yVals)
	plt.plot(xVals, yInt, linestyle= '-.')
	plt.plot(xVals, yPred, linestyle= '--')
	plt.show()
	return
###############################################################################
if __name__ == "__main__":
	test_integrate()