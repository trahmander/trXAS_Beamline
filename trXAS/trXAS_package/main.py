# -*- coding: utf-8 -*-
"""
use: Average and shift the  trXAS data.
@newfield revision: revision
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
import numpy as np
from matplotlib import pyplot as plt
#From trXAS average package
from user_input import get_directory  
from user_input import get_column
from user_input import get_bunches
from user_input import get_integration_bounds
from load_files import get_data_files
from load_files import load_file
from load_files import select_files
from shift import photonE_counts_plot
from shift import shift_spline
from integrate import def_integral
from average import average_vals
# Load global variables
from config import peaks
from config import peakAvgs
from config import splines
from config import lines 
from config import peaksAll
from config import splinesAll
from config import linesAll
from config import rawVals
from config import rawPhotonE
from config import integrals
from config import integralsAll
###############################################################################
#Main driver function for all other modules in the trXAS package.
###############################################################################
#Compares the averaging, need to manually change Johannes column number to switch between columns of the files for now.
def main():
    direct = get_directory()
    column = get_column()
    paths = os.listdir(direct)
    for i in range( len(paths) ):
        paths[i] = os.path.join(direct, paths[i])
    for path in paths:
         if "avg" in path:
            paths.remove(path)
    first, last = get_bunches()
    xLow, xHigh = get_integration_bounds()
#    pump = get_pump()
#    probe = get_probe()
#    sample = get_sample()
    shiftedSplines=[] 
    for j in range( len(paths) ) :
        path = paths[j]
        dataFiles = get_data_files(path)
        dataFiles = select_files(dataFiles, first = first, last = last)
        dataSet, header = load_file(dataFiles[0])
        columnName = header[column]
        
        fig_data = plt.figure(dpi=100)
        plt.title(path+" "+columnName+" Bunches: "+first+"-"+last)
        for i in range(len(dataFiles)):
            file = dataFiles[i]
            dataSet, header = load_file(file)
            photonE_counts_plot(dataSet, column, file)
        
        for k in range ( len(splines) ):
            shiftedVals, shiftedLine = shift_spline(k, peaks, splines, lines)
            shiftedSplines.append(shiftedVals)
            plt.plot(shiftedLine, shiftedVals, linewidth=1)
           
            integral= def_integral(shiftedLine, shiftedVals, xLow, xHigh)
            integrals.append(integral)   
        # print(shiftedSplines)
        fig_int = plt.figure(dpi=100)
        plt.title(path+" "+columnName+" Bunches: "+first+"-"+last+ " Integrate: "+str(xLow)+"-"+str(xHigh))
        plt.plot(range(len(integrals)) , integrals)
        


        
        # print( peaks )
        # print( set(peaks) )
#        peakAvgs.append( np.average(peaks) )
        
        peaksAll.extend(peaks)
        splinesAll.extend(splines)
        linesAll.extend(lines)
        integralsAll.extend(integrals)
        peaks.clear()
        splines.clear()
        lines.clear()
        integrals.clear()
        shiftedSplines.clear()
#    print( peakAvgs )
    
#    for i in range ( len(splines) ) :
#        shiftedVals, shiftedLine = shift_spline(i)
#        fig = plt.figure(dpi=100)
#        plt.plot(shiftedLine, shiftedVals, linewidth=1, color='b')
#        plt.plot(lines[i], splines[i](lines[i]), linewidth=1,  color='g')
    fig = plt.figure(dpi=100)
    plt.title("All shifted splines "+columnName+" Bunches: "+first+" to "+last)  
    for i in range ( len(splinesAll) ) :
        shiftedVals, shiftedLine = shift_spline(i, peaksAll, splinesAll, linesAll)
        shiftedSplines.append(shiftedVals)
        plt.plot(shiftedLine, shiftedVals, linewidth=1)
   
    valAvg, lineAvg = average_vals(shiftedSplines, linesAll[0])
    # for i in range(len(splinesAll)):
    #     splinesAll[i] = splinesAll[i](linesAll[i])
    # noshiftAvg, noshiftlineAvg = average_vals(splinesAll, linesAll[0])
    # rawAvg, rawline = average_vals(rawVals, rawPhotonE[0])

    head = "PhotonE\t"+"Average counts\n"

    # fileName =os.path.join(direct,
    #                         "0195_0196_0197_0198_0199_0201_0202_avg",
    #                         "0195_0196_0197_0198_0199_0201_0202_avg_pump_23-27_minus_ref_1-22.txt")
    # old_avg = load_file(fileName)[0].T
    fig = plt.figure(dpi=100)
    plt.title("Average spline "+columnName+" Bunches: "+first+"-"+last)
    plt.plot(lineAvg, valAvg, linewidth=1, color= 'r')
    # plt.plot(old_avg[0], old_avg[38], linewidth=3, linestyle= ":", color= 'g') # the average johannes made from raw data
    # plt.plot(noshiftlineAvg, noshiftAvg, linewidth=2, linestyle="-.", color='b')# average from non shifted splines
    # plt.plot(rawline, rawAvg, linewidth=1, linestyle="-.", color = 'orange')   # my average from raw data
    plt.show()
    
    return
    
    
if __name__ == "__main__":
    main()
