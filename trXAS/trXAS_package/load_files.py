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
import sys
import numpy as np
import csv
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
        print( (start_ref, end_ref) )
        dFiles=[]
        for file in dataFiles:
            bunches = file.split("_pump_")[1].split("_minus_")[0]
    #        print (bunches)
            bunches = bunches.split("-")
            
            low = int( bunches[0] )
            high = int( bunches[1] )
            
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
###############################################################################
#test function for load_files.
###############################################################################
def test_load_files():
    direct = os.path.normpath(os.pardir+ os.sep+ "test_data")
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
        print(dataFiles)
        print(bunchNum)
        print()
        for i in range(len(dataFiles)):
            file = dataFiles[i]
            dataSet, header = load_file(file)
         #   print( header[0] )        
    return
###############################################################################
if __name__ == "__main__":   
    test_load_files()