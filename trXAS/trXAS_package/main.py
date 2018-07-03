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
# from user_input import (user_directory,  
#                         user_column,
#                         user_column_name,
#                         user_bunches,
#                         user_integration_bounds)
from load_files import (get_data_files,
                        load_file,
                        select_files,
                        select_data,
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
from integrate import (def_integral, 
                       average_integrals, 
                       find_nearest_bounds,
                       remove_dup,
                       exp)
from average import (average_vals,
                     standard_error,
                     sum_error,
                     cut_splines,
                     chunk_list,
                     remove_outliers)
# Load global variables. These are also used in shift.py
from config import (openDirectory as direct,
                    column as columnName,
                    refColumn,
                    transColumn,
                    firstBunch, 
                    lastBunch,
                    averageStart,
                    averageEnd,
                    averageBinning,
                    photonEnergyStart as xLow,
                    photonEnergyEnd as xHigh,
                    shiftPeak,
                    shiftCenter,
                    shiftMinimize,
                    shiftNone,
                    peakFindStart,
                    peakFindEnd,
                    literaturePeakValue,
                    offSet,
                    saveTransients,
                    showTransients,
                    saveSplines,
                    showSplines,
                    saveAverage,
                    splines,
                    lines)
###############################################################################
###############################################################################
#Helper functions for main()
###############################################################################
def initialize():
    splines.clear()
    lines.clear()
    return
# def ask_user():
#     direct = user_directory()
# #    column = user_column()
#     column = user_column_name()
#     first, last = user_bunches()
#     xLow, xHigh = user_integration_bounds()
# #    pump = user_pump()
# #    probe = user_probe()
# #    sample = user_sample()
#     return direct, column, first, last, xLow, xHigh
def save_splines(shiftedEnergy, shiftedColumns, bunchNum, bunchNumAll, head, pathToFiles, log,  missingBunch, missingHeader, saveDirectory, litDiff):
    print("Computing shifts...")
    
    paths = pathToFiles.keys()
    averageSplines = []
    averageBunches= []
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
                    plt.axhline(0, linestyle = "-", color= "grey")
                    if col == transColumn and bool( float(xLow) ):
                        plt.axvline(float(xLow), linestyle = "-.", linewidth = 0.5)
                        plt.axvline(float(xHigh), linestyle = "-.", linewidth = 0.5)
                    if col == refColumn and bool( float(peakFindStart) ):
                        plt.axvline(float(peakFindStart)-litDiff, linestyle = "-.", linewidth= 0.5, color = 'g' )
                        plt.axvline( float(peakFindEnd)-litDiff, linestyle = "-.", linewidth= 0.5, color = 'g' )
                        for i in range( len(shiftedSplines) ):
                            plt.plot(shiftedLines[i], shiftedSplines[i], linewidth=0.5, linestyle = "--")
                        
            lineAvg, valAvg = average_vals(shiftedSplines, shiftedLines)

            lineErr, valErr = standard_error(shiftedSplines, shiftedLines, valAvg, lineAvg)
            if showSplines and col in columnName:
                plt.plot(lineAvg, valAvg, linestyle = "-", linewidth =1.5 )
            
            avgColumns.append(valAvg)
            avgColumns.append(valErr)
    
        avgColumns.insert(0, lineAvg)
        avgColumns.insert(1, lineErr)
        avgColumns = np.array(avgColumns)
        if saveAverage and bunch >= int(averageStart) and bunch <= int(averageEnd):
            averageSplines.append(avgColumns)
            averageBunches.append(bunch)
        fileName = "avg"+"_bunch_"+first+"_"+last+".txt"
        hdr=""
        for col in head[:-1]:
            hdr += col+"\t"+"SE "+col+"\t"
        hdr = hdr[:-1]
        if not os.path.exists(saveDirectory):
           os.makedirs(saveDirectory)
        save_multicolumn(avgColumns, header = hdr, filename = saveDirectory+os.sep+fileName, com = '')
        print("Saved Bunch:\t"+first+"_"+last, file = log)
        print("Saved Bunch:\t"+first+"_"+last)
        if ( len(missingBunch)!=0 ):
            print("\tMissing bunch:\t"+str( sorted(missingBunch) ), file = log)
            missingBunch.clear()
    if ( len(missingHeader)!=0 ):
        print("\nMissing header:" + str( sorted(missingHeader) ), file = log)
    
    print( "\nSaving Shifts: "+ str( datetime.now() ), file = log )
    if showSplines:
        plt.show()
        plt.close()
    if saveAverage:
        avg_bunches(averageSplines, averageBunches,head, averageStart, averageEnd, saveDirectory, binning=int(averageBinning) )
    return
def avg_bunches(dataSets, bunches, head, first, last, saveDirectory, binning=1):
    print("Averaging bunches:\t"+str(first)+"-"+str(last) )
    print(bunches)
    if binning == 1:
        return
    else:
        saveDirectory = os.path.normpath(saveDirectory + os.sep + "binned_avg")
        if not os.path.exists(saveDirectory):
            os.makedirs(saveDirectory)
 
        head = head[:-1]
        hd = []
        for h in head:
            hd.append(h)
            hd.append("SE "+h)

        chunkBunch = chunk_list(bunches, binning)
        for i, chunk in enumerate(chunkBunch):
            firstChunk = str(chunk[0])
            lastChunk = str(chunk[-1])
            avgColumns=[]
            photonE=[]
            for j, col in enumerate( hd ):
                colVal=[]
                colIndex = hd.index(col)
                for dataSet in dataSets:
                    if j == 0 :
                        photonE.append( dataSet[0] )
                    colVal.append( dataSet[colIndex] )
                if j == 0:
                    chunkE = chunk_list(photonE, binning )
                chunkCol = chunk_list(colVal, binning )
               
       
                if j % 2 == 0:
                    photonEAvg, colAvg = average_vals( chunkCol[i], chunkE[i] )
                    avgColumns.append(colAvg)
                else:
                    err = sum_error(chunkCol[i])
                    avgColumns.append(err)
            avgColumns = np.array(avgColumns)
            fileName = "avg"+"_bunch_"+firstChunk+"_"+lastChunk+".txt"
            hdr=""
            for col in hd[:-1]:
                hdr += col+"\t"+"SE "+col+"\t"
            hdr = hdr[:-1]
            print("Saved Bunch:\t"+firstChunk+"_"+lastChunk)
            save_multicolumn(avgColumns, header = hdr, filename = saveDirectory+os.sep+fileName, com = '')
    return
def compute_integral( title, pathToFiles, head, transientColumns, bunch, shiftedEnergy, shiftedColumns,saveDirectory, savePlot= False, binning=1):        
    transIndex = head.index(transColumn)
    shiftedSplines = [ shiftedColumns[i][transIndex] for i in range( len(shiftedColumns) ) ]

    integrals = [ def_integral( e,s, xHigh,xLow ) for e,s in zip(shiftedEnergy, shiftedSplines) ]
    bunch, Int = average_integrals(bunch, integrals)
    Int = [ I for b, I in sorted( zip(bunch, Int), key = lambda pair: pair[0] ) ]
    bunch.sort()
    timeDelay =[ (2*b -2 + offSet) if b>0 else (2*b + offSet) for b in bunch]
    timeDelay, Int = remove_outliers(timeDelay, Int)

    transientColumns.append( timeDelay )
    transientColumns.append( Int )
    print("saved transient:\t"+title)
#    opt, cov = curve_fit(exp, timeDelay, Int, p0=[0.1, 10.0, offSet] )
#    print( "A="+str(opt[0])+"\nT="+str(opt[1])+"\nt0="+str(opt[2]) )
    if showTransients:
        fig_int = plt.figure(dpi=100)
        plt.title(title+"_transient")
        plt.axhline(0, linestyle = "-", color= "grey")
        plt.ylabel(transColumn+" Integrated  [Arb]")
        plt.xlabel("Time Delay [ns]")
        plt.plot(timeDelay , Int, marker = 'd', linestyle= "-", color = "orange")
#        plt.plot(timeDelay, exp(timeDelay, opt[0], opt[1], opt[2]) )
        if savePlot:
            scanType = saveDirectory.split(os.sep)[-2]
            saveName  = saveDirectory+os.sep+scanType+"_transient_avg_"+xLow+"-"+xHigh+"eV.eps"
            plt.savefig( saveName, bbox_inches="tight", format = "eps")
    return
def save_integral(pathToFiles, head, bunchNumAll, shiftedEnergy, shiftedColumns, log, saveDirectory):
    print("Computing transients...")
    scanType = direct.split(os.sep)[-1]
    saveDirectory = os.path.normpath(saveDirectory + os.sep + "transients")
    transCol=[]
    header = "Delay[ns]\tAvg Transient\t"
    if not os.path.exists(saveDirectory):
        os.makedirs(saveDirectory)
    compute_integral(saveDirectory.split(os.sep)[-1], pathToFiles, head, transCol, 
                      bunchNumAll, 
                      shiftedEnergy, 
                      shiftedColumns,
                      saveDirectory,
                      savePlot=True)
    start=0
    end=0
    for path, files in  pathToFiles.items():
        title = path.split(os.sep)[-1].split("_")[0]
        header += title+" Delay[ns]\t"+title+" Transient\t"
        end  = start + len( files )
        compute_integral(title, pathToFiles, head, transCol, 
                      bunchNumAll[start:end], 
                      shiftedEnergy[start:end], 
                      shiftedColumns[start:end],
                      saveDirectory)
        start = end

    header = header[:-1]
    transCol = pd.DataFrame(transCol).values

    fileName = "transient_"+xLow+"_"+xHigh+"_bunch_"+firstBunch+"_"+lastBunch+".txt"
    save_multicolumn(transCol, header, saveDirectory + os.sep + fileName)
    print( "\nSaved Transients: "+ str( datetime.now() ), file = log )                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   )
    return
