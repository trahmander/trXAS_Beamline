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
from datetime import datetime
from timeit import default_timer as timer
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
from matplotlib import pyplot as plt
#From modules in trXAS_package
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
                   find_peak,
                   find_center,
                   shift_spline,
                   get_deltas,
                   diff_deltas,
                   apply_shift)
# from shift import shift_lists
from integrate import (def_integral, 
                       average_integrals, 
                       find_nearest_bounds,
                       remove_dup,
                       exp)
from average import (average_vals,
                     standard_error,
                     cut_splines)
# Load global variables. These are also used in shift.py
from config import (openDirectory as direct,
#                    saveDirectory,
                    column as columnName,
                    refColumn,
                    transColumn,
                    firstBunch, 
                    lastBunch,
                    photonEnergyStart as xLow,
                    photonEnergyEnd as xHigh,
                    shiftPeak,
                    shiftCenter,
                    shiftMinimize,
                    shiftNone,
                    peakFindStart,
                    peakFindEnd,
                    offSet,
                    saveTransients,
                    showTransients,
                    saveSplines,
                    showSplines,
#                    peaks,
                    splines,
#                    refSplines,
                    lines)
###############################################################################
###############################################################################
#Helper functions for main()
###############################################################################
def initialize():
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
def save_splines(shiftedEnergy, shiftedColumns, bunchNum, bunchNumAll, head, pathToFiles, log,  missingBunch, missingHeader, saveDirectory):
    print("Computing shifts...")
#    print(len(shiftedColumns)  )
#    shiftedSplines= []
#    shiftedLines= []
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
#        print(bunchIndices)
        shiftedLines = [ shiftedEnergy[ind] for ind in bunchIndices]
#        shiftedLines = cut_splines(shiftedLines,deltas)
         
        for j, col in enumerate( head[1:-1] ):

            shiftedSplines= [shiftedColumns[i][j] for i in bunchIndices ]
#            shiftedSplines = cut_splines(shiftedSplines, deltas)
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
#            print(title+" Bunches: "+first+"-"+last)
#            print(valAvg)
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
#        if not os.path.exists(saveDirectory):
#            os.makedirs(saveDirectory)
        save_multicolumn(avgColumns, header = hdr, filename = saveDirectory+os.sep+fileName)
        print("Saved Bunch:\t"+first+"_"+last, file = log)
        print("Saved Bunch:\t"+first+"_"+last)
        if ( len(missingBunch)!=0 ):
            print("\tMissing bunch:\t"+str( sorted(missingBunch) ), file = log)
            missingBunch.clear()
    if ( len(missingHeader)!=0 ):
        print("\nMissing header:" + str( sorted(missingHeader) ), file = log)
    
    print( "\nSaving Shifts: "+ str( datetime.now() ), file = log )
#    log.close()
    plt.show()
    plt.close()
    return
def compute_integral( title, pathToFiles, head, transientColumns, bunch, shiftedEnergy, shiftedColumns, binning=1):        
    transIndex = head.index(transColumn)
    shiftedSplines = [ shiftedColumns[i][transIndex] for i in range( len(shiftedColumns) ) ]
#    shiftedSplines = cut_splines(shiftedSplines, deltas)
#    shiftedEnergy = cut_splines(shiftedEnergy,deltas)
    integrals = [ def_integral( e,s, xHigh,xLow ) for e,s in zip(shiftedEnergy, shiftedSplines) ]
#    print(bunch)
    bunch, Int = average_integrals(bunch, integrals)
    Int = [ I for b, I in sorted( zip(bunch, Int), key = lambda pair: pair[0] ) ]
    bunch.sort()
    timeDelay =[ (2*b - offSet) if b>0 else (2*b + offSet) for b in bunch]
#    print(timeDelay)

#    if not os.path.exists(saveDirectory):
#        os.makedirs(saveDirectory)
    transientColumns.append( timeDelay )
    transientColumns.append( Int )
    print("saved transient:\t"+title)
#    opt, cov = curve_fit(exp, timeDelay, Int, p0=[0.1, 10.0, offSet] )
#    print( "A="+str(opt[0])+"\nT="+str(opt[1])+"\nt0="+str(opt[2]) )
    if showTransients:
        fig_int = plt.figure(dpi=100)
        plt.title(title+"_transient: "+xLow+"-"+xHigh+" eV")
        plt.ylabel(transColumn+" sum ")
        plt.xlabel("Time Delay [ns]")
        plt.plot(timeDelay , Int, marker = 'd')
#        plt.plot(timeDelay, exp(timeDelay, opt[0], opt[1], opt[2]) )
    return
def save_integral(pathToFiles, head, bunchNumAll, shiftedEnergy, shiftedColumns, log, saveDirectory):
    print("Computing transients...")
    transCol=[]
    header = "Delay[ns]\tAvg Transient\t"
    compute_integral(saveDirectory.split(os.sep)[-1], pathToFiles, head, transCol, 
                      bunchNumAll, 
                      shiftedEnergy, 
                      shiftedColumns )
    start=0
    end= 0
    for path, files in  pathToFiles.items():
        title = path.split(os.sep)[-1].split("_")[0]
        header += title+" Delay[ns]\t"+title+" Transient\t"
        end  = start + len( files )
        compute_integral(title, pathToFiles, head, transCol, 
                      bunchNumAll[start:end], 
                      shiftedEnergy[start:end], 
                      shiftedColumns[start:end] )
        start = end

    header = header[:-1]
    transCol = pd.DataFrame(transCol).values
    if not os.path.exists(saveDirectory):
        os.makedirs(saveDirectory)
    fileName = "transient_"+xHigh+"_"+xLow+"_bunch_"+firstBunch+"_"+lastBunch+".txt"
    save_multicolumn(transCol, header, saveDirectory + os.sep + fileName)
    print( "\nSaved Transients: "+ str( datetime.now() ), file = log )
