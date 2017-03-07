#!/usr/bin/python
# -*- coding: UTF-8 -*-
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
            output_line += '"' + type_mapping(type) + 'percentage": ' + str(consume_amount_year_dict[type] / all_type_amount) + ", "
        else:
            output_line += '"' + type_mapping(type) + 'percentage": ' + "0, "

    return output_line


root_loc = "/Users/mac/Documents/contest/data/original_data/card_train_inverted_cleaned.txt"
feature_loc = "/Users/mac/Documents/contest/data/original_data/card_feature.txt"

w = open(feature_loc, 'w')

lines = open(root_loc).readlines()

# for every person
for line in lines:
    output_line = "{"
    temps = line.strip("\n").split("$")
    output_line += '"stuId": ' + temps[0] + ", "
    print temps[0]

    consume_amount_year_dict = {}
    consume_count_year_dict = {}
    day_consume_total_dict = {}
    month_consume_total_dict = {}
    days_set = set()
    top_up_year = 0.0
    max_consume_amount_once = 0.0
    max_top_up_amount_once = 0.0

    # every record for one person
    for i in range(1, len(temps)):
        records = temps[i].split(",")
        cate = records[0].strip("\"")
        location = records[1].strip("\"")
        type = records[2].strip("\"")
        time = records[3].strip("\"")
        date = time.split(" ")[0]
        month = date.split("/")[0] + "/" + date.split("/")[1]

        amount = float(records[4].strip("\""))
        balance = float(records[5].strip("\""))

        days_set.add(time.split(" ")[0])

        if cate == "POS消费":

            if not consume_amount_year_dict.has_key(type):
                consume_amount_year_dict[type] = 0.0
                consume_count_year_dict[type] = 0.0
            consume_amount_year_dict[type] += amount
            consume_count_year_dict[type] += 1

            if not day_consume_total_dict.has_key(date):
                day_consume_total_dict[date] = 0.0
            day_consume_total_dict[date] += amount

            if not month_consume_total_dict.has_key(month):
                month_consume_total_dict[month] = 0.0
            month_consume_total_dict[month] += amount

            if amount > max_consume_amount_once:
                max_consume_amount_once = amount

        if cate == "圈存转账" or cate == "支付领取" or cate == "卡充值":
            top_up_year += amount
            if amount > max_top_up_amount_once:
                max_top_up_amount_once = amount

    output_line += get_consume_type_feature(consume_amount_year_dict, consume_count_year_dict, len(days_set))
    output_line += '"top_up_amount": ' + str(top_up_year / len(days_set)) + ", "
    output_line += '"max_top_up_once": ' + str(max_top_up_amount_once) + ", "
    output_line += '"max_consume_once": ' + str(max_consume_amount_once) + ", "
    output_line += '"max_consume_day":' + str(get_max_value_from_dict(day_consume_total_dict)) + ", "
    # output_line += "月最大消费额:" + str(get_max_value_from_dict(month_consume_total_dict)) + ","
    output_line = output_line[0:-2]
    output_line += "}"
    w.write(output_line + "\n")
w.close()
