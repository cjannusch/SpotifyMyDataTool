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
from datetime import timedelta
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from SpotifyApiKeys import CLIENT_ID,CLIENT_SECRET
import random


def createSpotifyAPIConnection():
    auth_manager = SpotifyClientCredentials(CLIENT_ID,CLIENT_SECRET)
    sp = spotipy.Spotify(auth_manager=auth_manager)
    
    return sp




def encode(num):
    """Encode a positive number into Base X and return the string.

    Arguments:
    - `num`: The number to encode
    - `alphabet`: The alphabet to use for encoding
    """
    
    BASE62 = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    
    if num == 0:
        return BASE62[0]
    arr = []
    arr_append = arr.append  # Extract bound-method for faster access.
    _divmod = divmod  # Access to locals is faster.
    base = len(BASE62)
    while num:
        num, rem = _divmod(num, base)
        arr_append(BASE62[rem])
    arr.reverse()
    return ''.join(arr)

def decode(string):
    """Decode a Base X encoded string into the number

    Arguments:
    - `string`: The encoded string
    - `alphabet`: The alphabet to use for decoding
    """
    
    BASE62 = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    
    base = len(BASE62)
    strlen = len(string)
    num = 0

    idx = 0
    for char in string:
        power = (strlen - (idx + 1))
        num += BASE62.index(char) * (base ** power)
        idx += 1

    return num




# TODO WORK IN PROGRESS IT NO WORKY
def findRandomSong(sp, n=10):
        
    listOfSongsToSearchFor = []
    
    SpotifyID = '6rqhFgbbKwnb9MLmUQDhG6'
    
    result = sp.track(SpotifyID)
    
    print(result)
    
    
    #for i in range(n):
        #number = random.randint()
    
    #number = 100
    
    pass


def lookAtUsersPublicPlayLists(sp):
    
    #q=track:TRACKNAME%20artist:ARTISTNAME&type=track
    #q=artist:ARTISTNAME&type=artist
    
    
    #newFile = open('ListOfNames.txt','w+',encoding = 'utf-8')
    
    SpotifyUserToSearchFor = str(getUser())
    #AlbumID= '0QIzRT7DLG6Eg74WfSUSvW'
    
    dictOfAlbums = {}
    
    count = 0
    
    playlists = sp.user_playlists(SpotifyUserToSearchFor)
    while playlists:
        for i, playlist in enumerate(playlists['items']):
            #print("Playlist = " + str(playlist['name']) + "\n")
            #newFile.write("Playlist = " + str(playlist['name']) + "\n")
            dictOfAlbums[str(playlist['name'])] = []
            
            result = sp.user_playlist_tracks(SpotifyUserToSearchFor,playlist['id'])
    
            for song in result['items']:
                if song == None:
                    pass
                    #print("total songs" + str(count) + "\n")
                    #newFile.write("total songs" + str(count) + "\n")
                    #newFile.close()
                count +=1
                #print('\t' + str(song['track']['name']) + "\n")
                #newFile.write('\t' + str(song['track']['name']) + "\n")
                stringToAppend = ""
                stringToAppend = stringToAppend + str(song['track']['name']) 
                #in case there are multiple listed artists for the track
                for artist in song['track']['artists']:
                    stringToAppend = stringToAppend + ' - ' + artist['name']
                dictOfAlbums[str(playlist['name'])].append(stringToAppend)
    
        if playlists['next']:
            playlists = sp.next(playlists)
        else:
            print("total songs",count)
            playlists = None

    print(dictOfAlbums)

def removeData():
    
    if path.exists('merged_file.json'):
        os.remove('merged_file.json')
        
    pass


def loadData(newMergeFile = False):
    
    if newMergeFile:
        removeData()
        
    # Performs automatic check to see if the merge file matches the MyData History
    # This is useful if you are running methods on multiple data sets in one session
    
    if path.exists('merged_file.json'):
        with open('merged_file.json', encoding="utf8") as f:
            inMerge = json.load(f)[0][0]
            with open('.\\my_spotify_data\\MyData\\StreamingHistory0.json', encoding="utf8") as g:
                inFirst = json.load(g)[0]
        if not inFirst == inMerge:
            print('data does not match')
            removeData()
    
    if path.exists('merged_file.json'):
        with open('merged_file.json') as f:
            data = json.load(f)
        return data
    
    read_files = []
    
    count = 0
    filename = '.\\my_spotify_data\\MyData\\StreamingHistory' + str(count) +'.json'
    print('merging file:',filename)
    read_files.append(filename)
    
    while (path.exists(filename)):
        count += 1
        filename = '.\\my_spotify_data\\MyData\\StreamingHistory' + str(count) +'.json'
        if not path.exists(filename):
            break
        print('merging file:',filename)
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
    
    total = 0
    
    for item in data:
        for item2 in item:
            total += item2['msPlayed']
    #print('days listened:',total / (60*60*24*1000))
    print('hours listened:',total / (60*60*1000))
    #print('minutes listened:',total / (60*1000))
    
    return total / (60*60*1000)
    
