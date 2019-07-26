import sys
import matplotlib 
matplotlib.use('Agg')
import  matplotlib.pyplot as plt
scoreFile = sys.argv[1]
results = sys.argv[2]
name = sys.argv[3]
target = sys.argv[4]
scores = sys.argv[5]
colors = ['m',  'g','c', 'b', 'y', 'k', ]
read = open(scores, 'r')
lines = read.readlines()
read.close()
methodNum = 0
topMods = []
modNums = [0]*3
for i in range(len(lines)):
        line = lines[i]
        if "Top" in line:
                methodNum +=1
                if methodNum != 1 and methodNum  != 2 and methodNum != 4:
                        continue
		mod = lines[i+1]
		mod = mod[:mod.rfind('\n')]
		topMods.append(mod)


o = open(scoreFile, 'r')
data = o.readlines()
o.close()
dict = {}
for i in range(len(data)):
        l = data[i]
	num = (l[l.find('model_'):l.find('\t')])
	dict[num] = [i+1]
	for j in range(len(topMods)):
		if topMods[j] == num:
			modNums[j] = i+1
		
		
o = open(results,'r')
data = o.readlines()
o.close()
for l in data:
	try:
		num = (l[l.find('model_'):l.find('\t')])
		line = l.split('\t')
		GTS = float(line[3])
		if num in dict:
			dict[num] = [dict[num][0],GTS]
	except:
		continue
X = []
Y = []
for k in dict.keys():
	X.append(dict[k][0])
	Y.append(dict[k][1])

	
methods = ['Clustered','DeepCluster_QA','Qprob']


plt.cla()
plt.plot(X,Y, 'r.')
for i in range(len(topMods)-1):
	plt.axvline(x=int(modNums[i]),color = colors[i], label = methods[i])
plt.legend(loc = 'upper right')
plt.xlabel('DeepCluster_QA ranking')
plt.title('DeepCluster_QA ranking vs. GDT-TS Scores of '+target+' models')
plt.ylabel('GDT-TS Score')
plt.savefig(name+'rankingVSGDT_TS.png', format = 'png')
