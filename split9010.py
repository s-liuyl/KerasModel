import sys
import numpy
inputFile = sys.argv[1]
filename = inputFile[:inputFile.rfind('.')]
#load dataset
f = open(inputFile, 'r')
data = f.readlines()
f.close()
 
#determine indices of different sequences
line = data[1]
firstID = line[line.rfind(' ')+2:line.rfind(':')]
dict = {firstID:[1]}
for i in range (2,len(data)):
        line = data[i]
	if 'LGA' in line:
		continue
        id = line[line.rfind(' ')+2:line.rfind(':')]
        if id in dict:
                dict[id] = dict[id] + [i]
        else:
		dict[id] = [i]
 
k = dict.keys()
cutoff = int(0.9*len(k))
write90 = open(filename + '_first90.txt', 'w')
write90.write(data[0])
for target in range(cutoff):
	ID = k[target]
        for index in range(len(dict[ID])):
                i = dict[ID][index]
		write90.write(data[i])
 
write90.close()
write10 = open(filename + '_last10.txt', 'w')
write10.write(data[0])
for target in range(cutoff, len(k)):
        ID = k[target]
        for index in range(len(dict[ID])):
                i = dict[ID][index]
                write10.write(data[i])
write10.close()