def countArtistListens(data,numberOfTopArtists,toGraph = False):
    
    artistCountDict = {}
    toGraph = {}
    
    for item in data:
        for item2 in item:
            if str(item2['artistName']) in artistCountDict:
                artistCountDict[str(item2['artistName'])] += 1
            else:
                artistCountDict[str(item2['artistName'])] = 1   
    for i in range(numberOfTopArtists):
        if len(artistCountDict.keys()) == 0:
            continue
        maximum = max(artistCountDict, key=artistCountDict.get)  # Just use 'min' instead of 'max' for minimum.
        print(str(i + 1)+':',maximum, '-', artistCountDict[maximum])
        toGraph[maximum] = artistCountDict[maximum]
        artistCountDict.pop(maximum)
        
    # Start of graphing stuff 
    
    if toGraph:
        
        dateStart,dateEnd = getTimePeriodOfData(data)
            
        font = {'family' : 'normal',
            'weight' : 'normal',
            'size'   : 10}
        plt.rc('font', **font)
        
        plt.bar(list(toGraph.keys()), toGraph.values(), color='r', width=0.8)
        #plt.legend(loc="upper left")
        plt.title(getUser()+'\'s favorite Artists \nfrom ' + str(dateStart) + ' --> ' + str(dateEnd))
        plt.ylabel('# of songs listened to')
        plt.style.use('ggplot')
        plt.xticks(rotation=45, ha='right')
        plt.autoscale()
        plt.show()

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
            to_zone = tz.tzlocal()
            utc = datetime.strptime(item2['endTime'], '%Y-%m-%d %H:%M')
            converted = utc.astimezone(to_zone)
            toSubtract = int(str(converted)[-6:-3])
            converted = str(converted)[0:-9] #converts to same format as before! woop woop
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
    
    dateStart,dateEnd = getTimePeriodOfData(data)
    
    plt.bar(list(listOfCounts.keys()), listOfCounts.values(), color='g')
    plt.title(getUser()+'\'s listening habits \nfrom ' + str(dateStart) + ' --> ' + str(dateEnd))
    plt.xlabel('Hour of The Day')
    plt.ylabel('# of songs listened to')
    plt.style.use('ggplot')
    #plt.show()
    
    return plt.gcf()


def subsetDataByDate(data,startDate,endDate):
    
    # format of dates is '2020-12-16 TI:ME'
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

def getUser():
    
    filename = '.\\my_spotify_data\\MyData\\Userdata.json'
    
    if not path.exists(filename): 
        return 'NO NAME LOL'
    
    with open(filename) as f:
        user = json.load(f)
        user = user['username']
        return user


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


# TODO Make this method smarter? or break into different methods i suppose
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
        #countPlayTime(subsetData)
        #countArtistListens(subsetData,3)
        countTimeOfDayListening(subsetData)
        
    #extra for december 
    start,end = year+'-12-01',year+'-12-31'
    subsetData = subsetDataByDate(data,start,end)
    print(start,'-->',end)
    #countPlayTime(subsetData)
    #countTimeOfDayListening(subsetData)
    countArtistListens(subsetData,3)
    

def countSongListens(data,numberOfTopSongs,toGraph = False):
    
    trackNameCountDict = {}
    toGraph = {}
    
    for item in data:
        for item2 in item:
            if '"'+str(item2['trackName'])+'" by: '+item2['artistName']  in trackNameCountDict:
                trackNameCountDict['"'+str(item2['trackName'])+'" by: '+item2['artistName']] += 1
            else:
                trackNameCountDict['"'+str(item2['trackName'])+'" by: '+item2['artistName']] = 1   
    for i in range(numberOfTopSongs):
        if len(trackNameCountDict.keys()) == 0:
            continue
        maximum = max(trackNameCountDict, key=trackNameCountDict.get)  # Just use 'min' instead of 'max' for minimum.
        print(str(i + 1)+':',maximum,'-', trackNameCountDict[maximum])
        toGraph[maximum] = trackNameCountDict[maximum]
        trackNameCountDict.pop(maximum)
        
    #Start of graph shiznit    
    
    if toGraph:
        
        dateStart,dateEnd = getTimePeriodOfData(data)
            
        font = {'family' : 'normal',
            'weight' : 'normal',
            'size'   : 10}
        plt.rc('font', **font)
        
        plt.bar(list(toGraph.keys()), toGraph.values(), color='r',align='edge', width=.8)
        #plt.legend(loc="upper left")
        plt.title(getUser()+'\'s favorite songs \nfrom ' + str(dateStart) + ' --> ' + str(dateEnd))
        plt.ylabel('# of songs listened to')
        plt.style.use('ggplot')
        plt.xticks(rotation=45, ha='right')
        plt.autoscale()
        plt.show()
    
        
    
