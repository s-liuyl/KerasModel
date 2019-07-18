import sys
import os
import numpy as np
import collections
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
clusterQAInfo = [0]*5
for i in range(length):
	line = d[i]
	clusterQAModels.append(line[:line.rfind("\t")])
c = open(clusteredFile, 'r')
d = c.readlines()
c.close()
count = 0
clusteredModels = []
clusteredInfo = [0]*5
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
deepRankInfo = [0]*5

deep = open(deepRankFile, 'r')
d = deep.readlines()
deep.close()
for i in range(length):
        line = d[i]
	deepRankModels.append(line[:line.rfind("\t")])
SBRODModels = []
SBRODInfo = [0]*5
s = open(SBRODFile, 'r')
d = s.readlines()
s.close()
dict = {}
for l in d:
	line = l.split('\t')
	line[0] = line[0][line[0].rfind('/')+1:]
	if float(line[1]) in dict:
		dict[float(line[1])]= dict[float(line[1])] + [(line[0])]
	else:
		dict[float(line[1])]= [(line[0])]
sortedMods = collections.OrderedDict(sorted(dict.items()))
k = list(sortedMods.keys())
count = 0
for i in range(len(k)):
	key = k[len(sortedMods)-1-i]
	v = sortedMods[key]
	for m in v:
		SBRODModels.append(str(m))
		count +=1
		if count==5:
			break
	if count==5:
		break
QprobModels = []
QprobInfo = [0]*5
q = open(QprobFile,'r')
d = q.readlines()
q.close()
for i in range(length):
        line = d[i]
	QprobModels.append(line[:line.rfind("\t")])
for l in data:
	try:
		num = (l[l.find('model_'):l.find('\t')])
        except:
                continue
	for i in range(len(clusterQAModels)):
		m = clusterQAModels[i]
		if m == num:
			clusterQAInfo[i] =l
	for i in range(len(clusteredModels)):
		m = clusteredModels[i]
		if m == num:
			clusteredInfo[i] =l
	for i in range(len(deepRankModels)):
		m = deepRankModels[i]
		if m == num:
			deepRankInfo[i] =l
	for i in range(len(SBRODModels)):
		m = SBRODModels[i]
		if m == num:
			SBRODInfo[i] = l
	for i in range(len(QprobModels)):
		m = QprobModels[i]
		if m == num:
			QprobInfo[i]=l
w = open(output, 'w')

w.write('Results::\nTop from top '+str(length)+' clusters')
clusteredgts = []
clusteredtm = []
for i in range(length):
	w.write('\n'+clusteredModels[i])
	line = clusteredInfo[i].split('\t')
	GTS = float(line[2])
	TM = float(line[3])
	w.write('\nGDT-TS = %.4f' %(GTS))
	w.write('\nTM-score = %.4f' %(TM))
	clusteredgts.append(GTS)
	clusteredtm.append(TM)

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
        w.write('\nGDT-TS = %.4f' %(GTS))
        w.write('\nTM-score = %.4f' %(TM))
	clusterQAgts.append(float('%.4f' %(GTS)))
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
        w.write('\nGDT-TS = %.4f' %(GTS))
        w.write('\nTM-score = %.4f' %(TM))
	deepRankgts.append(float('%.4f' %(GTS)))
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
        w.write('\nGDT-TS = %.4f' %(GTS))
        w.write('\nTM-score = %.4f' %(TM))
        Qprobgts.append(float('%.4f' %(GTS)))
	Qprobtm.append(float('%.4f' %(TM)))
w.write('\n\nAverage GDT-TS = '+str(np.mean(np.asarray(Qprobgts))))
w.write('\nAverage TM-score = '+str(np.mean(np.asarray(Qprobtm))))

SBRODgts = []
SBRODtm = []
w.write("\n\nTop "+ str(length) + " SBROD")
for i in range(length):
	w.write('\n'+SBRODModels[i])
	line = SBRODInfo[i].split('\t')
	GTS = float(line[2])
        TM = float(line[3])
	w.write('\nGDT-TS = %.4f' %(GTS))
        w.write('\nTM-score = %.4f' %(TM))
	SBRODgts.append(float('%.4f' %(GTS)))
	SBRODtm.append(float('%.4f' %(TM)))
w.write('\n\nAverage GDT-TS = '+str(np.mean(np.asarray(SBRODgts))))
w.write('\nAverage TM-score = '+str(np.mean(np.asarray(SBRODtm))))





	
