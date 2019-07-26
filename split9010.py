#######################################################################
#                                                                     #
#	split9010.py                                                  #
#                                                                     #
#       This code splits a dataset into two files: one with the       #
#	first 90% of targets and one with the last 10% of targets.    #
#                                                                     #
#	This code requires 1 arguments: the dataset file              #
#	and the directory to save the model.                          #
#                                                                     #
#	These will be saved in one .txt file with the first 90%       #
#	of targets and one .txt file with the last 10% of targets.    #
#                                                                     #
#######################################################################
import sys
import numpy
dataFile = sys.argv[1]
filename = dataFile[:dataFile.rfind('.')]
#load dataset
f = open(dataFile, 'r')
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
