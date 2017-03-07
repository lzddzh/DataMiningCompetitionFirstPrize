root_loc = "/Users/mac/Documents/contest/data/original_data/"
dorm_file = "dorm_train.txt"

stu_id=5555
output_loc="/Users/mac/Documents/contest/data/distribution/dorm_"+str(stu_id)+".txt"
w=open(output_loc,'w')

lines = open(root_loc + dorm_file).readlines()
for line in lines:
    temps = line.strip("\n").split(",")
    id = int(temps[0])
    time = temps[1]
    date = time.split(" ")[0]
    if id==stu_id:
        w.write(line)

w.close()
