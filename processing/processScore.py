import json
import readFromFile
import sys

students = ""
if sys.argv[1] == 'train':
    lines = readFromFile.readLines('../studentForm/train/score_train_invert.txt')
elif sys.argv[1] == 'test':
    lines = readFromFile.readLines('../studentForm/test/score_test_invert.txt')
else:
    print 'Invalid arguments'
    
print lines[0]
count = 0 
maxRankOfFaculties = {}
for line in lines:
    records = line.split('$')
    twoNumber = records[1].split(',')
    faculty = int(twoNumber[0])
    rank = int(twoNumber[1])
    if faculty in maxRankOfFaculties:
        if rank > maxRankOfFaculties[faculty]:
            maxRankOfFaculties[faculty] = rank
    else:
        maxRankOfFaculties[faculty] = rank
print maxRankOfFaculties

linesTest = readFromFile.readLines('../studentForm/test/score_test_invert.txt')
for line in linesTest:
    records = line.split('$')
    twoNumber = records[1].split(',')
    faculty = int(twoNumber[0])
    rank = int(twoNumber[1])
    if faculty in maxRankOfFaculties:
        if rank > maxRankOfFaculties[faculty]:
            maxRankOfFaculties[faculty] = rank
    else:
        maxRankOfFaculties[faculty] = rank
print maxRankOfFaculties

linesTest1 = readFromFile.readLines('../studentForm/test1/score_test_invert.txt')
for line in linesTest1:
    records = line.split('$')
    twoNumber = records[1].split(',')
    faculty = int(twoNumber[0])
    rank = int(twoNumber[1])
    if faculty in maxRankOfFaculties:
        if rank > maxRankOfFaculties[faculty]:
            maxRankOfFaculties[faculty] = rank
    else:
        maxRankOfFaculties[faculty] = rank
print maxRankOfFaculties
    
for line in lines:
    features = {'stuId':-1, 'rankPercent':0, 'absoluteRank':0}
    #for i in range(1,20):
    #    features['faculty' + str(i)] = 0
    records = line.split('$')
    features['stuId'] = int(records[0])
    twoNumber = records[1].split(',')
    facultyNum = int(twoNumber[0])
    #features['faculty' + str(facultyNum)] = 1
    features['rankPercent'] = int(twoNumber[1])/float(maxRankOfFaculties[facultyNum])
    features['absoluteRank'] = int(twoNumber[1])
    students += json.dumps(features, sort_keys=True) + '\n'

with open(sys.argv[1] + 'Processed/ScoreProcessed.txt', 'w') as fw:
    fw.write(students)
