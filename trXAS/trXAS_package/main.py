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
                        save_multicolumn,
                        bin_data)
from shift import (photonE_counts_plot, 
                   shift_spline)
# from shift import shift_lists
from integrate import (def_integral, 
                       average_integrals, 
                       find_nearest_bounds,
                       remove_dup)
from average import (average_vals,
                     standard_error)
# Load global variables. These are also used in shift.py
import config
from config import (openDirectory as direct,
                    saveDirectory,
                    column as columnName,
                    refColumn,
                    firstBunch as first, 
                    lastBunch as last,
                    photonEnergyStart as xLow,
                    photonEnergyEnd as xHigh,
                    showIntegrals,
                    showSplines,
                    peaks,
                    splines,
                    refSplines,
                    lines)
###############################################################################
###############################################################################
#Helper functions for main()
###############################################################################
def initialize():
    peaks.clear()
    splines.clear()
    refSplines.clear()
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
def plot_spline(splines, peaks, lines, title, columnName, shiftedSplines, rawEnergy= [], integrals=False):
    if showSplines:
        fig = plt.figure(dpi=100)
        plt.title(title+" Bunches: "+first+"-"+last)
        plt.ylabel(columnName)
        plt.xlabel("Probe [eV]")        
    for k in range ( len(splines) ):
        shiftedVals, shiftedLine = shift_spline(k, peaks, splines, lines)
        shiftedSplines.append(shiftedVals)
        if integrals != False:
            integral= def_integral(shiftedLine, shiftedVals, xLow, xHigh)
            integrals.append(integral)
        if showSplines :
            lo, hi = find_nearest_bounds(shiftedLine ,xLow, xHigh)
            shiftedLine = shiftedLine[lo:hi]
            shiftedVals = shiftedVals[lo:hi]
            plt.plot(shiftedLine, shiftedVals, linewidth=0.5)   
    lineAvg, valAvg = average_vals(shiftedSplines)
    if len(rawEnergy) != 0  :
        save_spline(lineAvg, valAvg, title, columnName, rawEnergy)
    print("saved spline:\t"+title)
    if showSplines:    
        lo,hi = find_nearest_bounds(lineAvg, xLow, xHigh)
        lineAvg = lineAvg[lo:hi]
        valAvg = valAvg[lo:hi]
        plt.plot(lineAvg, valAvg, linewidth=2, linestyle="--", color = 'r')
    return
def save_spline(xVals, yVals, title, columnName, xOrig):
    if not os.path.exists(saveDirectory):
        os.makedirs(saveDirectory)
    saveFileName = os.path.normpath(saveDirectory +os.sep+ title+"_"+columnName+"_bunch_"+first+"-"+last )
    save_file(xVals, "Photon E [eV]", yVals, columnName, saveFileName+".txt")
#    xVals, yVals = bin_data(xVals, yVals, xOrig)
#    save_file(xVals, "Photon E [eV]", yVals, columnName+" sum", saveFileName+"_binned.txt")    
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
    first = config.firstBunch
    last = config.lastBunch
    bunchNumAll = []
#    direct, column, first, last, xLow, xHigh = ask_user()
    paths = os.listdir(direct)
    for i in range( len(paths) ):
        paths[i] = os.path.join(direct, paths[i])
    for path in paths:
         if "avg" in path:
            paths.remove(path)
    for i  in range( len(paths) ):
        path = paths[i]
        dataFiles = get_data_files(path)
        dataFiles = select_files(dataFiles, first = first, last = last)
        bunchNumAll.extend( get_selected_bunches(dataFiles) )
        bunchNumAll = remove_dup(bunchNumAll)
    
    dataFiles = get_data_files(paths[1])
#    dataFiles = select_files(dataFiles, first = "1", last = "1")
#    bunchNumAll = get_selected_bunches(dataFiles,first = first, last = last)
    dataSet, header = load_file(dataFiles[0])
    refColumnNum = header.index(refColumn)
    bunchNumAll = sorted(bunchNumAll)
    print(bunchNumAll)
    print("Number of bunches:\t"+str( len(bunchNumAll) ) )
    
    peaksAll=[]
    splinesAll=[]
    linesAll=[]
    integralsAll=[]
#    bunchNumAll=[137]
#    bunchNum = []
    
    while ( len(bunchNumAll) != 0 ) :
       
        bunch = bunchNumAll[0]
        first = last = str(bunch)
