feature_loc = "../original_data/idexamples_train_std.txt"
output_loc = "../original_data/training_examples.txt"
subsidy_file = "../original_data/subsidy_train.txt"
w = open(output_loc, 'w')

subsidy_dict = {}
lines = open(subsidy_file).readlines()
for line in lines:
    temps = line.strip("\n").strip("\r").split(",")
    id = temps[0].strip("\"")
    subsidy = temps[1].strip("\"")
    subsidy_dict[id] = subsidy

lines = open(feature_loc).readlines()
for line in lines:
    id = line.split(",")[0].split(":")[1]
    line_added = "subsidy:" + subsidy_dict[id] + "," + line
    w.write(line_added)

w.close()
