#!/usr/bin/env python
###############################################################################
#Import modules
###############################################################################
from scipy.integrate import simps, romb, trapz, cumtrapz
from scipy.optimize import curve_fit
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
# returns the first index which is closest to xLow and the first index closest to xHigh
def find_nearest_bounds(xVals, xLow, xHigh):
    if xLow  == "all" :
        xHigh = "all"
        low = 0
        high = len(xVals) -1
    else:
        xHigh = float(xHigh)
        xLow = float(xLow)
        if xHigh < xLow :
            xHigh = xHigh + xLow
            xLow = xHigh - xLow
            xHigh = xHigh - xLow
        low = find_nearest_index(xVals, xLow)
        high = find_nearest_index(xVals, xHigh)
    return low, high
# integrates yVals over a given region in xVals
def def_integral(xVals, yVals, xLow, xHigh):
    low, high = find_nearest_bounds(xVals, xLow, xHigh)
    yInterval = yVals[low:high]
    xInterval = xVals[low:high]
    try:
        integral = simps(yInterval, xInterval )
    except ValueError:
        print( ( len(yInterval),len(xInterval) ) )
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
	integrals = remove_dup(integralsAverage)# this isnt a good solution. what if two bunches are degenerate
	bunchNum = remove_dup(bunchNum)
	return bunchNum, integrals

def exp(t, A, T, t0):
    return A*np.heaviside(t-t0, 0.5)*np.e**(-1*(t - t0)/T)

    
###############################################################################
#Test function for integrate.py
###############################################################################
def test_integrate():
    x_axis = np.linspace(-10, 100, 1000)
    y = [exp(x, 1.0, 2.0, 3.0 ) + 0.1*random.randint(0,100) for x in x_axis]
    opt, cov = curve_fit(exp, x_axis, y, p0 = [1.0, 2.0])
    print(opt)
    y_fit = exp(x_axis, opt[0], opt[1], opt[2])
    plt.plot(x_axis,y)
    plt.plot(x_axis, y_fit)
    return

###############################################################################
if __name__ == "__main__":
	test_integrate()