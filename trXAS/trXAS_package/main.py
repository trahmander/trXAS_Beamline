# -*- coding: utf-8 -*-
"""
use: This is the file that user should run.
"""
__author__  = "Tahiyat Rahman"
__date__    = "2018-02-21"
__credits__ = ["Johannes Mahl"]
__email__ = "trahman@lbl.gov"
###############################################################################
#Import modules
###############################################################################
#From buit in modules
import os  #for dealing with file operations and creating directories.
from datetime import datetime #used to get the current date and time.
from timeit import default_timer as timer #for getting time in ms at moment function is called
import numpy as np #for dealing with array manipulations and saveing arrays to files.
import pandas as pd #used during integration for organizing data into data frame structure.
from matplotlib import pyplot as plt #used for plotting.
###############################################################################
#From modules in trXAS_package
# used for saving and loading files. used for getting the right bunches.
from load_files import (get_data_files,
                        load_file,
                        select_files,
                        select_data,
                        get_selected_bunches,
                        save_file,
                        save_multicolumn,
                        bin_data)
#stores files into 2d arrays. Stores values in xOrig, lines, splines list. Deals with shifting.
from shift import (data_to_column,
                   find_peak,
                   find_center,
                   shift_spline,
                   get_deltas,
                   diff_deltas,
                   apply_shift)
#for dealing with transients in non phase shifter scans.
from integrate import (def_integral, 
                       average_integrals, 
                       remove_dup)
#averaging indivudal bunches and multiple bunches.
from average import (average_vals,
                     standard_error,
                     sum_error,
                     cut_splines,
                     chunk_list)
#dealing with transients from phase shifter scans
from phase_shifter import get_time_delays
# all configurations that the user specifies for this code.
# Load global variables. These are also used in shift.py
from config import (openDirectory as direct,
                    column as columnName,
                    refColumn,
                    transColumn,
                    psColumn,
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
                    saveOriginalX,
                    showSplines,
                    saveAverage,
                    savePhaseShifter,
                    splines,
                    lines,
                    xOrig)
###############################################################################
###############################################################################
#Helper functions for main()
###############################################################################
#Clearing some global variables used by main.py and shift.py
def initialize():
    splines.clear()
    lines.clear()
    xOrig.clear()
    return
# for saving indivual bunches and averaged bunches to files and manipulating 2d-data.
def save_splines(shiftedEnergy, shiftedColumns, bunchNum, bunchNumAll, head, pathToFiles, log,  missingBunch, missingHeader, saveDirectory, litDiff):
    print("Computing shifts...")
    
    paths = pathToFiles.keys()
    if saveAverage:
        averageSplines = []
        averageBunches= []
    if saveOriginalX:
        print("saving with original x")
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
        peOrg = xOrig[ bunchIndices[0] ] - litDiff
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
                        
            lineAvg, valAvg  = average_vals(shiftedSplines, shiftedLines)

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
        if saveOriginalX:
            fileName = "avg"+"_bunch_"+first+"_"+last+"_origX.txt"
            avgColumns = bin_data(avgColumns, peOrg )
        if saveSplines or saveOriginalX:
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
# for averaging multiple bunches together.
def avg_bunches(dataSets, bunches, head, first, last, saveDirectory, binning=1):
    print("Averaging bunches:\t"+str(first)+"-"+str(last) )
    print(bunches)
    #Does nothing if binning is 1 otherwise, it chunks bunches together based on binning set in config.
    if binning == 1:
        return
    else:
        saveDirectory = os.path.normpath(saveDirectory + os.sep + "binned_avg")
        if not os.path.exists(saveDirectory):
            os.makedirs(saveDirectory) 
        head = head[:-1] #removes last tab from header.
        hd = []         
        for h in head:
            hd.append(h)
            hd.append("SE "+h)
        chunkBunch = chunk_list(bunches, binning) # a list of tuples containing bunches to be averaged.
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
                if j % 2 == 0: # average normal columns
                    photonEAvg, colAvg = average_vals( chunkCol[i], chunkE[i] )
                    avgColumns.append(colAvg)
                else: # sum standard error of error columns
                    err = sum_error(chunkCol[i])
                    avgColumns.append(err)
            avgColumns = np.array(avgColumns)
            fileName = "avg"+"_bunch_"+firstChunk+"_"+lastChunk+".txt"
            if saveOriginalX:
                fileName = "avg"+"_bunch_"+firstChunk+"_"+lastChunk+"_origX.txt"
            hdr=""
            for col in hd:
                hdr += col+"\t"
            hdr = hdr[:-1]
            # print(hdr)
            print("Saved Bunch:\t"+firstChunk+"_"+lastChunk)
            save_multicolumn(avgColumns, header = hdr, filename = saveDirectory+os.sep+fileName, com = '')
    return
#helper function to save_integral. does integration and collect appropriate column from the interpolation matrix.
def compute_integral( title, pathToFiles, head, transientColumns, bunch, shiftedEnergy, shiftedColumns,saveDirectory, savePlot= False, binning=1, wantPlot=False):        
    transIndex = head.index(transColumn)
    shiftedSplines = [ shiftedColumns[i][transIndex] for i in range( len(shiftedColumns) ) ]
    integrals = [ def_integral( e,s, xLow,xHigh , wantPlot=wantPlot) for e,s in zip(shiftedEnergy, shiftedSplines) ]
    bunch, Int = average_integrals(bunch, integrals)
    Int = [ I for b, I in sorted( zip(bunch, Int), key = lambda pair: pair[0] ) ]
    bunch.sort()
    timeDelay =[ (2*b -2 + offSet) if b>0 else (2*b + offSet) for b in bunch]
    # timeDelay, Int = remove_outliers(timeDelay, Int)
    transientColumns.append( timeDelay )
    transientColumns.append( Int )
    print("saved transient:\t"+title)
    if showTransients:
        fig_int = plt.figure(dpi=100)
        plt.title(title+"_transient")
        plt.axhline(0, linestyle = "-", color= "grey")
        plt.ylabel(transColumn+" Integrated  [Arb]")
        plt.xlabel("Time Delay [ns]")
        plt.plot(timeDelay , Int, marker = 'd', linestyle= "-", color = "orange")
        if savePlot:
            scanType = saveDirectory.split(os.sep)[-2]
            saveName  = saveDirectory+os.sep+scanType+"_transient_avg_"+xLow+"-"+xHigh+"eV.eps"
            plt.savefig( saveName, bbox_inches="tight", format = "eps")
    return
