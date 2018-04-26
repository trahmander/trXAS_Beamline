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
import numpy as np
from matplotlib import pyplot as plt
from user_input import (user_directory,  
                        user_column,
                        user_column_name,
                        user_bunches,
                        user_integration_bounds)
from load_files import (get_data_files,
                        load_file,
                        select_files,
                        get_selected_bunches,
                        save_file,
                        bin_data)
from shift import (photonE_counts_plot, 
                   shift_spline)
# from shift import shift_lists
from integrate import (def_integral, 
                       average_integrals, 
                       find_nearest_bounds)
from average import average_vals
# Load global variables. These are also used in shift.py
from config import (openDirectory as direct,
                    saveDirectory,
                    column as columnName,
                    firstBunch as first, 
                    lastBunch as last,
                    photonEnergyStart as xLow,
                    photonEnergyEnd as xHigh,
                    showPlots,
                    peaks,
                    splines,
                    lines)
###############################################################################
def initialize():
    peaks.clear()
    splines.clear()
    lines.clear()
    return
def ask_user():
    direct = user_directory()
#    column = user_column()
    column = user_column_name()
    first, last = user_bunches()
    xLow, xHigh = user_integration_bounds()
#    pump = user_pump()
#    probe = user_probe()
#    sample = user_sample()
    return direct, column, first, last, xLow, xHigh
def plot_spline(splines, peak, lines, title, shiftedSplines, integrals=False):
    if showPlots:
        fig = plt.figure(dpi=100)
        plt.title(title+" Bunches: "+first+"-"+last)
        plt.ylabel(columnName)
        plt.xlabel("Probe [eV]")        
    for k in range ( len(splines) ):
        shiftedVals, shiftedLine = shift_spline(k, peak, splines, lines)
        shiftedSplines.append(shiftedVals)
        lo, hi = find_nearest_bounds(shiftedLine ,xLow, xHigh)
        shiftedLine = shiftedLine[lo:hi]
        shiftedVals = shiftedVals[lo:hi]
        plt.plot(shiftedLine, shiftedVals, linewidth=0.5)
        
        if integrals != False:
            integral= def_integral(shiftedLine, shiftedVals, xLow, xHigh)
            integrals.append(integral)   
    valAvg, lineAvg = average_vals(shiftedSplines, lines[0])
#    save_spline(lineAvg, valAvg, xOrig)
    if showPlots:    
        lo,hi = find_nearest_bounds(lineAvg, xLow, xHigh)
        lineAvg = lineAvg[lo:hi]
        valAvg = valAvg[lo:hi]
        plt.plot(lineAvg, valAvg, linewidth=2, linestyle="--", color = 'r')
    return
def save_spline(xVals, yVals, xOrig):
    saveFileName = os.path.normpath(saveDirectory +os.sep+ title+"_int_"+xLow+"-"+xHigh )
    save_file(xVals, "Photon E [eV]", Int, columnName+" sum", saveFileName+".txt")
    xVals, yVals = bin_data(xVals, yVals, xOrig)
    save_file(xVals, "Photon E [eV]", Int, columnName+" sum", saveFileName+"_binned.txt")    
    return
def save_integral(bunch, Int, title):
    Int = [I for b, I in sorted( zip(bunch, Int), key = lambda pair: pair[0] )]
    bunch.sort()
    bunch, Int = average_integrals(bunch, Int)
    timeDelay = np.multiply(2.0,bunch)
    if not os.path.exists(saveDirectory):
        os.makedirs(saveDirectory)
    saveFileName = os.path.normpath(saveDirectory +os.sep+ title+"_int_"+xLow+"-"+xHigh+".txt" )
    save_file(timeDelay, "Time Delay [ns]", Int, columnName+" sum", saveFileName)
    if showPlots:
        fig_int = plt.figure(dpi=100)
        plt.title(title+" Bunches: "+first+"-"+last+ " Integration: "+xLow+"-"+xHigh)
        plt.ylabel(columnName)
        plt.xlabel("Time Delay [ns]")
        plt.plot(timeDelay , Int, marker = 'd')
    return
###############################################################################
#Main driver function for trXAS package
###############################################################################
def main():
    initialize()
