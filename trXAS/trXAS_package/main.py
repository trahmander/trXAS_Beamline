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
                    firstBunch, 
                    lastBunch,
                    photonEnergyStart as xLow,
                    photonEnergyEnd as xHigh,
                    peakFindStart,
                    peakFindEnd,
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
def save_spline(xVals, yVals, title, columnName, xOrig):
    if not os.path.exists(saveDirectory):
        os.makedirs(saveDirectory)
    saveFileName = os.path.normpath(saveDirectory +os.sep+ title+"_"+columnName+"_bunch_"+first+"_"+last )
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
#    sys.stdout= open(saveDirectory+os.sep+"save_log.txt", "w+")
#    first = config.firstBunch
#    last = config.lastBunch
    initialize()
    missingBunch = set([])
    missingHeader = set([])
    missingColumn = set([])
    log = saveDirectory+os.sep+"save_log_"+firstBunch+"_"+lastBunch+".txt"
    
    print("",file= open(log, "w"))
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
#    bunchNumAll = sorted(bunchNumAll)    
        
    for i  in range( len(paths) ):
#        skip = 1
        path = paths[i]
        dataFiles = get_data_files(path)
        dataFiles = select_files(dataFiles, first= firstBunch, last = lastBunch)
        try:
            bunchNumAll.extend( get_selected_bunches(dataFiles) )
        except:
            continue
        
        file = dataFiles[0]
        dataSet, header = load_file(file)
        photonE = data_to_column(dataSet, refColumnNum, file)
    initialize()
    bunchNum = sorted(remove_dup(bunchNumAll))
#    deltas= [get_delta(peaks, i) for i,s in enumerate(splines)]

#        try:
#            dataFiles = select_files(dataFiles, first = firstBunch, last = lastBunch)
#            dataSet, header = load_file(dataFiles[0])
#        except:
##                    print("Missing Bunch:\t"+first+"-"+last+"\n\t at:\t"+path.strip(direct))
#            missingBunch.add(path.strip(direct)+"_"+first+"_"+last)
#            continue
#                bunchNum =  get_selected_bunches(dataFiles)

#        columnName = header[column]
#        try:
#            columnNum = header.index(col)
#        except:
##                    print("Missing header:\t"+col+"\n\t at:\t"+path.strip(direct)+" Bunch:\t"+first+"-"+last)
#            missingHeader.add(path.strip(direct)+"_"+first+"_"+last)
#            skip=0
#                    continue
#                refColumnNum = header.index(refColumn)            
#    splinesAllScans=[]
#s    deltasAllScans=[]
    for path in paths:
#        skip=1
        dataFiles = get_data_files(path)
        dataFiles = select_files(dataFiles, first = firstBunch, last = lastBunch)
        for i in range(len(dataFiles)):
            skip=1
            file = dataFiles[i]
#                    print(file+"\t"+str(skip))
            dataSet, header = load_file(file, skip=skip)
            photonE = data_to_column(dataSet, refColumnNum, file)
#        deltas = [ get_delta(peaks, i) for i,s in enumerate(splines) ]
#        deltasAllScans.append(deltas)    
#        splinesAllScans.append(splines)
#        splines.clear()
#    deltas = [ get_delta(peaks, i) for i,s in enumerate(splines) ]
    deltas = get_deltas(peaks)
    print(len(peaks))
    print( [len(s) for s in splines if len(s)!=0] )
    print(peaks)
    print(len(deltas))
    print(deltas)
    shiftedEnergy, shiftedColumns = apply_shift(deltas, splines, lines )
#            rawEnergy.append(photonE)
    
#    dataFiles = get_data_files(paths[1])
#    dataSet, head = load_file(dataFiles[0])
#    refColumnNum = head.index(refColumn)
#    bunchNumAll = sorted(bunchNumAll)
    
    print("Bunches:\n" + str(bunchNum), file = log)
    print("Bunches:\n" + str(bunchNum),)
    print("Number of bunches:\t"+str( len(bunchNum) ), file = log )
    print( [len(s) for s in shiftedEnergy if len(s)!=0] )
    print( shiftedEnergy )
    print( [len(s) for s in shiftedColumns if len(s) != 0 ])
    
    
#    peaksAll=[]
#    splinesAll=[]
#    linesAll=[]
#    integralsAll=[]
#    bunchNumAll=[137]
#    bunchNum = []
#    missingBunch = set([])
#    missingHeader = set([])
#    missingColumn = ([])
#    while ( len(bunchNumAll) != 0 ) :
    shiftedSplines= []
    shiftedLines= []
    for bunch in bunchNum  :
