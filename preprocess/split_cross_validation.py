#!/usr/bin/python
# -*- coding: UTF-8 -*-
import random

feature_file = "../original_data/idexamples_train.txt"
subsidy_file = "../original_data/subsidy_train.txt"

cv_w_list = []
for i in range(5):
    cv_w_list.append(open("../original_data/cv_fold_" + str(i) + ".txt", 'w'))

subsidy_dict = {}
lines = open(subsidy_file).readlines()
for line in lines:
    temps = line.strip("\n").strip("\r").split(",")
    id = temps[0].strip("\"")
    subsidy = temps[1].strip("\"")
    subsidy_dict[id] = subsidy

# random assign to cross validation set and add target varible
random.seed(2017)

lines = open(feature_file).readlines()
for line in lines:
    id = line.split(",")[0].split(":")[1]
    cv_num = random.randint(0, 4)
    line_added = "获奖情况:" + subsidy_dict[id] + "," + line
    cv_w_list[cv_num].write(line_added)

for i in range(5):
    cv_w_list[i].close()
