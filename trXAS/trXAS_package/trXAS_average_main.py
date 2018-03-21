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
__revision__= "5"
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

from trXAS_average_shift import photonE_counts_plot
#from trXAS_average_shift import get_spline as get_spline
#from trXAS_average_shift import find_peak as find_peak
from trXAS_average_shift import shift_spline

from trXAS_average_user_input import get_directory  
from trXAS_average_user_input import get_column
from trXAS_average_user_input import get_bunches


from trXAS_average_shift import peaks
from trXAS_average_shift import peakAvgs
from trXAS_average_shift import splines
from trXAS_average_shift import lines 
from trXAS_average_shift import peaksAll
from trXAS_average_shift import splinesAll
from trXAS_average_shift import linesAll

#from trXAS_average_user_input import 
#from trXAS_average_shift import stepSize as stepSize



#def average_splines(splineSet, line):
#    splineSum = np.zeros_like(line)
#    numSpline=0
#    for i in range( len(splineSet) ):
#        spline = splineSet[i](line)
#        splineSum = splineSum + spline
#        numSpline+=1
#    splineAvg = splineSum/numSpline
#    return splineAvg

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
    for j in range( len(paths) ) :
        path = paths[j]
        dataFiles = get_data_files(path)
        first, last = get_bunches()
        dataFiles = select_bunches(dataFiles, first, last)
        
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
    for i in range ( len(splinesAll) ) :
        shiftedVals, shiftedLine = shift_spline(i, peaksAll, splinesAll, linesAll)
        plt.plot(shiftedLine, shiftedVals, linewidth=1)
    return
    
if __name__ == "__main__":
    main()