def make_shifts(dataFiles, paths, missingHeader, refColumnNum):
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
            file = dataFiles[i]
            if load_file(file, wantMissing=True) :
                missingHeader.append( file.split(os.sep)[-1] )
            dataSet, header = load_file(file, skip=skip)
            refSpline = data_to_column(dataSet, refColumnNum, file)
            if i!=0:
                refPeaks.append(refPeaks[-1])
                if shiftCenter or shiftMinimize:
                     refCenters.append(refCenters[-1])
            else:
                refPeaks.append( find_peak(refSpline) )
                if shiftCenter or shiftMinimize:
                    refCenters.append( find_center(lines[-1], refSpline) )
                if shiftMinimize:
                    refSplines.append( splines[-1] )
                    refLines.append( lines[-1] )
                else:
                    break            
#   shifts every column based on deltas calculated from reference column
    if shiftPeak:
        deltas = get_deltas(refPeaks, literaturePeakValue)
        print("peak matching shift")
    elif shiftCenter:
        deltas = get_deltas(refCenters)
        print("geometric center matching shift")
    elif shiftMinimize:
        deltas = diff_deltas(refSplines, refLines, scanSize, refPeaks, header.index(refColumn)-1, literaturePeakValue)
        print("least squares minimizing shift")
    if shiftNone :
        deltas = np.zeros_like( lines )
        print("No shift")
    shiftedEnergy, shiftedColumns, litDiff = apply_shift(deltas, splines, lines, refPeaks, literaturePeakValue )
    shiftedEnergy = cut_splines(shiftedEnergy,deltas)
    shiftedColumns = [ cut_splines(column, deltas) for column in shiftedColumns ]
    return shiftedEnergy, shiftedColumns
