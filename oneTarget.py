#################################################
#						#
#	oneTarget.py				#
#						#
#	This file takes in two required 	#
#	arguments: the template dataset	file 	#
#	and the ALL_scores folder.		#
#						#
#	This file can take in an optional 	#	
#	argument: the resulting .txt file 	#	
#	name.					#
#						#
#	This file creates the .txt file for 	#
#	one target using the information in 	#
#	its ALL_scores folder. It will format	#	
#	the file and order the features 	#
#	according to the dataset file that is	# 
#	provided.				#
#						#
#################################################

import numpy
import sys
import math
import glob
trainingSet = sys.argv[1]
targetFolder = sys.argv[2]
f = open(trainingSet, 'r')
d = f.readlines()
f.close()

featNames = d[0].split(' ')
files = glob.glob(targetFolder + '*')
if len(sys.argv) ==4:
        targetFileName = sys.argv[3]
else:
        targetFileName = files[0][files[0].rfind('.')+1:]+'.txt'
if targetFolder.rfind('/') != len(targetFolder)-1:
        targetFolder = targetFolder+'/'
files = glob.glob(targetFolder + '*')
dict = {}
tar = files[0][files[0].rfind('.')+1:]
for i in range(len(featNames)):
	if 'LGA' in featNames[i]:
		featNames[i] = 'LGA_score'
	else:
		s = featNames[i]
		if '\n' in s:
			s = s[:s.rfind('\n')]
		featNames[i] = s[s.rfind(':')+1:]
dict = {}
thisFeatNames = []
for i in files:
	feature = i[i.rfind('/')+1:i.rfind('.')]
	if feature.rfind('.') != -1:
		continue
	thisFeatNames.append(feature)
	r = open(i, 'r')
	data = r.readlines()
	r.close()
	scores = []
	for line in data:
		if 'END' in line:
			break
		if '\t' in line:
        		x = line.split('\t')
		else:
			x = line.split(' ')
		x[1] = (x[1])[:(x[1]).rfind('\n')]
		if '/' in x[0]:
                        x[0] = (x[0])[x[0].rfind('/')+1:]
		scores.append(x)
	for score in scores:
		model = score[0]
		if '/'in model:
			model = model[model.rfind('/')+1:]
		try:
			float(score[1])
			sc = score[1]
		except:
			continue
		if model in dict:
			dict[model] = dict[model] + [sc]
		else:
			dict[model] = [sc]
origToThisInd = [50]*len(featNames)
writer = open(targetFileName, 'a+')
thisLGA = float('inf')
existsLGA = False
origToThisInd = [50]*len(featNames)
for i in range(len(featNames)):
	if "LGA" in featNames[i]:
		thisLGA = i
	for j in range(len(thisFeatNames)):
                if "LGA" in thisFeatNames[j]:
			existsLGA = True
		if thisFeatNames[j] == featNames[i]:
                        origToThisInd[i] = j
			break
w = open(targetFileName, 'w')
w.write(d[0])
w.close()

for k in dict.keys():
	fs = dict[k]
	if len(fs) ==1:
		continue	
	if existsLGA:
		writer.write(fs[thisLGA]+' ')
	else:
		writer.write("0 ")
	for i in range(len(featNames)):
		if thisLGA == i:
			continue
		elif origToThisInd[i] == 50:
			
			if (i > thisLGA):
				writer.write(str(i)+":0 ")
			else:
				writer.write(str(i+1) + ":0 ")
        	elif i > thisLGA:
                	writer.write(str(i)+":"+fs[origToThisInd[i]]+' ')
		else:
                	writer.write(str(i+1)+":"+fs[origToThisInd[i]]+' ')
	writer.write('#'+tar+':'+k)
	writer.write('\n')
writer.close()
