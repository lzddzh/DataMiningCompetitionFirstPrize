# !/usr/bin/python
# -*- coding: UTF-8 -*-
import time
import datetime
import numpy as np


def get_statistic_info(record_l, if_count=True, if_sum=True, if_max=True, if_min=True, if_mean=True, if_median=True,
                       if_variance=False):
    if len(record_l) != 0:
        record_np = np.asarray(record_l)
        count_v = -1
        sum_v = -1
        max_v = -1
        min_v = -1
        mean_v = -1
        median_v = -1
        var_v = -1

        if if_count:
            count_v = len(record_np)
        if if_sum:
            sum_v = record_np.sum()
        if if_max:
            max_v = record_np.max()
        if if_min:
            min_v = record_np.min()
        if if_mean:
            mean_v = record_np.mean()
        if if_median:
            median_v = np.median(record_np)
        if if_variance:
            var_v = np.var(record_np)
        return count_v, sum_v, max_v, min_v, mean_v, median_v, var_v
    else:
        return 0, 0, 0, 0, 0, 0, 0


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
    elif chinese == "淋浴":
        return "shower_"
    elif chinese == "圈存转账":
        return "quancun_"
    elif chinese == "支付领取":
        return "zhifulingqu_"
    elif chinese == "卡充值":
        return "kachongzhi_"


def get_max_value_from_dict(any_dict):
    if len(any_dict) == 0:
        return 0

    any_dict_list = sorted(any_dict.iteritems(), key=lambda d: d[1], reverse=True)
    return any_dict_list[0][1]


# def get_consume_type_feature(consume_amount_year_dict, consume_count_year_dict, day_num):
#     output_line = ""
#     type_list = ["图书馆", "", "校医院", "超市", "开水", "食堂", "洗衣房", "其他", "教务处", "文印中心", "校车", "淋浴"]
#
#     all_type_amount = 0.0
#     all_type_count = 0.0
#
#     for type in type_list:
#         if consume_amount_year_dict.has_key(type):
#             all_type_amount += consume_amount_year_dict[type]
#             all_type_count += consume_count_year_dict[type]
#             output_line += '"' + type_mapping(type) + 'amount": ' + str(consume_amount_year_dict[type] / day_num) + ", "
#             output_line += '"' + type_mapping(type) + 'count": ' + str(consume_count_year_dict[type] / day_num) + ", "
#         else:
#             output_line += '"' + type_mapping(type) + 'amount": ' + "0, "
#             output_line += '"' + type_mapping(type) + 'count": ' + "0, "
#
#     output_line += '"total_consume_amount": ' + str(all_type_amount / day_num) + ", "
#     output_line += '"total_consume_count": ' + str(all_type_count / day_num) + ", "
#
#     for type in type_list:
#         if consume_amount_year_dict.has_key(type):
#             output_line += '"' + type_mapping(type) + 'percentage": ' + str(
#                 consume_amount_year_dict[type] / all_type_amount) + ", "
#         else:
#             output_line += '"' + type_mapping(type) + 'percentage": ' + "0, "
#
#     return output_line

def get_loc_dict(loc_dict):
    lines = open("../original_data/loc_dict.csv").readlines()
    for line in lines:
        temps = line.strip("\r\n").split(",")
        id = temps[0]
        temp_list = []
        for i in range(1, len(temps)):
            temp_list.append(temps[i])
        loc_dict[id] = temp_list


def get_loc_impor(loc_impor):
    lines = open("../original_data/loc_impor.csv").readlines()
    for line in lines:
        temps = line.strip("\r\n").split(",")
        loc = temps[0]
        position = int(temps[1])

        loc_impor[loc] = position


root_loc = "../studentForm/test/card_final_test_inverted_cleaned.txt"
feature_loc = "../original_data/card_feature_test.txt"

