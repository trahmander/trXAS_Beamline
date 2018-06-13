# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 13:35:37 2018
load_files.py: load files and choose bunches from directory specified by user_inputs.py
@author: 2-310-GL group
"""
###############################################################################
#Import modules
###############################################################################
import os
#import sys
import random
import numpy as np
import itertools
import pandas as pd
import csv
import matplotlib.pyplot as plt
from integrate import find_nearest_index
from config import (saveDirectory,
                    transColumn,
                    offSet)
from integrate import remove_dup
###############################################################################
#returns a list of all the files from the path chosen by user.
def get_data_files(path):
    pathName = path
    dataFiles = os.listdir(pathName)
    dFiles = []    
    for file in dataFiles:
        if  file.endswith("data.txt") and not( "average" in file) :
#            print(file)
            dFiles.append(os.path.join(pathName,file))
    return dFiles
#Returns a 2d array of sorted data from a file and the header row. sorts array by the first column.
def is_float(x):
    try:
        float(x)
        return True
    except ValueError:
        return False
def load_file(fileName, skip=1, wantHeader=True, wantMissing=False):
#    dataSet = np.genfromtxt(fileName, delimiter="\t", skip_header=skip)
    skip=1
    with open(fileName, "r") as f:
        reader = csv.reader(f, delimiter = "\t", )
        header = next(reader)
#   check whether the file has a header and wether 1st line should be skipped.
    if not all( [ not (is_float(h) ) for h in header ] ) :
        skip=0
    if wantMissing:
        return not bool(skip) 
    dataSet = np.genfromtxt(fileName, delimiter="\t", skip_header=skip)
    dataSet = dataSet.tolist()
    dataSet.sort(key= lambda x:x[0])
    dataSet = np.array(dataSet)                                                 # Sort data based on photonE column.
    if wantHeader:
        return dataSet, header
    else:
        return dataSet
#returns a list of data files with only the chosen bunches.
def select_bunches(dataFiles, first, last):
    if first == "all":
        dFiles= dataFiles
    else:
        ref = dataFiles[0].split("_ref_")[1].split("_data.txt")[0]
        ref = ref.split("-")
        
        start_ref = int( ref[0] )
        end_ref = int( ref[1] )
#        print( (start_ref, end_ref) )
        dFiles=[]
        for file in dataFiles:
            bunches = file.split("_pump_")[1].split("_minus_")[0]
    #        print (bunches)
            bunches = bunches.split("-")
            
            low = int( bunches[0] )
            high = int( bunches[1] )
            if low - end_ref >= 0:
                low+=1
            if high - end_ref >=0:
                high+=1
            if low == high :
                if (low - end_ref > int(first)) and (low - end_ref <= int(last) + 1):
                    dFiles.append(file)
            else:
                if low - end_ref == int(first) and high - end_ref == int(last) :
                    dFiles.append(file)
#    if (len(dFiles) ) == 0:
#        raise Exception
    #        print(file)
    return dFiles
#returns data files with the chosen pump
def select_pump(dataFiles, pump):
    if pump == "all":
        dFiles = dataFiles
    else:
        dFiles=[]
        for file in dataFiles:
            if pump in dataFiles:
                dFiles.append(file)
    return dFiles
#returns data files with the chosen edge.
def select_probe(dataFiles, probe):
    if probe == "all":
        dFiles=dataFiles
    else:
        dFiles=[]
        for file in dataFiles:
            if probe in dataFiles:
                dFiles.append(file)
    return dFiles
#returns data files with the chosen sample
def select_sample(dataFiles, sample):
    if sample == "all":
        dFiles=dataFiles
    else:
        dFiles=[]
        for file in dataFiles:
            if sample in dataFiles:
                dFiles.append(file)
    return dFiles
#functions which combines all the "select" functions.
def select_files(dataFiles, first="all", last="all", sample="all", pump="all", probe="all", *args, **kwargs):
    dataFiles = select_bunches(dataFiles, first, last)
    dataFiles = select_sample(dataFiles, sample)
    dataFiles = select_pump(dataFiles, pump)
    dataFiles = select_probe(dataFiles, probe)
    return dataFiles
def get_selected_bunches(dataFiles):
    bunchNum=[]
    ref = dataFiles[0].split("_ref_")[1].split("_data.txt")[0]
    ref = ref.split("-")
    
    start_ref = int( ref[0] )
    end_ref = int( ref[1] )
#    print( (start_ref, end_ref) )
    for file in dataFiles:
        bunches = file.split("_pump_")[1].split("_minus_")[0]
#        print (bunches)
        bunches = bunches.split("-")
        
        low = int( bunches[0] )
        high = int( bunches[1] )
        if high > end_ref:
            bunchNum.append(high-end_ref)
        else:
            bunchNum.append(high-end_ref-1)
    return bunchNum
def bin_data(xVals, yVals, xOriginal):
    binning = [find_nearest_index(xVals, x) for x in xOriginal]
    xBin = np.zeros(len(binning))
    yBin = np.zeros(len(binning))    
    for i in range( len(binning)) :
      cur = binning[i]
      if i==0:
          nxt = binning[i+1]
          midNxt  = int( np.ceil( (cur+nxt )/2 ) )
          xBin[i] = np.average(xVals[:midNxt])
          yBin[i] = np.average(yVals[:midNxt])
      elif i==len(binning)-1:
          pre = binning[i-1]
          midPre = int( np.floor( (cur+pre )/2 ) )
          xBin[i] = np.average(xVals[midPre:])
          yBin[i] = np.average(yVals[midPre:])
      else:
          pre = binning[i-1]
          nxt = binning[i+1]
          midPre = int( np.floor( (cur+pre )/2 ) )
          midNxt  = int( np.ceil( (cur+nxt )/2 ) )
#          print(midPre)
#          print(midNxt)
          if midPre >= midNxt :
              xBin[i] = xVals[midNxt]
              yBin[i] = yVals[midNxt]
          else:
              xBin[i] = np.average(xVals[midPre:midNxt])
              yBin[i] = np.average(yVals[midPre:midNxt])
    return xBin, yBin
def save_file(xVals, xName, yVals, columnName, fileName):
    head = xName+"\t"+columnName
    xVals = np.array(xVals)
    yVals = np.array(yVals)
    data = np.array([xVals, yVals])
    data = data.T
#    print(data)
#    with open (fileName, 'w+') as csvfile :
#        writer = csv.writer(csvfile, delimiter = "\t", )
#        writer.writerow(head)
#        writer.writerows( data )
    np.savetxt( fileName, data , header = head, delimiter="\t", newline = os.linesep)
    return
def save_multicolumn(data, header, filename):
    data = np.array(data).T
    np.savetxt(filename, data, fmt= "%6e", header = header, delimiter = "\t", newline = os.linesep)
    return
def select_data(bunchSet, dataSet):
    data = []
    bunches = []
    for d in dataSet:
        bunch = d.strip("avg_bunch").strip(".txt").split("_")[0]
        if int(bunch) in bunchSet:
            data.append(d)
            bunches.append( int(bunch) )
    dataSet = data
    bunchSet = bunches
    return dataSet, bunchSet
###############################################################################
#test function for load_files.
###############################################################################
def test_load_files():
#    sys.stdout= open(saveDirectory+os.sep+"save_log.txt", "w+")
    direct = os.path.normpath(os.pardir+ os.sep+ "CuO_O_K-edge_532nm_14pc")
#    paths = os.listdir(direct)
#    paths = [ os.path.join(direct, p) for p in paths if not "avg" in p ]
#    print( [p.split(os.sep)[-1].split("_")[0] for p in paths] )
#    print (paths)
#    for path  in paths :
#        dataFiles = get_data_files(path)
#        dataFiles = select_files(dataFiles, first= -2, last = 2)
##        pathToFiles[path] = dataFiles
#        try:
#            print(dataFiles)
#            newBunch = get_selected_bunches(dataFiles)
#            print(newBunch)
#            bunchNumAll.extend( newBunch )
#        except:
#            continue
    paths = os.listdir(direct)
    path = [ os.path.join(direct,p) for p in paths if "avg" in p ][0]
    datafiles = os.listdir(path)
    datafiles = [d for d in datafiles if "avg_bunch" in d]
    bunches = [1,3,135,140,-1]
    datafiles, bunches = select_data(bunches, datafiles)
    datafiles = [os.path.join(path, d) for d in datafiles]
    dataSet, head = load_file(datafiles[0])
    transIndex = head.index(transColumn)
    
    photonE=[]
    trans=[]
    delay =[ int( (2*b -2 + offSet)*1000 ) if b>0 else int( (2*b + offSet)*1000 ) for b in bunches]
    for file in datafiles:
        dataSet = load_file(file, wantHeader=False)
        dataSet = dataSet.T
        photonE.append( dataSet[0] )
        trans.append( dataSet[transIndex] )
    fig,ax = plt.subplots(dpi=100)
    plt.title("Pump-Probe Difference for different time delays")
    plt.xlabel("Probe [eV]")
    plt.xlim(530, 545)
    plt.ylabel("Pump-Probe Difference [Arb]")
    plt.axvline(533.2, linestyle = "-.", linewidth = 0.5, color = "orange")
    plt.axvline(534.9, linestyle = "-.", linewidth = 0.5, color = "orange")
    plt.axvline(535.0, linestyle = "-.", linewidth = 0.5, color = "green")
    plt.axvline(536.0, linestyle = "-.", linewidth = 0.5, color = "green")
    for i in range( len(trans) ):
        line = ax.plot(photonE[i], trans[i], linestyle="-", linewidth= "1.5", label = str(delay[i])+" ps"  )
    ax.legend()
    plt.savefig( , bbox_inches="tight", format = "eps")
    return
###############################################################################
if __name__ == "__main__":   
    test_load_files()