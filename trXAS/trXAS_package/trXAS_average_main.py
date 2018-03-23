# -*- coding: utf-8 -*-
"""
trXAS_average.py: Used to average the integrated trxas data for time plots.
@newfield revision: revision
"""
__author__  = "Tahiyat Rahman"
__date__    = "2018-02-21"
__credits__ = ["Johannes Mahl"]
__email__ = "trahman@lbl.gov"
__status__ = "production"
__revision__= "6"
###############################################################################
#Import modules
###############################################################################
import os
import sys
import numpy as np
#import itertools as iter
from matplotlib import pyplot as plt
#from scipy.interpolate import UnivariateSpline
#from scipy.interpolate import InterpolatedUnivariateSpline
#import scipy.interpolate as itp

from trXAS_average_load_files import get_data_files
from trXAS_average_load_files import load_file
from trXAS_average_load_files import select_bunches
from trXAS_average_load_files import select_probe
from trXAS_average_load_files import select_pump
from trXAS_average_load_files import select_files

from trXAS_average_shift import photonE_counts_plot
#from trXAS_average_shift import get_spline as get_spline
#from trXAS_average_shift import find_peak as find_peak
from trXAS_average_shift import shift_spline

from trXAS_average_user_input import get_directory  
from trXAS_average_user_input import get_column
from trXAS_average_user_input import get_bunches
from trXAS_average_user_input import get_probe
from trXAS_average_user_input import get_pump

from trXAS_average_average import average_vals

from trXAS_average_shift import peaks
from trXAS_average_shift import peakAvgs
from trXAS_average_shift import splines
from trXAS_average_shift import lines 
from trXAS_average_shift import peaksAll
from trXAS_average_shift import splinesAll
from trXAS_average_shift import linesAll



#from trXAS_average_user_input import 
#from trXAS_average_shift import stepSize as stepSize





def main():
#dir = os.path.dirname(__file__)
#    paths = ["trXAS data sample - date eval software/hv scans processed/0198_CuO_O_K-edge_355nm_58pc/",
#             "trXAS data sample - date eval software/hv scans processed/0199_CuO_O_K-edge_355nm_58pc/",
#             "trXAS data sample - date eval software/hv scans processed/0201_CuO_O_K-edge_355nm_58pc/",
#             "trXAS data sample - date eval software/hv scans processed/0202_CuO_O_K-edge_355nm_58pc/"]
#    path = "trXAS data sample - date eval software/hv scans processed/0198_CuO_O_K-edge_355nm_58pc/"
    direct = get_directory()
    column = get_column()
    paths = os.listdir(direct)
    for i in range( len(paths) ):
        paths[i] = os.path.join(direct, paths[i])
    for path in paths:
         if "avg" in path:
            paths.remove(path)
    first, last = get_bunches()
#    pump = get_pump()
#    probe = get_probe()
#    sample = get_sample()
    for j in range( len(paths) ) :
        path = paths[j]
        dataFiles = get_data_files(path)
#        dataFiles = select_bunches(dataFiles, first, last)
#        dataFiles = select_pump(dataFiles, pump)
#        dataFiles = select_probe(dataFiles, probe)
        dataFiles = select_files(dataFiles, first = first, last = last)
        
        
        
        fig = plt.figure(dpi=100)
        plt.title(path)
        for i in range(len(dataFiles)):
            file = dataFiles[i]
            dataSet = load_file(file)
            photonE_counts_plot(dataSet, column, file)
        
            shiftedVals, shiftedLine = shift_spline(i, peaks, splines, lines)
            plt.plot(shiftedLine, shiftedVals, linewidth=1)
        
        print( peaks )
        print( set(peaks) )
        peakAvgs.append( np.average(peaks) )
        
        peaksAll.extend(peaks)
        splinesAll.extend(splines)
        linesAll.extend(lines)
        peaks.clear()
        splines.clear()
        lines.clear()
    print( peakAvgs )
    
    
#    print( splines[0](lines[0]) )
#    print( shiftedVals )
#    for i in range ( len(splines) ) :
#        shiftedVals, shiftedLine = shift_spline(i)
#        fig = plt.figure(dpi=100)
#        plt.plot(shiftedLine, shiftedVals, linewidth=1, color='b')
#        plt.plot(lines[i], splines[i](lines[i]), linewidth=1,  color='g')
    fig = plt.figure(dpi=100)
    plt.title("All shifted splines")
    shifted_splines=[]   
    for i in range ( len(splinesAll) ) :
        shiftedVals, shiftedLine = shift_spline(i, peaksAll, splinesAll, linesAll)
        shifted_splines.append(shiftedVals)
        plt.plot(shiftedLine, shiftedVals, linewidth=1)
   
    valAvg, lineAvg = average_vals(shifted_splines, linesAll[0])
#    dataAvg = np.hstack( [lineAvg, valAvg] ).T
    head = "PhotonE\t"+"Average counts\n"
    fileName = os.path.join(direct,"average.txt")
#    with open(fileName, 'w+') as f:
#    np.savetxt(fileName, (lineAvg.T, valAvg.T), fmt="%.4e", 
#                   delimiter= "\t", newline="\n")
    fileName =os.path.join(direct,"0195_0196_0197_0198_0199_0201_0202_avg\\0195_0196_0197_0198_0199_0201_0202_avg_pump_23-27_minus_ref_1-22.txt")
    old_avg = load_file(fileName).T
    fig = plt.figure(dpi=100)
    plt.title("Average spline")
    plt.plot(lineAvg, valAvg, linewidth=1)
    plt.plot(old_avg[0], old_avg[38], linewidth=1, linestyle= "--")
    plt.plot()
    
    return
    
    
if __name__ == "__main__":
    main()
