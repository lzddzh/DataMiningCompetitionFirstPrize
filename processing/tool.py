# encoding=utf-8
import readFromFile
import sys
import json
import numpy as np
from scipy import stats

originalFile = 'examples.txt'


def distinctIds():
    files = []
    files.append(readFromFile.readLines('../data/train/borrow_train.txt'))
    files.append(readFromFile.readLines('../data/train/card_train.txt'))
    files.append(readFromFile.readLines('../data/train/dorm_train.txt'))
    files.append(readFromFile.readLines('../data/train/library_train.txt'))
    files.append(readFromFile.readLines('../data/train/score_train.txt'))
    files.append(readFromFile.readLines('../data/train/subsidy_train.txt'))

    ids = []
    for each in files:
        for line in each:
            items = line.split(',')
            if items[0] != '\n' and items[0] != "":
                ids.append(int(items[0]))

    distinctIds = list(set(ids))
    distinctIds.sort()
    
    print "Get " + str(len(distinctIds)) + "distinct ids in total."
    print "The first 10 of them is: ", distinctIds[:10]
    print "The last 10 of them is: ", distinctIds[-10:]
    return distinctIds

def appendCollum(filePath, collum, collumName):
    fr = open(filePath)
    content = fr.read()
    fr.close()
    
    lines = content.strip().split('\n')
    print lines[:10]
    print lines[-10:]
    if len(lines) != (len(collum) + 1):
        print "Different rows when append a collum named " + collumName + " to file."
        print "One is " + str(len(lines)) + " while another is " + str(len(collum)+1)
        return

    s = ""
    for index, each in enumerate(lines):
        if index == 0:
            s += each + "," + collumName + '\n'
        else:
            s += each + ", " + str(collum[index - 1]) + '\n'
    fw = open(filePath, 'w')
    fw.write(s)
    fw.close()

def initFile(filePath):
    # Test the input file are there
    f1 = readFromFile.read('../data/train/borrow_train.txt')
    f2 = readFromFile.read('../data/train/card_train.txt')
    f3 = readFromFile.read('../data/train/dorm_train.txt')
    f4 = readFromFile.read('../data/train/library_train.txt')
    f5 = readFromFile.read('../data/train/score_train.txt')
    f6 = readFromFile.read('../data/train/subsidy_train.txt')
    
    print "Find 6 files with each file start content shown as below:\n"
    print f1[:100] + '\n'
    print f2[:100] + '\n'
    print f3[:100] + '\n'
    print f4[:100] + '\n'
    print f5[:100] + '\n'
    print f6[:100] + '\n'

    fw = open(filePath, 'w')
    out = "id"
    for each in distinctIds():
        out += '\n' + str(each)
    fw.write(out)

def getIdList(filePath):
    fr = open(filePath)
    content = fr.read()
    lines = content.strip().split('\n')
    ret = []
    for each in lines[1:]:
        ret.append(each.split(',')[0])
    return ret


def addLabel(students):
    lines = readFromFile.readLines(originalFile)
    out = lines[0] + ',label\n'
    i = 0
    j = 1 
    while i < len(students) and j < len(lines):
        stuId = int(lines[j].split(',')[0])
        if int(students[i]['stuId']) == stuId:
            out += lines[j] + ',' + students[i]['subsidy'] + '\n'   
            i += 1
            j += 1
        elif int(students[i]['stuId']) < stuId:
            i += 1
        else:
            out += lines[j] + ',' + 'null' + '\n'
            j += 1
    while j < len(lines):
        out += lines[j] + ',null\n'
        j += 1
    with open(originalFile, 'w') as fw:
        fw.write(out)
    