def save_phases_shifter():
    print("Computing phase shifter transients")

    return

###############################################################################
###############################################################################
#Main driver function for trXAS package
###############################################################################
def main():
    # startTime = timer()
    initialize()
    missingBunch = []
    missingHeader = []
    
    bunchNumAll = []
    print( "Scans:\t" + direct.split(os.sep)[-1] )
    paths = os.listdir(direct)
    paths = [ os.path.join(direct, p) for p in paths if not "avg" in p ]
    paths = sorted(paths)
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
    make_shifts()
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
            file = dataFiles[i]
            if load_file(file, wantMissing=True) :
                missingHeader.append( file.split(os.sep)[-1] )
            dataSet, header = load_file(file, skip=skip)
            refSpline = data_to_column(dataSet, refColumnNum, file)
            if i!=0:
                refPeaks.append(refPeaks[-1])
                if shiftCenter or shiftMinimize:
                     refCenters.append(refCenters[-1])
            else:
                refPeaks.append( find_peak(refSpline) )
                if shiftCenter or shiftMinimize:
                    refCenters.append( find_center(lines[-1], refSpline) )
                if shiftMinimize:
                    refSplines.append( splines[-1] )
                    refLines.append( lines[-1] )
                else:
                    break            
#   shifts every column based on deltas calculated from reference column
    if shiftPeak:
        deltas = get_deltas(refPeaks, literaturePeakValue)
        print("peak matching shift")
    elif shiftCenter:
        deltas = get_deltas(refCenters)
        print("geometric center matching shift")
    elif shiftMinimize:
        deltas = diff_deltas(refSplines, refLines, scanSize, refPeaks, header.index(refColumn)-1, literaturePeakValue)
        print("least squares minimizing shift")
    if shiftNone :
        deltas = np.zeros_like( lines )
        print("No shift")
    shiftedEnergy, shiftedColumns, litDiff = apply_shift(deltas, splines, lines, refPeaks, literaturePeakValue )
    shiftedEnergy = cut_splines(shiftedEnergy,deltas)
    shiftedColumns = [ cut_splines(column, deltas) for column in shiftedColumns ]
#   averages and saves collumns from scans.
    if saveSplines:
        save_splines(shiftedEnergy, shiftedColumns, bunchNum,bunchNumAll, head, pathToFiles, log, missingBunch, missingHeader, saveDirectory, litDiff)
#   averages and saves transients from all scans. Also saves each individual scan.
    if saveTransients:
        save_integral(pathToFiles, head, bunchNumAll, shiftedEnergy, shiftedColumns, log, saveDirectory)
    log.close()
    # endTime = timer()
    # print( "Time:\t"+ str(endTime - startTime) )
    initialize()
    if showSplines or showTransients:
        plt.show()
        plt.close()
    return 
###############################################################################        
if __name__ == "__main__":
    main()
