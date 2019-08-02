#######################################################################
#                                                                     #
#	distribution.py				    		      #
#								      #
#	This file creates the distribution plots for all models of    #
#	a single target.					      #
#								      #
#	This file creates two .png files: one with the GDT-TS	      #
#	distribution and one with the TM distribution. It also 	      #
#	writes the minimum, maximum, and average GDT-TS and TM 	      #
#	scores onto a designated .txt file. 			      #
#								      #
#	This file takes 5 arguments: The complete model scores file,  #
#	the file to write the output, the name of the target protein, #
#	the results directory, and the file with the results from     #
#	compareMethods.py.					      #
#								      #
#######################################################################

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
scores = sys.argv[5]
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
		GTS = float(line[3])
		TM = float(line[2])
		GTStext = ("%.4f" %(GTS))
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
read = open(scores, 'r')
lines = read.readlines()
read.close()
gtsScores = []
tmScores = []
methods = []
methodNum = 0
for i in range(len(lines)):
	line = lines[i]
	if "Top" in line:
		methodNum +=1
		if methodNum != 1 and methodNum  != 2 and methodNum != 4:
			continue
		method = line[line.rfind(' '):]
		if 'clusters' in method:
			method = "Clustered"
                if '\n' in method:
                        method = method[:method.rfind('/')]		
 
		methods.append(method)
		gdt_ts = lines[i+2]	
		tm_score = lines[i+3]
		gtsScores.append(float(gdt_ts[gdt_ts.rfind('=')+2:]))
		tmScores.append(float(tm_score[tm_score.rfind('=')+2:]))
methods = ['Clustered','DeepCluster_QA','Qprob']
plt.cla()
plt.figure()
plt.title('GDT-TS Score distribution of unclustered data')
plt.xlabel('GDT-TS score')
plt.ylabel('frequency')
plt.xlim(0,1)
for i in range(len(gtsScores)):
	plt.axvline(x=float(gtsScores[i]),label = methods[i],color = colors[i])
plt.plot(GTSx,GTSy,'r')
plt.legend(loc='upper right')
plt.savefig(resFolder+name+'GTS.png', format = 'png')
plt.cla()
plt.figure()
for i in range(len(tmScores)):
        plt.axvline(x=float(tmScores[i]),color = colors[i], label = methods[i])
plt.xlabel('TM score')
plt.title('TM-Score distribution of unclustered data')
plt.ylabel('frequency')
plt.plot(TMx,TMy,'r')
plt.legend(loc='upper right')
plt.xlim(0,1)
plt.savefig(resFolder+name+'TM.png', format = 'png')

print(count)
