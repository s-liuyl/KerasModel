import sys
if len(sys.argv) != 2:
	print("The parameter is not correct!")
	exit(-1)


inputfile = sys.argv[1]

f = open(inputfile,'r')
dataset = f.readlines()
f.close


for line in dataset:
	if '#LGA' not in line:
		continue
	print(line)
