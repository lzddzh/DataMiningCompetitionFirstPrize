import random


def read_data_with_label(file_loc_list, x, y, impor_fea_list, negtive_id_list):
    for file_loc in file_loc_list:
        lines = open(file_loc).readlines()
        for line in lines:
            fea_list = []
            temps = line.strip("\n").strip("\r").split(",")
            label = temps[0].split(":")[1]
            id = temps[1].split(":")[1]
            if negtive_id_list != None and label == "0" and id not in negtive_id_list:
                continue
            y.append(label)
            temps = temps[2:]

            fea_id = 0
            for temp in temps:
                if impor_fea_list == None or fea_id in impor_fea_list:
                    fea_list.append(temp.split(":")[1])
                fea_id += 1
            fea_list = [float(i) for i in fea_list]
            x.append(fea_list)


def read_data_without_label(file_loc_list, x, test_ids):
    for file_loc in file_loc_list:
        lines = open(file_loc).readlines()
        for line in lines:
            fea_list = []
            temps = line.strip("\n").strip("\r").split(",")
            test_ids.append(temps[0].split(":")[1])
            temps = temps[1:]
            for temp in temps:
                fea_list.append(temp.split(":")[1])
            fea_list = [float(i) for i in fea_list]
            x.append(fea_list)


def simple_negative_sample(x, y, select_rate):
    random.seed(2017)
    new_x = []
    new_y = []
    for i in range(len(x)):
        label = y[i]
        if label == "0":
            if random.random() > select_rate:
                continue

        new_x.append(x[i])
        new_y.append(y[i])

    return (new_x, new_y)


def add_positive_sample(x, y):
    new_x = []
    new_y = []
    for i in range(len(x)):
        label = y[i]
        if label == "1000":
            for j in range(1):
                new_x.append(x[i])
                new_y.append(y[i])
        elif label == "1500":
            for j in range(1):
                new_x.append(x[i])
                new_y.append(y[i])
        elif label == "2000":
            for j in range(2):
                new_x.append(x[i])
                new_y.append(y[i])
        else:
            if random.random() <= 0.15:
                new_x.append(x[i])
                new_y.append(y[i])
    return (new_x, new_y)


def get_subsidy_distribution(y_list):
    count_dict = {}
    for y in y_list:
        if not count_dict.has_key(y):
            count_dict[y] = 0
        count_dict[y] += 1

    print "subsidy distribution:-----------------"
    for key in ["0", "1000", "1500", "2000"]:
        print str(key) + " : " + str(count_dict.get(key, 0))
    print "--------------------------------------"


def read_fea_list(fea_file_loc):
    important_fea_list = []
    lines = open(fea_file_loc).readlines();
    for line in lines:
        important_fea_list.append(int(line.strip("\n")))
    return important_fea_list


def read_negative_id(negative_ids_loc):
    negative_ids = []
    lines = open(negative_ids_loc).readlines();
    for line in lines:
        negative_ids.append(line.strip("\n"))
    return negative_ids


def read_blending_data_with_label(file_loc_list, x, y):
    for file_loc in file_loc_list:
        lines = open(file_loc).readlines()
        for line in lines:
            fea_list = []
            temps = line.strip("\n").strip("\r").split(",")
            label = temps[0]
            y.append(label)
            temps = temps[1:]
            for temp in temps:
                fea_list.append(temp)
            fea_list = [float(i) for i in fea_list]
            x.append(fea_list)


def read_blending_data_without_label(file_loc_list, test_x, test_ids):
    for file_loc in file_loc_list:
        lines = open(file_loc).readlines()
        for line in lines:
            fea_list = []
            temps = line.strip("\n").strip("\r").split(",")
            id = temps[0]
            test_ids.append(id)
            temps = temps[1:]
            for temp in temps:
                fea_list.append(temp)
            fea_list = [float(i) for i in fea_list]
            test_x.append(fea_list)