#    plt.show()
#    plt.close()                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    )
    return
###############################################################################
###############################################################################
#Main driver function for trXAS package
###############################################################################
def main():
    startTime = timer()
    initialize()
    missingBunch = []
    missingHeader = []
    
    bunchNumAll = []
#    direct, column, first, last, xLow, xHigh = ask_user()

    paths = os.listdir(direct)
    paths = [ os.path.join(direct, p) for p in paths if not "avg" in p ]
    saveDirectory= direct+os.sep
    for p in paths:
        saveDirectory += ( p.split(os.sep)[-1].split("_")[0] ) + "_"
    saveDirectory +="avg"
    if not os.path.exists(saveDirectory):
        os.makedirs(saveDirectory)
    log = saveDirectory+os.sep+"save_log_"+firstBunch+"_"+lastBunch+".txt"    
    print("",file= open(log, "w+"))
    log = open(log, "w+")
    print( "Log Start: "+ str( datetime.now() )+"\n", file = log )
    dataFiles = get_data_files(paths[1])
    dataSet, head = load_file(dataFiles[0])
    refColumnNum = head.index(refColumn)
#   Load the data sets of all the scans and get the bunches found. Calculates
#   the splines for splines for reference column from first file in scan.
    pathToFiles = {} 
    
    for path  in paths :
        dataFiles = get_data_files(path)
        dataFiles = select_files(dataFiles, first= firstBunch, last = lastBunch)
        pathToFiles[path] = dataFiles
        try:
            newBunch = get_selected_bunches(dataFiles)
#            print(newBunch)
            bunchNumAll.extend( newBunch )
        except:
            continue
        file = dataFiles[0]
        dataSet, header = load_file(file)
        refSpline= data_to_column(dataSet, refColumnNum, file)
    initialize()
    bunchNum = sorted(remove_dup(bunchNumAll))
    print("Bunches:\n" + str(bunchNum), file = log)
    print("Bunches:\n" + str(bunchNum),)
    print("Number of bunches:\t"+str( len(bunchNum) )+"\n", file = log )
#   calculates the linear interpolation and finds reference peaks from reference column.  
    print("Loading files...")
    refPeaks=[]
    refCenters= []
    refSplines = []
    refLines = []
    scanSize=[]
    for path in paths:
        dataFiles = get_data_files(path)
        dataFiles = select_files(dataFiles, first = firstBunch, last = lastBunch)
        scanSize.append( len(dataFiles) )
        for i in range(len(dataFiles)):
            skip=1
#            findPeak=True
            file = dataFiles[i]
            if load_file(file, wantMissing=True) :
                missingHeader.append( file.split(os.sep)[-1] )
            dataSet, header = load_file(file, skip=skip)
            refSpline = data_to_column(dataSet, refColumnNum, file)
            if i!=0:
#                findPeak = False
                if shiftPeak or shiftMinimize:
                    refPeaks.append(refPeaks[-1])
                elif shiftCenter or shiftMinimize:
                     refCenters.append(refCenters[-1])
#                if shiftMinimize:
#                    refSplines.append( refSplines[-1] )
#                    refLines.append( refLines[-1] )
            else:
#                refSpline = data_to_column(dataSet, refColumnNum, file)
                if shiftPeak or shiftMinimize:
                    refPeaks.append( find_peak(refSpline) )
                elif shiftCenter or shiftMinimize:
                    refCenters.append( find_center(lines[-1], refSpline) )
                if shiftMinimize:
                    refSplines.append( splines[-1] )
                    refLines.append( lines[-1] )
                else:
                    break
            
#   shifts every column based on deltas calculated from reference column
#    print(refCenters)
    if shiftPeak:
        deltas = get_deltas(refPeaks)
        print("peak matching shift")
    elif shiftCenter:
        deltas = get_deltas(refCenters)
        print("geometric center matching shift")
    elif shiftMinimize:
        deltas = diff_deltas(refSplines, refLines, scanSize, refPeaks, header.index(refColumn)-1)
        print("least squares minimizing shift")
    if shiftNone :
        deltas = np.zeros_like(lines)
        print("No shift")
#    print( len(paths)  )
#    print(  deltas  )
#    print(refPeaks)
#    print( np.array(refPeaks) - np.array(deltas) )
#    print( len(lines) )
#    print( len(splines) )
    shiftedEnergy, shiftedColumns = apply_shift(deltas, splines, lines )
    shiftedEnergy = cut_splines(shiftedEnergy,deltas)
    shiftedColumns = [ cut_splines(column, deltas) for column in shiftedColumns ]
#   averages and saves collumns from scans.
    if saveSplines:
        save_splines(shiftedEnergy, shiftedColumns, bunchNum,bunchNumAll, head, pathToFiles, log, missingBunch, missingHeader, saveDirectory)
#   averages and saves transients from all scans. Also saves each individual scan.
    if saveTransients:
        save_integral(pathToFiles, head, bunchNumAll, shiftedEnergy, shiftedColumns, log, saveDirectory)
    log.close()
    endTime = timer()
    print( "Time:\t"+ str(endTime - startTime) )
    plt.show()
    plt.close()
    return 
###############################################################################        
if __name__ == "__main__":
    main()
