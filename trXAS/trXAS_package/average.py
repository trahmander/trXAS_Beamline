# -*- coding: utf-8 -*-
"""
Created on Wed Mar 21 17:32:58 2018

@author: 2-310-GL group
"""
import numpy as np

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
def test_average():
    return
if __name__ == "__main__":
    test_average