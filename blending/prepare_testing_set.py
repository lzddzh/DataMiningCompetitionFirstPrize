from commons import variables
import random
import os

lines_list = []

# file_list = [3, 7, 10, 12, 23, 32, 33]
#
# for i in range(len(file_list)):
#     lines_list.append(open("../original_data/gdbt_blending/prediction_with_class_gdbt_seed_" + str(
#         file_list[i]) + ".csv").readlines())

# for file_name in os.listdir("../original_data/gdbt_blending"):
#     if file_name != ".DS_Store":
#         lines_list.append(open("../original_data/gdbt_blending/"+file_name).readlines())

lines_list.append(open("../original_data/blending_final/prediction_with_class_gdbt_1.csv").readlines())
lines_list.append(open("../original_data/blending_final/prediction_with_class_gdbt_2.csv").readlines())
lines_list.append(open("../original_data/blending_final/prediction_with_class_gdbt_3.csv").readlines())
lines_list.append(open("../original_data/blending_final/prediction_with_class_xgb.csv").readlines())
lines_list.append(open("../original_data/blending_final/prediction_with_class_ada.csv").readlines())
lines_list.append(open("../original_data/blending_final/prediction_with_class_rf.csv").readlines())
lines_list.append(open("../original_data/blending_final/prediction_with_class_et.csv").readlines())




w = open(variables.root_loc + "test_set_blending.txt", 'w')
test_num = len(lines_list[0])

for i in range(1, test_num):
    output_line = ""
    output_line += lines_list[0][i].strip("\n") + ","

    for j in range(1, len(lines_list)):
        # temp_list = lines_list[j][i].strip("\n").split(",")
        # for k in range(1, 5):
        #     output_line += temp_list[k] + ","
        output_line += lines_list[j][i].strip("\n").split(",")[1] + ","

    output_line = output_line[:-1]
    w.write(output_line + "\n")

w.close()
