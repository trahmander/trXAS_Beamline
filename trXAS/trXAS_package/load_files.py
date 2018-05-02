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
import random
import numpy as np
import pandas as pd
import csv
from integrate import find_nearest_index
from config import saveDirectory
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
def load_file(fileName):
    dataSet = np.genfromtxt(fileName, delimiter="\t", skip_header=1)
    with open(fileName, "r") as f:
        reader = csv.reader(f, delimiter = "\t", )
        header = next(reader)
    dataSet = dataSet.tolist()
    dataSet.sort(key= lambda x:x[0])
    dataSet = np.array(dataSet)                                                 # Sort data based on photonE column.
    return dataSet, header
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
def get_selected_bunches(dataFiles ,first='all', last='all'):
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
    direct = os.path.normpath(os.pardir+ os.sep+ "test_data_bunchbybunch")
    paths = os.listdir(direct)
   
    for path in paths:
         if "avg" in path:
            paths.remove(path)
    print(paths)
    for i in range( len(paths) ):
        paths[i] = os.path.join(direct, paths[i])
    for path in paths :
        dataFiles = get_data_files(path)
        dataFiles = select_files(dataFiles)
        bunchNum = get_selected_bunches(dataFiles)
#        print(dataFiles)
#        print(bunchNum)
#        print()
#        for i in range(len(dataFiles)):
        file = dataFiles[0]
        dataSet, header = load_file(file)
     #   print( header[0] )    
        title = path.strip(direct)
#        print(dataSet[0])
#        print(dataSet[1] )
#        for i in range( len(header) -1 ):        
#            print(title + " " + str(i+1))
#            save_file(dataSet[0], header[0], dataSet[i+1], header[i+1], saveDirectory+os.sep+title+"_test_save_"+header[i+1]+".txt")
#            with open(saveDirectory+os.sep+title+"_test_save_"+header[i+1]+".txt", 'r') as file:
#                reader = csv.reader(file, delimiter = "\t")
#                for row in reader:
#                    print(row)
#    randomLists=[]
#    header = ""
#    for i in range(5):
#        header +=str(i+1)+"\t"
#        rand= [random.randint(0,100) for r in range(10) ]
#        randomLists.append(rand)
#        print(rand)
#    print(randomLists)
#    save_multicolumn(randomLists, header , "test_save.txt" )
    fileName = "all_columns"+"_bunch_"+first+"-"+"last"+".txt"
    with open(saveDirectory+os.sep+fileName) as file:
        read = csv.reader(file, delimiter = "\t")
        head = next(read)
        print( head )
        print(len(head))
        for i, row in enumerate( read):
            print( len(row) ) 
            
            if i >19:
                break
    
    return
###############################################################################
if __name__ == "__main__":   
    test_load_files()