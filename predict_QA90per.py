#######################################################################
#                                                                     #
#	predict_QA90percent.py                                        #
#                                                                     #
#	This code takes in one argument: the path for the dataset.    #
#                                                                     #
#	After loading the model, it will predict the values of the    #
#	last 10% of the dataset  a keras model using the last 10% of  #
#	the dataset.                                                  #
#                                                                     #
#######################################################################




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
if(inputfile.rfind('/')==-1):
	filename = inputfile[0:inputfile.rfind('.')]
else:
	filename = inputfile[1+inputfile.rfind('/'):inputfile.rfind('.')]
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
#determine indices of different sequences
firstS = dataset[0][features+1]
firstID = firstS[1:firstS.index(":")]
dict = {firstID:[0]}
for i in range (0,len(dataset)):
        s = dataset[i][features+1]
        id = s[1:(s.index(":"))]
        if id in dict:
                dict[id] = dict[id] + [i]
        else:
                dict[id] = [i]


X = []
Y = []

for ID in dict:
        cutoff = int(0.9*len(dict[ID]))
	Is = []
        for index in range(cutoff,len(dict[ID])):
                i = dict[ID][index]
                x = []
		Is.append(len(Y))
		for j in range(0,1+features):
                        if j!=0:
                                s = dataset[i][j]
                                x.append(float(s[(1+s.index(':')):]))
                        else:
                                Y.append(float(dataset[i][j]))
                
        	X.append(x) 
	dict[ID] = Is

#### load the model
# load json and create model
json_file = open("./models/model90percent_"+filename+".json", 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights("./models/model90percent_"+filename+".h5")
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
	corr, p_value = pearsonr(predictedYs[i],actualYs[i])
	correlation_scipy.append(corr)

for i in range(len(IDs)):
	print(IDs[i]+" - loss: %.2f, correlation: %f" %(loss[i], correlation_scipy[i]))

l = np.asarray(loss)
avgL = np.mean(l)
avgC2 = np.mean(np.asarray(correlation_scipy))
print("average loss: %f, average correlation: %f" %(avgL, avgC2))

