root_loc = "/Users/mac/Documents/contest/data/original_data/"
subsidy_file = "subsidy_train.txt"
score_file = "score_train.txt"

subsidy_dict = {}

lines = open(root_loc + subsidy_file).readlines()
for line in lines:
    temps = line.strip("\n").split(",")
    id = int(temps[0])
    subsidy = int(temps[1])
    subsidy_dict[id] = subsidy

count500 = 0
count1000 = 0
count1500 = 0
count2000 = 0
count2500 = 0
count3000 = 0

count500_s = 0
count1000_s = 0
count1500_s = 0
count2000_s = 0
count2500_s = 0
count3000_s = 0
school = []
school_s=[]
for i in range(20):
    school.append(0)
    school_s.append(0)

lines = open(root_loc + score_file).readlines()
for line in lines:
    temps = line.strip("\n").split(",")
    id = int(temps[0])
    rank = int(temps[2])
    school_id=int(temps[1])
    school[school_id]+=1
    if subsidy_dict[id] != 0:
        school_s[school_id] += 1

    if 0 < rank <= 500:
        count500 += 1
        if subsidy_dict[id] != 0:
            count500_s += 1
    if 500 < rank <= 1000:
        count1000 += 1
        if subsidy_dict[id] != 0:
            count1000_s += 1
    if 1000 < rank <= 1500:
        count1500 += 1
        if subsidy_dict[id] != 0:
            count1500_s += 1
    if 1500 < rank <= 2000:
        count2000 += 1
        if subsidy_dict[id] != 0:
            count2000_s += 1
    if 2000 < rank <= 2500:
        count2500 += 1
        if subsidy_dict[id] != 0:
            count2500_s += 1
    if 2500 < rank <= 3000:
        count3000 += 1
        if subsidy_dict[id] != 0:
            count3000_s += 1

print str(count500) + " " + str(count500_s) + " " + str(float(count500_s) / count500)
print str(count1000) + " " + str(count1000_s) + " " + str(float(count1000_s) / count1000)
print str(count1500) + " " + str(count1500_s) + " " + str(float(count1500_s) / count1500)
print str(count2000) + " " + str(count2000_s) + " " + str(float(count2000_s) / count2000)
print str(count2500) + " " + str(count2500_s) + " " + str(float(count2500_s) / count2500)
print str(count3000) + " " + str(count3000_s) + " " + str(float(count3000_s) / count3000)


for i in range(1,20):
    print str(i)+ " "+str(school[i])+" "+str(school_s[i])+" "+str(100*float(school_s[i])/school[i])