import sys
file_loc = sys.argv[1] 
output_loc = sys.argv[2]
w = open(output_loc, 'w')
lines = open(file_loc).readlines()

for line in lines:
    output_line = "ID:" + line
    w.write(output_line)
w.close()
