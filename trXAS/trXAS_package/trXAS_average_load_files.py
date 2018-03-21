# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 13:35:37 2018

@author: 2-310-GL group
"""
import os
import sys
import numpy as np

def get_data_files(path):
    pathName = path
    dataFiles = os.listdir(pathName)
    dFiles = []    
    for file in dataFiles:
        if  file.endswith("data.txt") and not( "average" in file) :
            print(file)
            dFiles.append(os.path.join(pathName,file))
    return dFiles
#Returns a 2d array of sorted data from a file. 
def load_file(fileName):
    dataSet = np.loadtxt(fileName, skiprows=1)
#    print(dataSet[:,0])
    dataSet = dataSet.tolist()
    dataSet.sort(key= lambda x:x[0])
    dataSet = np.array(dataSet)                                                 # Sort data based on photonE column.
    return dataSet
def select_bunches(dataFiles, first, last):
    start = dataFiles[0].split("_ref_1_")[1].split("_data.txt")[0]
    start = int(start)
    dFiles=[]
    for file in dataFiles:
        bunches = file.split("pump_")[1].split("_minus")[0].split("-")
        low = int( bunches[0] )
        high = int( bunches[1] )
    if low - start == first and high - start == last :
        dFiles.append(file)
        print(file)
    return dFiles
def test_load_files():
    direct ="trXAS data sample - date eval software/hv scans processed/"
    paths = os.listdir(direct)
    print(paths)
    for i in range( len(paths) ):
        paths[i] = os.path.join(direct, paths[i])
    for path in paths:
         if "avg" in path:
            paths.remove(path)
    for j in range( len(paths) ) :
        path = paths[j]
        dataFiles = get_data_files(path)
        print(dataFiles)
        print()
        for i in range(len(dataFiles)):
            file = dataFiles[i]
#            print(file)
            dataSet = load_file(file)
    return

if __name__ == "__main__":   
    test_load_files()