# coding=utf-8
import json
import string
import readFromFile
import sys

students = ""
TOEFL = ['TOEFL', 'toefl', 'IELTS', 'ielts', '托福', '雅思']
Kaoyan = ['考研']
Programming = ['c++', 'java', 'JAVA', '编程', 'C++', 'PHP', 'php', 'html', 'HTML', 'web', 'Web', 'WEB', "代码", '算法']

if sys.argv[1] == 'train':
    lines = readFromFile.readLines('../studentForm/train/borrow_train_invert.txt')
elif sys.argv[1] == 'test':
    lines = readFromFile.readLines('../studentForm/test/borrow_test_invert.txt')
else:
    print 'Invalid arguments'

for line in lines:
    features = {"stuId":-1, "ifBorrowed":0, "numOfBorrowed":0, 
            "timesOfTOEFL":0, "timesOfKaoyan":0, "timesOfProg":0, "numOfCateBorrowed":0}
    # Add category A-Z number counters to dic features
    for i in list(string.ascii_uppercase):
        if i == 'T' and i != 'L' and i != 'M' and i != 'W' and i != 'Y':
            features["numInCate" + i] = 0
    books = line.split('$')
    features['stuId'] = int(books[0])
    if len(books) > 1:
        features['ifBorrowed'] =  1 
        features['numOfBorrowed'] = len(books) - 1
        for i in range(1, len(books)):
            # filter out the "..." signs in the string.
            items = books[i].strip().split('\",\"')
            if len(items) < 3:
                continue
            print items
            time     = items[0][1:]
            bookName = items[1]
            bookISBN = items[2][:-1]
            # Count category A-Z borrowed times. 
            if bookISBN[0] == 'T' and bookISBN[0] in string.ascii_uppercase:
                features["numInCate" + bookISBN[0]] += 1
            # Count times of toefl books, KaoYan books and Programming books.
            for each in TOEFL:
                if each in bookName:
                    features['timesOfTOEFL'] += 1
                    break
            for each in Kaoyan:
                if each in bookName:
                    features['timesOfKaoyan'] += 1
                    break
            for each in Programming:
                if each in bookName:
                    features['timesOfProg'] += 1
                    break
            
        # Count the number of distinct categories this person has borrowed.
        for i in list(string.ascii_uppercase):
            if i == 'T' and i != 'L' and i != 'M' and i != 'W' and i != 'Y':
                features['numOfCateBorrowed'] += 0 if features['numInCate' + i] == 0 else 1 
        
    #students.append(json.dumps(features, sort_keys=True))
    students += json.dumps(features, sort_keys=True) + '\n'
        
with open(sys.argv[1] + 'Processed/BorrowProcessed.txt', 'w') as fw:
    fw.write(students)