loc_dict = {}
loc_impor = {}
get_loc_dict(loc_dict)
get_loc_impor(loc_impor)

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
                        "bus_": 0, "shower_": 0, "empty_": 0, "all_": 0}

    # 不同消费的消费纪录
    consume_dict = {"labrary_": [], "hospital_": [], "market_": [], "water_": [], "canteen_": [], "landry_": [],
                    "other_": [], "academic_office_": [], "printing_": [],
                    "bus_": [], "shower_": [], "empty_": [], "all_": []}

    # 几个充值类纪录
    cate_dict = {"quancun_": [], "zhifulingqu_": [], "kachongzhi_": [], "all_": []}

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

    # 覆盖人数最多的10个地点
    popular_dict = {"21": [], "91": [], "26": [], "6": [], "192": [], "188": [], "219": [], "61": [], "213": [],
                    "195": []}

    # 前十大地点消费金额和次数
    place_amount_dict = {}
    place_count_dict = {}

    # 每种类型去过多少地方
    type_place_dict = {"labrary_": set(), "hospital_": set(), "market_": set(), "water_": set(), "canteen_": set(),
                       "landry_": set(),
                       "other_": set(), "academic_office_": set(), "printing_": set(),
                       "bus_": set(), "shower_": set(), "empty_": set(), "all_": set()}

    # 用户一日最高消费额度  {type:{date:total_amount}}
    day_consume_total_dict = {"labrary_": {}, "hospital_": {}, "market_": {}, "water_": {}, "canteen_": {},
                              "landry_": {},
                              "other_": {}, "academic_office_": {}, "printing_": {},
                              "bus_": {}, "shower_": {}, "empty_": {}, "all_": {}}

    # 每日第一条纪录 {type:{date: time}}
    first_record_dict = {"labrary_": {}, "hospital_": {}, "market_": {}, "water_": {}, "canteen_": {},
                         "landry_": {},
                         "other_": {}, "academic_office_": {}, "printing_": {},
                         "bus_": {}, "shower_": {}, "empty_": {}, "all_": {}}
    # 每日最后一条纪录 {type:{date :time}}
    last_record_list = {"labrary_": {}, "hospital_": {}, "market_": {}, "water_": {}, "canteen_": {},
                        "landry_": {},
                        "other_": {}, "academic_office_": {}, "printing_": {},
                        "bus_": {}, "shower_": {}, "empty_": {}, "all_": {}}
    # 每天消费的种类 {date : set(type)}
    day_type_dict = {}

    # 用户是否更新卡
    if_update_card = 0

    # 用户是否挂失卡
    if_lost_card = 0

    # 用户是否换卡
    if_change_card = 0

    # 用户是否补办卡
    if_reissued_card = 0

    # 用户是否开户
    if_open_card = 0

    # 用户是否注销账户
    if_cancel_card = 0

    # 用户是否解冻卡
    if_unfreezed_card = 0

    # 去过多少个单价最高的前k个地方
    place_set_impor_place = [set(), set(), set(), set(), set()]

    # 单价最高的前k个地方去过多少次
    count_impor_place = [0, 0, 0, 0, 0]

    # 单价最高的前k个地方花过多少钱
    amount_impor_place = [0, 0, 0, 0, 0]

    days_set = set()

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
        minute = time.split(" ")[1].split(":")[1]
        second = time.split(" ")[1].split(":")[2]
        elipsed_time = int(hour) * 3600 + int(minute) * 60 + int(second)
        amount = float(records[4].strip("\""))
        balance = float(records[5].strip("\""))
        weekends = datetime.datetime(int(date.split("/")[0]), int(date.split("/")[1]),
                                     int(date.split("/")[2])).strftime("%w")

        days_set.add(time.split(" ")[0])

        balance_list.append(balance)

        if cate_dict.has_key(type_mapping(cate)):
            cate_dict[type_mapping(cate)].append(amount)
            cate_dict["all_"].append(amount)

        if cate == "POS消费":

            sum_consume_dict[type] += amount
            sum_consume_dict["all_"] += amount

            if not day_consume_total_dict[type].has_key(date):
                day_consume_total_dict[type][date] = 0
            day_consume_total_dict[type][date] += amount

            if not day_consume_total_dict["all_"].has_key(date):
                day_consume_total_dict["all_"][date] = 0
            day_consume_total_dict["all_"][date] += amount

            type_place_dict[type].add(location)
            type_place_dict["all_"].add(location)

            if not first_record_dict[type].has_key(date):
                first_record_dict[type][date] = 90000
            if elipsed_time < first_record_dict[type][date]:
                first_record_dict[type][date] = elipsed_time

            if not first_record_dict["all_"].has_key(date):
                first_record_dict["all_"][date] = 90000
            if elipsed_time < first_record_dict["all_"][date]:
                first_record_dict["all_"][date] = elipsed_time

            if not last_record_list[type].has_key(date):
                last_record_list[type][date] = -1
            if elipsed_time > last_record_list[type][date]:
                last_record_list[type][date] = elipsed_time

            if not last_record_list["all_"].has_key(date):
                last_record_list["all_"][date] = -1
            if elipsed_time > last_record_list["all_"][date]:
                last_record_list["all_"][date] = elipsed_time

            if not day_type_dict.has_key(date):
                day_type_dict[date] = set()
            day_type_dict[date].add(type)

            if loc_impor.get(location, float("inf")) <= 10:
                place_set_impor_place[0].add(location)
                count_impor_place[0] += 1
                amount_impor_place[0] += amount
            if loc_impor.get(location, float("inf")) <= 30:
                place_set_impor_place[1].add(location)
                count_impor_place[1] += 1
                amount_impor_place[1] += amount
            if loc_impor.get(location, float("inf")) <= 50:
                place_set_impor_place[2].add(location)
                count_impor_place[2] += 1
                amount_impor_place[2] += amount
            if loc_impor.get(location, float("inf")) <= 100:
                place_set_impor_place[3].add(location)
                count_impor_place[3] += 1
                amount_impor_place[3] += amount
            if loc_impor.get(location, float("inf")) <= 500:
                place_set_impor_place[4].add(location)
                count_impor_place[4] += 1
                amount_impor_place[4] += amount

            if amount >= 0:

                consume_dict["all_"].append(amount)
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

                if popular_dict.has_key(location):
                    popular_dict[location].append(amount)

                if not place_amount_dict.has_key(location):
                    place_amount_dict[location] = amount
                    place_count_dict[location] = 1
                else:
                    place_amount_dict[location] += amount
                    place_count_dict[location] += 1

        if cate == "换卡":
            if_change_card = 1

        if cate == "更新卡信息":
            if_update_card = 1

        if cate == "卡挂失":
            if_lost_card = 1

        if cate == "卡补办":
            if_reissued_card = 1

        if cate == "卡片开户":
            if_open_card = 1

        if cate == "卡片销户":
            if_cancel_card = 1

        if cate == "卡解挂":
            if_unfreezed_card = 1

    # 拼接不同消费类型总额及占比
    total_amount = sum_consume_dict["all_"]
    for key, value in sum_consume_dict.items():
        output_line += '"' + key + '_sum": ' + str(value) + ", "
        output_line += '"' + key + '_sum_relative": ' + str(float(value) / len(days_set)) + ", "
        if total_amount != 0:
            if key != "all_":
                output_line += '"' + key + '_percentage": ' + str(float(value) / total_amount) + ", "
        else:
            if key != "all_":
                output_line += '"' + key + '_percentage": ' + "0" + ", "

    # 各种类每天第一条纪录的统计
    for key, value in first_record_dict.items():
        (count_value, sum_value, max_value, min_value, mean_value, median_value, var_value) = get_statistic_info(
            value.values(), False, False, True, True, True, True, True)
        output_line += '"' + key + '_first_record_min": ' + str(min_value) + ", "
        output_line += '"' + key + '_first_record_max": ' + str(max_value) + ", "
        output_line += '"' + key + '_first_record_avg": ' + str(mean_value) + ", "
        output_line += '"' + key + '_first_record_median": ' + str(median_value) + ", "
        output_line += '"' + key + '_first_record_var": ' + str(var_value) + ", "

    # 个种类每天最后一条纪录的统计
    for key, value in last_record_list.items():
        (count_value, sum_value, max_value, min_value, mean_value, median_value, var_value) = get_statistic_info(
            value.values(), False, False, True, True, True, True, True)
        output_line += '"' + key + '_last_record_min": ' + str(min_value) + ", "
        output_line += '"' + key + '_last_record_max": ' + str(max_value) + ", "
        output_line += '"' + key + '_last_record_avg": ' + str(mean_value) + ", "
        output_line += '"' + key + '_last_record_median": ' + str(median_value) + ", "
        output_line += '"' + key + '_last_record_var": ' + str(var_value) + ", "

    # 各种类消费的相互比
    type_list = sum_consume_dict.keys()
    for i in range(len(type_list)):
        for j in range(i + 1, len(type_list)):
            if type_list[i] != "all_" and type_list[j] != "all_":
                if sum_consume_dict[type_list[i]] == 0 or sum_consume_dict[type_list[j]] == 0:
                    output_line += '"' + type_list[i] + '_divide_' + type_list[j] + '":' + "-1" + ", "
                else:
                    output_line += '"' + type_list[i] + '_divide_' + type_list[j] + '":' + str(
                        sum_consume_dict[type_list[i]] / sum_consume_dict[type_list[j]]) + ", "

    # 拼接不同种类的消费的各种统计值
    for key, record_list in consume_dict.items():
        (count_value, sum_value, max_value, min_value, mean_value, median_value, var_value) = get_statistic_info(
            record_list, True, False, True, True, True, True, True)
        output_line += '"' + key + '_count": ' + str(count_value) + ", "
        output_line += '"' + key + '_count_relative": ' + str(float(count_value) / len(days_set)) + ", "
        output_line += '"' + key + '_max": ' + str(max_value) + ", "
        output_line += '"' + key + '_min": ' + str(min_value) + ", "
        output_line += '"' + key + '_mean": ' + str(mean_value) + ", "
        output_line += '"' + key + '_median": ' + str(median_value) + ", "
        output_line += '"' + key + '_var": ' + str(var_value) + ", "

    # 拼接不同充值的各种统计值
    for key, record_list in cate_dict.items():
        (count_value, sum_value, max_value, min_value, mean_value, median_value, var_value) = get_statistic_info(
            record_list, True, True, True, True, True, True, True)
        output_line += '"' + key + 'top_up_count": ' + str(count_value) + ", "
        output_line += '"' + key + 'top_up_count_relative": ' + str(float(count_value) / len(days_set)) + ", "
        output_line += '"' + key + 'top_up_sum": ' + str(sum_value) + ", "
        output_line += '"' + key + 'top_up_sum_relative": ' + str(float(sum_value) / len(days_set)) + ", "
        output_line += '"' + key + 'top_up_max": ' + str(max_value) + ", "
        output_line += '"' + key + 'top_up_min": ' + str(min_value) + ", "
        output_line += '"' + key + 'top_up_mean": ' + str(mean_value) + ", "
        output_line += '"' + key + 'top_up_median": ' + str(median_value) + ", "
        output_line += '"' + key + 'top_up_var": ' + str(var_value) + ", "

    # 余额特征
    (count_value, sum_value, max_value, min_value, mean_value, median_value, var_value) = get_statistic_info(
        balance_list)
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
        (count_value, sum_value, max_value, min_value, mean_value, median_value, var_value) = get_statistic_info(
            record_list)
        output_line += '"hour_' + key + '_sum": ' + str(sum_value) + ", "
        output_line += '"hour_' + key + '_sum_per_day": ' + str(float(sum_value) / len(days_set)) + ", "
        output_line += '"hour_' + key + '_count": ' + str(count_value) + ", "
        output_line += '"hour_' + key + '_sum_relative": ' + str(float(sum_value) / len(days_set)) + ", "
        output_line += '"hour_' + key + '_count_relative": ' + str(float(count_value) / len(days_set)) + ", "
        output_line += '"hour_' + key + '_max": ' + str(max_value) + ", "
        output_line += '"hour_' + key + '_min": ' + str(min_value) + ", "
        output_line += '"hour_' + key + '_mean": ' + str(mean_value) + ", "
        output_line += '"hour_' + key + '_median": ' + str(median_value) + ", "

    week_avg = 0
    non_week_avg = 0

    # 周末特征
    (count_value, sum_value, max_value, min_value, mean_value, median_value, var_value) = get_statistic_info(week_list)
    key = "week"
    output_line += '"' + key + '_sum": ' + str(sum_value) + ", "
    output_line += '"' + key + '_count": ' + str(count_value) + ", "
    output_line += '"' + key + '_max": ' + str(max_value) + ", "
    output_line += '"' + key + '_min": ' + str(min_value) + ", "
    output_line += '"' + key + '_mean": ' + str(mean_value) + ", "
    output_line += '"' + key + '_median": ' + str(median_value) + ", "
    week_avg = mean_value

    # 非周末特征
    (count_value, sum_value, max_value, min_value, mean_value, median_value, var_value) = get_statistic_info(
        non_week_list)
    key = "non_week"
    output_line += '"' + key + '_sum": ' + str(sum_value) + ", "
    output_line += '"' + key + '_count": ' + str(count_value) + ", "
    output_line += '"' + key + '_max": ' + str(max_value) + ", "
    output_line += '"' + key + '_min": ' + str(min_value) + ", "
    output_line += '"' + key + '_mean": ' + str(mean_value) + ", "
    output_line += '"' + key + '_median": ' + str(median_value) + ", "
    non_week_avg = mean_value

    output_line += '"non_week_diff": ' + str(week_avg - non_week_avg) + ", "

    # 暑假特征
    (count_value, sum_value, max_value, min_value, mean_value, median_value, var_value) = get_statistic_info(
        vacation_list)
    key = "vacation"
    output_line += '"' + key + '_sum": ' + str(sum_value) + ", "
    output_line += '"' + key + '_count": ' + str(count_value) + ", "
    output_line += '"' + key + '_max": ' + str(max_value) + ", "
    output_line += '"' + key + '_min": ' + str(min_value) + ", "
    output_line += '"' + key + '_mean": ' + str(mean_value) + ", "
    output_line += '"' + key + '_median": ' + str(median_value) + ", "

    # 前十大食堂
    for key, record_list in canteen_dict.items():
        (count_value, sum_value, max_value, min_value, mean_value, median_value, var_value) = get_statistic_info(
            record_list)
        output_line += '"canteen_' + key + '_sum": ' + str(sum_value) + ", "
        output_line += '"canteen_' + key + '_count": ' + str(count_value) + ", "
        output_line += '"canteen_' + key + '_sum_relative": ' + str(float(sum_value) / len(days_set)) + ", "
        output_line += '"canteen_' + key + '_count_relative": ' + str(float(count_value) / len(days_set)) + ", "
        output_line += '"canteen_' + key + '_max": ' + str(max_value) + ", "
        output_line += '"canteen_' + key + '_min": ' + str(min_value) + ", "
        output_line += '"canteen_' + key + '_mean": ' + str(mean_value) + ", "
        output_line += '"canteen_' + key + '_median": ' + str(median_value) + ", "

    # 覆盖人数最多的前十个地点
    for key, record_list in popular_dict.items():
        (count_value, sum_value, max_value, min_value, mean_value, median_value, var_value) = get_statistic_info(
            record_list)
        output_line += '"popular_' + key + '_sum": ' + str(sum_value) + ", "
        output_line += '"popular_' + key + '_count": ' + str(count_value) + ", "
        output_line += '"popular_' + key + '_sum_relative": ' + str(float(sum_value) / len(days_set)) + ", "
        output_line += '"popular_' + key + '_count_relative": ' + str(float(count_value) / len(days_set)) + ", "
        output_line += '"popular_' + key + '_max": ' + str(max_value) + ", "
        output_line += '"popular_' + key + '_min": ' + str(min_value) + ", "
        output_line += '"popular_' + key + '_mean": ' + str(mean_value) + ", "
        output_line += '"popular_' + key + '_median": ' + str(median_value) + ", "

    # 用户消费最高的10地点

    top_ten_amount_statistics = [0, 0, 0, 0, 0, 0]

    place_amount_dict_list = sorted(place_amount_dict.iteritems(), key=lambda d: d[1], reverse=True)

    if len(place_amount_dict_list) >= 10:
        for i in range(10):
            key = place_amount_dict_list[i][0]
            amount = place_amount_dict_list[i][1]
            for j in range(len(top_ten_amount_statistics)):
                top_ten_amount_statistics[j] += float(loc_dict[key][j])

            output_line += '"top_amount_place_' + str(i) + '_count": ' + str(place_count_dict[key]) + ", "
            output_line += '"top_amount_place_' + str(i) + '_amount": ' + str(amount) + ", "
            output_line += '"top_amount_place_' + str(i) + '_count_relative": ' + str(
                float(place_count_dict[key]) / len(days_set)) + ", "
            output_line += '"top_amount_place_' + str(i) + '_amount_relative": ' + str(
                float(amount) / len(days_set)) + ", "
    else:
        for i in range(len(place_amount_dict_list)):
            key = place_amount_dict_list[i][0]

            amount = place_amount_dict_list[i][1]
            for j in range(len(top_ten_amount_statistics)):
                top_ten_amount_statistics[j] += float(loc_dict[key][j])

            output_line += '"top_amount_place_' + str(i) + '_count": ' + str(place_count_dict[key]) + ", "
            output_line += '"top_amount_place_' + str(i) + '_amount": ' + str(amount) + ", "
            output_line += '"top_amount_place_' + str(i) + '_count_relative": ' + str(
                float(place_count_dict[key]) / len(days_set)) + ", "
            output_line += '"top_amount_place_' + str(i) + '_amount_relative": ' + str(
                float(amount) / len(days_set)) + ", "

        for i in range(len(place_amount_dict_list), 10):
            output_line += '"top_amount_place_' + str(i) + '_count": ' + "0" + ", "
            output_line += '"top_amount_place_' + str(i) + '_amount": ' + "0" + ", "
            output_line += '"top_amount_place_' + str(i) + '_count_relative": ' + "0" + ", "
            output_line += '"top_amount_place_' + str(i) + '_amount_relative": ' + "0" + ", "

    output_line += '"top_ten_amount_place_count": ' + str(top_ten_amount_statistics[0]) + ", "
    output_line += '"top_ten_amount_place_amount": ' + str(top_ten_amount_statistics[1]) + ", "
    output_line += '"top_ten_amount_place_visit": ' + str(top_ten_amount_statistics[2]) + ", "
    output_line += '"top_ten_amount_place_amount_per_person": ' + str(top_ten_amount_statistics[3]) + ", "
    output_line += '"top_ten_amount_place_count_per_person": ' + str(top_ten_amount_statistics[4]) + ", "
    output_line += '"top_ten_amount_place_amount_per_time": ' + str(top_ten_amount_statistics[5]) + ", "

    # 用户去的最多的10个地方
    top_ten_count_statistics = [0, 0, 0, 0, 0, 0]

    place_count_dict_list = sorted(place_count_dict.iteritems(), key=lambda d: d[1], reverse=True)

    if len(place_count_dict_list) >= 10:
        for i in range(10):
            key = place_count_dict_list[i][0]

            count = place_count_dict_list[i][1]
            for j in range(len(top_ten_count_statistics)):
                top_ten_count_statistics[j] += float(loc_dict[key][j])

            output_line += '"top_count_place_' + str(i) + '_count": ' + str(count) + ", "
            output_line += '"top_count_place_' + str(i) + '_amount": ' + str(place_amount_dict[key]) + ", "
            output_line += '"top_count_place_' + str(i) + '_count_relative": ' + str(
                float(count) / len(days_set)) + ", "
            output_line += '"top_count_place_' + str(i) + '_amount_relative": ' + str(
                float(place_amount_dict[key]) / len(days_set)) + ", "
    else:
        for i in range(len(place_amount_dict_list)):
            key = place_count_dict_list[i][0]

            count = place_count_dict_list[i][1]
            for j in range(len(top_ten_count_statistics)):
                top_ten_count_statistics[j] += float(loc_dict[key][j])

            output_line += '"top_count_place_' + str(i) + '_count": ' + str(count) + ", "
            output_line += '"top_count_place_' + str(i) + '_amount": ' + str(place_amount_dict[key]) + ", "
            output_line += '"top_count_place_' + str(i) + '_count_relative": ' + str(
                float(count) / len(days_set)) + ", "
            output_line += '"top_count_place_' + str(i) + '_amount_relative": ' + str(
                float(place_amount_dict[key]) / len(days_set)) + ", "

        for i in range(len(place_amount_dict_list), 10):
            output_line += '"top_count_place_' + str(i) + '_count": ' + "0" + ", "
            output_line += '"top_count_place_' + str(i) + '_amount": ' + "0" + ", "
            output_line += '"top_count_place_' + str(i) + '_count_relative": ' + "0" + ", "
            output_line += '"top_count_place_' + str(i) + '_amount_relative": ' + "0" + ", "

    output_line += '"top_ten_count_place_count": ' + str(top_ten_count_statistics[0]) + ", "
    output_line += '"top_ten_count_place__amount": ' + str(top_ten_count_statistics[1]) + ", "
    output_line += '"top_ten_count_place__visit": ' + str(top_ten_count_statistics[2]) + ", "
    output_line += '"top_ten_count_place__amount_per_person": ' + str(top_ten_count_statistics[3]) + ", "
    output_line += '"top_ten_count_place__count_per_person": ' + str(top_ten_count_statistics[4]) + ", "
    output_line += '"top_ten_count_place__amount_per_time": ' + str(top_ten_count_statistics[5]) + ", "

    # 前k个单价最高的地方的统计
    for i in range(5):
        output_line += '"top_' + str(i) + '_impor_place_have_been":' + str(len(place_set_impor_place[i])) + ", "
        output_line += '"top_' + str(i) + '_impor_place_have_count":' + str(count_impor_place[i]) + ", "
        output_line += '"top_' + str(i) + '_impor_place_amount":' + str(amount_impor_place[i]) + ", "

    # 用户去过多少地方

    for key, value in type_place_dict.items():
        output_line += '"' + key + 'place_have_gone": ' + str(len(value)) + ", "

    # 各个种类下 每个用户每日消费额度的最大值,最小值,和方差
    for key, value in day_consume_total_dict.items():
        (count_value, sum_value, max_value, min_value, mean_value, median_value, var_value) = get_statistic_info(
            value.values(),
            False, False,
            True, True, False,
            False, True)
        output_line += '"' + key + '_consume_one_day_max": ' + str(max_value) + ", "
        output_line += '"' + key + '_consume_one_day_min": ' + str(min_value) + ", "
        output_line += '"' + key + '_consume_one_day_var": ' + str(var_value) + ", "

    # 各个种类涉及的天数
    for key, value in day_consume_total_dict.items():
        # all 相对天数肯定为1
        if key != "all_":
            output_line += '"' + key + '_relative_involved_day": ' + str(float(len(value)) / len(days_set)) + ", "

    # 每天消费的种类
    type_num_list = []
    for value in day_type_dict.values():
        type_num_list.append(len(value))
    (count_value, sum_value, max_value, min_value, mean_value, median_value, var_value) = get_statistic_info(
        type_num_list, False, False, True, True, True, False, False)
    output_line += '"day_type_max":' + str(max_value) + ", "
    output_line += '"day_type_min":' + str(min_value) + ", "
    output_line += '"day_type_avg":' + str(mean_value) + ", "

    # 用户是否更新卡
    output_line += '"if_update_card": ' + str(if_update_card) + ", "

    # 用户是否挂失卡
    output_line += '"if_lost_card": ' + str(if_lost_card) + ", "

    # 用户是否换卡
    output_line += '"if_change_card": ' + str(if_change_card) + ", "

    # 用户是否补办卡
    output_line += '"if_reissued_card": ' + str(if_reissued_card) + ", "

    # 用户是否开户
    output_line += '"if_open_card": ' + str(if_open_card) + ", "

    # 用户是否注销账户
    output_line += '"if_cancel_card": ' + str(if_cancel_card) + ", "

    # 用户是否解冻卡
    output_line += '"if_unfreezed_card": ' + str(if_unfreezed_card) + ", "

    output_line = output_line[0:-2]
    output_line += "}"
    w.write(output_line + "\n")

w.close()
