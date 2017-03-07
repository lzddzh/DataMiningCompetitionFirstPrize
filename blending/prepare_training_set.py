from commons import variables
import random
import os

lines_list = []
# file_list = [3, 7, 10, 12, 23, 32, 33]
#
# for i in range(len(file_list)):
#     lines_list.append(open("../original_data/gdbt_blending_offline/cv_prediction_with_class_gdbt_seed_" + str(
#         file_list[i]) + ".txt").readlines())

# for file_name in os.listdir("../original_data/gdbt_blending_offline"):
#     if file_name != ".DS_Store":
#         lines_list.append(open("../original_data/gdbt_blending_offline/"+file_name).readlines())
#
# lines_list=lines_list[:5]


lines_list.append(open("../original_data/cv_prediction_with_class_gdbt1.txt").readlines())
lines_list.append(open("../original_data/cv_prediction_with_class_gdbt2.txt").readlines())
lines_list.append(open("../original_data/cv_prediction_with_class_gdbt3.txt").readlines())
lines_list.append(open("../original_data/cv_prediction_with_class_xgb.txt").readlines())
lines_list.append(open("../original_data/cv_prediction_with_class_ada.txt").readlines())
lines_list.append(open("../original_data/cv_prediction_with_class_rf.txt").readlines())
lines_list.append(open("../original_data/cv_prediction_with_class_et.txt").readlines())


w = open(variables.root_loc + "training_set_blending.txt", 'w')
exam_num = len(lines_list[0])

for i in range(exam_num):
    output_line = ""
    output_line += lines_list[0][i].strip("\n") + ","

    for j in range(1, len(lines_list)):
        output_line += lines_list[j][i].strip("\n").split(",")[1] + ","

    output_line = output_line[:-1]
    w.write(output_line + "\n")

w.close()

# split cross validation
# cv_w_list = []
# for i in range(5):
#     cv_w_list.append(open("../original_data/cv_fold_blending_" + str(i) + ".txt", 'w'))
#
# lines = open(variables.root_loc + "training_set_blending.txt").readlines()
#
# for line in lines:
#     cv_num = random.randint(0, 4)
#     cv_w_list[cv_num].write(line)
#
# for i in range(5):
#     cv_w_list[i].close()
