# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 12:40:16 2018

@author: 2-310-GL group
"""
def get_directory():
    print("This software is used for averaging spectral distributions :)")
#    direct = input("Please enter the directory that you wish to send data.")
    direct ="../trXAS data sample - date eval software/hv scans processed/"
    return direct

def get_column():
    print("Which column do you want to look at?")
#    keys= ["0a", "0b", "1a", "1b", "1c", "1d", "2a", "2b", "2c", "2d", 
#          "3a", "3b", "3c", "3d", "4a", "4b", "4c", "4d", "5a", "5b", "5c", "5d",
#          "6a", "6b", "6c", "6d", "7a", "7b", "7c", "7d", "8a", "8b", "8c", "8d",
#          "9a", "9b", "10a", "10b", "11a", "11b", "12a", "12b", "13a", "13b",
#          "9c", "9d", "10c", "10d", "11c", "11d", "12c", "12d", "13c", "13d",]
    keys= ["0a", "0b", "1a", "1b", "2a", "2b", "3a", "3b", "4a", "4b", 
           "5a", "5b", "6a", "6b", "7a", "7b", "8a", "8b", "9a", "10a", 
           "11a", "12a", "13a", "9b", "10b", "11b", "12b", "13b"]

    print("Which column do you want to look at?")
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
              "12:\t X BCSC\n"+
              "13:\t BCLR\n")
    column += input("a: Normalized \t b: Non-normalized \n")
    print (column)
    index = keys.index(column)
    return index

def get_bunches():
    first = input("Please enter the first bunch to look at:\t")
    last = input("Please enter the last bunch to look at:\t")
    return first, last

def test_user_input():
    print( get_directory() )
    print( get_column() )
    return

if __name__ == "__main__":
    test_user_input()