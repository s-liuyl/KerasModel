import numpy as np
import math
import pandas
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasRegressor
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from keras.models import model_from_json
from scipy.stats import pearsonr
import sys
inputfile = sys.argv[1]

#load dataset
f = open(inputfile, 'r')
data = f.readlines()
f.close()
dataset = []
for line in data:
	if '#LGA' in line:
		continue
	dataset.append(line.split(' '))


features = len(dataset[0])-2
X = []
Y = []
cutoff = int(len(dataset)*0.9)



for i in range(cutoff, len(dataset)):
	
	x = []
	for j in range(0,1+features):
		if j!=0:
			s = dataset[i][j]
			x.append(float(s[(1+s.index(":")):]))
		else:
			Y.append(float(dataset[i][j]))
	X.append(x)
#determine indices of different sequences
firstS = dataset[cutoff][features+1]
firstID = firstS[1:firstS.index(":")]
dict = {firstID:[0]}
for i in range (cutoff+1,len(dataset)):
	s = dataset[i][features+1]
	id = s[1:(s.index(":"))]
	if id in dict:
		dict[id] = dict[id] + [i-cutoff]
	else:
		dict[id] = [i-cutoff]


#### load the model
# load json and create model
json_file = open('model90percentCASP12.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights("model90percentCASP12.h5")
print("Loaded model from disk")



loaded_model.compile(loss='mean_squared_error', optimizer='adam')

# Fit the model

X = np.asarray(X)
#print(X[0,:])
#print(X.shape)

Y = np.asarray(Y)
#print(Y[0])
#print(Y.shape)


# evaluate the model
scores = loaded_model.evaluate(X, Y, verbose=0)
print("The mse is ",scores)



# predict the data 
pred = loaded_model.predict(X)
print(pred)


#determining loss and correlation coefficient
loss = []
correlation = []
IDs = []
predictedYs = []
actualYs = []
for ID in dict:
	IDs.append(ID)
	p = []
	a = []
	maxP = float("-inf")
	maxPind = 0
	maxAind = 0
	maxA = float("-inf")
	for i in dict[ID]:
		p.append(pred[i][0])
		a.append(Y[i])
		if pred[i][0]>maxP:
			maxP = pred[i][0]
			maxPind = i
		if Y[i]>maxA:
			maxA = Y[i]
			maxAind = i
	loss.append(abs(Y[maxAind]-Y[maxPind])) 
	predictedYs.append(np.asarray(p))
	actualYs.append(np.asarray(a))

correlation_scipy = []
for i in range(len(IDs)):
	meanP = np.mean(predictedYs[i])
	meanA = np.mean(actualYs[i])
	devP = predictedYs[i] - meanP
	devA = 	actualYs[i] - meanA
	devsQP = np.sum(devP**2)
	devsQA = np.sum(devA**2)
	length = len(predictedYs[i])
	sP = math.sqrt(devsQP/(length-1))
	sA = math.sqrt(devsQA/(length-1))
	correlation.append((np.sum(np.multiply(devP, devA))/(sP*sA))/(length-1))
	corr, p_value = pearsonr(predictedYs[i],actualYs[i])
	correlation_scipy.append(corr)

for i in range(len(IDs)):
	print(IDs[i]+" - loss: %.2f, correlation: %f, correlation_scipy: %f" %(loss[i], correlation[i], correlation_scipy[i]))

l = np.asarray(loss)
avgL = np.mean(l)
c = np.asarray(correlation)
avgC = np.mean(c)
avgC2 = np.mean(np.asarray(correlation_scipy))
print("average loss: %f, average correlation: %f, average correlation_scipy: %f" %(avgL,avgC, avgC2))

