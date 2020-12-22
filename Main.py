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
from datetime import date
from dateutil import tz

def removeData():
    
    if path.exists('merged_file.json'):
        os.remove('merged_file.json')
        
    pass


def loadData(newMergeFile = False):
    
    if newMergeFile:
        removeData()
    
    if path.exists('merged_file.json'):
        #print('Merged File already exists, run removeData() if the Data is incorrect')
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
        if len(artistCountDict.keys()) == 0:
            continue
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
    
    sizes = []
    sumOfCounts = 0
    
    for point in listOfCounts:
        sumOfCounts += listOfCounts[point]
        
    for point in listOfCounts:
        sizes.append(listOfCounts[point])
    
    #print(sizes)
    
    dateStart,dateEnd = getTimePeriodOfData(data)
    
    plt.bar(list(listOfCounts.keys()), listOfCounts.values(), color='g')
    plt.title(getUser()+'\'s listening habits \nfrom ' + str(dateStart) + ' --> ' + str(dateEnd))
    plt.xlabel('Hour of The Day')
    plt.ylabel('# of songs listened to')
    plt.style.use('ggplot')
    plt.show()


def subsetDataByDate(data,startDate,endDate):
    
    # format of dates is '2020-12-16 TI:ME'
    #print(type(data))
    newData = []
    
    startYear = startDate[0:4]
    startMonth = startDate[5:7]
    startDay = startDate[8:10]
    endYear = endDate[0:4]
    endMonth = endDate[5:7]
    endDay = endDate[8:10]
    start = date(int(startYear), int(startMonth),int(startDay))
    end = date(int(endYear), int(endMonth),int(endDay))

    for item in data:
        for item2 in item:
            itemDay = item2['endTime'][8:10]
            itemMonth = item2['endTime'][5:7]
            itemYear = item2['endTime'][0:4]
            time = date(int(itemYear), int(itemMonth),int(itemDay))
            if start <= time <= end:
                newData.append(item2)
            
    return [newData]
    pass

def getUser():
    
    filename = '.\\my_spotify_data\\MyData\\Userdata.json'
    
    if not path.exists(filename): 
        return 'NO NAME LOL'
    
    with open(filename) as f:
        user = json.load(f)
        user = user['username']
        return user
    
    pass


def getTimePeriodOfData(data):
    
    startDate = None
    
    for item in data:
        for item2 in item:
            itemDay = item2['endTime'][8:10]
            itemMonth = item2['endTime'][5:7]
            itemYear = item2['endTime'][0:4]
            time = date(int(itemYear), int(itemMonth),int(itemDay))
            if startDate == None:
                startDate = time
            
    endDate = time
    
    return (startDate,endDate)

def runMethodOnYear(data,year):
    
    for i in range(12):
        #data = loadData()
        if i == 0:
            continue
        start,end = year+'-',year+'-'
        if len(str(i)) == 1:
            temp1 = '0'+str(i)
        else:
            temp1 = str(i)
        if len(str(i + 1)) == 1:
            temp2 = '0'+str(i + 1)
        else:
            temp2 = str(i + 1)
        start = start + temp1 + '-01'
        end = end + temp2 + '-01'
        
        print(start,'-->',end)
        
        subsetData = subsetDataByDate(data,start,end)
        countArtistListens(subsetData,3)
        #countTimeOfDayListening(subsetData)
    
    
    pass

def Main():
    #data = loadData(True)
    data = loadData()

    #countPlayTime(data)
    #countArtistListens(data,10)
    #countArtistPlayTime(data,'Young the Giant')
    
    countTimeOfDayListening(data)
    
    #data = subsetDataByDate(data,'2020-07-01','2020-08-01')
    
    runMethodOnYear(data,'2020')

    
    #countArtistListens(data,10)
    #countTimeOfDayListening(data)
    
    
    #removeData()
    
    
    pass



Main()