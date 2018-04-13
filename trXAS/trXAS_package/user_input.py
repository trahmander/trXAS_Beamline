# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 12:40:16 2018
use: ask for directory and ask for column, ask for bunches to average over.
@author: 2-310-GL group
"""
#prompts user for the directory to look for files.
import os
def get_directory():
    print("This software is used for averaging spectral distributions")
    print("Please enter the directory that you wish to send data.")
  #  direct = input("Enter:\t")
    # direct =os.path.normpath( os.pardir + os.sep + 
    #   "trXAS data sample - date eval software" +os.sep 
    #   + "hv scans processed" )
    # direct ="..\\trXAS data sample - date eval software\\hv scans processed\\"
    # direct= os.path.normpath(os.pardir+ os.sep+ "2018-02_BL_8_0_1_TRXAS")
    direct = os.path.normpath(os.pardir+ os.sep+ "test_data")
    return direct
# prompts user to choose a column to look at.
def get_column():
    print("Which column do you want to look at?")

    keys= ["0a", "1a", "1b", "2a", "2b", "3a", "3b", "4a", "4b", 
           "5a", "5b", "6a", "6b", "7a", "7b", "8a", "8b", "9a", "10a", 
           "11a", "12a", "13a", "9b", "10b", "11b", "12b", "13b"]


    column = input("1:\t X Reference\n"+
              "2:\t X Pump\n"+
              "3:\t Y Reference\n"+
              "4:\t Y Pump\n"+
              "5:\t X All\n"+
              "6:\t Y All\n"+
              "7:\t X All Y Reference\n"+
              "8:\t Y All X Reference\n"+
              "9:\t BC X Histogram\n"+
              "10:\t BC Y Histogram\n"+
              "11:\t STS\n"+
              "12:\t BCSC\n"+
              "13:\t BCLR\n"+
              "Enter:\t")
    column += input("a: Normalized \t b: Non-normalized \n"+
                    "Enter:\t")
    print (column)
    index = keys.index(column)
    return index
# prompts user to select first and last bunches after the reference. enter "all" for all bunches.
def get_bunches():
    print('Choose the first bunch to look at or choose \"all\"')
    first =  input("Enter:\t")
    # first = 'all' 
    if first != 'all':
      print('Choose the last bunch to look at.')
      last = input("Enter:\t")
    else:
      last = '' 
    return first, last
def get_integration_bounds():
  print('Choose the bounds for the integration_region')
  xLow = float( input("Lower:\t") )
  xHigh = float ( input("Upper:\t") )
  # xLow = 530.0
  # xHigh= 535.0
  return xLow, xHigh
#prompts user for pump wavelength (currently unused)
def get_pump():
    keyToPump = {"a":"532", "b":"355", "c":"all"}
    print("Choose your pump wavelength.\n"+
          "a: 532nm\t b: 355nm\t c: All")
    key = input( "Enter:\t" )
    pump = keyToPump[key]
    return pump
#prompts user for the edge 
def get_probe():
    keyToProbe= {"a": "O_K-edge", "b": "O1s", "c": "C1s", "d":"all"}
    print("Choose which edge to look at.\n"+
          "a: Oxygen K-edge\t b: Oxygen 1s\t c: Carbon 1s\t d: All")
    key = input( "Enter:\t" )
    probe = keyToProbe[key]
    return probe
#prompts user for the sample.
def get_sample():
    keyToSample= {"a":"Cu", "b":"TiO2", "c":"all"}
    print("Choose which sample to look at.\n"+
          "a: Cu\t b: TiO2\t c: All")
    key = input( "Enter:\t" )
    sample = keyToSample[key]
    return sample
###############################################################################
#Test function for user_input
###############################################################################
def test_user_input():
    print( get_directory() )
    print( get_column() )
    return

if __name__ == "__main__":
    test_user_input()