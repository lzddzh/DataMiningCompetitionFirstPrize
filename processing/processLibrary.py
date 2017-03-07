import json
from sets import Set
from datetime import date, time, datetime
import readFromFile
import sys

timeCritera = ['00_00', '01_00', '03_00', '06_00', '09_00', '11_20', '12_50', '16_50', '19_00', '22_00', '24_00'] # '24:00' does not exsits, but is useful as the last element.

students = ""

if sys.argv[1] == 'train':
    lines = readFromFile.readLines('../studentForm/train/library_train_invert.txt')
elif sys.argv[1] == 'test':
    lines = readFromFile.readLines('../studentForm/test/library_test_invert.txt')
else:
    print 'Invalid arguments'
print lines[0]
count = 0
for line in lines:
    '''
    The feature will record below features:
        1: value of 2/3 
        2: total record times of a student
        3. total days in library
        4. times a student 19:00-22:00 has record in library.
        5. weekenday in library times.

        2-5 should divede by the 3 
    '''
    features = {'stuId':-1, 'totalRecordTimes':0, 'totalDays':0, 'eveningTimes':0, 'weekendTimes':0,
            'timesPerDay':0.0}
    # For example, features['01:00enter'] means feature No. 10 in above comment.
    # Note that features['22:00enter'] means time interval 22:00-01:00
    for i in range(1, len(timeCritera) - 1):
        features[timeCritera[i] + 'library'] = 0

    # Split one students records apart.
    records = line.split('$')
    # The first is the student ID.
    features['stuId'] = int(records[0])
    # If there exsits records for this student
    if len(records) > 1:
        features['totalRecordTimes'] = len(records) - 1
        distinctDays = Set()
        dateList = []
        # Iterate from the first record to the last record.
        for i in range(1, len(records)):
            items = records[i].split(',')
            # items = [ '"7"', '"2013/12/04 17:50:51"' ]
            if len(items) != 2:
                print "Error in split one record into items. wrong number of items in record."
            items[1] = items[1][1:-1]
            date = items[1].split(' ')[0]
            time = items[1].split(' ')[1]
            # Add the date of one record into a set, so the set size is distinct days
            distinctDays.add(date)

            hourMin = time[:5].replace(':', '_')
            for i in range(1, len(timeCritera)):
                if timeCritera[i] > hourMin:
                    if timeCritera[i] == '01_00':
                        features['22_00' + 'library'] += 1
                    else:
                        features[timeCritera[i - 1] + 'library'] += 1
                    break
            
            hour = int(time.split(':')[0])
            if hour >= 19 and hour <= 22:
                features['eveningTimes'] += 1
            #dt = datetime.strptime("2015/08/31 23:21:45", "%Y/%m/%d %H:%M:%S")
            dt = datetime.strptime(items[1], "%Y/%m/%d %H:%M:%S")
            # Each slot of the timetuple is a int number of year, month, ....
            weekday = dt.timetuple()[6] # timetuple[6]== 0 means Monday, 1 means Tue
            if weekday == 5 or weekday == 6:
                features['weekendTimes'] += 1

            dateList.append(dt.date())
            
        features['totalDays'] = len(distinctDays)
        features['timesPerDay(Div)'] = float(features['totalRecordTimes']) / features['totalDays']
        features['eveningTimesDiv'] = features['eveningTimes'] / float(features['totalDays'])
        features['weekendTimesDiv'] = features['weekendTimes'] / float(features['totalDays'])
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
    students += json.dumps(features, sort_keys=True) + '\n'

#print "The total number of people that has only no more than one day record is ", count
with open(sys.argv[1] + 'Processed/LibraryProcessed.txt', 'w') as fw:
    fw.write(students)
