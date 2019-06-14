import sys
import numpy
inputFile = sys.argv[1]
filename = inputFile[:inputFile.rfind('.')]
#load dataset
f = open(inputFile, 'r')
data = f.readlines()
f.close()
dataset = []
for line in data:
        if '#LGA' in line:
		continue
        dataset.append(line.split(' '))
 
write10 = open(filename + '_last10.txt', 'w')
write90 = open(filename + '_first90.txt', 'w')
write10.write(data[0])
write90.write(data[0])
#determine indices of different sequences
features = len(dataset[0])-2
firstS = dataset[0][features+1]
firstID = firstS[1:firstS.index(":")]
dict = {firstID:[0]}
for i in range (0,len(dataset)):
        s = dataset[i][features+1]
        id = s[1:(s.index(":"))]
        if id in dict:
                dict[id] = dict[id] + [i]
        else:
                dict[id] = [i]
for ID in dict:
        cutoff = int(0.9*len(dict[ID]))
        for index in range(len(dict[ID])):
                i = dict[ID][index]
		if index >= cutoff:
			print(data[i][data[i].rfind('#')+1:])
			write10.write(data[i])
		else:
			write90.write(data[i])


