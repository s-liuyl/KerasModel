import sys
import numpy as np
import matplotlib 
matplotlib.use('Agg')
import  matplotlib.pyplot as plt
import collections 
inputfile = sys.argv[1]
writeFile = sys.argv[2]
name = sys.argv[3]
resFolder = sys.argv[4]
gtsScores = sys.argv[5]
tmScores = sys.argv[6]
if resFolder.rfind('/') !=len(resFolder)-1:
        resFolder = resFolder+'/'
r = open(inputfile, 'r')
data = r.readlines()
r.close()
gts = []
tm = []
GTSdict = {}
TMdict = {}
count = 0
for l in data:
	try:
		num = int(l[l.find('_')+1:l.find('\t')])
		count+=1
		line = l.split('\t')
		GTS = float(line[2])
		TM = float(line[3])
		GTStext = ("%.2f" %(GTS))
		TMtext = ("%.4f" %(TM))
		tm.append(TM)
		gts.append(GTS)
		if GTStext in GTSdict:
			GTSdict[GTStext] = GTSdict[GTStext]+1
		else:
			GTSdict[GTStext] = 1
		if TMtext in TMdict:
			TMdict[TMtext] = TMdict[TMtext] + 1
		else:
			TMdict[TMtext] = 1
	except:
		continue
gts = np.asarray(gts)
tm = np.asarray(tm)
w = open(writeFile, 'a+')
w.write(name+'\n')
w.write("GTS - minimum: "+ str(np.amin(gts)) + " maximum: "+str(np.amax(gts))+" average: "+ str(np.mean(gts)) )
w.write("\nTM - minimum: "+ str(np.amin(tm)) + " maximum: "+str(np.amax(tm))+" average: "+ str(np.mean(tm))+'\n' )
w.close()
GTSx = []
GTSy = []
GTSod = collections.OrderedDict(sorted(GTSdict.items()))
for k, v in GTSod.iteritems():
	GTSy.append(v)
	GTSx.append(float(k))
TMx = []
TMy = []
TMod = collections.OrderedDict(sorted(TMdict.items()))
for k, v in TMod.iteritems():
	TMy.append(v)
        TMx.append(float(k))
colors = ['m',  'g','c', 'b', 'y', 'k', ]
gtsScores = gtsScores.split(',')
plt.cla()
plt.figure()
plt.xlabel('GDT-TS score')
plt.ylabel('frequency')
for i in range(len(gtsScores)):
	plt.axvline(x=float(gtsScores[i]),color = colors[i])
plt.plot(GTSx,GTSy,'r')
plt.savefig(resFolder+name+'GTS.png', format = 'png')
tmScores = tmScores.split(',')
plt.cla()
plt.figure()
for i in range(len(tmScores)):
        plt.axvline(x=float(tmScores[i]),color = colors[i])
plt.xlabel('GDT-TM score')
plt.ylabel('frequency')
plt.plot(TMx,TMy,'r')
plt.savefig(resFolder+name+'TM.png', format = 'png')

print(count)