#        bunch = bunchNumAll[0]
        first = last = str(bunch)
#        print("Bunch: "+first+"-"+last)
        avgColumns = []
        lineAvg=0      
        lineErr=0
        bunchIndices = [i for i,x in enumerate(bunchNumAll) if x == bunch]
        shiftedLines = [ shiftedEnergy[ind] for ind in bunchIndices]
#        shiftedSplines=[]
        for j, col in enumerate( head[1:-1] ):
#            shiftedSplinesAll = []
#            rawEnergy = []
#            integrals=[]
            shiftedSplines= [shiftedColumns[ind][j] for ind in bunchIndices ]
#            print( [len(s) for s in shiftedLines] )
#            print( [len(s) for s in shiftedSplines] )
#            shiftedLines=[]
            title = col
            if showSplines and col in columnName:
                fig = plt.figure(dpi=100)
                plt.title(title+" Bunches: "+first+"-"+last)
                plt.ylabel(col)
                plt.xlabel("Probe [eV]")        
#            for j in range( len(paths) ) :  
#                skip=1
#                path = paths[j]
#                dataFiles = get_data_files(path)
#                try:
#                    dataFiles = select_files(dataFiles, first = first, last = last)
#                    dataSet, header = load_file(dataFiles[0])
#                except:
##                    print("Missing Bunch:\t"+first+"-"+last+"\n\t at:\t"+path.strip(direct))
#                    missingBunch.add(path.strip(direct)+"_"+first+"_"+last)
#                    continue
##                bunchNum =  get_selected_bunches(dataFiles)
#    
#                
#        #        columnName = header[column]
#                try:
#                    columnNum = header.index(col)
#                except:
##                    print("Missing header:\t"+col+"\n\t at:\t"+path.strip(direct)+" Bunch:\t"+first+"-"+last)
#                    missingHeader.add(path.strip(direct)+"_"+first+"_"+last)
#                    skip=0
##                    continue
##                refColumnNum = header.index(refColumn)            
#                for i in range(len(dataFiles)):
#                    file = dataFiles[i]
##                    print(file+"\t"+str(skip))
#                    dataSet, header = load_file(file, skip)
#
#                    try:
#                        photonE = data_to_column(dataSet, refColumnNum, columnNum, file)
#                    except:
##                        print("Missing Column:\t"+col+"\n\t at:\t"+file.strip(direct))
#                        missingColumn.add(file.strip(direct))
#                        continue
#                    rawEnergy.append(photonE)
#           
#                for k in range ( len(splines) ):
#                    shiftedVals, shiftedLine = shift_spline(k, peaks, splines[col], lines)
#                    shiftedSplines.append(shiftedVals)
#                    shiftedLines.append(shiftedLine)
#                    plt.plot(shiftedLine, shiftedVals, linewidth=0.5)
                    
    #                    integral= def_integral(shiftedLine, shiftedVals, xLow, xHigh)
    #                    integrals.append(integral)
    
        #        save_integral(bunchNum, integrals, title)
    
                if showSplines and col in columnName:
#                    lo, hi = find_nearest_bounds(shiftedLine ,xLow, xHigh)
#                    shiftedLine = shiftedLine[lo:hi]
#                    shiftedVals = shiftedVals[lo:hi]
                    plt.axvline(float(xLow), linestyle = "-.", linewidth = 0.5)
                    plt.axvline(float(xHigh), linestyle = "--", linewidth = 0.5)
                    plt.axvline(float(peakFindStart), linestyle = "--", linewidth= 0.5, color = 'g' )
                    plt.axvline( float(peakFindEnd), linestyle = "--", linewidth= 0.5, color = 'g' )
                    for i in range( len(shiftedSplines) ):
                        plt.plot(shiftedLines[i], shiftedSplines[i], linewidth=0.5)
            
#            peaksAll.extend(peaks)
#            splinesAll.extend(splines)
#            linesAll.extend(lines)
#            integralsAll.extend(integrals)
    #            bunchNumAll.extend(bunchNum)
#            shiftedSplinesAll.append(shiftedSplines)
            
            lineAvg, valAvg = average_vals(shiftedSplines, shiftedLines)
            lineErr, valErr = standard_error(shiftedSplines, shiftedLines, valAvg, lineAvg)
    #            valAvg = valAvg.tolist()
            if showSplines and col in columnName:
                plt.plot(lineAvg, valAvg, linestyle = "--", color = 'r', linewidth =1 )
            
            avgColumns.append(valAvg)
            avgColumns.append(valErr)
    
