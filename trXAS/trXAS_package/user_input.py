# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 12:40:16 2018
use: ask for directory and ask for column, ask for bunches to average over.
@author: 2-310-GL group
"""
#prompts user for the directory to look for files.
import os
def user_directory():
    print("This software is used for averaging spectral distributions")
    print("Please enter the directory that you wish to send data.")
    direct = input("Enter:\t")
    return direct
# prompts user to choose a column to look at.
def user_column():
    print("Which column do you want to look at?")

    keys= ["0a", "1a", "1b", "2a", "2b", "3a", "3b", "4a", "4b", 
           "5a", "5b", "6a", "6b", "7a", "7b", "8a", "8b", "9a", "10a", 
           "11a", "12a", "13a", "9b", "10b", "11b", "12b", "13b"]


    print("1:\t X Reference\n"+
          "2:\t X Pump\n"+
          "3:\t Y Reference\n"+
          "4:\t Y Pump\n"+
          "5:\t X All\n"+
          "6:\t Y All\n"+
          "7:\t X All Y Reference\n"+
          "8:\t Y All X Reference\n"+
          "9:\t BC X Histogram\n"+
          "10:\t BC Y Histogram\n"+
          "11:\t StS\n"+
          "12:\t BCSC\n"+
          "13:\t BCLR\n")
    column = input("Enter:\t")
    print("a: Normalized \t b: Non-normalized \n")
    column += input("Enter:\t")
    print (column)
    index = keys.index(column)
    return index
def user_column_name():
    print("Which column do you want to look at?")
    columnName= input("Enter:\t")
    return columnName
# prompts user to select first and last bunches after the reference. enter "all" for all bunches.
def user_bunches():
    print('Choose the first bunch to look at or choose \"all\"')
    first =  input("Enter:\t")
    if first != 'all':
      print('Choose the last bunch to look at.')
      # last = input("Enter:\t")
    else:
      last = '' 
    print(first+" - "+last+" bunches")
    return first, last
def user_integration_bounds():
  print("Choose the lower bound or select all.")
  xLow =  input("Enter:\t")
  if xLow != "all" :
    print("Choose the upper bound.")
    xHigh = input("Enter:\t")
  else:
    xHigh = '' 
  print(str(xLow)+" - "+str(xHigh)+"eV")
  return xLow, xHigh
#prompts user for pump wavelength (currently unused)
def user_pump():
    keyToPump = {"a":"532", "b":"355", "c":"all"}
    print("Choose your pump wavelength.\n"+
          "a: 532nm\t b: 355nm\t c: All")
    key = input( "Enter:\t" )
    pump = keyToPump[key]
    return pump
#prompts user for the edge 
def user_probe():
    keyToProbe= {"a": "O_K-edge", "b": "O1s", "c": "C1s", "d":"all"}
    print("Choose which edge to look at.\n"+
          "a: Oxygen K-edge\t b: Oxygen 1s\t c: Carbon 1s\t d: All")
    key = input( "Enter:\t" )
    probe = keyToProbe[key]
    return probe
#prompts user for the sample.
def user_sample():
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
    print( user_directory() )
    print( user_column() )
    return
###############################################################################
if __name__ == "__main__":
    test_user_input()