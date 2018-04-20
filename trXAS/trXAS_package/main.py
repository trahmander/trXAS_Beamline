# -*- coding: utf-8 -*-
"""
use: Average and shift the  trXAS data. Also integrate the data in a region of interest.
@newfield revision: revision
"""
__author__  = "Tahiyat Rahman"
__date__    = "2018-02-21"
__credits__ = ["Johannes Mahl"]
__email__ = "trahman@lbl.gov"
###############################################################################
#Import modules
###############################################################################
#From buit in modules
import os
import sys
import numpy as np
from matplotlib import pyplot as plt
#From trXAS average package
from user_input import user_directory  
from user_input import user_column
from user_input import user_bunches
from user_input import user_integration_bounds
from load_files import get_data_files
from load_files import load_file
from load_files import select_files
from load_files import get_selected_bunches
from shift import photonE_counts_plot
from shift import shift_spline
# from shift import shift_lists
from integrate import def_integral
from integrate import average_integrals
from integrate import find_nearest_index
from average import average_vals
# Load global variables. These are also used in shift.py
from config import peaks
from config import splines
from config import lines 
###############################################################################
###############################################################################
#Main driver function for all other modules in the trXAS package.
###############################################################################
#Compares the averaging, need to manually change Johannes column number to switch between columns of the files for now.
def main():
    peaks.clear()
    splines.clear()
    lines.clear()
    direct = user_directory()
    column = user_column()
    paths = os.listdir(direct)
    for i in range( len(paths) ):
        paths[i] = os.path.join(direct, paths[i])
    for path in paths:
         if "avg" in path:
            paths.remove(path)
    first, last = user_bunches()
    xLow, xHigh = user_integration_bounds()
#    pump = user_pump()
#    probe = user_probe()
#    sample = user_sample()
    
    integrals=[]
    shiftedSplines=[]
    peaksAll=[]
    splinesAll=[]
    linesAll=[]
    integralsAll=[]
    bunchNumAll=[] 
    for j in range( len(paths) ) :
        path = paths[j]
        dataFiles = get_data_files(path)
        dataFiles = select_files(dataFiles, first = first, last = last)
        bunchNum= get_selected_bunches(dataFiles, first = first, last = last)
        dataSet, header = load_file(dataFiles[0])
        columnName = header[column]
        
        fig_data = plt.figure(dpi=100)
        plt.title(path+" Bunches: "+first+"-"+last)
        plt.ylabel(columnName)
        plt.xlabel("Probe [eV]")
        for i in range(len(dataFiles)):
            file = dataFiles[i]
            dataSet, header = load_file(file)
            photonE_counts_plot(dataSet, column, file)
        
        for k in range ( len(splines) ):
            shiftedVals, shiftedLine = shift_spline(k, peaks, splines, lines)
            shiftedSplines.append(shiftedVals)
            lo,hi = find_nearest_index(shiftedLine ,xLow, xHigh)
            shiftedLine = shiftedLine[lo:hi]
            shiftedVals = shiftedVals[lo:hi]
            plt.plot(shiftedLine, shiftedVals, linewidth=1)
           
            integral= def_integral(shiftedLine, shiftedVals, xLow, xHigh)
            integrals.append(integral)   

        integrals = [Int for bunch, Int in sorted( zip(bunchNum, integrals), key = lambda pair: pair[0] )]
        bunchNum.sort()
        bunchNum, integrals = average_integrals(bunchNum, integrals)
        timeDelay = np.multiply(2.0,bunchNum)
        fig_int = plt.figure(dpi=100)
        plt.title(path+" Bunches: "+first+"-"+last+ " Integration: "+xLow+"-"+xHigh)
        plt.ylabel(columnName+" total ")
        plt.xlabel("Time Delay [ns]")
        plt.plot(timeDelay , integrals, marker = 'd')
        
        peaksAll.extend(peaks)
        splinesAll.extend(splines)
        linesAll.extend(lines)
        integralsAll.extend(integrals)
        bunchNumAll.extend(bunchNum)
        peaks.clear()
        splines.clear()
        lines.clear()
        shiftedSplines.clear()
        integrals.clear()
        bunchNum.clear()
    
#    for i in range ( len(splines) ) :
#        shiftedVals, shiftedLine = shift_spline(i)
#        fig = plt.figure(dpi=100)
#        plt.plot(shiftedLine, shiftedVals, linewidth=1, color='b')
#        plt.plot(lines[i], splines[i](lines[i]), linewidth=1,  color='g')
    fig = plt.figure(dpi=100)
    plt.title("All shifted splines"+" Bunches: "+first+" to "+last)
    plt.ylabel(columnName)
    plt.xlabel("Probe [eV]")  
    for i in range ( len(splinesAll) ) :
        shiftedVals, shiftedLine = shift_spline(i, peaksAll, splinesAll, linesAll)
        shiftedSplines.append(shiftedVals)
        lo,hi = find_nearest_index(shiftedLine ,xLow, xHigh)
        shiftedLine = shiftedLine[lo:hi]
        shiftedVals = shiftedVals[lo:hi]
        plt.plot(shiftedLine, shiftedVals, linewidth=1)
   
    valAvg, lineAvg = average_vals(shiftedSplines, linesAll[0])
    lo,hi = find_nearest_index(lineAvg, xLow, xHigh)
    lineAvg = lineAvg[lo:hi]
    valAvg = valAvg[lo:hi]

    # head = "PhotonE\t"+"Average counts\n"
    fig = plt.figure(dpi=100)
    plt.title("Average spline "+"Bunches: "+first+"-"+last)
    plt.ylabel(columnName)
    plt.xlabel("Probe [eV]")
    plt.plot(lineAvg, valAvg, linewidth=1, color= 'r')
    
    integralsAll = [Int for bunch, Int in sorted( zip(bunchNumAll, integralsAll), key = lambda pair: pair[0] )]
    bunchNumAll.sort()
    bunchNumAll, integralsAll = average_integrals(bunchNumAll, integralsAll)
    timeDelayAll = np.multiply(2.0,bunchNumAll)
    fig_int = plt.figure(dpi=100)
    plt.title("All Integrals"+" Bunches: "+first+"-"+last+ " Integration: "+xLow+"-"+xHigh)
    plt.ylabel(columnName+" total ")
    plt.xlabel("Time Delay [ns]")
    plt.plot(timeDelayAll , integralsAll, marker = 'd')
    
    plt.show()
    plt.close()   
    return
###############################################################################        
if __name__ == "__main__":
    main()
