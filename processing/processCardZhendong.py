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
def type_mapping(chinese):
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

nian = ['2013/01/09', '2014/01/31', '2015/02/19', '2016/02/08']
_slice = [0, 2.5, 5.0, 10.0, 15.0, 20.0, 30.0, 50.0, float('inf')]
_slice2 = [0, 10, 20, 30, 40, 50]
type_list = ["图书馆", "", "校医院", "超市", "开水", "食堂", "洗衣房", "其他", "教务处", "文印中心", "校车", "淋浴"]
for i in range(len(type_list)):
    type_list[i] = type_mapping(type_list[i])
lines = open(root_loc).readlines()
fw = open(sys.argv[1] + 'Processed/Card2Processed.txt', 'w')
# for every person
for line in lines[:500]:
    temps = line.strip("\n").split("$")
    #print temps[0]
    print(temps[0])
    features = {'stuId':int(temps[0]), 'publick_holiday_amount':0, 'breakfastTime_ave':0, 'lunchTime_ave':0, 'dinnerTime_ave':0, 
            'breakfastTime_min':0, 'lunchTime_min':0, 'dinnerTime_min':0, 'breakfastTime_max':0, 'lunchTime_max':0, 'dinnerTime_max':0, 
            'breakfastTime_var':0, 'lunchTime_var':0, 'dinnerTime_var':0 }
    for i in range(len(_slice) - 1):
        features['slice_' + str(_slice[i]) + '_' + str(_slice[i + 1])] = 0
    for i in range(len(_slice2)):
        features['consumeDayOver_' + str(_slice2[i])] = 0
    breakfastTimes = []
    lunchTimes = []
    dinnerTimes = []
    weekdays = {}
    dateSet = set()
    lastDate = ""
    lastTime = ""
    consumeDay = 0.0
    dayMax = 0
    intervalSeconds = {}
    intervalDays = {} 
    cateLastTime = {}
    cateLastDay = {} 
    firstDay2013 = '2016/12/30'
    lastDay2013 = '2012/01/01'
    firstDay2014 = '2016/12/30'
    lastDay2014 = '2012/01/01'
    firstDay2015 = '2016/12/30'
    lastDay2015 = '2012/01/01'
    aveCateenPlaces = 0
    lastWeekends = 0 
    countWeeks = 1 
    cateenSet = set()
    topUp5DaysList = []
    topUp5DaysBalanceList = []
    boolNian = [False, False, False, False] # 2013, 2014, 2015
    for typeName in type_list:
        cateLastTime[typeName] = cateLastDay[typeName] = ""
        intervalSeconds[typeName] = []
        intervalDays[typeName] = []
    for i in range(7):
        weekdays[i] = []

    # every record for one person 
    for i in range(1, len(temps)):
        records = temps[i].split(",")
        cate = records[0].strip("\"")
        #python2 location = unicode(records[1].strip("\""), "utf-8")[2:]
        location = records[1].strip("\"")[2:] 
        type = type_mapping(records[2].strip("\""))
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

        # Count the nearest days of top-up
        if cate == "圈存转账" or cate == "支付领取" or cate == "卡充值":
            j = i
            while j < len(temps):
                records1 = temps[j].split(",")
                time1 = records1[3].strip("\"")
                cate1 = records1[0].strip("\"")
                amount1 = float(records1[4].strip("\""))
                date1 = time1.split(" ")[0]
                balance1 = float(records1[5].strip("\""))
                if "POS消费" == cate1:
                    topUp5DaysList.append(amount1)
                    topUp5DaysBalanceList.append(balance1)

                a = datetime.datetime.strptime(date, "%Y/%m/%d")
                b = datetime.datetime.strptime(date1, "%Y/%m/%d")
                delta = (a - b).days
                if delta > 3 or delta < -3:
                    break
                j += 1
            j = i
            while j > 0:
                records1 = temps[j].split(",")
                time1 = records1[3].strip("\"")
                cate1 = records1[0].strip("\"")
                amount1 = float(records1[4].strip("\""))
                date1 = time1.split(" ")[0]
                balance1 = float(records1[5].strip("\""))
                if "POS消费" == cate1:
                    topUp5DaysList.append(amount1)
                    topUp5DaysBalanceList.append(balance1)

                a = datetime.datetime.strptime(date, "%Y/%m/%d")
                b = datetime.datetime.strptime(date1, "%Y/%m/%d")
                delta = (a - b).days
                if delta > 3 or delta < -3:
                    break
                j -= 1

        # How many places this student have been for canteen in a week
        if weekends < lastWeekends and i != 1:
            aveCateenPlaces += len(cateenSet)
            cateenSet = set()
            countWeeks += 1

        if "POS消费" == cate and "canteen_" == type:
            cateenSet.add(location)
        
        # the first record in a year
        if month[:4] == '2013':
            if firstDay2013 > date and date > nian[0]:
                firstDay2013 = date
        if month[:4] == '2014':
            if firstDay2014 > date and date > nian[1]:
                firstDay2014 = date
        if month[:4] == '2015':
            if firstDay2015 > date and date > nian[2]:
                firstDay2015 = date

        # the last record in a year
        if month[:4] == '2013':
            if lastDay2013 < date and date < nian[1]:
                lastDay2013 = date
        if month[:4] == '2014':
            if lastDay2014 < date and date < nian[2]:
                firstDay2014 = date
        if month[:4] == '2015':
            if lastDay2015 < date and date < nian[3]:
                lastDay2015 = date
        
        # See if this student has record around the spring festval
        for i in range(len(nian)):
            a = datetime.datetime.strptime(date, "%Y/%m/%d")
            b = datetime.datetime.strptime(nian[i], "%Y/%m/%d")
            delta = (a - b).days
            if delta < 50:
                boolNian[i] = True

        # count holidays
        if month_day == '01/01' or month_day == '02/14' or month_day == '04/05' or month_day == '05/01' or month_day == '10/01' \
          or month_day == '10/02' or month_day == '10/03' or month_day == '10/04' or month_day == '10/05' or month_day == '12/05':
            if cate == "POS消费" and amount > 0:
                if 'holidays_amount' not in features:
                    features['holidays_amount'] = amount
                else: 
                    features['holidays_amount'] += amount
        else:
            if cate == "POS消费" and amount > 0:
                if 'non_holidays_amount' not in features:
                    features['non_holidays_amount'] = amount
                else:
                    features['non_holidays_amount'] += amount

        # If a new day.
        if date != lastDate and i != 1:
            for i in range(len(_slice2)):
                if consumeDay > _slice2[i]: 
                    features['consumeDayOver_' + str(_slice2[i])] += 1
            consumeDay = 0

        # get time interval
        if date == lastDate:
            for typeName in type_list:
                if type == typeName:
                    if cateLastTime[typeName] != "":
                        intervalSeconds[typeName].append( 60 * 60 * int(timeMin[:2]) + 60 * int(timeMin[3:5]) + int(timeMin[6:]) - ( 60 * 60 * int(cateLastTime[typeName][:2]) + 60 * int(cateLastTime[typeName][3:5]) + int(cateLastTime[typeName][6:]) ) )
                    cateLastTime[typeName] = timeMin

        # get day interval
        if date != lastDate:
            # initial the lastTime 
            for typeName in type_list:
                cateLastTime[typeName] = ""
            for typeName in type_list:
                if type == typeName:
                    if cateLastDay[typeName] != "":
                        a = datetime.datetime.strptime(date, "%Y/%m/%d")
                        b = datetime.datetime.strptime(cateLastDay[typeName], "%Y/%m/%d")
                        delta = (a - b).days
                        intervalDays[typeName].append(delta)
                    cateLastDay[typeName] = date
        
        # for calculate the consume times of a day on _slice2
        if 'POS消费' == cate and amount > 0: 
            consumeDay += amount

        # add date to set
        dateSet.add(date)
        
        # the breakfast, lunch and dinner time
        if 'canteen_' == type:
            if timeMin >= '05:00:00' and timeMin <= '10:40:00':
                breakfastTimes.append(int(timeMin[:2]) * 60 * 60 + int(timeMin[3:5]) * 60 + int(timeMin[6:8]))
            if timeMin >= '10:40:00' and timeMin <= '15:00:00':
                lunchTimes.append(int(timeMin[:2]) * 60 * 60 + int(timeMin[3:5]) * 60 + int(timeMin[6:8]))
            if timeMin >= '15:00:00' and timeMin <= '21:00:00':
                dinnerTimes.append(int(timeMin[:2]) * 60 * 60 + int(timeMin[3:5]) * 60 + int(timeMin[6:8]))

        # divide consume into monday to sundays.
        if 'POS消费' == cate and amount > 0:
            weekdays[weekends].append(amount)

        # divide consume amount into picese, according to the criteria given in _slice
        for i in range(len(_slice) - 1):
            if 'POS消费' == cate and amount >= _slice[i] and amount <= _slice[i + 1]:
                if 'slice' + str(i) + '_' + str(i + 1) not in features:
                    features['slice_' + str(_slice[i]) + '_' + str(_slice[i + 1])] = 1
                else:
                    features['slice_' + str(_slice[i]) + '_' + str(_slice[i + 1])] += 1
        lastDate = date
        lastWeekends = weekends
    #print intervalSeconds, intervalDays
    # totalDays is the number of days a student is active
    totalDays = len(dateSet)

    if len(breakfastTimes) == 0:
        breakfastTimes.append(0)
    if len(lunchTimes) == 0:
        lunchTimes.append(0)
    if len(dinnerTimes) == 0:
        dinnerTimes.append(0)
    
    # add features of meals
    features['breakfastTime_ave'] = np.mean(breakfastTimes)
    features['lunchTime_ave'] = np.mean(lunchTimes) 
    features['dinnerTime_ave'] = np.mean(dinnerTimes) 
    features['breakfastTime_min'] = min(breakfastTimes)
    features['lunchTime_min'] = min(lunchTimes)
    features['dinnerTime_min'] = min(dinnerTimes) 
    features['breakfastTime_max'] = max(breakfastTimes)
    features['lunchTime_max'] = max(lunchTimes)
    features['dinnerTime_max'] = max(dinnerTimes)
    features['breakfastTime_var'] = np.var(breakfastTimes)
    features['lunchTime_var'] = np.var(breakfastTimes) 
    features['dinnerTime_var'] = np.var(breakfastTimes) 
    
    # add features of weekdays

    '''
    for i in range(7):
        if 0 == len(weekdays[i]):
            weekdays[i].append(0)
    for i in range(7):
        features['weekday' + str(i) + '_amount'] = sum(weekdays[i])
        features['weekday' + str(i) + '_ave'] = np.mean(weekdays[i])
        features['weekday' + str(i) + '_min'] = min(weekdays[i])
        features['weekday' + str(i) + '_max'] = max(weekdays[i])
        features['weekday' + str(i) + '_var'] = np.var(weekdays[i])
    '''

    for i in range(len(_slice) - 1):
        features['slice_' + str(_slice[i]) + '_' + str(_slice[i + 1])] /= float(totalDays)

    for i in range(len(_slice2)):
        features['consumeDayOver_' + str(_slice2[i])] /= float(totalDays)

    # add the interval of two consume, by category
    for typeName in type_list:
        features['interval_Seconds_ave' + typeName] = np.mean(intervalSeconds[typeName]) if len(intervalSeconds[typeName]) != 0 else -1
        features['interval_Seconds_min' + typeName] = min(intervalSeconds[typeName]) if len(intervalSeconds[typeName]) != 0 else -1 
        features['interval_Seconds_max' + typeName] = max(intervalSeconds[typeName]) if len(intervalSeconds[typeName]) != 0 else -1
        features['interval_Days_ave' + typeName] = np.mean(intervalDays[typeName]) if len(intervalDays[typeName]) != 0 else -1
        features['interval_Days_min' + typeName] = min(intervalDays[typeName]) if len(intervalDays[typeName]) != 0 else -1
        features['interval_Days_max' + typeName] = max(intervalDays[typeName]) if len(intervalDays[typeName]) != 0 else -1

    # holidays and non-holidays
    if 'holidays_amount' not in features:
        features['holidays_amount'] = 0
    if 'non_holidays_amount' not in features:
        features['non_holidays_amount'] = 0

    features['holidays_amount'] /= float(totalDays)
    features['non_holidays_amount'] /= float(totalDays)
    features['sub_holidaysNone_amount'] = features['holidays_amount'] - features['non_holidays_amount']

    # the firstday
    delta = -1 
    c = 0
    if boolNian[0] and firstDay2013 != '2016/12/30':
        a = datetime.datetime.strptime(firstDay2013, "%Y/%m/%d")
        b = datetime.datetime.strptime(nian[0], "%Y/%m/%d")
        delta = (a - b).days
        c += 1
    
    if boolNian[1] and firstDay2014 != '2016/12/30':
        a = datetime.datetime.strptime(firstDay2014, "%Y/%m/%d")
        b = datetime.datetime.strptime(nian[1], "%Y/%m/%d")
        delta += (a - b).days
        c += 1

    if boolNian[2] and firstDay2015 != '2016/12/30':
        a = datetime.datetime.strptime(firstDay2015, "%Y/%m/%d")
        b = datetime.datetime.strptime(nian[2], "%Y/%m/%d")
        delta += (a - b).days
        c += 1

    features['firstDayInYear'] = delta / float(c) if c != 0 else -1

    # the lastday
    delta = -1
    c = 0
    if boolNian[0] and lastDay2013 != '2012/01/01':
        a = datetime.datetime.strptime(lastDay2013, "%Y/%m/%d")
        b = datetime.datetime.strptime(nian[0], "%Y/%m/%d")
        delta = (a - b).days
        c += 1

    if boolNian[1] and lastDay2014 != '2012/01/01':
        a = datetime.datetime.strptime(lastDay2014, "%Y/%m/%d")
        b = datetime.datetime.strptime(nian[1], "%Y/%m/%d")
        delta += (a - b).days
        c += 1

    if boolNian[2] and lastDay2015 != '2012/01/01':
        a = datetime.datetime.strptime(lastDay2015, "%Y/%m/%d")
        b = datetime.datetime.strptime(nian[2], "%Y/%m/%d")
        delta += (a - b).days
        c += 1

    features['lastDayInYear'] = delta / float(c) if c != 0 else -1
    features['winterHoliday'] = features['lastDayInYear'] + features['firstDayInYear']

    # count the differen places of canteen in a week
    features['canteenPlacesWeek'] = aveCateenPlaces / float(countWeeks)


    # top up nearest 5 days
    features['topUp5DaysConsume_ave'] = np.mean(topUp5DaysList) if len(topUp5DaysList) != 0 else 0
    features['topUp5DaysConsume_min'] = min(topUp5DaysList) if len(topUp5DaysList) != 0 else 0
    features['topUp5DaysConsume_max'] = max(topUp5DaysList) if len(topUp5DaysList) != 0 else 0

    features['topUp5DaysBalance_ave'] = np.mean(topUp5DaysList) if len(topUp5DaysBalanceList) != 0 else 0
    features['topUp5DaysBalance_min'] = min(topUp5DaysList) if len(topUp5DaysBalanceList) != 0 else 0
    features['topUp5DaysBalance_max'] = max(topUp5DaysList) if len(topUp5DaysBalanceList) != 0 else 0

    #print json.dumps(features, sort_keys=True)
    fw.write(json.dumps(features, sort_keys=True) + '\n')
