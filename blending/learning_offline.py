import sys

sys.path.append("../")
from commons import variables
from commons import tools
from commons import validation
from learning_algorithm import *
import time


def run_model():
    avg_macro_f1 = 0

    total_num = 10885
    right_num_dict = {}
    prediction_num_dict = {}
    actual_num_dict = {}

    for subsidy in ["1000", "1500", "2000"]:
        right_num_dict[subsidy] = 0
        prediction_num_dict[subsidy] = 0
        actual_num_dict[subsidy] = 0

    test_x = []
    test_y = []
    tools.read_blending_data_with_label([variables.root_loc + "training_set_blending.txt"], test_x, test_y)

    predict_y_list = vote_blending.learn(test_x)  # test_y

    (right_num_dict, prediction_num_dict, actual_num_dict) = validation.validate(predict_y_list,
                                                                                 test_y)

    # write_blending_result
    # w = open("../original_data/cv_prediction_with_class_gdbt_blending_seeds_2933.txt","w")
    # for real, prediction in zip(test_y, predict_y_list):
    #     w.write(str(real) + "," + str(prediction) + "\n")
    #w.close()


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


# variables.n_estimators_gdbt_b = int(sys.argv[1])
# print "n_estimators_gdbt_b= " + str(variables.n_estimators_gdbt_b)

# single
start = time.time()
run_model()
end = time.time()
print "time:" + str(end - start)


# for i in range(1, 10):
#     variables.min_samples_leaf_gdbt_b = i * 5
#     print "max_depth_gdbt_b= " + str(variables.max_depth_gdbt_b) + "  min_samples_leaf_gdbt_b= " + str(
#         variables.min_samples_leaf_gdbt_b) + "--------------------"
#     start = time.time()
#     run_model()
#     end = time.time()
#     print "time:" + str(end - start)
