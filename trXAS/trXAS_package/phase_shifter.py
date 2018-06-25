# -*- coding: utf-8 -*-
"""
Created on Wed Jun 20 12:02:24 2018

@author: 2-310-GL group
"""

def data_to_column(dataSet, col, file):
    dataSet = dataSet.T
    try:
        columns = (delay, #SEphotonE,
            xRefNorm, #SExRefNorm,
            xRef, #SExRef,
            xPumpNorm, #SExPumpNorm, 
            xPump, #SExPump,
            yRefNorm, #SEyRefNorm,
            yRef, #SEyRef,
            yPumpNorm, #SEyPumpNorm,
            yPump, #SEyPump,
            xAllNorm, #SExAllNorm,
            xAll, #SExAll,
            yAllNorm, #SEyAllNorm,
            yAll, #SEyAll,
            xAllyRefNorm, #SExAllyRefNorm,
            xAllyRef, #SExAllyRef,
            yAllxRefNorm, #SEyAllxRefNorm, 
            yAllxRef, #SEyAllxRef,
            BCxHistNorm, #SEBCxHistNorm, 
            BCyHistNorm, #SEBCyHistNorm,
            stsNorm, #SEstsNorm,
            BCSCNorm, #SEBCSCNorm, 
            BCLRNorm, #SEBCLRNorm,
            BCxHist, #SEBCxHist,
            BCyHist, #SEBCyHist,
            sts, #SEsts,
            BCSC, #SEBCSC, 
            BCLR, #SEBCLR,
            #SE, #SE2
            ) = dataSet                                
    except Exception as e:
        print("Didn't load to array:\t"+file)
        print( e )
        bunches = file.split("_pump_")[1].split("_minus_")[0]
        bunches = bunches.split("-")             
    return columns[col]
def get_time_delays(file, delay):
    bunches = file.split("_pump_")[1].split("_minus_")[0]
    bunches = bunches.split("-")
    if bunches[0] == bunches[1]:
        ref = file.split("_ref_")[1].split("_data.txt")[0]
        ref = ref.split("-")        
        start_ref = int( ref[0] )
        end_ref = int( ref[1] )
        high = int( bunches[1] )
        if high > end_ref:
            bunch = high-end_ref
        else:
            bunch = high-end_ref-1        
        timeDelay = [ (2*bunch -2 + d ) if bunch>0 else (2*bunch + d) for d in delay]
    return timeDelay