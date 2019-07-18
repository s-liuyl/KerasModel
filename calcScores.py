import sys
import os
import numpy as np
modelsInfo = sys.argv[1]
clusteredFile = sys.argv[2]
kerasFile = sys.argv[3]
deepRankFile = sys.argv[4]
SBRODFile = sys.argv[5]
QprobFile = sys.argv[6]
output = sys.argv[7]
if len(sys.argv)==9:
	length = int(sys.argv[8])
else:
	length = 5
k = open(kerasFile, 'r')
d = k.readlines()
k.close()
clusterQAModels = []
clusterQAInfo = []
for i in range(length):
	line = d[i]
	clusterQAModels.append(line[:line.rfind("\t")])
c = open(clusteredFile, 'r')
d = c.readlines()
c.close()
count = 0
clusteredModels = []
clusteredInfo = []
for i   in range(len(d)):
	if 'Item' in d[i]:
		count +=1
		line = d[i+1]
		clusteredModels.append(line[line.rfind('m'):line.rfind(" ")])
	if count ==length:
		break


o = open( modelsInfo, 'r')
data = o.readlines()
o.close()
deepRankModels = []
deepRankInfo = []

deep = open(deepRankFile, 'r')
d = deep.readlines()
deep.close()
for i in range(length):
        line = d[i]
	deepRankModels.append(line[:line.rfind("\t")])
SBRODModels = []
SBRODInfo = []
s = open(SBRODFile, 'r')
d = s.readlines()
s.close()
#for i in range(length):
#        line = d[i]
#	SBRODModels.append(line[:line.rfind("\t")])

QprobModels = []
QprobInfo = []
q = open(QprobFile,'r')
d = q.readlines()
q.close()
for i in range(length):
        line = d[i]
	QprobModels.append(line[:line.rfind("\t")])
#w.write("Top "+str(length)+" ClusterQA")
#w.write('\nTop from top '+str(length)+' clusters')
for l in data:
	try:
		num = (l[l.find('model_'):l.find('\t')])
        except:
                continue
	for m in clusterQAModels:
		if m == num:
			clusterQAInfo.append(l)
	for m in clusteredModels:
		if m == num:
			clusteredInfo.append(l)
	for m in deepRankModels:
		if m == num:
			deepRankInfo.append(l)
	for m in SBRODModels:
		if m == num:
			SBRODInfo.append(l)
	for m in QprobModels:
		if m == num:
			QprobInfo.append(l)
w = open(output, 'w')

w.write('Results::\nTop from top '+str(length)+' clusters\n')
clusteredgts = []
clusteredtm = []
for i in range(length):
	w.write('\n'+clusteredModels[i])
	line = clusteredInfo[i].split('\t')
	GTS = float(line[2])
	TM = float(line[3])
	w.write('\nGDT-TS = %.4f' %(GTS))
	w.write('\nTM-score = %.4f' %(TM))
	clusteredgts.append(float('%.2f' %(GTS)))
	clusteredtm.append(float('%.4f' %(TM)))

w.write('\n\nAverage GDT-TS = '+str(np.mean(np.asarray(clusteredgts))))
w.write('\nAverage TM-score = '+str(np.mean(np.asarray(clusteredtm))))

w.write("\n\nTop "+str(length)+" ClusterQA")
clusterQAgts = []
clusterQAtm = []
for i in range(length):
        w.write('\n'+clusterQAModels[i])
	line = clusterQAInfo[i].split('\t')
	GTS = float(line[2])
        TM = float(line[3])
        w.write('\nGDT-TS = %.2f' %(GTS))
        w.write('\nTM-score = %.4f' %(TM))
	clusterQAgts.append(float('%.2f' %(GTS)))
        clusterQAtm.append(float('%.4f' %(TM)))
w.write('\n\nAverage GDT-TS = '+str(np.mean(np.asarray(clusterQAgts))))
w.write('\nAverage TM-score = '+str(np.mean(np.asarray(clusterQAtm))))

w.write("\n\nTop "+str(length)+" DeepRank")
deepRankgts = []
deepRanktm = []
for i in range(length):
	w.write('\n'+deepRankModels[i])
	line = deepRankInfo[i].split('\t')
        GTS = float(line[2])
        TM = float(line[3])
        w.write('\nGDT-TS = %.2f' %(GTS))
        w.write('\nTM-score = %.4f' %(TM))
	deepRankgts.append(float('%.2f' %(GTS)))
	deepRanktm.append(float('%.4f' %(TM)))
w.write('\n\nAverage GDT-TS = '+str(np.mean(np.asarray(deepRankgts))))
w.write('\nAverage TM-score = '+str(np.mean(np.asarray(deepRanktm))))
					
Qprobgts = []
Qprobtm = []
w.write("\n\nTop "+str(length)+" Qprob")
for i in range(length):
	w.write('\n'+QprobModels[i])
	line =  QprobInfo[i].split('\t')
	GTS = float(line[2])
        TM = float(line[3])
        w.write('\nGDT-TS = %.2f' %(GTS))
        w.write('\nTM-score = %.4f' %(TM))
        Qprobgts.append(float('%.2f' %(GTS)))
	Qprobtm.append(float('%.4f' %(TM)))
w.write('\n\nAverage GDT-TS = '+str(np.mean(np.asarray(Qprobgts))))
w.write('\nAverage TM-score = '+str(np.mean(np.asarray(Qprobtm))))
	
