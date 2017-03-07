import sys

sys.path.append("../")
from commons import *
from learning_algorithm import *

learning_model = "et"

# variables.random_seed = int(sys.argv[1])
# print "random_seed= " + str(variables.random_seed)

training_file_loc = "../original_data/training_examples.txt"
test_file_loc = "../original_data/idexamples_test.txt"

if variables.prob_mode:
    output_file_loc = "../original_data/et_prediction/prediction_with_prob_" + learning_model + "_seed_" + str(
        variables.random_seed) + ".csv"
else:
    output_file_loc = "../original_data/et_prediction/prediction_with_class_" + learning_model + "_seed_" + str(
        variables.random_seed) + ".csv"


x = []
y = []
test_ids = []
test_x = []
prediction = []

tools.read_data_with_label([training_file_loc], x, y, None, None)
tools.read_data_without_label([test_file_loc], test_x, test_ids)

if learning_model == "gdbt":
    prediction_list, prediction_list_prob = gradient_boosting.learn(x, y, test_x)
elif learning_model == "svm":
    prediction_list, prediction_list_prob = support_vector_machine.learn(x, y, test_x)
elif learning_model == "ada":
    prediction_list, prediction_list_prob = ada_boosting.learn(x, y, test_x)
elif learning_model == "nn":
    prediction_list, prediction_list_prob = neural_network.learn(x, y, test_x)
elif learning_model == "xgb":
    prediction_list, prediction_list_prob = xgboosting.learn(x, y, test_x)
elif learning_model == "et":
    prediction_list, prediction_list_prob = extra_trees.learn(x, y, test_x)
elif learning_model == "rf":
    prediction_list, prediction_list_prob = random_forest.learn(x, y, test_x)

tools.get_subsidy_distribution(prediction_list)

if variables.prob_mode:
    w = open(output_file_loc, 'w')
    w.write("studentid,0,1000,1500,2000\n")
    for id, prediction_prob in zip(test_ids, prediction_list_prob):
        temp_line = ""
        temp_line += str(id) + ","
        for prob in prediction_prob:
            temp_line += str(prob) + ","
        temp_line = temp_line[:-1]
        w.write(temp_line + "\n")
    w.close()

else:
    w = open(output_file_loc, 'w')
    w.write("studentid,subsidy\n")
    for id, prediction in zip(test_ids, prediction_list):
        if int(id) >= 22300:
            prediction = 0
        w.write(str(id) + "," + str(prediction) + "\n")
    w.close()


