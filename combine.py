import sys
import glob

# Usage: python program.py directory output_filename
# main
directory = str(sys.argv[1])
outfile = open(str(sys.argv[2]), 'w')

mylist = glob.glob(directory + '/part*')
for file_name in sorted(mylist):
    infile = open(file_name, 'r')
    lines = infile.readlines()
    for line in lines:
        outfile.write(line)
    infile.close()

outfile.close()