#saves transients for all scans and also saves transients for each individual scan and puts them all in one file.
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
                      saveDirectory,
                      wantPlot=False)
        start = end

    header = header[:-1]
    transCol = pd.DataFrame(transCol).values

    fileName = "transient_"+xLow+"_"+xHigh+"_bunch_"+firstBunch+"_"+lastBunch+".txt"
    save_multicolumn(transCol, header, saveDirectory + os.sep + fileName)
    # print( ("\nSaved Transients:\t"+fileName ), file = log )                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   )
    return
#Apply's the shifts to the interpolations based on the method chosen in config.
def make_shifts(dataFiles, paths, missingHeader, refColumnNum):
    print("Loading files...")
    refPeaks=[]
    refCenters= []
    refSplines = []
    refLines = []
    scanSize=[]
    #loads all files and puts data into splines, lines, and xOrig
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
                refSplines.append( splines[-1] )
                refLines.append( lines[-1] )       
#   shifts every column based on deltas calculated from reference colum
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
    return shiftedEnergy, shiftedColumns, litDiff
def save_phase_shifter(head, paths, saveDirectory, missingHeader):
    print("Computing phase shifter transients")
    transIndex = head.index(psColumn)
    saveDirectory = os.path.normpath(saveDirectory+os.sep+"phase_shifter_transients")
    if not os.path.exists(saveDirectory):
        os.makedirs(saveDirectory)
    allDelays=[]
    allTrans=[]
    for path in paths:
        dataFiles = get_data_files(path)
        dataFiles = select_files(dataFiles, first = firstBunch, last = lastBunch)
        pathDelay=[]
        pathTrans=[]
        for i in range(len(dataFiles)):
            skip=1
            file = dataFiles[i]
            if load_file(file, wantMissing=True) :
                missingHeader.append( file.split(os.sep)[-1] )
            dataSet, header = load_file(file, skip=skip)
            delay = data_to_column(dataSet, 0, file, wantSpline=False)
            delay = get_time_delays(file, delay)
            transCol = data_to_column(dataSet, transIndex, file, wantSpline=False)
            pathDelay.extend(delay)
            pathTrans.extend(transCol)
            allDelays.extend( list(delay) )
            allTrans.extend( list(transCol) )

        delayAvg, transAvg = average_integrals(pathDelay, pathTrans)
        # print(len(transAvg))
        transAvg = [ I for b, I in sorted( zip(delayAvg, transAvg), key = lambda pair: pair[0] ) ]
        delayAvg.sort()
        if showTransients:
            fig = plt.figure(dpi=100)
            plt.title(path+" PS")
            plt.xlabel("Time Delay [ns]")
            plt.ylabel(psColumn)
            plt.plot(pathDelay, pathTrans, marker='d', linestyle = "None")
    # print(len(allDelays))
    delayAvg, transAvg = average_integrals(allDelays, allTrans)
    # print( len(delayAvg) )
    transAvg = [ I for b, I in sorted( zip(delayAvg, transAvg), key = lambda pair: pair[0] ) ]
    delayAvg.sort()
    saveCol=[delayAvg, transAvg]
    saveCol = pd.DataFrame(saveCol).values
    fileName = "ps_transient"+"_bunch_"+firstBunch+"_"+lastBunch+".txt"
    header = "Delay [ns]\t"+psColumn
    save_multicolumn(saveCol, header, saveDirectory + os.sep + fileName, com='')
    if showTransients:
        fig = plt.figure(dpi=100)
        plt.title("average PS")
        plt.xlabel("Time Delay [ns]")
        plt.ylabel(psColumn)
        plt.plot(delayAvg, transAvg, linestyle= "None", marker = 'd')
    print("Saved transient:\t"+fileName)
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
        refSpline= data_to_column(dataSet, refColumnNum, file, wantSpline=False)
    initialize()
    bunchNum = sorted(remove_dup(bunchNumAll))
    print("Bunches:\n" + str(bunchNum), file = log)
    print("Bunches:\n" + str(bunchNum),)
    print("Number of bunches:\t"+str( len(bunchNum) )+"\n", file = log )
#   calculates the linear interpolation and finds reference peaks from reference column.  

#   averages and saves collumns from scans.
    if saveSplines or saveAverage or saveOriginalX or saveTransients or showSplines:
        shiftedEnergy, shiftedColumns, litDiff = make_shifts(dataFiles, paths, missingHeader, refColumnNum)
        if saveSplines or saveAverage or saveOriginalX or showSplines:
            save_splines(shiftedEnergy, shiftedColumns, bunchNum,bunchNumAll, head, pathToFiles, log, missingBunch, missingHeader, saveDirectory, litDiff)
    #   averages and saves transients from all scans. Also saves each individual scan.
        if saveTransients:
            save_integral(pathToFiles, head, bunchNumAll, shiftedEnergy, shiftedColumns, log, saveDirectory)
    elif savePhaseShifter:
        save_phase_shifter(head, paths, saveDirectory, missingHeader)
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
