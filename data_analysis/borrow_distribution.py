#!/usr/bin/python
# -*- coding: UTF-8 -*-
import  re
root_loc = "/Users/mac/Documents/contest/data/original_data/"
subsidy_file = "subsidy_train.txt"
borrow_file = "borrow_train.txt"

if_subset = True
borrow_dict = {}
subsidy_dict = {}

lines = open(root_loc + subsidy_file).readlines()
for line in lines:
    temps = line.strip("\n").split(",")
    id = int(temps[0])
    subsidy = int(temps[1])
    subsidy_dict[id] = subsidy

lines = open(root_loc + borrow_file).readlines()

total_book_count=set()
total_book_count_s=set()

total_book_type_count=set()
total_book_type_count_s=set()

has_isbn_count=0

for line in lines:
    temps = line.strip("\n").split(",")
    id = int(temps[0])
    book = temps[2]
    ISBN=temps[3]

    #bookname
    if re.search('数学|线性代数', book):
        total_book_count.add(id)
        if subsidy_dict[id]!=0:
            total_book_count_s.add(id)


    if len(line.strip("\n").split("\""))>=6 and  line.strip("\n").split("\"")[5][0]=='J':
        has_isbn_count+=1
        total_book_type_count.add(id)
        if subsidy_dict[id]!=0:
            total_book_type_count_s.add(id)

    if not borrow_dict.has_key(id):
        borrow_dict[id] = 1
    else:
        borrow_dict[id] += 1
    if not subsidy_dict.has_key(id):
        if_subset = False


print("user number: " + str(len(borrow_dict)))
print("if subset: " + str(if_subset))

borrow_dict_list = sorted(borrow_dict.iteritems(), key=lambda d: d[1], reverse=True)

for i in range(100):
    print (str(i) + ": " + str(subsidy_dict[borrow_dict_list[i][0]]))

print ("\n\n\n")

for i in range(len(borrow_dict) - 100, len(borrow_dict)):
    print (str(i) + ": " + str(subsidy_dict[borrow_dict_list[i][0]]))

borrow_count = 0
not_borrow_count = 0
for id, subsidy in subsidy_dict.items():
    if subsidy != 0:
        if borrow_dict.has_key(id):
            borrow_count += 1
        else:
            not_borrow_count += 1
print "borrow_count" + str(borrow_count)
print "not_borrow_count" + str(not_borrow_count)


print "totol book: "+str(len(total_book_count))
print "totol book_s: "+str(len(total_book_count_s))
print "percentage: "+str(float(len(total_book_count_s))/len(total_book_count))

print "totol book: "+str(len(total_book_type_count))
print "totol book_s: "+str(len(total_book_type_count_s))
print "percentage: "+str(float(len(total_book_type_count_s))/len(total_book_type_count))
print "isbn num"+str(has_isbn_count)