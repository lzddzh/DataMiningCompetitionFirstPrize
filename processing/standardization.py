import readFromFile
import sys
import numpy as np
from sklearn import preprocessing

def loadToArray(filePath):
    lines = readFromFile.readLines(filePath)
    X_stuId = []
    X = []
    for line in lines:
        stuId = int(line.split(',', 1)[0])
        X_stuId.append(stuId)
        values = [ float(v.split(':')[1]) for v in line.split(',')[1:] ]
        X.append(values)
    X_np = np.array(X)
    feaNames = [ v.split(':')[0] for v in lines[0].split(',')[1:] ]
    return X_np, feaNames, X_stuId

def writeToFile(filePath, feaNames, X, stuId):
    fw = open(filePath, 'w')
    for i in range(len(stuId)):
        out = ""
        out += str(stuId[i])
        for j in range(X.shape[1]):
            out += ', ' + feaNames[j] + ':' + str(X[i][j]) 
        out += '\n'
        fw.write(out)

if __name__=='__main__':
    if sys.argv[2] == 'std':
        X, feaNames1, stuId1 = loadToArray('trainProcessed/examples_train.txt')
        scaler = preprocessing.StandardScaler().fit(X)
        #X = scaler.transform(X)
        if sys.argv[1] == 'test':
            X_test, feaNames2, stuId2 = loadToArray('testProcessed/examples_test.txt')
            print np.vstack((X, X_test)).shape
            scaler = preprocessing.StandardScaler().fit(np.vstack((X, X_test)))
            X = scaler.transform(X)
            X_test = scaler.transform(X_test)
            writeToFile('testProcessed/examples_test_std.txt', feaNames2, X_test, stuId2)
        writeToFile('trainProcessed/examples_train_std.txt', feaNames1, X, stuId1)
    else:
        X, feaNames1, stuId1 = loadToArray('trainProcessed/examples_train.txt')
        scaler = preprocessing.MinMaxScaler()
        #X = scaler.fit_transform(X)
        if sys.argv[1] == 'test':
            X_test, feaNames2, stuId2 = loadToArray('testProcessed/examples_test.txt')
            X_test = scaler.fit_transform(X_test)
            writeToFile('testProcessed/examples_test_minmax.txt', feaNames2, X_test, stuId2)
        writeToFile('trainProcessed/examples_train_minmax.txt', feaNames1, X, stuId1)

