# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 12:40:16 2018

@author: 2-310-GL group
"""
def get_directory():
    print("This software is used for averaging spectral distributions :)")
#    direct = input("Please enter the directory that you wish to send data.")
#   direct ="..\\trXAS data sample - date eval software\\hv scans processed\\"
#   direct="..\\2018-02_BL_8_0_1_TRXAS\\"
    direct = "..\\test_data\\"
    return direct

def get_column():
    print("Which column do you want to look at?")

    keys= ["0a", "0b", "1a", "1b", "2a", "2b", "3a", "3b", "4a", "4b", 
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

def get_bunches():
    first =  input("Please enter the first bunch to look at:\t") 
    last = input("Please enter the last bunch to look at:\t") 
    return first, last
def get_pump():
    keyToPump = {"a":"532", "b":"355", "c":"all"}
    print("Choose your pump wavelength.\n"+
          "a: 532nm\t b: 355nm\t c: All")
    key = input( "Enter:\t" )
    pump = keyToPump[key]
    return pump
def get_probe():
    keyToProbe= {"a": "O_K-edge", "b": "O1s", "c": "C1s", "d":"all"}
    print("Choose which edge to look at.\n"+
          "a: Oxygen K-edge\t b: Oxygen 1s\t c: Carbon 1s\t d: All")
    key = input( "Enter:\t" )
    probe = keyToProbe[key]
    return probe
def get_sample():
    keyToSample= {"a":"Cu", "b":"TiO2", "c":"all"}
    print("Choose which sample to look at.\n"+
          "a: Cu\t b: TiO2\t c: All")
    key = input( "Enter:\t" )
    sample = keyToSample[key]
    return sample
def test_user_input():
    print( get_directory() )
    print( get_column() )
    return

if __name__ == "__main__":
    test_user_input()