#            print("Saved:\t"+col)
#            if showSplines and col == columnName:    
#                lo,hi = find_nearest_bounds(lineAvg, xLow, xHigh)
#                lineAvg = lineAvg[lo:hi]
#                valAvg = valAvg[lo:hi]
#                plt.plot(lineAvg, valAvg, linewidth=2, linestyle="--", color = 'r')
                
            
#            peaks.clear()
#            splines.clear()
#            lines.clear()
#            rawEnergy.clear()
#            shiftedSplines.clear()
#            integrals.clear()
##            bunchNum.clear()
#            shiftedLines.clear()
        
        print( [len(s) for s in shiftedLines] )
        print( [len(s) for s in shiftedSplines] )   
#        print("Missing Column:")
#        print(missingColumn)
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
            print("\tMissing bunch:\t"+str(missingBunch), file = log)
#            print(missingBunch, file = log)
            missingBunch.clear()
        if ( len(missingHeader)!=0 ):
            print("\tMissing header:" + str(missingHeader), file = log)
#            print(missingHeader, file = log)
            missingHeader.clear()
        if ( len(missingColumn)!=0 ):
            print("\tMissing column:" + str(missingColumn), file = log)
#            print(missingColumn, file = log)
            missingColumn.clear()
#        bunchNumAll.remove(bunch)

#        if len(bunchNumAll)==0:
#            break        
#    plot_spline(splinesAll, peaksAll, linesAll, "All Splines", shiftedSplines)   
#    save_integral(bunchNumAll, integralsAll, "All Integrals")
    
    print( "\nLog End: "+ str( datetime.now() ), file = log )
    log.close()
    plt.show()
    plt.close()
    return
#def test():
#    log = saveDirectory+os.sep+"save_log_"+firstBunch+"_"+lastBunch+".txt"
#    print("",file= open(log, "w"))
#    log = open(log, "w+")
#    print( "Log Start: "+ str( datetime.now() )+"\n", file = log )
#    initialize()
#
#    bunchNumAll = []
##    direct, column, first, last, xLow, xHigh = ask_user()
#    paths = os.listdir(direct)
#    for i in range( len(paths) ):
#        paths[i] = os.path.join(direct, paths[i])
#    for path in paths:
#         if "avg" in path:
#            paths.remove(path)
#    splinesAll=[] 
#    dataFiles = get_data_files(paths[1])
##    dataFiles = select_files(dataFiles, first = "1", last = "1")
##    bunchNumAll = get_selected_bunches(dataFiles,first = first, last = last)
#    dataSet, head = load_file(dataFiles[0])
#    refColumnNum = head.index(refColumn)
#    bunchNumAll = sorted(bunchNumAll)
#    missingColumn= set([])
#       
#    for i  in range( len(paths) ):
#        path = paths[i]
#        dataFiles = get_data_files(path)
#        dataFiles = select_files(dataFiles, first = firstBunch, last = lastBunch)
#        bunchNumAll.extend( get_selected_bunches(dataFiles) )
##        splinesAll.append(dataFiles)
#        bunchNumAll = remove_dup(bunchNumAll)
#        for i in range(len(dataFiles)):
#            skip=1
#            file = dataFiles[i]
##                    print(file+"\t"+str(skip))
#            dataSet, header = load_file(file, skip)
#            for col in head[1:-1]:
#                columnNum = head.index(col)
#                photonE = data_to_column(dataSet, refColumnNum, columnNum, file)
#                
#   
##                for k in range ( len(splines) ):
##                    shiftedVals, shiftedLine = shift_spline(k, peaks, splines, lines)
##                    shiftedSplines.append(shiftedVals)
##                    shiftedLines.append(shiftedLine)
#            
#    
#    dataFiles = get_data_files(paths[1])
#    dataSet, head = load_file(dataFiles[0])
#    refColumnNum = head.index(refColumn)
#    bunchNumAll = sorted(bunchNumAll)
#    
##    print("Bunches:\n" + str(bunchNumAll), file = log)
#    print("Bunches:\n" + str(bunchNumAll))
##    print("Number of bunches:\t"+str( len(bunchNumAll) ), file = log ) 
#
#        
#    
#    
##    print( "\nLog End: "+ str( datetime.now() ), file = log )
##    log.close()
#    return
###############################################################################        
if __name__ == "__main__":
    main()
