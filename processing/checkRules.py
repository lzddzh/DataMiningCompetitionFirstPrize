import sys
import json
predict = open(sys.argv[1])
features = open(sys.argv[2] + 'Processed/Card3Processed.txt')

targetFea = {}
students = features.readlines()
for each in students:
    featureDict = json.loads(each)
    targetFea[featureDict['stuId']] = featureDict['if_change_card']

count = 0
countAll = 0
countNotIn = 0
lines = predict.readlines()
for line in lines[1:]:
    itmes = line.strip().split(',')
    stuId = itmes[0]
    label = itmes[1]
    if int(stuId) not in targetFea:
        countNotIn += 1
        continue
    if label != '0':
        print stuId, targetFea[int(stuId)]
    if targetFea[int(stuId)] == 1:
        countAll += 1
    if label != '0' and targetFea[int(stuId)] == 1:
        count += 1

print "among " + str(len(lines)) + " students, " + str(count) + " get reward and ..."
print "among " + str(len(lines)) + " students, totally " + str(countAll) + "..."
print str(countNotIn) + " students get reword but not in this form."
