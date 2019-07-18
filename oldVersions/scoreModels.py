import sys
import numpy as np
import matplotlib 
matplotlib.use('Agg')
import  matplotlib.pyplot as plt
import collections 
inputfile = sys.argv[1]
r = open(inputfile, 'r')
data = r.readlines()
r.close()
gts = []
tm = []
GTSdict = {}
TMdict = {}
for l in data:
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
gts = np.asarray(gts)
tm = np.asarray(tm)
writeFile = sys.argv[2]
name = sys.argv[3]
resFolder = sys.argv[4]
if resFolder.rfind('/') !=len(resFolder)-1:
	resFolder = resFolder+'/'
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
plt.cla()
plt.figure()
plt.plot(GTSx,GTSy,'r')
plt.savefig(resFolder+name+'GTS.png', format = 'png')

plt.cla()
plt.figure()
plt.plot(TMx,TMy,'r')
plt.savefig(resFolder+name+'TM.png', format = 'png')
