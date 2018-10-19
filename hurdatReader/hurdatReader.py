#!/usr/bin/env python 3.2
'''
Module for reading a HURDAT data file.

Import and call methods.

@author: David Stack
'''

__all__ = ['isHeader', 'isFooter', 'madeLandfall', 'getName', 'getYear',
           'getMonth', 'getDay', 'getStormNum', 'getNumDays', 'getDailyData',
           'getStage','getLat', 'getLon', 'getWind', 'getPressure',
           'getCategory','test']

import classifier

def isHeader(line):
    '''Returns True if line is header, false if not.'''
    if line[0:2] in ['AL','EP','CP']:
        result = True
    else:
        result = False
    return result

def isFooter(line):
    '''Returns True if line is footer, false if not.'''
    result = False
#    try:
#        int(line[6])
#    except ValueError:
#        result = True
#    return result

def madeLandfall(line):
    '''Returns if storm made landfall or not.'''
    landfall = line[16:17]
    if landfall[0] == 'L':
        return 'Landfall'
    return '0'
#    if (isHeader(line) and line[52] == '1'):
#        result = 1
#    else:
#        result = 0
#    return result

def getName(line):
    '''Returns storm name.'''
    if isHeader(line):
        name = line[18:28]
    return name

def getYear(line):
    '''Returns storm year.'''
    if isHeader(line):
        year = line[4:8]
    return int(year)

def getMonth(line):
    '''Returns storm month.'''
    month = line[4:6]
    if month[0] == '0':
        month = ' ' + month[1]
    return int(month)

def getDay(line):
    '''Returns storm day.'''
    day = line[6:8]
    if day[0] == '0':
        day = ' ' + day[1]
    return int(day)

def getHour(line):
    '''Returns storm hour'''
    hour = line[10:12]
    if hour[0] == '0':
        hour = ' ' + hour[1]
    return int(hour)

def getStormID(line):
    '''Returns the number of the storm (from total record).'''
    if isHeader(line):
        stormID = line[2:4].strip().zfill(2)
    stormID = str(getYear(line)) + stormID
    return int(stormID)

def getNumDays(line):
    '''Returns the number of days of data there are.'''
    if isHeader(line):
        numDays = int(line[33:36])
    return numDays

def getStage(line, x, y):
    stage = line[19:21]
    if stage == 'TD':
        stage = 'Tropical Depression'
    elif stage == 'TS':
        stage = 'Tropical Storm'
    elif stage in ['HU','TY','ST']:
        stage = 'Hurricane'
    elif stage in ['EX','ET']:
        stage = 'Extratropical Cyclone'
    elif stage == 'SD':
        stage = 'Subtropical Depression'
    elif stage == 'SS':
        stage = 'Subtropical Storm'
    elif stage == 'WV':
        stage = 'Tropical Wave'
    elif stage == 'LO':
        stage = 'Remnant Low'
    elif stage == 'DB':
        stage = 'Disturbance'
    elif stage == 'PT':
        stage = 'Post-Tropical'
    return stage

def getLat(line, x, y):
    '''Returns the latitude for specific 6 hour measurement.'''
    lat = line[23:27]
    lat = lat[0:2] + '.' + lat[3]
    try:
        float(lat)
    except ValueError:
        print (line)
    return float(lat)

def getLon(line, x, y):
    '''Returns the longitude for specific 6 hour measurement.'''
    lon = line[30:35]
    lon = lon[0:3] + '.' + lon[4]
    lon = float(lon)
    hem = line[35:36]
    if hem == 'E':
        lon = 360 - lon
    return lon * -1

def getWind(line, x, y):
    '''Returns wind spead for specific 6 hour measurement.'''
    wind = line[38:41]
    return int(wind)

def getPressure(line, x, y):
    '''Returns pressure for specific 6 hour measurement.'''
    pressure = line[43:47]
    if pressure == '   0':
        pressure = -999
    return int(pressure)

def getCategory(line, x, y):
    '''Returns category for specific 6 hour measurement.'''
    category = classifier.classify(getWind(line, x, y))
    return category

def test():
    '''Test function.'''
    print('---Module hurdatReader test---')
    import os, fileIO
    
    ## Atlantic
    #hurdatData = fileIO.openFile('hurdat2-1851-2017-050118.txt', '..\\data')

    # East Pacific
    hurdatData = fileIO.openFile('hurdat2-nepac-1949-2017-050418.txt', '..\\data')
    
    hourList = [0,6,12,18]
    for line in hurdatData:
        if isHeader(line):
            ID = getStormID(line)
            name = getName(line).strip()
            year = getYear(line)
        elif isFooter(line):
            pass
        else:
            x = 0
            y = 0
#            for i in range(4):
            lon = getLon(line, x, y)
            if (getLat(line, x, y) and lon != 0.0 and year == 2014):
#                if lon >= 180.0:
#                    lon = (lon - 360)*-1
#                else:
#                    lon = lon * -1
                print('\n')
                print('ID   :', str(ID))
                print('Name :', name)
                print('Year :', str(year))
                print('Month:', str(getMonth(line)))
                print('Day  :', str(getDay(line)))
                print('Hour :', str(getHour(line))) # write hour
                print('Lat  :', str(getLat(line, x, y)))
                print('Lon  :', str(lon).strip())
                print('Wind :', str(getWind(line, x, y)))
                print('Press:', str(getPressure(line, x, y)))
                print('Stage:', getStage(line, x, y))
                print('Cat  :', getCategory(line, x, y))
                print('Land :', str(madeLandfall(line)))
#            x = y
#            y = x + 17
            if getMonth(line) == 12 and getDay(line) == 31 and getHour(line) == 18:
                year = year + 1
    hurdatData.close()

# Run test if module is run as a program
if __name__ == '__main__':
    test()
