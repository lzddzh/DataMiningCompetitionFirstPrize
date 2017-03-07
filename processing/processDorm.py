import json
import operator # for sort diction by value
from sets import Set
from datetime import date, time, datetime
import readFromFile
import sys

timeCritera = ['00_00', '01_00', '03_00', '06_00', '09_00', '11_20', '12_50', '16_50', '19_00', '22_00', '24_00'] # '24:00' does not exsits, but is useful as the last element.

if sys.argv[1] == 'train':
    lines = readFromFile.readLines('../studentForm/train/dorm_train_invert.txt')
elif sys.argv[1] == 'test':
    lines = readFromFile.readLines('../studentForm/test/dorm_test_invert.txt')
else:
    print "Invalid arguments"
print lines[0]

students_earest = {}
students_lastest = {}
# see rank:
for line in lines:
    # Split one students records apart.
    records = line.split('$')
    # stuId  = int(records[0]) 
    # If there exsits records for this student
    if len(records) > 1:
        earest = '24:00:00'
        lastest1 = '00:00:00'
        lastest2 = '00:00:00'
        ave_earest = 0 
        ave_lastest = 0 
        countDayEarest = 1 
        countDayLastest = 1 
        # initially, lastDate = the first date in the list 
        lastDate = records[1].split(',')[0][1:-1].split(' ')[0]
        #print int(records[0])
        #print records
        # Iterate from the first record to the last record.
        for i in range(1, len(records)):
            items = records[i].split(',')
            # items = [ '"2013/12/04 17:50:51"', '"1"' ]
            if len(items) != 2:
                print "Error in split one record into items. wrong number of items in record."
            items[0] = items[0][1:-1]
            items[1] = items[1][1:-1]
            date = items[0].split(' ')[0]
            time = items[0].split(' ')[1]
            if lastDate != date and time > '05:55:00':
                #print lastDate, date
                lastDate = date
                #print int(records[0]), date, time, countDay
                ave_earest += int(earest[:2]) * 60 * 60 + int(earest[3:5]) * 60 + int(earest[6:8])
                #print "**", lastest1, lastest2
                temp = lastest1 if lastest2 == '00:00:00' else lastest2
                ave_lastest += int(temp[:2]) * 60 * 60 + int(temp[3:5]) * 60 + int(temp[6:8])
                if temp != '00:00:00':
                    countDayLastest += 1
                if earest != '24:00:00':
                    countDayEarest += 1
                #print ave_earest, lastest1, lastest2
                earest = '24:00:00'
                lastest1 = '00:00:00'
                lastest2 = '00:00:00'
            if earest > time and time > '05:55:00':
                earest = time
            if lastest2 < time and '00:00:00' <= time and time <= '05:54:00':
                if '00:00:00' == time:
                    lastest2 = '00:00:01'
                lastest2 = time
            #print time
            if lastest1 < time and '16:00:00' <= time and time < '24:00:00':
                lastest1 = time
        #print countDay, ave_earest, earest, lastest1, lastest2
        ave_earest += int(earest[:2]) * 60 * 60 + int(earest[3:5]) * 60 + int(earest[6:8])
        temp = lastest1 if lastest2 == '00:00:00' else lastest2
        ave_lastest += int(temp[:2]) * 60 * 60 + int(temp[3:5]) * 60 + int(temp[6:8])
        ave_earest /= countDayEarest
        hour = ave_earest/3600
        ave_earest -= hour * 3600
        minute = ave_earest/60
        ave_earest -= minute * 60
        second = ave_earest
        str_hour = str(hour) if len(str(hour)) == 2 else ('0'+str(hour))
        str_minute = str(minute) if len(str(minute)) == 2 else ('0'+str(minute))
        str_second = str(second) if len(str(second)) == 2 else ('0'+str(second))
        students_earest[int(records[0])] = str_hour + ':' + str_minute + ':' + str_second
        ave_lastest /= countDayLastest
        hour = ave_lastest/3600
        ave_lastest -= hour * 3600
        minute = ave_lastest/60
        ave_lastest -= minute * 60
        second = ave_lastest
        str_hour = str(hour) if len(str(hour)) == 2 else ('0'+str(hour))
        str_minute = str(minute) if len(str(minute)) == 2 else ('0'+str(minute))
        str_second = str(second) if len(str(second)) == 2 else ('0'+str(second))
        if str_hour < '05':
            str_hour = str(int(str_hour) + 24) 
        students_lastest[int(records[0])] = str_hour + ':' + str_minute + ':' + str_second
        #if int(records[0]) == 20591:
        #    print students_earest[int(records[0])]
        #    print students_lastest[int(records[0])]
        #    exit()

#print students_earest
#print students_lastest
#sorted_earest = sorted(students_earest.items(), key=operator.itemgetter(1))
#sorted_lastest = sorted(students_lastest.items(), key=operator.itemgetter(1), reverse=True)

#print sorted_lastest[:100]
#print sorted_earest[:100]
#print ranks
                    
