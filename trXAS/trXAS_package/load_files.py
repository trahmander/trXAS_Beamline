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
import pandas as pd
import csv
from integrate import find_nearest_index
from config import saveDirectory
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
def load_file(fileName, skip=1, wantHeader=True):
#    dataSet = np.genfromtxt(fileName, delimiter="\t", skip_header=skip)
    skip=1
    with open(fileName, "r") as f:
        reader = csv.reader(f, delimiter = "\t", )
        header = next(reader)
#   check whether the file has a header and wether 1st line should be skipped.
    if not all( [ not (is_float(h) ) for h in header ] ) :
        skip=0
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
                if (low - end_ref >= int(first)) and (low - end_ref <= int(last)):
                    dFiles.append(file)
            else:
                if low - end_ref == int(first) and high - end_ref == int(last) :
                    dFiles.append(file)
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
        if high >= end_ref:
            bunchNum.append(high-end_ref+1)
        else:
            bunchNum.append(high-end_ref)
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
###############################################################################
#test function for load_files.
###############################################################################

def test_load_files():
#    sys.stdout= open(saveDirectory+os.sep+"save_log.txt", "w+")
    direct = os.path.normpath(os.pardir+ os.sep+ "test_data_bunchbybunch")
#    paths = os.listdir(direct)
#    bunchNumAll=[]
#    for path in paths:
#         if "avg" in path:
#            paths.remove(path)
#    for i in range( len(paths) ):
#        paths[i] = os.path.join(direct, paths[i])
#    print(paths)
#    for i  in range( len(paths) ):
#        path = paths[i]
#        print(path.strip(direct).split("_")[0])
#        dataFiles = get_data_files(path)
#        dataFiles = select_files(dataFiles, first = "-1", last = "1")
#        print([file.strip(direct) for file in dataFiles])
#        bunchNumAll.extend( get_selected_bunches(dataFiles) )
#        bunchNumAll = remove_dup(bunchNumAll)
#    print(sorted(bunchNumAll))
#    print("Number of bunches:\t"+str(len(bunchNumAll) ) )
    
    paths = os.listdir(direct)
    for i in range( len(paths) ):
        paths[i] = os.path.join(direct, paths[i])
    for path in paths:
         if "avg" in path:
            paths.remove(path)
    
    dataFiles = get_data_files(paths[0])
    dataSet, head = load_file(dataFiles[1])
    refColumnNum = head.index(refColumn)
    
    return
###############################################################################
if __name__ == "__main__":   
    test_load_files()