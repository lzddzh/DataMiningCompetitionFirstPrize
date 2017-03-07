# !/usr/bin/python
# -*- coding: UTF-8 -*-

def extract_loc_info(loc_dict, file_name):
    lines = open(file_name).readlines()
    # every person
    for line in lines:
        temps = line.strip("\n").split("$")
        id = temps[0]

        # every record
        for i in range(1, len(temps)):
            records = temps[i].split(",")
            cate = records[0].strip("\"")
            location = unicode(records[1].strip("\""), "utf-8")[2:]
            amount = float(records[4].strip("\""))

            if cate == "POS消费":
                if not loc_dict.has_key(location):
                    loc_dict[location] = [0, 0.0, set(), -1, -1, -1]
                loc_dict[location][0] += 1
                loc_dict[location][1] += amount
                loc_dict[location][2].add(id)


# {相应地点 : [ 产生的总计数，产生的总金额，来过的人数，每人花钱数，每人来的次数,每次花的钱数] }
loc_dict = {}
extract_loc_info(loc_dict, "../studentForm/train/card_train_inverted_cleaned.txt")
extract_loc_info(loc_dict, "../studentForm/test/card_final_test_inverted_cleaned.txt")
extract_loc_info(loc_dict, "../studentForm/test_old/card_test_inverted_cleaned.txt")

w = open("../original_data/loc_dict.csv", 'w')

# 按照每个地点的单价进行排序
w1 = open("../original_data/loc_impor.csv", 'w')

price_per_time_dict = {}
for key, value in loc_dict.items():
    value[2] = len(value[2])
    value[3] = float(value[1]) / value[2]
    value[4] = float(value[0]) / value[2]
    value[5] = float(value[1]) / value[0]
    price_per_time_dict[key] = value[5]

price_per_time_dict_list = sorted(price_per_time_dict.iteritems(), key=lambda d: d[1], reverse=True)

position = 1
for temp in price_per_time_dict_list:
    key = temp[0]
    w.write(
        key + "," + str(loc_dict[key][0]) + "," + str(loc_dict[key][1]) + "," + str(loc_dict[key][2]) + "," + str(
            loc_dict[key][3]) + "," +
        str(loc_dict[key][4]) + "," + str(loc_dict[key][5]) + "\n")
    if loc_dict[key][2] >= 3000:
        w1.write(key + "," + str(position) + "\n")
        position += 1

w.close()
w1.close()
