# !/usr/bin/python
# -*- coding: UTF-8 -*-
import time
import datetime
import numpy as np
import sys
import os.path
root_loc = ""
feature_loc = ""
if os.path.isfile('trainProcessed/card_test_inverted_cleaned.txt') == False:
    if sys.argv[1] == 'train':
        root_loc = "../studentForm/train/card_train_invert.txt"
        output_loc = "trainProcessed/card_train_inverted_cleaned.txt"
    elif sys.argv[1] == 'test':
        root_loc = "../studentForm/test/card_test_invert.txt"
        output_loc = "testProcessed/card_test_inverted_cleaned.txt"
    else:
        print "Invalid arguments"
    w = open(output_loc, "w")
    
    lines = open(root_loc).readlines()
    count = 0
    for line in lines:
        if count % 1000 == 0:
            print count
        count += 1
        temps = line.strip("\n").split('$');
        output_line = temps[0] + "$"
        record_list = []
        for i in range(1, len(temps)):
            if temps[i] not in record_list:
                record_list.append(temps[i])
                output_line += temps[i] + "$"
        output_line = output_line[0:-1]
        w.write(output_line + "\n")
    w.close()

def get_statistic_info(record_l):
    if len(record_l) != 0:
        record_np = np.asarray(record_l)
        count_v = len(record_np)
        sum_v = record_np.sum()
        max_v = record_np.max()
        min_v = record_np.min()
        mean_v = record_np.mean()
        median_v = np.median(record_np)
        return count_v, sum_v, max_v, min_v, mean_v, median_v
    else:
        return 0, 0, 0, 0, 0, 0


def type_mapping(chinese):
    if chinese == "图书馆":
        return "labrary_"
    elif chinese == "":
        return "empty_"
    elif chinese == "校医院":
        return "hospital_"
    elif chinese == "超市":
        return "market_"
    elif chinese == "开水":
        return "water_"
    elif chinese == "食堂":
        return "canteen_"
    elif chinese == "洗衣房":
        return "landry_"
    elif chinese == "其他":
        return "other_"
    elif chinese == "教务处":
        return "academic_office_"
    elif chinese == "文印中心":
        return "printing_"
    elif chinese == "校车":
        return "bus_"
    else:
        return "shower_"


def get_max_value_from_dict(any_dict):
    if len(any_dict) == 0:
        return 0

    any_dict_list = sorted(any_dict.iteritems(), key=lambda d: d[1], reverse=True)
    return any_dict_list[0][1]


def get_consume_type_feature(consume_amount_year_dict, consume_count_year_dict, day_num):
    output_line = ""
    type_list = ["图书馆", "", "校医院", "超市", "开水", "食堂", "洗衣房", "其他", "教务处", "文印中心", "校车", "淋浴"]

    all_type_amount = 0.0
    all_type_count = 0.0

    for type in type_list:
        if consume_amount_year_dict.has_key(type):
            all_type_amount += consume_amount_year_dict[type]
            all_type_count += consume_count_year_dict[type]
            output_line += '"' + type_mapping(type) + 'amount": ' + str(consume_amount_year_dict[type] / day_num) + ", "
            output_line += '"' + type_mapping(type) + 'count": ' + str(consume_count_year_dict[type] / day_num) + ", "
        else:
            output_line += '"' + type_mapping(type) + 'amount": ' + "0, "
            output_line += '"' + type_mapping(type) + 'count": ' + "0, "

    output_line += '"total_consume_amount": ' + str(all_type_amount / day_num) + ", "
    output_line += '"total_consume_count": ' + str(all_type_count / day_num) + ", "

    for type in type_list:
        if consume_amount_year_dict.has_key(type):
            output_line += '"' + type_mapping(type) + 'percentage": ' + str(
                consume_amount_year_dict[type] / all_type_amount) + ", "
        else:
            output_line += '"' + type_mapping(type) + 'percentage": ' + "0, "

    return output_line


if sys.argv[1] == 'train':
    root_loc = "trainProcessed/card_train_inverted_cleaned.txt"
    feature_loc = "trainProcessed/CardProcessed.txt"
elif sys.argv[1] == 'test':
    root_loc = "testProcessed/card_test_inverted_cleaned.txt"
    feature_loc = "testProcessed/CardProcessed.txt"
else:
    print "Invalid arguments"

w = open(feature_loc, 'w')

lines = open(root_loc).readlines()