#        print("Bunch: "+first+"-"+last)
        avgColumns = []
        lineAvg=0      
        lineErr=0
        
        for col in header[1:-1] :
            shiftedSplinesAll = []
            rawEnergy = []
            integrals=[]
            shiftedSplines=[]
            shiftedLines=[]
            title = col
            if showSplines:
                fig = plt.figure(dpi=100)
                plt.title(title+" Bunches: "+first+"-"+last)
                plt.ylabel(col)
                plt.xlabel("Probe [eV]")        
            for j in range( len(paths) ) :            
                path = paths[j]
                dataFiles = get_data_files(path)
                try:
                    dataFiles = select_files(dataFiles, first = first, last = last)
                    dataSet, header = load_file(dataFiles[0])
                except:
                    print("Missing Bunch:\t"+first+"-"+last+"\n\t at:\t"+path.strip(direct))
                    continue
#                bunchNum =  get_selected_bunches(dataFiles)
    
                
        #        columnName = header[column]
                try:
                    columnNum = header.index(col)
                except:
                    print("Missing header:\t"+col+"\n\t at:\t"+path.strip(direct)+" Bunch:\t"+first+"-"+last)
#                refColumnNum = header.index(refColumn)            
                for i in range(len(dataFiles)):
                    file = dataFiles[i]
                    dataSet, header = load_file(file)
                    try:
                        photonE = photonE_counts_plot(dataSet, refColumnNum, columnNum, file)
                    except:
                        print("Missing Column:\t"+col+"\n\t at:\t"+file.strip(direct))
                        continue
                    rawEnergy.append(photonE)
           
                for k in range ( len(splines) ):
                    shiftedVals, shiftedLine = shift_spline(k, peaks, splines, lines)
                    shiftedSplines.append(shiftedVals)
                    shiftedLines.append(shiftedLine)
                    
    #                    integral= def_integral(shiftedLine, shiftedVals, xLow, xHigh)
    #                    integrals.append(integral)
    
        #        save_integral(bunchNum, integrals, title)
    
                if showSplines :
                    lo, hi = find_nearest_bounds(shiftedLine ,xLow, xHigh)
                    shiftedLine = shiftedLine[lo:hi]
                    shiftedVals = shiftedVals[lo:hi]
                    plt.plot(shiftedLine, shiftedVals, linewidth=0.5)
            
            peaksAll.extend(peaks)
            splinesAll.extend(splines)
            linesAll.extend(lines)
            integralsAll.extend(integrals)
    #            bunchNumAll.extend(bunchNum)
            shiftedSplinesAll.append(shiftedSplines)
            
            lineAvg, valAvg = average_vals(shiftedSplines, shiftedLines)
            lineErr, valErr = standard_error(shiftedSplines, shiftedLines, valAvg, lineAvg)
    #            valAvg = valAvg.tolist()
    
            avgColumns.append(valAvg)
            avgColumns.append(valErr)
    
#            print("Saved:\t"+col)
            if showSplines:    
                lo,hi = find_nearest_bounds(lineAvg, xLow, xHigh)
                lineAvg = lineAvg[lo:hi]
                valAvg = valAvg[lo:hi]
                plt.plot(lineAvg, valAvg, linewidth=2, linestyle="--", color = 'r')
                
            
            peaks.clear()
            splines.clear()
            lines.clear()
            rawEnergy.clear()
            shiftedSplines.clear()
            integrals.clear()
#            bunchNum.clear()
            shiftedLines.clear()
    
        avgColumns.insert(0, lineAvg)
        avgColumns.insert(1, lineErr)
        avgColumns = np.array(avgColumns)
        fileName = "avg"+"_bunch_"+first+"-"+last+".txt"
        head=""
        for col in header[:-1]:
            head += col+"\t"+"SE "+col+"\t"
        head = head[:-1]
        save_multicolumn(avgColumns, header = head, filename = saveDirectory+os.sep+fileName)
        print("Saved Bunch:\t"+first+"-"+last)
        bunchNumAll.remove(bunch)

#        if len(bunchNumAll)==0:
#            break        
#    plot_spline(splinesAll, peaksAll, linesAll, "All Splines", shiftedSplines)   
#    save_integral(bunchNumAll, integralsAll, "All Integrals")

    return
###############################################################################        
if __name__ == "__main__":
    main()
