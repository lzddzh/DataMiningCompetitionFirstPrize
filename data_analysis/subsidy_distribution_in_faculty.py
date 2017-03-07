root_loc = "/Users/mac/Documents/contest/a_data/data_backup/raw_data/train/"
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
    faculty = int(temps[1])
    subsidy = subsidy_dict[id]
    if not faculty_dict.has_key(faculty):
        faculty_dict[faculty] = {}
    if not faculty_dict[faculty].has_key(subsidy):
        faculty_dict[faculty][subsidy] = 0
    faculty_dict[faculty][subsidy] += 1

for key, value in faculty_dict.items():
    output = ""
    output += "faculty " + str(key) + " : "
    for i in [0, 1000, 1500, 2000]:
        output += str(value.get(i, 0)) + " "
    print output

