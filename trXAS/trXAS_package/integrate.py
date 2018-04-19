#!/usr/bin/env python
from scipy.integrate import simps, romb, trapz, cumtrapz
import random
from config import stepSize
import numpy as np
from matplotlib import pyplot as plt
# resturns the first index which is closest to xLow and the first index closest to xHigh
def find_nearest_index(xVals, xLow, xHigh):
	# print(xVals)
	low=0; high=0
	lowVals = np.abs( xVals - xLow ) 
	highVals = np.abs( xVals - xHigh ) 
	# print(lowVals)
	# print(highVals)
	lowMin = lowVals[0]
	highMin = highVals[0]
	for i in range( len(xVals) ):
		if lowVals[i] < lowMin:
			lowMin = lowVals[i]
			low=i
		if highVals[i] < highMin:
			highMin = highVals[i]
			high = i
	# print( (xVals[low], low) )
	# print( (xVals[high], high) )
	return low, high
def def_integral(xVals, yVals, xLow, xHigh):
	# print(yVals)
	low, high = find_nearest_index(xVals, xLow, xHigh)
	yInterval = yVals[low:high]
	xInterval = xVals[low:high]
	integral = simps(yInterval, xInterval )
	return integral
def remove_dup(seq):
	seen = set()
	seen_add = seen.add
	return [x for x in seq if not( x in seen or seen_add(x) )]
def average_integrals(bunchNum, integrals):
	i=0
	stop= len(bunchNum)
	# print ( len( set(bunchNum) ) )
	integralsAverage = []
	while (i < stop):
		bunch = bunchNum[i]
		Int = integrals[i]
		indices = [j for j, x in enumerate(bunchNum) if x == bunch ]
		Int = np.average( [integrals[j] for j in indices] )
		integralsAverage.append(Int)
		# for j in indices[1:]:
		# 	del integrals[j]
		# 	del bunchNum[j]
		# 	stop-=1
		i+=1

	integrals = remove_dup(integralsAverage)
	bunchNum = remove_dup(bunchNum)
	# print( len(bunchNum) )
	# print( len(integrals) )
	# print()
	return bunchNum, integrals


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

if __name__ == "__main__":
	test_integrate()