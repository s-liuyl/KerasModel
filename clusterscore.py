import sys
import numpy as np
import matplotlib 
matplotlib.use('Agg')
import  matplotlib.pyplot as plt
import collections 
import glob
inputfile = sys.argv[1]
writeFile = sys.argv[2]
name = sys.argv[3]
resFolder = sys.argv[4]
clusteredModels = sys.argv[5]
if resFolder.rfind('/') !=len(resFolder)-1:
        resFolder = resFolder+'/'
if clusteredModels.rfind('/') != len(resFolder)-1:
        clusteredModels += '/'
clusteredModels +='*'
r = open(inputfile, 'r')
data = r.readlines()
r.close()
gts = []
tm = []
GTSdict = {}
TMdict = {}
m = glob.glob(clusteredModels)
models = []
count = 0
for i in m:
	
	models.append(int(i[1+i.rfind('_'):]))
models = sorted(models)
def inArrBinarySearch(arr,l,r,x):
	mid = (r+l)/2
	if r < l :
		return False
	if arr[mid] == x:
		return True
	if arr[mid]>x:
		return inArrBinarySearch(arr, l, mid-1,x) 
	return inArrBinarySearch(arr, mid+1, r, x)
numModels = len(models)
for l in data:
	try:
		num = int(l[l.rfind('_')+1:l.find('\t')])
		if inArrBinarySearch(models, 0, numModels-1, num):
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
plt.cla()
plt.figure()
plt.plot(GTSx,GTSy,'r')
plt.savefig(resFolder+name+'GTS.png', format = 'png')

plt.cla()
plt.figure()
plt.plot(TMx,TMy,'r')
plt.savefig(resFolder+name+'TM.png', format = 'png')

print(count)
