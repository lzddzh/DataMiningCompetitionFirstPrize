# -*- coding: UTF-8 -*-
import time
import datetime
import numpy as np
import sys
import os.path
import json        

if sys.argv[1] == 'train': 
    root_loc = "trainProcessed/card_train_inverted_cleaned.txt"
    feature_loc = "trainProcessed/CardProcessed.txt"
elif sys.argv[1] == 'test':
    root_loc = "testProcessed/card_test_inverted_cleaned.txt"
    feature_loc = "testProcessed/CardProcessed.txt"
else:
    #print "Invalid arguments"
    print("invalid arguments")

# translate Chinese to English
def typemapping(chinese):
    if chinese == "图书馆":
        return "labrary_"
    elif chinese == "":
        return "empty_"
    elif chinese == "校医院":
        return "hospital_"
    elif chinese == "超市":
        return "market_"
    elif chinese == "开水":
        return "water_"
    elif chinese == "食堂":
        return "canteen_"
    elif chinese == "洗衣房":
        return "landry_"
    elif chinese == "其他":
        return "other_"
    elif chinese == "教务处":
        return "academic_office_"
    elif chinese == "文印中心":
        return "printing_"
    elif chinese == "校车":
        return "bus_"
    else:
        return "shower_"

typelist = ["图书馆", "", "校医院", "超市", "开水", "食堂", "洗衣房", "其他", "教务处", "文印中心", "校车", "淋浴"]
for i in range(len(typelist)):
    typelist[i] = typemapping(typelist[i])
lines = open(root_loc).readlines()
fw = open(sys.argv[1] + 'Processed/Card4Processed.txt', 'w')
# for every person
for line in lines:
    temps = line.strip("\n").split("$")
    print(temps[0])
    features = {'stuId':int(temps[0]) }
    lastDate = ""
    dateSet = set()
    countdays07_08 = 0
    countdays11_12 = 0
    countdays17_18 = 0
    # every record for one person 
    typedict = {"labrary_": 0, "hospital_": 0, "market_": 0, "water_": 0, "canteen_": 0, "landry_": 0,
                        "other_": 0, "academic_office_": 0, "printing_": 0,
                        "bus_": 0, "shower_": 0, "empty_": 0} ## notice! there is no 'all' attribute.
    inlist = ['labrary_', 'market_', 'canteen_', 'landry_', 'bus_', 'water_']
    inlist = set(inlist)
    for each in typedict:
        if each not in inlist:
            continue
        features['07_0730' + each + '_amount'] = features['0730_08' + each + '_amount'] = 0.0
        features['11_1130' + each + '_amount'] = features['1130_12' + each + '_amount'] = 0.0
        features['17_1730' + each + '_amount'] = features['1730_18' + each + '_amount'] = 0.0  
        features['07_0730' + each + '_count'] = features['0730_08' + each + '_count'] = 0.0
        features['11_1130' + each + '_count'] = features['1130_12' + each + '_count'] = 0.0
        features['17_1730' + each + '_count'] = features['1730_18' + each + '_count'] = 0.0  
    features['07_08countDays'] = features['11_12countDays'] = features['17_18countDays'] = 0.0   
    for i in range(1, len(temps)):
        records = temps[i].split(",")
        cate = records[0].strip("\"")
        #python2 location = unicode(records[1].strip("\""), "utf-8")[2:]
        location = records[1].strip("\"")[2:] 
        type = typemapping(records[2].strip("\""))
        time = records[3].strip("\"")
        date = time.split(" ")[0]
        timeMin = time.split(" ")[1]
        month = date.split("/")[0] + "/" + date.split("/")[1]
        month_day = date.split("/")[1] + "/" + date.split("/")[2]
        hour = time.split(" ")[1].split(":")[0]
        amount = float(records[4].strip("\""))
        balance = float(records[5].strip("\""))
        weekends = datetime.datetime(int(date.split("/")[0]), int(date.split("/")[1]),
                                     int(date.split("/")[2])).strftime("%w")
        weekends = int(weekends)
        # POS消费 1099 shower_ 2015/01/06 07:59:04 2015/01/06 2015/01 01/06 07 1.3 4.31 2
        # print cate, location, type, time, date, month, month_day, hour, amount, balance, weekends

        dateSet.add(date)

        if cate == 'POS消费':
            if "07:00" <= timeMin[:5] and timeMin[:5] <= "08:00":
                countdays07_08 = 1
            if "11:00" <= timeMin[:5] and timeMin[:5] <= "12:00":
                countdays11_12 = 1
            if "17:00" <= timeMin[:5] and timeMin[:5] <= "18:00":
                countdays17_18 = 1
            
        if date != lastDate:
            features['07_08countDays'] += countdays07_08
            countdays07_08 = 0
            features['11_12countDays'] += countdays11_12
            countdays11_12 = 0
            features['17_18countDays'] += countdays17_18
            countdays17_18 = 0


        if cate == "POS消费" and type in inlist:
            if "07:00" <= timeMin[:5] and timeMin[:5] <= "07:30":
                features['07_0730' + type + '_amount'] += amount
                features['07_0730' + type + '_count'] += 1
            if "07:30" < timeMin[:5] and timeMin[:5] < "08:00":
                features['0730_08' + type + '_amount'] += amount
                features['0730_08' + type + '_count'] += 1
            if "11:00" <= timeMin[:5] and timeMin[:5] <= "11:30":
                features['11_1130' + type + '_amount'] += amount
                features['11_1130' + type + '_count'] += 1
            if "11:30" < timeMin[:5] and timeMin[:5] <= "12:00":
                features['1130_12' + type + '_amount'] += amount
                features['1130_12' + type + '_count'] += 1
            if "17:00" < timeMin[:5] and timeMin[:5] <= "17:30":
                features['17_1730' + type + '_amount'] += amount
                features['17_1730' + type + '_count'] += 1
            if "17:30" < timeMin[:5] and timeMin[:5] <= "18:00":
                features['1730_18' + type + '_amount'] += amount
                features['1730_18' + type + '_count'] += 1
        lastDate = date

    totalDays = len(dateSet)
    for each in typedict:
        if each not in inlist:
            continue
        features['07_0730' + each + '_amount'] /= float(totalDays)
        features['0730_08' + each + '_amount'] /= float(totalDays)
        features['11_1130' + each + '_amount'] /= float(totalDays)
        features['1130_12' + each + '_amount'] /= float(totalDays)
        features['17_1730' + each + '_amount'] /= float(totalDays)
        features['1730_18' + each + '_amount'] /= float(totalDays)
        features['07_0730' + each + '_count'] /= float(totalDays)
        features['0730_08' + each + '_count'] /= float(totalDays)
        features['11_1130' + each + '_count'] /= float(totalDays)
        features['1130_12' + each + '_count'] /= float(totalDays)
        features['17_1730' + each + '_count'] /= float(totalDays)
        features['1730_18' + each + '_count'] /= float(totalDays)

    features['07_08countDays'] /= float(totalDays)
    features['11_12countDays'] /= float(totalDays)
    features['17_18countDays'] /= float(totalDays)

    fw.write(json.dumps(features, sort_keys=True) + '\n')
