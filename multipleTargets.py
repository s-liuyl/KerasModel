import numpy
import sys
import math
import glob
targetsFolder = sys.argv[1]
if targetsFolder.rfind('/') != len(targetsFolder)-1:
	targetsFolder = targetsFolder+'/'

targets = glob.glob(targetsFolder+"*")
targetFolder = targets[0]+'/ALL_scores/'
if len(sys.argv) ==3:
	targetFileName = sys.argv[2]+'.txt'
else:
	targetFileName = 'dataset.txt'
if targetFolder.rfind('/') != len(targetFolder)-1:
	targetFolder = targetFolder+'/'
files = glob.glob(targetFolder + '*')
dict = {}
featNames = []
for i in files:
	feature = i[i.rfind('/')+1:i.rfind('.')]
	if feature.rfind('.') != -1:
		continue
	featNames.append(feature)
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
writer = open(targetFileName, 'w')
writer.write('#LGA ')
LGA = float('inf')
for i in range(len(featNames)):
        if "LGA" in featNames[i]:
                LGA = i
        elif i > LGA:
		writer.write(str(i)+":"+featNames[i]+' ')
	else:
		writer.write(str(i+1)+":"+featNames[i]+' ')
writer.write('\n')
for k in dict.keys():
	thisKeyFs = dict[k]
	if len(thisKeyFs) == len(featNames):
		writer.write(thisKeyFs[LGA]+' ')
		for i in range(len(featNames)):
        		if LGA == i:
                		continue
        		elif i > LGA:
                		writer.write(str(i)+":"+thisKeyFs[i]+' ')
        		else:
                		writer.write(str(i+1)+":"+thisKeyFs[i]+' ')
		t = targets[0]
		tar = t[t.rfind('/')+1:]
		writer.write('#'+ tar + ':'+ k)
		writer.write('\n')
writer.close()
targets = glob.glob(targetsFolder+"*")
first = True
for t in targets:
        if first:
                first = False
                continue
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
        origToThisInd = [50]*len(thisFeatNames)
	for i in range(len(featNames)):
                for j in range(len(thisFeatNames)):
			if "LGA" in thisFeatNames[j]:
                        	thisLGA = i
                        if thisFeatNames[j] == featNames[i]:
                                origToThisInd[i] = j
                                break
	
        for k in dict.keys():
                thisKeyFs = dict[k]
                
		if len(thisKeyFs) == len(featNames):
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




