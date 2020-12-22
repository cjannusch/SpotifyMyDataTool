# -*- coding: utf-8 -*-
"""
Created on Sat Dec 19 09:30:51 2020

@author: Clayton
"""

import matplotlib.pyplot as plt
import json
import os.path
from os import path
from datetime import datetime
from dateutil import tz

def removeData():
    
    if path.exists('merged_file.json'):
        os.remove('merged_file.json')
        
    pass


def loadData():
    
    if path.exists('merged_file.json'):
        print('Merged File already exists, run removeData() if the Data is incorrect')
        with open('merged_file.json') as f:
            data = json.load(f)
        return data
    
    read_files = []
    
    count = 0
    filename = '.\\my_spotify_data\\MyData\\StreamingHistory' + str(count) +'.json'
    print('merging file:',filename)
    #print(path.exists(filename))
    read_files.append(filename)
    
    while (path.exists(filename)):
        count += 1
        filename = '.\\my_spotify_data\\MyData\\StreamingHistory' + str(count) +'.json'
        if not path.exists(filename):
            break
        print('merging file:',filename)
        #print(path.exists(filename))
        read_files.append(filename)

        
    output_list = []

    for f in read_files:
        with open(f, "rb") as infile:
            output_list.append(json.load(infile))
    
    with open("merged_file.json", "w") as outfile:
        json.dump(output_list, outfile)
        
    with open('merged_file.json') as f:
        data = json.load(f)
        
    return data
    
    
def countPlayTime(data):
    
    #print(data)
    
    total = 0
    #print(len(data))
    
    for item in data:
        for item2 in item:
            #print(item2)
            total += item2['msPlayed']
    #print('days listened:',total / (60*60*24*1000))
    print('hours listened:',total / (60*60*1000))
    #print('minutes listened:',total / (60*1000))
    
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
    count = 0
    total = 0
    for item in data:
        for item2 in item:
            if artistName == item2['artistName']:
                count += 1
                total += item2['msPlayed']
                
    minutes = total / (60 * 1000)
    hours = total / (60 * 60 * 1000)
    days = total / (60 * 60 * 1000 * 24)
    
    #print('Total listen time for',artistName,'is',days,'days over',count,'songs.')
    print('Total listen time for',artistName,'is',hours,'hours over',count,'songs.')
    #print('Total listen time for',artistName,'is',minutes,'mintues over',count,'songs.')
    pass

def countTimeOfDayListening(data):
    
    listOfCounts = {'00':0,'01':0,'02':0,'03':0,'04':0,'05':0,'06':0,'07':0,'08':0,'09':0,'10'
                    :0,'11':0,'12':0,'13':0,'14':0,'15':0,'16':0,'17':0,'18':0,'19':0,'20':0,
                    '21':0,'22':0,'23':0}
    
    for item in data:
        for item2 in item:
            #print(item2['endTime'])
            to_zone = tz.tzlocal()
            utc = datetime.strptime(item2['endTime'], '%Y-%m-%d %H:%M')
            converted = utc.astimezone(to_zone)
            toSubtract = int(str(converted)[-6:-3])
            #print(toSubtract)
            converted = str(converted)[0:-9] #converts to same format as before! woop woop
            #central = datetime.strptime(str(central), '%Y-%m-%d %H:%M')
            #print(converted)
            #print(item2['endTime'][-5:-3]) previous way of doing it only works for CST
            hour = str((int(converted[-5:-3]) + toSubtract) % 24)
            if len(hour) == 1:
                hour = '0' + hour
            listOfCounts[hour] += 1
            
            
            pass
    
    sizes = []
    sumOfCounts = 0
    
    for point in listOfCounts:
        sumOfCounts += listOfCounts[point]
        
    for point in listOfCounts:
        sizes.append(listOfCounts[point])
    
    print(sizes)
    
    plt.bar(list(listOfCounts.keys()), listOfCounts.values(), color='g')
    plt.show()


def subsetDataByDate(data,startDate,endDate):
    
    # format of dates is '2020-12-16 TI:ME'
    #print(type(data))
    newData = []
    
    startYear = startDate[0:4]
    startMonth = startDate[5:7]
    endYear = endDate[0:4]
    endMonth = endDate[5:7]
    #print(startYear, startMonth)
    
    for item in data:
        for item2 in item:
            #print(item2)
            itemMonth = item2['endTime'][5:7]
            itemYear = item2['endTime'][0:4]
            if (int(endYear) - int(itemYear)) >= 0 and (int(startYear) - int(itemYear)) <= 0:
                if (int(endMonth) - int(itemMonth)) >= 0 and (int(startMonth) - int(itemMonth)) <= 0:
                    newData.append(item2)
            pass

    #print(len(data[2]))
    #print(len(newData))
    return [newData]
    pass

def Main():
    data = loadData()

    #countPlayTime(data)
    #countArtistListens(data,10)
    #countArtistPlayTime(data,'Young the Giant')
    
    #countTimeOfDayListening(data)
    
    data = subsetDataByDate(data,'2020-00','2020-12')
    
    countArtistListens(data,10)
    
    #removeData()
    
    
    pass



Main()