def addFeatures(students, fileName, normalization = True):
    lines = readFromFile.readLines(originalFile)
    # Calculate the exists collum number
    existsColNum = len(lines[0].split(',')) - 1
    # Give order to dictionary keys so we can visite them in the same order
    sortedFeaNames = [ key for key, val in sorted(students[0].items()) ]
    sortedFeaNames.remove('stuId')
    print sortedFeaNames
    with open(sys.argv[4] + 'Processed/collumInfo.txt', 'a') as fw:
        out2 = ""
        for i in range(0, len(sortedFeaNames)):
            out2 += 'fea' + str(i + existsColNum) + '    ' + fileName + '    ' + sortedFeaNames[i] + '\n'
        fw.write(out2)

    # Dealing with the missing features value for some students that have no records.
    # Here we will use one of: 1.0 2.Mean 3.Median 4. MostFrequent 5.Min 6.Max
    Minus = {}
    Zero = {}
    Mean = {}
    Median = {}
    MostFre = {}
    Min = {}
    Max = {}
    for key in sortedFeaNames:
        oneCollum = [ x[key] for x in students ]
        Minus[key] = -1
        Zero[key] = 0
        Mean[key] = np.mean(oneCollum)
        Median[key] = np.median(oneCollum)
        MostFre[key] = stats.mode(oneCollum)[0][0]
        Min[key] = min(oneCollum)
        Max[key] = max(oneCollum)

    ''' For Debug Only
    print Mean
    print Median
    print MostFre
    print Min
    print Max
    sys.exit(0)
    '''
    staDict = {'-1':Minus, '0':Zero, 'mean':Mean, 'median':Median, 'mostFre':MostFre, 'min':Min, 'max':Max}
    FeaturesFill = {'BorrowProcessed.txt-ifBorrowed':'0',
            'BorrowProcessed.txt-numInCate':'0',
            'BorrowProcessed.txt-numOfBorrowed':'0',
            'BorrowProcessed.txt-numOfCateBorrowed': '0',
            'BorrowProcessed.txt-ratioOfBorrowedMonths': '0',
            'BorrowProcessed.txt-timesOfKaoyan': '0',
            'BorrowProcessed.txt-timesOfProg': '0',
            'BorrowProcessed.txt-timesOfTOEFL': '0',
            'DormProcessed.txt-enterExit': 'mean',
            'DormProcessed.txt-maxMonthDensity': 'mean', 
            'DormProcessed.txt-timesPerDay': 'mean',
            'DormProcessed.txt-totalDays': 'mean',
            'DormProcessed.txt-weekendTimes': 'mean',
            'LibraryProcessed.txt-eveningTimes': 'mean',
            'LibraryProcessed.txt-timesPerDay': 'mean',
            'LibraryProcessed.txt-totalDays': 'mean',
            'LibraryProcessed.txt-totalRecordTimes': 'mean',
            'LibraryProcessed.txt-weekendTimes': 'mean',
            'ScoreProcessed.txt-faculty': '0',
            'ScoreProcessed.txt-rankPercent': '-1'
            }
    if fileName == 'CardProcessed.txt':
        for key in sortedFeaNames:
            FeaturesFill['CardProcessed.txt-' + key] = '0'

    if fileName == 'LibraryProcessed.txt':
        for key in sortedFeaNames:
            FeaturesFill['LibraryProcessed.txt-' + key] = '0'

    if fileName == 'ScoreProcessed.txt':
        for key in sortedFeaNames:
            FeaturesFill['ScoreProcessed.txt-' + key] = '0'
        FeaturesFill['ScoreProcessed.txt-rankPercent'] = '-1'

    if fileName == 'DormProcessed.txt':
        for key in sortedFeaNames:
            FeaturesFill['DormProcessed.txt-' + key] = '0'
    
    if fileName == 'BorrowProcessed.txt':
        for key in sortedFeaNames:
            FeaturesFill['BorrowProcessed.txt-' + key] = '0'
    # Begin join two forms (two form rows are sorted by their 'stuId')
    i = 0
    j = 0 
    fw = open(originalFile, 'w')
    while i < len(students) and j < len(lines):
        print lines[j]
        stuId = int(lines[j].split(',')[0])
        print i, stuId
        temp = ""
        if int(students[i]['stuId']) == stuId:
            temp += lines[j]
            for key in sortedFeaNames:
                if normalization == False or key == 'ifBorrowed' or key[:-1] == 'faculty':
                    temp += ',' + key + ':' + str(students[i][key])
                else:
                    temp += ',' + key + ':' + str((students[i][key] - Mean[key]) / float(Max[key] - Min[key]))
            temp += '\n'
            i += 1
            j += 1
        elif int(students[i]['stuId']) < stuId:
            i += 1
        else:
            temp += lines[j]
            for key in sortedFeaNames:
                if key[:-1] == 'numInCate':
                    if normalization:
                        temp += ',' + key + ':' + str((staDict[FeaturesFill[filePath + '-numInCate']][key] - Mean[key]) / float(Max[key] - Min[key]))
                    else:
                        temp += ',' + key + ':' + str(staDict[FeaturesFill[filePath + '-numInCate']][key])
                elif key[5:] == 'enter' or key[5:] == 'exit':
                    if normalization:
                        temp += ',' + key + ':' + str((staDict[FeaturesFill[filePath + '-enterExit']][key] - Mean[key]) / float(Max[key] - Min[key]))
                    else:
                        temp += ',' + key + ':' + str(staDict[FeaturesFill[filePath + '-enterExit']][key])
                else:
                    if normalization == False or key == 'ifBorrowed' or key[:-1] == 'faculty':
                        temp += ',' + key + ':' + str(staDict[FeaturesFill[filePath + '-' + key]][key])
                    else:
                        temp += ',' + key + ':' + str((staDict[FeaturesFill[filePath + '-' + key]][key] - Mean[key]) / float(Max[key] - Min[key]))
            temp += '\n'
            j += 1
        fw.write(temp)
    while j < len(lines):
        print lines[j]
        temp = lines[j]
        for key in sortedFeaNames:
            if key[:-1] == 'numInCate':
                temp += ',' + key + ':' + str(staDict[FeaturesFill[filePath + '-numInCate']][key])
            elif key[5:] == 'enter' or key[5:] == 'exit':
                temp += ',' + key + ':' + str(staDict[FeaturesFill[filePath + '-enterExit']][key])
            else:
                if normalization:
                    temp += ',' + key + ':' + str((staDict[FeaturesFill[filePath + '-' + key]][key] - Mean[key]) / float(Max[key] - Min[key]))
                else:
                    temp += ',' + key + ':' + str(staDict[FeaturesFill[filePath + '-' + key]][key])
        temp += '\n'
        j += 1
        fw.write(temp)
    
