root_loc = "../original_data/raw_data/train/"
score_file = "score_train.txt"
subsidy_file = "subsidy_train.txt"

subsidy_dict = {}
faculty_dict = {}

lines = open(root_loc + subsidy_file).readlines()
for line in lines:
    temps = line.strip("\n").split(",")
    id = int(temps[0])
    subsidy = int(temps[1])
    subsidy_dict[id] = subsidy

lines = open(root_loc + score_file).readlines()
for line in lines:
    temps = line.strip("\n").split(",")
    id = int(temps[0])
    faculty = temps[1]
    subsidy = subsidy_dict[id]
    if not faculty_dict.has_key(faculty):
        faculty_dict[faculty] = {}
    if not faculty_dict[faculty].has_key(subsidy):
        faculty_dict[faculty][subsidy] = 0
    faculty_dict[faculty][subsidy] += 1

for key, value in faculty_dict.items():
    totol_num = 0
    for i in [0, 1000, 1500, 2000]:
        totol_num += value.get(i, 0)
    value["0_percent"] = float(value.get(0, 0)) / totol_num
    value["1000_percent"] = float(value.get(1000, 0)) / totol_num
    value["1500_percent"] = float(value.get(1500, 0)) / totol_num
    value["2000_percent"] = float(value.get(2000, 0)) / totol_num
    value["totol_num"] = totol_num

print faculty_dict

w = open("../original_data/faculty_feature_train.txt", 'w')
lines = open(root_loc + score_file).readlines()
for line in lines:
    output_line = "{"
    temps = line.strip("\n").split(",")
    id = int(temps[0])
    faculty = temps[1]
    output_line += '"stuId": ' + str(id) + ", "
    output_line += '"0_num":' + str(faculty_dict[faculty][0]) + ","
    output_line += '"1000_num":' + str(faculty_dict[faculty][1000]) + ","
    output_line += '"1500_num":' + str(faculty_dict[faculty].get(1500, 0)) + ","
    output_line += '"2000_num":' + str(faculty_dict[faculty][2000]) + ","
    output_line += '"0_percent":' + str(faculty_dict[faculty]["0_percent"]) + ","
    output_line += '"1000_percent":' + str(faculty_dict[faculty]["1000_percent"]) + ","
    output_line += '"1500_percent":' + str(faculty_dict[faculty]["1500_percent"]) + ","
    output_line += '"2000_percent":' + str(faculty_dict[faculty]["2000_percent"]) + ","
    output_line += '"totol_num_faculty":' + str(faculty_dict[faculty]["totol_num"]) + "}"
    w.write(output_line+"\n")
w.close()


w = open("../original_data/faculty_feature_test.txt", 'w')
lines = open("../original_data/raw_data/test/score_final_test.txt").readlines()
for line in lines:
    output_line = "{"
    temps = line.strip("\n").split(",")
    id = int(temps[0])
    faculty = temps[1]
    output_line += '"stuId": ' + str(id) + ", "
    output_line += '"0_num":' + str(faculty_dict[faculty][0]) + ","
    output_line += '"1000_num":' + str(faculty_dict[faculty][1000]) + ","
    output_line += '"1500_num":' + str(faculty_dict[faculty].get(1500, 0)) + ","
    output_line += '"2000_num":' + str(faculty_dict[faculty][2000]) + ","
    output_line += '"0_percent":' + str(faculty_dict[faculty]["0_percent"]) + ","
    output_line += '"1000_percent":' + str(faculty_dict[faculty]["1000_percent"]) + ","
    output_line += '"1500_percent":' + str(faculty_dict[faculty]["1500_percent"]) + ","
    output_line += '"2000_percent":' + str(faculty_dict[faculty]["2000_percent"]) + ","
    output_line += '"totol_num_faculty":' + str(faculty_dict[faculty]["totol_num"]) + "}"
    w.write(output_line+"\n")
w.close()

