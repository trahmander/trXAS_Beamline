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
import sys
from datetime import datetime
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
from shift import (data_to_column, 
                   shift_spline,
                   get_deltas,
                   apply_shift)
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
                    transColumn,
                    firstBunch, 
                    lastBunch,
                    photonEnergyStart as xLow,
                    photonEnergyEnd as xHigh,
                    peakFindStart,
                    peakFindEnd,
                    offSet,
                    showIntegrals,
                    showSplines,
                    peaks,
                    splines,
#                    refSplines,
                    lines)
###############################################################################
###############################################################################
#Helper functions for main()
###############################################################################
def initialize():
    peaks.clear()
    splines.clear()
#    refSplines.clear()
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
def save_splines(shiftedEnergy, shiftedColumns, bunchNum, bunchNumAll, head, pathToFiles, log,  missingBunch, missingHeader):
    shiftedSplines= []
    shiftedLines= []
    paths = pathToFiles.keys()
    for bunch in bunchNum  :
        first = last = str(bunch)
        for path in  paths :
            try:
                f = select_files( pathToFiles[path], first, last )
                if len(f)==0:
                    missingBunch.append( path.strip(direct) )
            except:
                missingBunch.append( path.strip(direct) )
        avgColumns = []
        lineAvg=0      
        lineErr=0
        bunchIndices = [i for i,x in enumerate(bunchNumAll) if x == bunch]
        shiftedLines = [ shiftedEnergy[ind] for ind in bunchIndices]
         
        for j, col in enumerate( head[1:-1] ):

            shiftedSplines= [shiftedColumns[i][j] for i in bunchIndices ]
            title = col
            if showSplines and col in columnName:
                fig = plt.figure(dpi=100)
                plt.title(title+" Bunches: "+first+"-"+last)
                plt.ylabel(col)
                plt.xlabel("Probe [eV]")        
    
                if showSplines and col in columnName:
                    if col == transColumn:
                        plt.axvline(float(xLow), linestyle = "-.", linewidth = 0.5)
                        plt.axvline(float(xHigh), linestyle = "--", linewidth = 0.5)
                    if col == refColumn:
                        plt.axvline(float(peakFindStart), linestyle = "--", linewidth= 0.5, color = 'g' )
                        plt.axvline( float(peakFindEnd), linestyle = "--", linewidth= 0.5, color = 'g' )
                    for i in range( len(shiftedSplines) ):
                        plt.plot(shiftedLines[i], shiftedSplines[i], linewidth=0.5)
                        
            lineAvg, valAvg = average_vals(shiftedSplines, shiftedLines)
            lineErr, valErr = standard_error(shiftedSplines, shiftedLines, valAvg, lineAvg)
            if showSplines and col in columnName:
                plt.plot(lineAvg, valAvg, linestyle = "--", color = 'r', linewidth =1 )
            
            avgColumns.append(valAvg)
            avgColumns.append(valErr)
    
        avgColumns.insert(0, lineAvg)
        avgColumns.insert(1, lineErr)
        avgColumns = np.array(avgColumns)
        fileName = "avg"+"_bunch_"+first+"_"+last+".txt"
        hdr=""
        for col in head[:-1]:
            hdr += col+"\t"+"SE "+col+"\t"
        hdr = hdr[:-1]
        if not os.path.exists(saveDirectory):
            os.makedirs(saveDirectory)
        save_multicolumn(avgColumns, header = hdr, filename = saveDirectory+os.sep+fileName)
        print("Saved Bunch:\t"+first+"_"+last, file = log)
        print("Saved Bunch:\t"+first+"_"+last)
        if ( len(missingBunch)!=0 ):
            print("\tMissing bunch:\t"+str( sorted(missingBunch) ), file = log)
            missingBunch.clear()
    if ( len(missingHeader)!=0 ):
        print("\nMissing header:" + str( sorted(missingHeader) ), file = log)
    
    print( "\nLog End: "+ str( datetime.now() ), file = log )
    log.close()
    plt.show()
    plt.close()
    return
