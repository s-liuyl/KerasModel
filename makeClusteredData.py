import sys
dataset = sys.argv[1] 
clusteredModels = sys.argv[2]
resFolder = sys.argv[3]
if clusteredModels.rfind('/') != len(clusteredModels)-1:
	clusteredModels = clusteredModels +'/'
clusteredModels +='*'
if resFolder.rfind('/') != len(resFolder) -1:
	resFolder = resFolder + '/'
import glob
m = glob.glob(clusteredModels)
r = open(dataset, 'r')
data = r.readlines()
r.close()
models = []
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
	
	
w = open(resFolder + dataset[dataset.rfind('/')+1:dataset.rfind('.')]+'Clustered.txt', 'w')
w.write(data[0])
numModels = len(models)
for line in data:
	try:
		i  = int(line[line.rfind('_')+1:])
		if inArrBinarySearch(models, 0, numModels-1, i):
			w.write(line)
	except:
		continue
w.close()
