import numpy
import sys
import math
import glob
trainingSet = sys.argv[1]
targetsFolder = sys.argv[2]
f = open(trainingSet, 'r')
d = f.readlines()
f.close()
if targetsFolder.rfind('/') != len(targetsFolder)-1:
	targetsFolder = targetsFolder+'/'

targets = glob.glob(targetsFolder+"*")
targetFolder = targets[0]+'/ALL_scores/'
if len(sys.argv) ==4:
	targetFileName = sys.argv[3]
else:
	targetFileName = 'dataset.txt'
if targetFolder.rfind('/') != len(targetFolder)-1:
	targetFolder = targetFolder+'/'
files = glob.glob(targetFolder + '*')
dict = {}
featNames = d[0].split(' ') 
writer = open(targetFileName, 'w')
writer.write(d[0])
writer.close()
for i in range(len(featNames)):
	if 'LGA' in featNames[i]:
		featNames[i] = 'LGA_score'
	else:
		s = featNames[i]
		if '\n' in s:
			s = s[:s.rfind('\n')]
		featNames[i] = s[s.rfind(':')+1:]

for t in targets:
	targetFolder = t+'/ALL_scores/'
        tar = t[t.rfind('/')+1:]
        if targetFolder.rfind('/') != len(targetFolder)-1:
                targetFolder = targetFolder+'/'
        files = glob.glob(targetFolder + '*')
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
        writer = open(targetFileName, 'a+')
	thisLGA = float('inf')
        origToThisInd = [50]*len(featNames)
	
	for i in range(len(featNames)):
                for j in range(len(thisFeatNames)):
			if "LGA" in thisFeatNames[j]:
				thisLGA = j

                        if thisFeatNames[j] == featNames[i]:
                                origToThisInd[i] = j
                                break
	for k in dict.keys():
                thisKeyFs = dict[k]
		if len(thisKeyFs) >= len(featNames):
			writer.write(thisKeyFs[thisLGA]+' ')
			for i in range(len(featNames)):
				if i == thisLGA:
					continue
				elif i > thisLGA:
					writer.write(str(i)+":"+thisKeyFs[origToThisInd[i]]+' ')
				else:
					writer.write(str(i+1)+":"+thisKeyFs[origToThisInd[i]]+' ')
			writer.write('#'+ tar + ':'+k)
               		writer.write('\n')
        writer.close()