# for every person
for line in lines:
    output_line = "{"
    temps = line.strip("\n").split("$")
    output_line += '"stuId": ' + temps[0] + ", "
    print temps[0]

    # 不同类型消费总额
    sum_consume_dict = {"labrary_": 0, "hospital_": 0, "market_": 0, "water_": 0, "canteen_": 0, "landry_": 0,
                        "other_": 0, "academic_office_": 0, "printing_": 0,
                        "bus_": 0, "shower_": 0, "empty_": 0, "all": 0}

    # 不同消费的消费纪录
    consume_dict = {"labrary_": [], "hospital_": [], "market_": [], "water_": [], "canteen_": [], "landry_": [],
                    "other_": [], "academic_office_": [], "printing_": [],
                    "bus_": [], "shower_": [], "empty_": [], "all": []}
    # 余额列表
    balance_list = []
    # 分时消费
    hour_consume_dict = {}
    for i in range(24):
        if i < 10:
            hour_consume_dict["0" + str(i)] = []
        else:
            hour_consume_dict[str(i)] = []

    # 周末和非周末消费
    week_list = []
    non_week_list = []

    # 暑假消费
    vacation_list = []

    # 前10大食堂消费
    canteen_dict = {"232": [], "118": [], "83": [], "203": [], "1155": [], "247": [], "272": [], "217": [], "526": [],
                    "72": []}
    # 前十大地点消费金额和次数
    place_amount_dict = {}
    place_count_dict = {}

    # 用户一日最高消费额度
    day_consume_total_dict = {}

    days_set = set()
    top_up_year = 0.0
    max_top_up_amount_once = 0.0

    # every record for one person
    for i in range(1, len(temps)):
        records = temps[i].split(",")
        cate = records[0].strip("\"")
        location = unicode(records[1].strip("\""), "utf-8")[2:]
        type = type_mapping(records[2].strip("\""))
        time = records[3].strip("\"")
        date = time.split(" ")[0]
        month = date.split("/")[0] + "/" + date.split("/")[1]
        month_day = date.split("/")[1] + "/" + date.split("/")[2]
        hour = time.split(" ")[1].split(":")[0]
        amount = float(records[4].strip("\""))
        balance = float(records[5].strip("\""))
        weekends = datetime.datetime(int(date.split("/")[0]), int(date.split("/")[1]),
                                     int(date.split("/")[2])).strftime("%w")

        days_set.add(time.split(" ")[0])

        balance_list.append(balance)

        if cate == "POS消费":

            sum_consume_dict[type] += amount
            sum_consume_dict["all"] += amount

            if not day_consume_total_dict.has_key(date):
                day_consume_total_dict[date] = 0.0
            day_consume_total_dict[date] += amount

            if amount >= 0:

                consume_dict["all"].append(amount)
                consume_dict[type].append(amount)

                hour_consume_dict[hour].append(amount)

                if weekends == "0" or weekends == "6":
                    week_list.append(amount)
                else:
                    non_week_list.append(amount)

                if "07/01" <= month_day <= "08/31":
                    vacation_list.append(amount)

                if canteen_dict.has_key(location):
                    canteen_dict[location].append(amount)

                if not place_amount_dict.has_key(location):
                    place_amount_dict[location] = amount
                    place_count_dict[location] = 1
                else:
                    place_amount_dict[location] += amount
                    place_count_dict[location] += 1

        if cate == "圈存转账" or cate == "支付领取" or cate == "卡充值":
            top_up_year += amount
            if amount > max_top_up_amount_once:
                max_top_up_amount_once = amount

    # 拼接不同消费类型总额及占比
    total_amount = sum_consume_dict["all"]
    for key, value in sum_consume_dict.items():
        output_line += '"' + key + '_sum": ' + str(value) + ", "
        output_line += '"' + key + '_sum_relative": ' + str(float(value) / len(days_set)) + ", "
        if total_amount != 0:
            output_line += '"' + key + '_percentage": ' + str(float(value) / total_amount) + ", "
        else:
            output_line += '"' + key + '_percentage": ' + "0" + ", "

    # 拼接不同种类的消费的各种统计值
    for key, record_list in consume_dict.items():
        (count_value, sum_value, max_value, min_value, mean_value, median_value) = get_statistic_info(record_list)
        output_line += '"' + key + '_count": ' + str(count_value) + ", "
        output_line += '"' + key + '_count_relative": ' + str(float(count_value) / len(days_set)) + ", "
        output_line += '"' + key + '_max": ' + str(max_value) + ", "
        output_line += '"' + key + '_min": ' + str(min_value) + ", "
        output_line += '"' + key + '_mean": ' + str(mean_value) + ", "
        output_line += '"' + key + '_median": ' + str(median_value) + ", "
    # 余额特征
    (count_value, sum_value, max_value, min_value, mean_value, median_value) = get_statistic_info(balance_list)
    key = "balance"
    output_line += '"' + key + '_max": ' + str(max_value) + ", "
    output_line += '"' + key + '_min": ' + str(min_value) + ", "
    output_line += '"' + key + '_mean": ' + str(mean_value) + ", "
    output_line += '"' + key + '_median": ' + str(median_value) + ", "

    # 分时特征
    for i in range(24):
        if i < 10:
            key = "0" + str(i)
        else:
            key = str(i)
        record_list = hour_consume_dict[key]
        (count_value, sum_value, max_value, min_value, mean_value, median_value) = get_statistic_info(record_list)
        output_line += '"hour_' + key + '_sum": ' + str(sum_value) + ", "
        output_line += '"hour_' + key + '_count": ' + str(count_value) + ", "
        output_line += '"hour_' + key + '_sum_relative": ' + str(float(sum_value) / len(days_set)) + ", "
        output_line += '"hour_' + key + '_count_relative": ' + str(float(count_value) / len(days_set)) + ", "
        output_line += '"hour_' + key + '_max": ' + str(max_value) + ", "
        output_line += '"hour_' + key + '_min": ' + str(min_value) + ", "
        output_line += '"hour_' + key + '_mean": ' + str(mean_value) + ", "
        output_line += '"hour_' + key + '_median": ' + str(median_value) + ", "

    # 周末特征
    (count_value, sum_value, max_value, min_value, mean_value, median_value) = get_statistic_info(week_list)
    key = "week"
    output_line += '"' + key + '_sum": ' + str(sum_value) + ", "
    output_line += '"' + key + '_count": ' + str(count_value) + ", "
    output_line += '"' + key + '_max": ' + str(max_value) + ", "
    output_line += '"' + key + '_min": ' + str(min_value) + ", "
    output_line += '"' + key + '_mean": ' + str(mean_value) + ", "
    output_line += '"' + key + '_median": ' + str(median_value) + ", "

    # 暑假特征
    (count_value, sum_value, max_value, min_value, mean_value, median_value) = get_statistic_info(vacation_list)
    key = "vacation"
    output_line += '"' + key + '_sum": ' + str(sum_value) + ", "
    output_line += '"' + key + '_count": ' + str(count_value) + ", "
    output_line += '"' + key + '_max": ' + str(max_value) + ", "
    output_line += '"' + key + '_min": ' + str(min_value) + ", "
    output_line += '"' + key + '_mean": ' + str(mean_value) + ", "
    output_line += '"' + key + '_median": ' + str(median_value) + ", "

    # 前十大食堂
    for key, record_list in canteen_dict.items():
        (count_value, sum_value, max_value, min_value, mean_value, median_value) = get_statistic_info(record_list)
        output_line += '"canteen_' + key + '_sum": ' + str(sum_value) + ", "
        output_line += '"canteen_' + key + '_count": ' + str(count_value) + ", "
        output_line += '"canteen_' + key + '_sum_relative": ' + str(float(sum_value) / len(days_set)) + ", "
        output_line += '"canteen_' + key + '_count_relative": ' + str(float(count_value) / len(days_set)) + ", "
        output_line += '"canteen_' + key + '_max": ' + str(max_value) + ", "
        output_line += '"canteen_' + key + '_min": ' + str(min_value) + ", "
        output_line += '"canteen_' + key + '_mean": ' + str(mean_value) + ", "
        output_line += '"canteen_' + key + '_median": ' + str(median_value) + ", "

    # 消费最高的10地点
    place_amount_dict_list = sorted(place_amount_dict.iteritems(), key=lambda d: d[1], reverse=True)

    if len(place_amount_dict_list) >= 10:
        for i in range(10):
            key = place_amount_dict_list[i][0]
            amount = place_amount_dict_list[i][1]
            output_line += '"place_' + str(i) + '_count": ' + str(place_count_dict[key]) + ", "
            output_line += '"place_' + str(i) + '_amount": ' + str(amount) + ", "
            output_line += '"place_' + str(i) + '_count_relative": ' + str(
                float(place_count_dict[key]) / len(days_set)) + ", "
            output_line += '"place_' + str(i) + '_amount_relative": ' + str(float(amount) / len(days_set)) + ", "
    else:
        for i in range(len(place_amount_dict_list)):
            key = place_amount_dict_list[i][0]
            amount = place_amount_dict_list[i][1]
            output_line += '"place_' + str(i) + '_count": ' + str(place_count_dict[key]) + ", "
            output_line += '"place_' + str(i) + '_amount": ' + str(amount) + ", "
            output_line += '"place_' + str(i) + '_count_relative": ' + str(
                float(place_count_dict[key]) / len(days_set)) + ", "
            output_line += '"place_' + str(i) + '_amount_relative": ' + str(float(amount) / len(days_set)) + ", "

        for i in range(len(place_amount_dict_list), 10):
            output_line += '"place_' + str(i) + '_count": ' + "0" + ", "
            output_line += '"place_' + str(i) + '_amount": ' + "0" + ", "
            output_line += '"place_' + str(i) + '_count_relative": ' + "0" + ", "
            output_line += '"place_' + str(i) + '_amount_relative": ' + "0" + ", "

    output_line += '"top_up_amount": ' + str(top_up_year / len(days_set)) + ", "
    output_line += '"max_top_up_once": ' + str(max_top_up_amount_once) + ", "
    output_line += '"max_consume_day":' + str(get_max_value_from_dict(day_consume_total_dict)) + ", "
    output_line = output_line[0:-2]
    output_line += "}"
    w.write(output_line + "\n")
w.close()
