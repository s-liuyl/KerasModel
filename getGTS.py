import sys
import os
file = sys.argv[1]
pre = sys.argv[2]
actualPDB = sys.argv[3]
kerasFile = sys.argv[4]
clusteredFile = sys.argv[5]
log = sys.argv[6]
output = sys.argv[7]
if len(sys.argv)==9:
	length = sys.argv[8]
else:
	length = 5
if '.'in file:
	file = file[:file.rfind('.')]
file +=' '
pre = ' '+ pre
o = open(kerasFile, 'r')
d = o.readlines()
o.close()
if pre.rfind('/') != len(pre) -1:
	pre+='/'
w = open(output, 'a+')
w.write("Top "+length+" ClusterQA")
op = open(log, 'r')
for i in range(length):
	line = d[i]
	w.write(line[:line.rfind("\\")]+'\n')
	os.system(file  +actualPDB + pre+ line[:line.rfind("\\")])
	all = op.read()
	w.write(all[all.rfind('GDT-TS'):all.rfind('GDT-TS') + 50]+'\n')
o = open(clusteredFile, 'r')
d = o.readlines()
o.close()
count = 0
w.write('\nTop from top '+length+' clusters')
for i   in range(len(d)):
	if 'Item' in d[i]:
		count +=1
		line = d[i+1]
		w.write(line[line.rfind('m'):line.rfind("\\")] +'\n')
		os.system(file  +actualPDB + pre+ line[line.rfind('m'):line.rfind("\\")])
		all = op.read()
		w.write(all[all.rfind('GDT-TS'):all.rfind('GDT-TS') + 50]+'\n')
	if count ==length:
		op.close()
		break
o = open(log , 'r')
d = o.readlines()
o.close()
count = 0
print("Top "+length+" ClusterQA")
for line in d:
	if 'GDT-TS' in line:
		count+= 1
		print(line)
	if count ==length:
		count+=1
		print("Top from top "+length+" clusters")