fw = open(sys.argv[1] + 'Processed/DormProcessed.txt', 'w')
#count = 0
for line in lines:
    '''
        Features:
           1. number of days that have record.
           2. averange number of records per day.
           3. 06:00-09:00 records per record day. Separete 0 and 1.
           4. 09:00-11:20 records per record day.
           5. 11:20-12:50 reocrds per record day.
           6. 12:50-16:50 records per record day.
           7. 16:50-19:00 records per record day.
           8. 19:00-22:00 records per record day.
           9. 22:00-01:00 records per reocrd day.
           10. 01:00-03:00 records per record day.
           11. 03:00-6:00 records per record day.
           12. Maxmium record density in months. add the (year, month) as the key to a dictionary.
           13. Number of records in every Sat and Sun day. Separete 0 and 1. Divide by 1.
    '''
    features = {'stuId':-1, 'totalDays':0, 'timesPerDay':0.0, 'maxMonthDensity':0.0, 'weekendTimes':0}
    # For example, features['01:00enter'] means feature No. 10 in above comment.
    # Note that features['22:00enter'] means time interval 22:00-01:00
    for i in range(1, len(timeCritera) - 1):
        features[timeCritera[i] + 'enter'] = features[timeCritera[i] + 'exit'] = 0
    
    # Split one students records apart.
    records = line.split('$')
    # The first is the student ID.
    features['stuId'] = int(records[0])
    ee_ = students_earest[features['stuId']]
    ll_ = students_lastest[features['stuId']]
    features['eariest_door_time'] = int(ee_[:2]) * 60 * 60 + int(ee_[3:5]) * 60 + int(ee_[6:]) 
    features['lastest_door_time'] = int(ll_[:2]) * 60 * 60 + int(ll_[3:5]) * 60 + int(ll_[6:])
    # If there exsits records for this student
    if len(records) > 1:
        totalRecordTimes = len(records) - 1
        distinctDays = Set()
        dateList = []
        # Iterate from the first record to the last record.
        for i in range(1, len(records)):
            items = records[i].split(',')
            # items = [ '"2013/12/04 17:50:51"', '"1"' ]
            if len(items) != 2:
                print "Error in split one record into items. wrong number of items in record."
            items[0] = items[0][1:-1]
            items[1] = items[1][1:-1]
            date = items[0].split(' ')[0]
            time = items[0].split(' ')[1]
            suffix = 'enter' if items[1] == '0' else 'exit'
            # Add the date of one record into a set, so the set size is distinct days
            distinctDays.add(date)
            
            hourMin = time[:5].replace(':', '_')
            for i in range(1, len(timeCritera)):
                if timeCritera[i] > hourMin:
                    if timeCritera[i] == '01_00':
                        features['22_00' + suffix] += 1
                    else:
                        features[timeCritera[i - 1] + suffix] += 1
                    break

            #dt = datetime.strptime("2015/08/31 23:21:45", "%Y/%m/%d %H:%M:%S")
            dt = datetime.strptime(items[0], "%Y/%m/%d %H:%M:%S")
            # Each slot of the timetuple is a int number of year, month, ....
            weekday = dt.timetuple()[6] # timetuple[6]== 0 means Monday, 1 means Tue
            if weekday == 5 or weekday == 6:
                features['weekendTimes'] += 1

            dateList.append(dt.date())

            
        features['totalDays'] = len(distinctDays)
        features['timesPerDay'] = float(totalRecordTimes) / features['totalDays']
        features['weekendTimesDiv'] = features['weekendTimes'] / float(features['totalDays'])
        for i in range(1, len(timeCritera) - 1):
            features[timeCritera[i] + 'enterDiv'] = features[timeCritera[i] + 'enter'] / float(features['totalDays'])
            features[timeCritera[i] + 'exitDiv'] = features[timeCritera[i] + 'exit'] / float(features['totalDays'])
            features[timeCritera[i] + 'both'] = float(features[timeCritera[i] + 'enter']) + float(features[timeCritera[i] + 'exit'])
            features[timeCritera[i] + 'bothDiv'] = features[timeCritera[i] + 'both'] / float(features['totalDays'])
            
        #Below calculat the max month density.
        monthDensities = {}
        for each in list(distinctDays):
            if each[:7] in monthDensities:
                monthDensities[each[:7]] += 1
            else:
                monthDensities[each[:7]] = 1
        features['maxMonthDensity'] = monthDensities[max(monthDensities, key = monthDensities.get)]

        #Below find the lastday and the first day of in the record.
        '''
        dateList = sorted(dateList)
        delta = dateList[-1] - dateList[0]
        if delta.days > 29:
            features['totalDays'] /= float(delta.days)
            features['totalRecordTimes'] /= float(delta.days)
            features['eveningTimes'] /= float(delta.days)
            features['weekendTimes'] /= float(delta.days)
        else:
            print "delta.days strange value: ", delta.days
            count += 1
        '''
    fw.write(json.dumps(features, sort_keys=True) + '\n')

#print "The total number of people that has only no more than one day record is ", count  (printed result is 0, all student have record)
