#!/usr/bin/env python
###############################################################################
#Import modules
###############################################################################
from scipy.integrate import simps, romb, trapz, cumtrapz
from scipy.optimize import curve_fit
import random
import numpy as np
from matplotlib import pyplot as plt
#From modules in trXAS_package
from config import stepSize, integrationWindow
###############################################################################
#find the closes index in xVals that matches x.
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
#a not so great method of finding a zero crossing given an intitaial guess xVal.
def find_zero(yVals, xVals, xVal):
	if integrationWindow !=0.0 :
		wind = int( integrationWindow / stepSize / 2.0 )
		ind = find_nearest_index(xVals, xVal)
		nearZero = xVals[ind-wind:ind+wind]
		nearZeroVal = yVals[ind-wind:ind+wind]
		fall=set([])
		for j in range( len(nearZero)-1 ):
			if nearZeroVal[j]>0 and nearZeroVal[j+1]<0:
				  fall.add( (nearZero[j] + nearZero[j+1])/2.0 )
		nearZeroVal = nearZeroVal[::-1]
		for j in range( len(nearZero)-1 ):
			if nearZeroVal[j]>0 and nearZeroVal[j+1]<0:
				  fall.add( (nearZero[j] + nearZero[j+1])/2.0 )
		if len(fall) == 0:
			zero = nearZero[ np.argmin( np.abs(nearZeroVal) ) ]
		else:
			zero = np.average( list(fall) )
		return zero
	else:
		return xVal
# returns the first indices which are closest to xLow and xHigh.
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
def def_integral(xVals, yVals, xLow, xHigh, wantPlot=False):
    if xHigh == "all" and xLow == "all":
        xLow = xVals[0]
        xHigh = xVals[-1]
    else:
        xHigh = find_zero(yVals, xVals, xHigh)
        xLow = find_zero(yVals, xVals, xLow)
    #see this plot by setting wantPlot to True in call to compute_integral in
    # save_integral function in main.
    if wantPlot:
        print( (xLow, xHigh) )
        fig1 = plt.figure(dpi=100)
        plt.plot(xVals, yVals)
        plt.axvline(x=float(xLow), linestyle = "--", color= "green", linewidth = 0.5)
        plt.axvline(x=float(xHigh), linestyle = "--", color= "red", linewidth = 0.5)
        plt.axhline(y=0, linestyle = "-", color= "grey")
    low, high = find_nearest_bounds(xVals, xLow, xHigh)
    #swaps values in case something is wrong, but this is probably unnecessary.
    if low > high:
        low = low + high
        high = low - high
        low = low - high
    yInterval = yVals[low:high]
    xInterval = xVals[low:high]
    try:
        integral = simps(yInterval, xInterval )
    except ValueError:
        print( ( len(yInterval),len(xInterval) ) )
    integral = integral / (high - low)
    return integral
# removes duplicates in list while preserving order.
def remove_dup(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not( x in seen or seen_add(x) )]
#averages the integrals if their bunches after the laser are the same. Only references last bunch
# forexample file with bunches 17-25 is weighted the same as one from 20-25. 
def average_integrals(bunchNum, integrals):
    i=0
    stop= len(bunchNum)
    integralsAverage = []
    repeat=[]
    while (i < stop):
        bunch = bunchNum[i]
        indices = [j for j, x in enumerate(bunchNum) if x == bunch ]
        Int = np.average( [integrals[j] for j in indices] )
        integralsAverage.append(Int)
        repeat.extend(indices[1:])
        i+=1
    integrals = [Int for k, Int in enumerate(integralsAverage) if not (k in repeat) ]
    bunchNum = remove_dup(bunchNum)
    return bunchNum, integrals
#Currently unused. This was just a step function with decay that was fit to 
# transient data to look at the effect that different shift methods had on the 
# best fit parameters.
def exp(t, A, T, t0):
    return A*np.heaviside(t-t0, 0.5)*np.e**(-1*(t - t0)/T)    
###############################################################################
#Test function for integrate.py
###############################################################################
def test_integrate():
    # x_axis = np.linspace(-10, 100, 1000)
    # y = [exp(x, 1.0, 2.0, 3.0 ) + 0.1*random.randint(0,100) for x in x_axis]
    # opt, cov = curve_fit(exp, x_axis, y, p0 = [1.0, 2.0])
    # print(opt)
    # y_fit = exp(x_axis, opt[0], opt[1], opt[2])
    # plt.plot(x_axis,y)
    # plt.plot(x_axis, y_fit)

    for i in range(4):
        rand= [random.randint(-50,50) for r in range(5) ]
        print( rand )
        zeroCross=set([])
        for j in range( len(rand) -1):
        	if ( rand[j]>=0 and rand[j+1]<=0  ) :
        		zeroCross.add(rand[j])
        print(zeroCross)
        rand = rand[::-1]
        for j in range( len(rand) -1):
        	if ( rand[j]>=0 and rand[j+1]<=0  ) :
        		zeroCross.add(rand[j])
        print(zeroCross)
    return
###############################################################################
if __name__ == "__main__":
    test_integrate()