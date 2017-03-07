from commons import *
from learning_algorithm import *

training_file_loc = "../original_data/training_set_blending.txt"
test_file_loc = "../original_data/test_set_blending.txt"
output_file_loc = "../original_data/prediction.csv"

x = []
y = []
test_ids = []
test_x = []
prediction = []

#tools.read_blending_data_with_label([training_file_loc], x, y)
tools.read_blending_data_without_label([test_file_loc], test_x, test_ids)

prediction_list = vote_blending.learn(test_x)

tools.get_subsidy_distribution(prediction_list)

w = open(output_file_loc, 'w')
w.write("studentid,subsidy\n")
for id, prediction in zip(test_ids, prediction_list):
    # if int(id) > 22300:
    #     prediction = 0
    w.write(str(id) + "," + str(prediction) + "\n")
w.close()
