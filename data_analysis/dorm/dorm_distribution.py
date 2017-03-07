root_loc = "/Users/mac/Documents/contest/data/original_data/"
dorm_file = "dorm_train.txt"


dorm_dict = {}
user_set=set()
id_greater_than_7500_set=set()

lines = open(root_loc + dorm_file).readlines()
for line in lines:
    temps = line.strip("\n").split(",")
    id = int(temps[0])
    time = temps[1]
    date = time.split(" ")[0]
    user_set.add(id)

    if id>22467:
        id_greater_than_7500_set.add(id)


    if dorm_dict.has_key(date):
        dorm_dict[date] += 1
    else:
        dorm_dict[date] = 0

dorm_dict_list = sorted(dorm_dict.iteritems(), key=lambda d: d[0], reverse=False)

for i in range(len(dorm_dict_list)):
    print str(dorm_dict_list[i])

print "user_num:"+str(len(user_set))
print "id_greater_than_7500_num:"+str(len(id_greater_than_7500_set))