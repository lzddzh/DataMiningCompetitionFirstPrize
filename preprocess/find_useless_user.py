root_location = "/Users/mac/Documents/contest/data/original_data/"

card_user_ids = set()
dorm_user_ids = set()
score_user_ids = set()
library_user_ids = set()
borrow_user_ids = set()

non_subsidy_ids = set()
subsidy_ids = set()

lines = open(root_location + "subsidy_train.txt").readlines()
for line in lines:
    if line.strip("\r\n").split(",")[1] == "0":
        non_subsidy_ids.add(line.split(",")[0])
    else:
        subsidy_ids.add(line.split(",")[0])

lines = open(root_location + "card_train.txt").readlines()
for line in lines:
    card_user_ids.add(line.split(",")[0])

lines = open(root_location + "dorm_train.txt").readlines()
for line in lines:
    dorm_user_ids.add(line.split(",")[0])

lines = open(root_location + "score_train.txt").readlines()
for line in lines:
    score_user_ids.add(line.split(",")[0])

lines = open(root_location + "library_train.txt").readlines()
for line in lines:
    library_user_ids.add(line.split(",")[0])

lines = open(root_location + "borrow_train.txt").readlines()
for line in lines:
    borrow_user_ids.add(line.split(",")[0])

result = card_user_ids.intersection(dorm_user_ids).intersection(score_user_ids).intersection(
    library_user_ids).intersection(
    borrow_user_ids).intersection(non_subsidy_ids)

w = open(root_location + "negative_ids.txt", "w")

for id in result:
    w.write(id + "\n")
w.close()
