#######################################################################
#                                                                     #
#	predict_QA90percent.py                                        #
#                                                                     #
#	This code either takes in 3 or 4 arguments.		      #
#	The first argument is the path for the dataset.		      #
#	The second argument is the directory to save the results.     #
#                                                                     #
#	There are two options for inputing the paths for the models.  #
#                                                                     #
#	The first option is to give the directory that has the json   #
#	and h5 files for the model as the third argument.	      #
#                                                                     #
#	The second option is to give the path of the json file and    #
#	the h5 file as the third and fourth arguments, respectively.  #
#                                                                     #
#	After loading the model, it will predict the values of the    #
#	last 10% of the dataset  a keras model using the last 10% of  #
#	the dataset.                                                  #
#                                                                     #
#######################################################################




import numpy as np
import math
import pandas
import glob
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
modelFolder = sys.argv[3]
if len(sys.argv) == 4:
	modelFolder = sys.argv[3]
	if modelFolder.rfind('/') != len(modelFolder)-1:
        	modelFolder = modelFolder+'/'
	h5File = glob.glob(modelFolder+"*.h5")[0]
	jsonFile = glob.glob(modelFolder+"*.json")[0]
else:
	jsonFile = sys.argv[3]
	h5File = sys.argv[4]
	
#### load the model
# load json and create model
json_file = open(jsonFile, 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights(h5File)
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
l = np.asarray(loss)
avgL = np.mean(l)
avgC = np.mean(np.asarray(correlation_scipy))


resFolder = sys.argv[2]
if resFolder.rfind('/') != len(resFolder)-1:
        resFolder = resFolder+'/'
writer = open(resFolder+filename +'.txt', 'w')
for i in range(len(IDs)):
	writer.write(IDs[i]+" - loss: %.2f, correlation: %f\n" %(loss[i], correlation_scipy[i]))
writer.write("average loss: %f, average correlation: %f" %(avgL, avgC))
writer.close()