def readFeaturesFromFile(filePath):
    lines = readFromFile.readLines(filePath)
    students = [ json.loads(line) for line in lines ]
    sortedStudents = sorted(students, key = lambda k: int(k['stuId']))
    return sortedStudents

def printUsage():
    print "Usage:\n 1. python tool.py init *notused\n      Create a 'example.txt' with id and label at current fold\n 2. python tool.py add [fileName] normalization=true train\n      Add the features from [fileName] to 'example.txt', and generate a collum info into 'collumInfo.txt'."

if __name__=='__main__':
    if len(sys.argv) < 2 or sys.argv[1] == 'help':
        printUsage()
    elif sys.argv[1] == 'init':
    # This situation will not happen now.
        initFile(originalFile)
        #students = readFeaturesFromFile('SubsidyProcessed.txt')
        #addLabel(students)
    elif sys.argv[1] == 'add':
        if sys.argv[4] == 'train':
            originalFile = 'trainProcessed/examples_train.txt'
        elif sys.argv[4] == 'test':
            originalFile = 'testProcessed/examples_test.txt'
        else:
            print 'Invalid arguments'
        filePath = sys.argv[2]
        students = readFeaturesFromFile(sys.argv[4] + 'Processed/' + filePath)
        addFeatures(students, filePath.split('/')[-1], True if sys.argv[3].split('=')[-1] == 'true' else False)
    else:
        printUsage()
