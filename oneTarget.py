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
origToThisInd = [50]*len(featNames)
for i in range(len(featNames)):
	for j in range(len(thisFeatNames)):
		if "LGA" in thisFeatNames[j]:
			thisLGA = j
                if thisFeatNames[j] == featNames[i]:
                        origToThisInd[i] = j
			break
	
if thisLGA!= float('inf'):
	w = open(targetFileName, 'w')
	w.write(d[0])
	w.close() 
else:
	w = open(targetFileName, 'w')
        w.write((d[0])[(d[0]).rfind('1:'):])
        w.close()
first = True
print(origToThisInd)
print(thisLGA)
print(featNames)
print(thisFeatNames)
for k in dict.keys():
	fs = dict[k]
#	if first:
		#first = False
		#print(fs)
	if len(fs) ==1:
		continue	
	if thisLGA != float('inf'):
		writer.write(fs[thisLGA]+' ')
	for i in range(len(featNames)):
		if origToThisInd[i] == 50:
			writer.write(str(i)+":0")
		elif thisLGA == i:
              		continue
        	elif i > thisLGA:
                	writer.write(str(i)+":"+fs[origToThisInd[i]]+' ')
		else:
                	writer.write(str(i+1)+":"+fs[origToThisInd[i]]+' ')
	writer.write('#'+tar+':'+k)
	writer.write('\n')
writer.close()



