#######################################################################
#                                                                     #
#	calculateAverage.py                                           #
#                                                                     #
#	This file calculates the average GDT-TS and TM scores for     #
#	different methods. 					      #
#								      #
#	This file takes in one argument: the file created from 	      #
#	compareMethods.py					      #
#                                                                     #
#######################################################################



import sys
import numpy as np
folder = sys.argv[1]
if folder.rfind('/')!=len(folder)-1:
	folder +='/'
folder +='*'
import glob
if len(sys.argv)==3:
	output = sys.argv[2]
files = glob.glob(folder)
clusteredGTS = []
clusteredTM = []
clusterQAGTS = []
clusterQATM = []
deepRankGTS = []
deepRankTM = []
QprobGTS = []
QprobTM = []
SBRODGTS = []
SBRODTM = []
for f in files:
	o = open(f,'r')
	d = o.readlines()
	o.close()
	count = 0
	for i in range(len(d)):
		if 'Top' in d[i]:
			if count ==0:
				clusgts = []
				count+=1
				l = [d[i+2],d[i+5],d[i+8],d[i+11],d[i+14]]
				for line in l:
					clusgts.append(float(line[line.rfind('=')+2:]))
                                clusteredGTS.append(np.amax(np.asarray(clusgts)))
				l = [d[i+3],d[i+6],d[i+9],d[i+12],d[i+15]]
				clustm = []
				for line in l:
					clustm.append(float(line[line.rfind('=')+2:]))
				clusteredTM.append(np.amax(np.asarray(clustm)))
			elif count==1:
				count+=1
                                clusterQAGTS.append(float(d[i+2][d[i+2].rfind('=')+2:]))
                                clusterQATM.append(float(d[i+3][d[i+3].rfind('=')+2:]))
			elif count==2:
                                count+=1
                                deepRankGTS.append(float(d[i+2][d[i+2].rfind('=')+2:]))
                                deepRankTM.append(float(d[i+3][d[i+3].rfind('=')+2:]))
			elif count==3:
                                count+=1
                                QprobGTS.append(float(d[i+2][d[i+2].rfind('=')+2:]))
                                QprobTM.append(float(d[i+3][d[i+3].rfind('=')+2:]))
			elif count ==4:
				count+=1
				SBRODGTS.append(float(d[i+2][d[i+2].rfind('=')+2:]))
				SBRODTM.append(float(d[i+3][d[i+3].rfind('=')+2:]))	
			else:
				break
clusgts = np.asarray(clusteredGTS)
clustm = np.asarray(clusteredTM)
cqagts = np.asarray(clusterQAGTS)
cqatm = np.asarray(clusterQATM)
drgts = np.asarray(deepRankGTS)
drtm = np.asarray(deepRankTM)
qgts = np.asarray(QprobGTS)
qtm = np.asarray(QprobTM)
sbgts = np.asarray(SBRODGTS)
sbtm = np.asarray(SBRODTM)
if len(sys.argv)==3:
	w = open(output, 'w')
	w.write("Clustered Averages: GDT-TS = "+ str(np.mean(clusgts))+ ", TM-score = "+ str(np.mean(clustm))+'\n\n')
	w.write("ClusterQA Averages: GDT-TS = "+ str(np.mean(cqagts))+ ", TM-score = "+ str(np.mean(cqatm))+'\n\n')
	w.write("DeepRank Averages: GDT-TS = "+ str(np.mean(drgts))+ ", TM-score = "+ str(np.mean(drtm))+'\n\n')
	w.write("Qprob Averages: GDT-TS = "+ str(np.mean(qgts))+ ", TM-score = "+ str(np.mean(qtm))+'\n\n')
	w.write("SBROD Averages: GDT-TS = "+ str(np.mean(sbgts))+", TM-score = "+ str(np.mean(sbtm))+'\n\n')
	w.close()
print("Clustered Averages: GDT-TS = "+ str(np.mean(clusgts))+ ", TM-score = "+ str(np.mean(clustm)))
print
print("ClusterQA Averages: GDT-TS = "+ str(np.mean(cqagts))+ ", TM-score = "+ str(np.mean(cqatm)))
print
print("DeepRank Averages: GDT-TS = "+ str(np.mean(drgts))+ ", TM-score = "+ str(np.mean(drtm)))
print											
print("Qprob Averages: GDT-TS = "+ str(np.mean(qgts))+ ", TM-score = "+ str(np.mean(qtm)))
print
print("SBROD Averages: GDT-TS = "+ str(np.mean(sbgts))+", TM-score = "+ str(np.mean(sbtm)))
