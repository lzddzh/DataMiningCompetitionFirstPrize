#!/usr/bin/python
# -*- coding: UTF-8 -*-
root_loc = "/Users/mac/Documents/contest/data/original_data/"
card_file = "card_train.txt"

lines = open(root_loc + card_file).readlines()

type_dict = {}
cate_dict = {}

for line in lines:
    temps = line.strip("\n").split(",")
    id = int(temps[0])
    cate = temps[1]
    type = temps[3]

    if cate_dict.has_key(cate):
        cate_dict[cate] += 1
    else:
        cate_dict[cate] = 0

    if cate=="\"POS消费\"":
        if type_dict.has_key(type):
            type_dict[type] += 1
        else:
            type_dict[type] = 1



for name,count in cate_dict.items():
    print name+" "+str(count)

print "\n\n"

for name,count in type_dict.items():
    print name+" "+str(count)