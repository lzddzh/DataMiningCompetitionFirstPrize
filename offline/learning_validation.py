import sys
import time

sys.path.append("../")
from commons import variables
from commons import tools
from commons import validation
from learning_algorithm import *


def run_model(cv_file_list, learning_model):
    avg_macro_f1 = 0

    total_num = 10885
    right_num_dict = {}
    prediction_num_dict = {}
    actual_num_dict = {}
    # fea_list = tools.read_fea_list(variables.root_loc + "important_features.txt")
    # negative_id_list = tools.read_negative_id(variables.root_loc + "negative_ids.txt")

    for subsidy in ["1000", "1500", "2000"]:
        right_num_dict[subsidy] = 0
        prediction_num_dict[subsidy] = 0
        actual_num_dict[subsidy] = 0

    if variables.if_write_cv_prediction:
        if variables.prob_mode:
            w = open(variables.write_cv_location + "prob_" + learning_model + ".txt", 'w')
        else:
            w = open(variables.write_cv_location + "class_" + learning_model + ".txt", 'w')

    for i in range(variables.cv_num):
        start = time.time()

        x = []
        y = []
        training_data_set = cv_file_list[:]
        del training_data_set[i]
        tools.read_data_with_label(training_data_set, x, y, None, None)

        test_x = []
        test_y = []
        tools.read_data_with_label([cv_file_list[i]], test_x, test_y, None, None)

        if learning_model == "gdbt":
            predict_y_list, predict_y_prob_list = gradient_boosting.learn(x, y, test_x)
        elif learning_model == "svm":
            predict_y_list, predict_y_prob_list = support_vector_machine.learn(x, y, test_x)
        elif learning_model == "ada":
            predict_y_list, predict_y_prob_list, predict_y_prob_list = ada_boosting.learn(x, y, test_x)
        elif learning_model == "rf":
            predict_y_list, predict_y_prob_list = random_forest.learn(x, y, test_x)
        elif learning_model == "et":
            predict_y_list, predict_y_prob_list = extra_trees.learn(x, y, test_x)
        elif learning_model == "knnBag":
            predict_y_list, predict_y_prob_list = knn_bagging.learn(x, y, test_x)
        elif learning_model == "nn":
            predict_y_list, predict_y_prob_list = neural_network.learn(x, y, test_x)
        elif learning_model == "xgb":
            predict_y_list, predict_y_prob_list = xgboosting.learn(x, y, test_x)

        if variables.if_write_cv_prediction:
            if variables.prob_mode:
                for real, prediction_prob in zip(test_y, predict_y_prob_list):
                    temp_line = ""
                    temp_line += str(real) + ","
                    for prob in prediction_prob:
                        temp_line += str(prob) + ","
                    temp_line = temp_line[:-1]
                    w.write(temp_line + "\n")
            else:
                for real, prediction in zip(test_y, predict_y_list):
                    w.write(str(real) + "," + str(prediction) + "\n")

        (right_num_dict_temp, prediction_num_dict_temp, actual_num_dict_temp) = validation.validate(predict_y_list,
                                                                                                    test_y)

        if variables.if_display_single_validation_result:
            macro_f1_single = 0
            total_num_single = len(test_y)
            for subsidy in ["1000", "1500", "2000"]:
                right_num_single = right_num_dict_temp.get(subsidy, 0)
                prediction_num_single = prediction_num_dict_temp.get(subsidy, 0)
                actual_num_single = actual_num_dict_temp.get(subsidy, 0)
                if prediction_num_single == 0:
                    precise_single = 0
                else:
                    precise_single = float(right_num_single) / prediction_num_single

                recall_single = float(right_num_single) / actual_num_single

                if precise_single + recall_single != 0:
                    f1_single = (2 * precise_single * recall_single) / (precise_single + recall_single)
                else:
                    f1_single = 0
                macro_f1_single += float(actual_num_single) / total_num_single * f1_single

                print subsidy + "case :" + "     right_num: " + str(right_num_single) + "   prediction_num:  " + str(
                    prediction_num_single) + "   acture_num:" + str(
                    actual_num_single) + "    prcise: " + str(precise_single) + "   recall: " + str(
                    recall_single) + "    f1: " + str(
                    f1_single)

            print "macro F1:" + str(macro_f1_single)

        for subsidy in ["1000", "1500", "2000"]:
            right_num_dict[subsidy] += right_num_dict_temp.get(subsidy, 0)
            prediction_num_dict[subsidy] += prediction_num_dict_temp.get(subsidy, 0)
            actual_num_dict[subsidy] += actual_num_dict_temp.get(subsidy, 0)

        end = time.time()

        print "one cv done  time: " + str(end - start)

    for subsidy in ["1000", "1500", "2000"]:
        right_num = right_num_dict.get(subsidy, 0)
        prediction_num = prediction_num_dict.get(subsidy, 0)
        actual_num = actual_num_dict.get(subsidy, 0)

        if prediction_num == 0:
            precise = 0
        else:
            precise = float(right_num) / prediction_num

        recall = float(right_num) / actual_num

        if precise + recall != 0:
            f1 = (2 * precise * recall) / (precise + recall)
        else:
            f1 = 0

        weighted_f1 = float(actual_num) / total_num * f1

        avg_macro_f1 += weighted_f1

        if variables.if_validation_detail:
            print subsidy + "case :" + "     right_num: " + str(right_num) + "   prediction_num:  " + str(
                prediction_num) + "   acture_num:" + str(
                actual_num) + "    prcise: " + str(precise) + "   recall: " + str(recall) + "    f1: " + str(
                f1) + "   weighted_f1:  " + str(weighted_f1)

    print "avg macro F1:" + str(avg_macro_f1)

    if variables.if_write_cv_prediction:
        w.close()

    return avg_macro_f1


learning_model = "et"

# variables.learning_rate_xgb = float(sys.argv[1])
# print "learning_rate_xgb= " + str(variables.learning_rate_xgb)

# try different parameter settings
cv_file_list = []

for i in range(variables.cv_num):
    cv_file_list.append(variables.root_loc + "cv_fold_" + str(i) + ".txt")

# single
start = time.time()
run_model(cv_file_list, learning_model)
end = time.time()
print "time:" + str(end - start)

# for i in range(10):
#     for j in range(10):
#         for k in range(10):
#             tree_num = 100 + i * 200
#             select_rate = 0.01 + 0.01 * j
#             max_depth = 1 + k
#             variables.select_rate = select_rate
#             print "select_rate = " + str(select_rate) +"select_rate = " + str(select_rate)+"select_rate = " + str(select_rate) + " --------------------------------------"
#             run_model(cv_file_list)


# for i in range(1, 10):
#     variables.n_estimators_xgb = i * 50
#     print "learning_rate= " + str(variables.learning_rate_xgb) + "  n_estimators_xgb= " + str(
#         variables.n_estimators_xgb) + "--------------------"
#     start = time.time()
#     run_model(cv_file_list, learning_model)
#     end = time.time()
#     print "time:" + str(end - start)
