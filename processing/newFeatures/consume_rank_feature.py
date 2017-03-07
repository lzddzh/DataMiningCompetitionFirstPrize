# !/usr/bin/python
# -*- coding: UTF-8 -*-
import time
import datetime
import numpy as np


def extract_consume_per_person(file_name, consume_dict):
    lines = open(file_name).readlines()
    for line in lines:
        temps = line.strip("\r\n").split("$")
        id = temps[0]
        totol_amount = 0
        active_date_set = set()

        for i in range(1, len(temps)):
            records = temps[i].split(",")
            cate = records[0].strip("\"")
            amount = float(records[4].strip("\""))
            time = records[3].strip("\"")
            date = time.split(" ")[0]
            active_date_set.add(date)
            if cate == "POS消费":
                totol_amount += amount
        consume_dict[id] = float(totol_amount) / len(active_date_set)


def read_faculty_dict(file_name, faculty_dict):
    r = open(file_name)
    lines = r.readlines()
    for line in lines:
        temps = line.strip("\n").split(",")
        id = temps[0]
        faculty = temps[1]
        if not faculty_dict.has_key(faculty):
            faculty_dict[faculty] = []
        faculty_dict[faculty].append(id)
    r.close()


def extract_rank_feature(file_name, final_rank, score_dict, if_train):
    if if_train:
        w = open("../original_data/rank_feature_train.txt", 'w')
    else:
        w = open("../original_data/rank_feature_test.txt", 'w')

    lines = open(file_name).readlines()
    for line in lines:
        if if_train:
            id = line.strip().split(",")[0]
        else:
            id = line.strip()
            print id
        w.write("{")
        w.write('"stuId": ' + id + ", ")

        if score_dict.has_key(id) and final_rank.has_key(id):
            w.write('"rank_in_faculty":' + str(final_rank[id]) + "," + '"rank_score_consume":' + str(
                final_rank[id] * score_dict[id]) + "} \n")
        else:
            w.write(
                '"rank_in_faculty":' + str(final_rank.get(id, -999)) + "," + '"rank_score_consume":' + str(
                    -999) + "} \n")

    w.close()


def read_score_dict(file_name, score_dict):
    lines = open(file_name).readlines()
    for line in lines:
        temps = line.strip("\n").split(",")
        id = temps[0]
        rank = float(temps[1])
        score_dict[id] = rank


final_rank = {}
faculty_dict = {}
score_dict = {}

read_score_dict("../original_data/forYance.txt", score_dict)

read_faculty_dict("../original_data/raw_data/test/score_final_test.txt", faculty_dict)
read_faculty_dict("../original_data/raw_data/train/score_train.txt", faculty_dict)
read_faculty_dict("../original_data/raw_data/old_test/score_test.txt", faculty_dict)
print faculty_dict

consume_dict = {}
extract_consume_per_person("../studentForm/test/card_final_test_inverted_cleaned.txt", consume_dict)
extract_consume_per_person("../studentForm/train/card_train_inverted_cleaned.txt", consume_dict)
extract_consume_per_person("../studentForm/test_old/card_test_inverted_cleaned.txt", consume_dict)
print consume_dict

for faculty_id in range(1, 20):
    faculty = str(faculty_id)
    student_list = faculty_dict[faculty]
    temp_dict = {}
    for id in student_list:
        if consume_dict.has_key(id):
            temp_dict[id] = consume_dict[id]
    temp_dict_list = sorted(temp_dict.iteritems(), key=lambda d: d[1], reverse=False)
    for i in range(len(temp_dict_list)):
        print str(temp_dict_list[i][0]) + "   " + str(temp_dict_list[i][1])
        final_rank[temp_dict_list[i][0]] = float(i + 1) / len(temp_dict_list)
extract_rank_feature("../original_data/raw_data/test/subsidy_final_test.txt", final_rank,
                     score_dict, False)
extract_rank_feature("../original_data/raw_data/train/subsidy_train.txt", final_rank,
                     score_dict, True)
