import readFromFile
import sys
import json

def getCollumNames():
    lines = readFromFile.readLines('trainProcessed/collumInfo.txt')
    feaNames = []
    for line in lines:
        feaNames.append(line.split('    ')[-1])
    return feaNames

def getCollum(feaName):
    lines = readFromFile.readLines('trainProcessed/idexamples_train.txt')
    feaValues = []
    feaDict = {}
    for line in lines:
        line = line.replace(',', ',\"')
        line = line.replace(':', '\":')
        feaDict = json.loads('{\"'+line+'}')
        feaValues.append(feaDict[feaName])
    return feaValues

def checkFea(values):
    print values
    valueDic = {}
    for each in values:
        each = str(each)
        if each in valueDic:
            valueDic[each] += 1
        else:
            valueDic[each] = 1
    print "Distinct Values and Their Apperance Times:"
    print valueDic

if __name__=='__main__':
    feaName = getCollumNames()[int(sys.argv[1])] 
    feaValues = getCollum(feaName)
    checkFea(feaValues)
