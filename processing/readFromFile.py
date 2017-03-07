import sys

# return the file on disk as a string.
def read(filePath):
    f = open(filePath)
    return f.read()

def readLines(filePath):
    f = open(filePath)
    return f.read().strip().split('\n')
    
if __name__=="__main__":
    if len(sys.argv) < 2:
        print "please follow the file name that you want to read when running this script."
    else:
        print read(sys.argv[1])[:1000] + "\n..."
