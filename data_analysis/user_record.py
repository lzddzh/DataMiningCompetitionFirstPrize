file_loc = "/Users/mac/Documents/contest/data/original_data/score_train.txt"
user_id_set=set()
lines = open(file_loc).readlines()
for line in lines:
    user_id_set.add(line.split(",")[0])
print len(user_id_set)

