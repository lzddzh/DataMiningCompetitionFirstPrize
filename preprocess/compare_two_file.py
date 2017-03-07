file_name_1 = "../original_data//prediction_gdbt.csv"
file_name_2 = "../original_data//prediction_ada.csv"
lines_1 = open(file_name_1).readlines()
lines_2 = open(file_name_2).readlines()
total_line_num = len(lines_1)
diff_line_num = 0
for line_1, line_2 in zip(lines_1, lines_2):
    predict_1 = line_1.strip("\r\n").split(",")[1]
    predict_2 = line_2.strip("\r\n").split(",")[1]
    if not predict_1 == predict_2:
        diff_line_num += 1

print "total_num : " + str(total_line_num)
print "diff_num : " + str(diff_line_num)