def save_integral( pathToFiles, bunchAll, shiftedEnergyAll, shiftedColumnsAll, head):
    # paths = pathToFiles.keys()
    start=0
    end= 0
    for path, files in  pathToFiles.items():
        title = path.strip(direct).split("_")[0]
        end  = end + len( files )
        
        bunch = bunchAll[start:end-1]
        shiftedColumns = shiftedColumnsAll[start:end-1]
        shiftedEnergy = shiftedEnergyAll[start:end-1]
        
        shiftedSplines = [ shiftedColumns[i][head.index(transColumn)] for i in range( len(shiftedColumns) ) ]
    #    stop=-1
    #    try:
    #    integrals=[]
    #    for e, s in zip(shiftedEnergy, shiftedSplines):
    #        integral = def_integral(e,s, xHigh, xLow )
    #        integrals.append(integral)
        integrals = [ def_integral( e,s, xHigh,xLow ) for e,s in zip(shiftedEnergy, shiftedSplines) ]
    #    except :
    #        print(stop)
        Int = [I for b, I in sorted( zip(bunch, integrals), key = lambda pair: pair[0] )]
        bunch.sort()
        bunch, Int = average_integrals(bunch, Int)
        timeDelay = np.zeros_like(bunch)
        for i, b in enumerate(bunch):
            if b > 0:
                timeDelay[i] = 2*b - offSet
            timeDelay[i] = 2*b + offSet
        if not os.path.exists(saveDirectory):
            os.makedirs(saveDirectory)
        saveFileName = os.path.normpath(saveDirectory +os.sep+ title+"_transient_"+xLow+"-"+xHigh+".txt" )
        save_file(timeDelay, "Time Delay [ns]", Int, transColumn+" sum", saveFileName)
        print("saved transient:\t"+title)
        if showIntegrals:
            fig_int = plt.figure(dpi=100)
            plt.title(title+"_transient: "+xLow+"-"+xHigh+" eV")
            plt.ylabel(columnName)
            plt.xlabel("Time Delay [ns]")
            plt.plot(timeDelay , Int, marker = 'd')
        start = end
    plt.show()
    plt.close()
    return
###############################################################################
###############################################################################
#Main driver function for trXAS package
###############################################################################
def main():
    initialize()
    missingBunch = []
    missingHeader = []
    log = saveDirectory+os.sep+"save_log_"+firstBunch+"_"+lastBunch+".txt"    
    print("",file= open(log, "w+"))
    log = open(log, "w+")
    print( "Log Start: "+ str( datetime.now() )+"\n", file = log )
    bunchNumAll = []
#    direct, column, first, last, xLow, xHigh = ask_user()
    paths = os.listdir(direct)
    for i in range( len(paths) ):
        paths[i] = os.path.join(direct, paths[i])
    for path in paths:
         if "avg" in path:
            paths.remove(path)
    dataFiles = get_data_files(paths[1])
    dataSet, head = load_file(dataFiles[0])
    refColumnNum = head.index(refColumn)
    
    pathToFiles = {}    
    for i  in range( len(paths) ):
        path = paths[i]
        dataFiles = get_data_files(path)
        dataFiles = select_files(dataFiles, first= firstBunch, last = lastBunch)
        pathToFiles[path] = dataFiles
        try:
            bunchNumAll.extend( get_selected_bunches(dataFiles) )
        except:
            continue
        file = dataFiles[0]
        if load_file(file, wantMissing=True) :
            missingHeader.append( file.split(os.sep)[-1] )
        dataSet, header = load_file(file)
        photonE = data_to_column(dataSet, refColumnNum, file, False)
    initialize()
    bunchNum = sorted(remove_dup(bunchNumAll))

    print("Bunches:\n" + str(bunchNum), file = log)
    print("Bunches:\n" + str(bunchNum),)
    print("Number of bunches:\t"+str( len(bunchNum) )+"\n", file = log )
    print("Loading files...")
    for path in paths:
        dataFiles = get_data_files(path)
        dataFiles = select_files(dataFiles, first = firstBunch, last = lastBunch)
        for i in range(len(dataFiles)):
            skip=1
            findPeak=True
            file = dataFiles[i]
            dataSet, header = load_file(file, skip=skip)
            if i!=0:
                findPeak = False
                peaks.append(peaks[-1])
            photonE = data_to_column(dataSet, refColumnNum, file, findPeak)

    deltas = get_deltas(peaks)
    shiftedEnergy, shiftedColumns = apply_shift(deltas, splines, lines )
    
#    print("Starting column saves...")
#    save_splines(shiftedEnergy, shiftedColumns, bunchNum,bunchNumAll, head, pathToFiles, log, missingBunch, missingHeader)
    print("Starting saving integrals...")
    
#    start=0
#    end= 0
#    for path, files in  pathToFiles.items():
#        title = path.strip(direct).split("_")[0]
#        end  = end + len( files )
    save_integral( pathToFiles, bunchNumAll, shiftedEnergy, shiftedColumns, head)
#        start = end
#    return 
###############################################################################        
if __name__ == "__main__":
    main()
