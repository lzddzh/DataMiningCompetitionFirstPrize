root_loc = "/Users/mac/Documents/contest/data/original_data/"
file_name = "subsidy_train.txt"
count_0 = 0
count_1000 = 0
count_1500 = 0
count_2000 = 0
lines = open(root_loc + file_name).readlines()
for line in lines:
    temps = line.strip("\n").split(",")
    subsidy = int(temps[1])
    if subsidy == 0:
        count_0 += 1
    if subsidy == 1000:
        count_1000 += 1
    if subsidy == 1500:
        count_1500 += 1
    if subsidy == 2000:
        count_2000 += 1
print (str(count_0)+"\n"+str(count_1000)+"\n"+str(count_1500)+"\n"+str(count_2000))

print count_0+count_1000+count_1500+count_2000