import sys
import shutil
log = sys.argv[1]
models = sys.argv[2]
if models.rfind('/') != len(models)-1:
	models = models +'/'
newFolder = sys.argv[3]
if newFolder.rfind('/') != len(newFolder)-1:
	newFolder = newFolder + '/'
r = open(log, 'r')
lines = r.readlines()
r.close()
count = 20
modelNames = []
for i in range(len(lines)):
	l = lines[i]
	if 'Item' in l:
		count = 0
	elif count<20:
		modelNames.append(l[l.rfind('model'):l.rfind(' ')])	
		count+= 1
for i in range(len(modelNames)):
	shutil.copy(models+modelNames[i], newFolder + modelNames[i])


