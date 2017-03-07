#!/usr/bin/python
# -*- coding: UTF-8 -*-
import random
import sys
sys.path.append('../')
from commons import variables

feature_file = "../original_data/idexamples_train_std.txt"
subsidy_file = "../original_data/subsidy_train.txt"

cv_w_list = []
for i in range(variables.cv_num):
    cv_w_list.append(open("../original_data/cv_fold_" + str(i) + ".txt", 'w'))

subsidy_dict = {}
lines = open(subsidy_file).readlines()
for line in lines:
    temps = line.strip("\n").strip("\r").split(",")
    id = temps[0].strip("\"")
    subsidy = temps[1].strip("\"")
    subsidy_dict[id] = subsidy

# random assign to cross validation set and add target varible
#random.seed(2348923)
random.seed(2017)

labels = ['0', '1000', '1500', '2000']

maxNum = {'0': 9325/variables.cv_num+1, '1500': 465/variables.cv_num+1, '2000': 354/variables.cv_num+1, '1000': 741/variables.cv_num+1}
count = [{'0':0, '1500':0, '2000':0, '1000':0},
        {'0':0, '1500':0, '2000':0, '1000':0},
        {'0':0, '1500':0, '2000':0, '1000':0},
        {'0':0, '1500':0, '2000':0, '1000':0},
        {'0':0, '1500':0, '2000':0, '1000':0}, 
        {'0':0, '1500':0, '2000':0, '1000':0},
        {'0':0, '1500':0, '2000':0, '1000':0},
        {'0':0, '1500':0, '2000':0, '1000':0},
        {'0':0, '1500':0, '2000':0, '1000':0},
        {'0':0, '1500':0, '2000':0, '1000':0}]

# this function returns a random number bewteen [0, 3], and promise #0 = 
def equalRandom(label):
    ran = random.randint(0, variables.cv_num - 1)
    if count[ran][label] + 1 <= maxNum[label]:
        count[ran][label] += 1
        return ran
    else:
        while count[ran][label] + 1 > maxNum[label]:
            ran = (ran + 1) % variables.cv_num 
        count[ran][label] += 1   
        return ran

def randomPush(labelIndex): #labelIndex == 0, 1, 2, 3
    lines = open(feature_file).readlines()
    for line in lines:
        id = line.split(",")[0].split(":")[1]
        if subsidy_dict[id] != labels[labelIndex]:
            continue
        cv_num = equalRandom(subsidy_dict[id])
        line_added = "获奖情况:" + subsidy_dict[id] + "," + line
        cv_w_list[cv_num].write(line_added)

for i in range(4):
    for dic in count:
        for key in dic:
            dic[key] = 0
    randomPush(i)
    print count

for i in range(variables.cv_num):
    cv_w_list[i].close()
