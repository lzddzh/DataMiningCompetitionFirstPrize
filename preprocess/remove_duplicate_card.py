root_loc = "/Users/mac/Documents/contest/data/original_data/card_train_invert.txt"
output_loc = "/Users/mac/Documents/contest/data/original_data/card_train_inverted_cleaned.txt"
w = open(output_loc, "w")

lines = open(root_loc).readlines()
count = 0
for line in lines:
    print count
    count += 1
    temps = line.strip("\n").split('$');
    output_line = temps[0] + "$"
    record_list = []
    for i in range(1, len(temps)):
        if temps[i] not in record_list:
            record_list.append(temps[i])
            output_line += temps[i] + "$"
    output_line = output_line[0:-1]
    w.write(output_line + "\n")
w.close()
