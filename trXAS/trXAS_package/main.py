# -*- coding: utf-8 -*-
"""
use: Average and shift the  trXAS data by bunch number. Also integrate the data in a region of interest.
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
                    showIntegrals,
                    showSplines,
                    peaks,
                    splines,
                    lines)
###############################################################################
###############################################################################
#Helper functions for main()
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
def plot_spline(splines, peak, lines, title, shiftedSplines, rawEnergy= [], integrals=False):
    if showSplines:
        fig = plt.figure(dpi=100)
        plt.title(title+" Bunches: "+first+"-"+last)
        plt.ylabel(columnName)
        plt.xlabel("Probe [eV]")        
    for k in range ( len(splines) ):
        shiftedVals, shiftedLine = shift_spline(k, peak, splines, lines)
        shiftedSplines.append(shiftedVals)
        if integrals != False:
            integral= def_integral(shiftedLine, shiftedVals, xLow, xHigh)
            integrals.append(integral)
        if showSplines :
            lo, hi = find_nearest_bounds(shiftedLine ,xLow, xHigh)
            shiftedLine = shiftedLine[lo:hi]
            shiftedVals = shiftedVals[lo:hi]
            plt.plot(shiftedLine, shiftedVals, linewidth=0.5)   
    valAvg, lineAvg = average_vals(shiftedSplines, lines[0])
    if len(rawEnergy) != 0  :
        save_spline(lineAvg, valAvg, title, rawEnergy)
    print("saved spline:\t"+title)
    if showSplines:    
        lo,hi = find_nearest_bounds(lineAvg, xLow, xHigh)
        lineAvg = lineAvg[lo:hi]
        valAvg = valAvg[lo:hi]
        plt.plot(lineAvg, valAvg, linewidth=2, linestyle="--", color = 'r')
    return
def save_spline(xVals, yVals, title, xOrig):
    if not os.path.exists(saveDirectory):
        os.makedirs(saveDirectory)
    saveFileName = os.path.normpath(saveDirectory +os.sep+ title+"_bunch_"+first+"-"+last )
    save_file(xVals, "Photon E [eV]", yVals, columnName+" sum", saveFileName+".txt")
    xVals, yVals = bin_data(xVals, yVals, xOrig)
    save_file(xVals, "Photon E [eV]", yVals, columnName+" sum", saveFileName+"_binned.txt")    
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
    print("saved integral:\t"+title)
    if showIntegrals:
        fig_int = plt.figure(dpi=100)
        plt.title(title+" Bunches: "+first+"-"+last+ " Integration: "+xLow+"-"+xHigh)
        plt.ylabel(columnName)
        plt.xlabel("Time Delay [ns]")
        plt.plot(timeDelay , Int, marker = 'd')
    return
###############################################################################
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
    shiftedSplinesAll = []
    for j in range( len(paths) ) :
        rawEnergy = []
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
            photonE = photonE_counts_plot(dataSet, columnNum, file)
            rawEnergy.append(photonE)
        title = path.strip(direct)
        plot_spline(splines, peaks, lines, title, shiftedSplines, rawEnergy[0], integrals)
        
        # Puts data for each scan in a bigger list for all the scans in the chosen directory.
        peaksAll.extend(peaks)
        splinesAll.extend(splines)
        linesAll.extend(lines)
        integralsAll.extend(integrals)
        bunchNumAll.extend(bunchNum)
        shiftedSplinesAll.extend(shiftedSplines)
        
        save_integral(bunchNum, integrals, title)
        #Clears data for this scan after it has been used.
        peaks.clear()
        splines.clear()
        lines.clear()
        rawEnergy.clear()
        shiftedSplines.clear()
        integrals.clear()
        bunchNum.clear()
        
    plot_spline(splinesAll, peaksAll, linesAll, "All Splines", shiftedSplines)   
    save_integral(bunchNumAll, integralsAll, "All Integrals")

    return
###############################################################################        
if __name__ == "__main__":
    main()
