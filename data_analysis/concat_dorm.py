root_loc = "/Users/mac/Documents/contest/data/original_data/"
subsidy_file = "subsidy_train.txt"
borrow_file = "score_train.txt"

output_loc = "/Users/mac/Documents/contest/data/distribution/score_concat.txt"

subsidy_dict = {}

w=open(output_loc,'w')

lines = open(root_loc + subsidy_file).readlines()
for line in lines:
    temps = line.strip("\n").split(",")
    id = int(temps[0])
    subsidy = int(temps[1])
    subsidy_dict[id] = subsidy

user_list=[]
lines = open(root_loc + borrow_file).readlines()
for line in lines:
    temps = line.strip("\n").split(",")
    id = int(temps[0])

    if subsidy_dict.has_key(id):
        subsidy = subsidy_dict[id]
        line=str(subsidy)+"--------"+line
    else:
        line="unknow--------"+line

    w.write(line)
w.close()