#    direct, column, first, last, xLow, xHigh = ask_user()
    paths = os.listdir(direct)
    for i in range( len(paths) ):
        paths[i] = os.path.join(direct, paths[i])
    for path in paths:
         if "avg" in path:
            paths.remove(path)
    peaksAll=[]
    splinesAll=[]
    linesAll=[]
    integralsAll=[]
    bunchNumAll=[] 
    for j in range( len(paths) ) :
        integrals=[]
        shiftedSplines=[]
        path = paths[j]
        dataFiles = get_data_files(path)
        dataFiles = select_files(dataFiles, first = first, last = last)
        bunchNum= get_selected_bunches(dataFiles, first = first, last = last)
        dataSet, header = load_file(dataFiles[0])
#        columnName = header[column]
        columnNum = header.index(columnName)
       

        for i in range(len(dataFiles)):
            file = dataFiles[i]
            dataSet, header = load_file(file)            
            photonE_counts_plot(dataSet, columnNum, file)
        title = path.strip(direct)
        plot_spline(splines, peaks, lines, title, shiftedSplines, integrals)
#        fig = plt.figure(dpi=100)
#        plt.title(title+" Bunches: "+first+"-"+last)
#        plt.ylabel(columnName)
#        plt.xlabel("Probe [eV]")        
#        for k in range ( len(splines) ):
#            shiftedVals, shiftedLine = shift_spline(k, peaks, splines, lines)
#            shiftedSplines.append(shiftedVals)
#            lo, hi = find_nearest_bounds(shiftedLine ,xLow, xHigh)
#            shiftedLine = shiftedLine[lo:hi]
#            shiftedVals = shiftedVals[lo:hi]
#            plt.plot(shiftedLine, shiftedVals, linewidth=0.5)
#           
#            integral= def_integral(shiftedLine, shiftedVals, xLow, xHigh)
#            integrals.append(integral)   
#        valAvg, lineAvg = average_vals(shiftedSplines, lines[0])
#        lo,hi = find_nearest_bounds(lineAvg, xLow, xHigh)
#        lineAvg = lineAvg[lo:hi]
#        valAvg = valAvg[lo:hi]
#        plt.plot(lineAvg, valAvg, linewidth=2, linestyle="--", color = 'r')
        
        peaksAll.extend(peaks)
        splinesAll.extend(splines)
        linesAll.extend(lines)
        integralsAll.extend(integrals)
        bunchNumAll.extend(bunchNum)
        
        save_integral(bunchNum, integrals, title)
       
        peaks.clear()
        splines.clear()
        lines.clear()
        shiftedSplines.clear()
        integrals.clear()
        bunchNum.clear()
    plot_spline(splinesAll, peaksAll, linesAll, "All Splines", shiftedSplines)
#    fig = plt.figure(dpi=100)
#    plt.title("All splines"+" Bunches: "+first+"-"+last)
#    plt.ylabel(columnName)
#    plt.xlabel("Probe [eV]")  
#    for i in range ( len(splinesAll) ) :
#        shiftedVals, shiftedLine = shift_spline(i, peaksAll, splinesAll, linesAll)
#        shiftedSplines.append(shiftedVals)
#        lo,hi = find_nearest_bounds(shiftedLine ,xLow, xHigh)
#        shiftedLine = shiftedLine[lo:hi]
#        shiftedVals = shiftedVals[lo:hi]
#        plt.plot(shiftedLine, shiftedVals, linewidth=0.5)
#   
#    valAvg, lineAvg = average_vals(shiftedSplines, linesAll[0])
#    lo,hi = find_nearest_bounds(lineAvg, xLow, xHigh)
#    lineAvg = lineAvg[lo:hi]
#    valAvg = valAvg[lo:hi]
#    plt.plot(lineAvg, valAvg, linewidth=2, linestyle = "--", color= 'r')

#    fig = plt.figure(dpi=100)
#    plt.title("Average spline "+"Bunches: "+first+"-"+last)
#    plt.ylabel(columnName)
#    plt.xlabel("Probe [eV]")
#    plt.plot(lineAvg, valAvg, linewidth=1, color= 'r')
    
    save_integral(bunchNumAll, integralsAll, "All Integrals")

    return
###############################################################################        
if __name__ == "__main__":
    main()