# TODO redo logic on this method
def countMostConsecutiveListens(data,minimumListenTime = 2):
    
    isNewListeningSession = True
    listOfListeningSessions = {}
    initialItem = None
    initialDate = None
    nextItem = None
    nextDate = None
    listOfShit = []
    
    count = 0
    length = 0
    
    for item in data:
        for i in range(len(item)-1):
            if isNewListeningSession:
                if length > minimumListenTime:
                    #print(initialDate,'to',nextDate,'number of songs',count,'length of listen session',length, 'hours.')
                    listOfShit.append(((str(initialDate)+' to '+str(nextDate)),length))
                initialDate = item[i]['endTime']
                nextDate = item[i+1]['endTime']
                count = 0
                length = 0
                isNewListeningSession = False
            initialItem = item[i]
            nextItem = item[i+1]
            nextDate = item[i+1]['endTime']
            
            isChain = convertStringToDatetimeHelper(nextItem['endTime']) - \
            convertStringToDatetimeHelper(initialItem['endTime']) <= timedelta(milliseconds =\
            initialItem['msPlayed'] + 90000)
            
            if not isChain:
                isNewListeningSession = True
                
            else:
                count += 1
                length += initialItem['msPlayed'] / (60000 * 60)
                isNewListeningSession = False
                
    fig, ax = plt.subplots()
    
    for point in listOfShit:
        plt.scatter(point[0][:10], point[1])
                

    plt.xticks(rotation=60, ha='right')
    startDate,endDate = getTimePeriodOfData(data)
    plt.title(getUser()+'\'s listening sessions greater than \n ' + str(minimumListenTime) + ' hours')
    #plt.xticks([])
    plt.ylabel('length of listening (hours)')
    plt.xlabel('from ' + str(startDate) + ' --> ' + str(endDate))
    
    if len(listOfShit) > 20:
        plt.xticks([])
    
    plt.show() 

def convertStringToDatetimeHelper(stringDate):
    
    Year = stringDate[0:4]
    Month = stringDate[5:7]
    Day = stringDate[8:10]
    Hour = stringDate[11:13]
    Second = stringDate[14:16]
    
    return datetime(int(Year),int(Month),int(Day),int(Hour),int(Second))
    
    
    
    pass
    
def getAllUserPlaylists():
    if not path.exists('.\\my_spotify_data\\MyData\\Playlist1.json'):
        print('file no exist bro')
        return
    with open('.\\my_spotify_data\\MyData\\Playlist1.json', encoding="utf8") as g:
        data = json.load(g)["playlists"]
    

    dictOfPlaylists = {}
    count = 0
    
    for playlist in data:
        dictOfPlaylists[playlist['name']] = []
        for song in playlist['items']:
            dictOfPlaylists[playlist['name']].append(song['track']['trackName'] \
                                                     + ' - ' + song['track']['artistName'])

    
    #print(data)
    
    return dictOfPlaylists



# TODO Write method to find new artists over monthly period

# TODO Make use of graphs more, everyone likes graphs

# TODO Link last Spotify Loopup program to this one

def Main():
    #data = loadData()
    #sp = createSpotifyAPIConnection()

    #countPlayTime(data)
    #countArtistListens(data,10)
    #countArtistPlayTime(data,'Big Gigantic')
    
    #countTimeOfDayListening(data)
    
    #data = subsetDataByDate(data,'2020-03-01','2020-05-01')
    
    #runMethodOnYear(data,'2020')

    #countArtistListens(data,10,True)
    #countSongListens(data,10,True)
    #countTimeOfDayListening(data)


    #countMostConsecutiveListens(data,0.2)

    #playlists = getAllUserPlaylists()

    #print(playlists.keys())
    #print(playlists['Westridge Pilot'])

    
    pass



Main()