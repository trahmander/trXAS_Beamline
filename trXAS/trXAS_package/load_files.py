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
from average import average_vals, sum_error
from average import chunk_list
from config import (transColumn,
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
# #returns data files with the chosen pump
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
# get a list of all the bunches that appear in a collection of files
def get_selected_bunches(dataFiles):
    bunchNum=[]
    ref = dataFiles[0].split("_ref_")[1].split("_data.txt")[0]
    ref = ref.split("-")
    
    start_ref = int( ref[0] )
    end_ref = int( ref[1] )
    for file in dataFiles:
        bunches = file.split("_pump_")[1].split("_minus_")[0]
        bunches = bunches.split("-")
        
        low = int( bunches[0] )
        high = int( bunches[1] )
        if high > end_ref:
            bunchNum.append(high-end_ref)
        else:
            bunchNum.append(high-end_ref-1)
    return bunchNum
def bin_data(splineCols, xOriginal):
    xVals = splineCols[0]
#    print(len(xOriginal))
#    print(len(xVals))
#    size = min( len(xVals), len(xOriginal) )

    binning = [find_nearest_index(xVals, x) for x in xOriginal] 
    binCols=[]
    for j, yVals in enumerate(splineCols):    
#        xBin = np.zeros(len(binning))
        yBin = np.zeros(len(binning))
        if j%2==0:
            collect = np.average
        else:
            collect = lambda err : sum_error(err, norm=True)
        for i in range( len(binning)) :
          cur = binning[i]
          if i==0:
              nxt = binning[i+1]
              midNxt  = int( np.ceil( (cur+nxt )/2 ) )
#              xBin[i] = np.average(xVals[:midNxt])
              yBin[i] = collect(yVals[:midNxt])
          elif i==len(binning)-1:
              pre = binning[i-1]
              midPre = int( np.floor( (cur+pre )/2 ) )
#              xBin[i] = np.average(xVals[midPre:])
              yBin[i] = collect(yVals[midPre:])
          else:
              pre = binning[i-1]
              nxt = binning[i+1]
              midPre = int( np.floor( (cur+pre )/2 ) )
              midNxt  = int( np.ceil( (cur+nxt )/2 ) )
              if midPre >= midNxt :
#                  xBin[i] = xVals[midNxt]
                  yBin[i] = yVals[midNxt]
              else:
#                  xBin[i] = np.average(xVals[midPre:midNxt])
                  yBin[i] = collect(yVals[midPre:midNxt])
        binCols.append(yBin)
    return binCols
def save_file(xVals, xName, yVals, columnName, fileName, com='# '):
    head = xName+"\t"+columnName
    xVals = np.array(xVals)
    yVals = np.array(yVals)
    data = np.array([xVals, yVals])
    data = data.T
    np.savetxt( fileName, data , header = head, delimiter="\t", newline = os.linesep)
    return
def save_multicolumn(data, header, filename, com= '# '):
    # if not os.path.exists(saveDirectory):
    #     os.makedirs(saveDirectory)
    data = np.array(data).T
    np.savetxt(filename, data, fmt= "%6e", header = header, delimiter = "\t", newline = os.linesep, comments = com)
    return
def select_data(bunchSet, dataSet):
    data = []
    bunches = []
    for d in dataSet:
        bunch = d.strip("avg_bunch").strip(".txt").split("_")
        first=bunch[0]
        last = bunch[1]
        if first == last and int(first) in bunchSet:
            data.append(d)
            bunches.append( int(first) )
    dataSet = data
    bunchSet = bunches
    return dataSet, bunchSet
###############################################################################
#test function for load_files.
###############################################################################
def test_load_files():
    dataFiles = ["C:\\Users\\2-310-GL group\\Desktop\ALS_beamtime\\trXAS\\CuO_O_K-edge_355nm_58pc\\0195_0196_0197_0198_0199_0201_0202_avg\\avg_bunch_-11_-11.txt",
    "C:\\Users\\2-310-GL group\\Desktop\ALS_beamtime\\trXAS\\CuO_O_K-edge_355nm_58pc\\0195_0196_0197_0198_0199_0201_0202_avg\\avg_bunch_-11_-11_binned.txt"]
    labels= ["unbinned", "binned"]
    dataSet, header = load_file(dataFiles[1])
    dataSets = [ np.array( load_file(file, wantHeader=False) ).T for file in dataFiles ]
    # print(header)
    # print(len(header))
    # print( [data.shape for data in dataSets] )
    for j, col in enumerate(header[:-1]):
        if j%2!=0:
        # if j%2==1:
        # print(col)

            fig,ax = plt.subplots(dpi=100)
            plt.title(col)
            plt.ylabel(col)
            plt.xlabel("Probe [eV]")
            for i, data in enumerate(dataSets):
                # if i == 1:    
                photonE = data[0]
                val = data[j]
                line = ax.plot(photonE, val, linewidth= 0.5, label = labels[i])
            ax.legend()
    plt.show()
    plt.close()

    


   
    return
###############################################################################
if __name__ == "__main__":   
    test_load_files()