# -*- coding: utf-8 -*-
"""
Created on Sat Dec 19 09:30:51 2020

@author: Clayton
"""

import matplotlib.pyplot as plt
import json
from io import StringIO
import os.path
from os import path
from jsonmerge import merge
import glob

def loadData():
    
    if path.exists('merged_file.json'):
        return
    
    read_files = []
    
    count = 0
    filename = '.\\my_spotify_data\\MyData\\StreamingHistory' + str(count) +'.json'
    print(filename)
    print(path.exists(filename))
    read_files.append(filename)
    
    while (path.exists(filename)):
        count += 1
        filename = '.\\my_spotify_data\\MyData\\StreamingHistory' + str(count) +'.json'
        if not path.exists(filename):
            break
        print(filename)
        print(path.exists(filename))
        read_files.append(filename)

        
    output_list = []

    for f in read_files:
        with open(f, "rb") as infile:
            output_list.append(json.load(infile))
    
    with open("merged_file.json", "w") as outfile:
        json.dump(output_list, outfile)
    
    
def countPlayTime(data):
    
    #print(data)
    
    total = 0
    print(len(data))
    
    for item in data:
        for item2 in item:
            #print(item2)
            total += item2['msPlayed']
    print('days listened:',total / (60*60*24*1000))
    print('hours listened:',total / (60*60*1000))
    print('minutes listened:',total / (60*1000))
    
    return total / (60*60*1000)
    
def countArtistListens(data,numberOfTopArtists):
    
    artistCountDict = {}
    
    for item in data:
        for item2 in item:
            if str(item2['artistName']) in artistCountDict:
                artistCountDict[str(item2['artistName'])] += 1
            else:
                artistCountDict[str(item2['artistName'])] = 1
    #print(artistCountDict)     
    for i in range(numberOfTopArtists):
        maximum = max(artistCountDict, key=artistCountDict.get)  # Just use 'min' instead of 'max' for minimum.
        print(maximum, artistCountDict[maximum])
        artistCountDict.pop(maximum)
    
    pass

def countArtistPlayTime(data,artistName):
    
    total = 0
    for item in data:
        for item2 in item:
            if artistName == item2['artistName']:
                total += item2['msPlayed']
                
    minutes = total / (60 * 1000)
    hours = total / (60 * 60 * 1000)
    days = total / (60 * 60 * 1000 * 24)
    
    print('Total listen time for',artistName,'is',days,'days.')
    print('Total listen time for',artistName,'is',hours,'hours.')
    print('Total listen time for',artistName,'is',minutes,'mintues.')
    pass

def Main():
    loadData()
    file = 'merged_file.json'
    with open(file) as f:
        data = json.load(f)
    countPlayTime(data)
    countArtistListens(data,10)
    countArtistPlayTime(data,'Young the Giant')
    
    
    pass



Main()