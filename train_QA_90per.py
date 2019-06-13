#######################################################################
#                                                                     #
#	train_QA.py                                                   #
#                                                                     #
#	This code requires 2 arguments: the path for the dataset      #
#	and the directory to save the model.                          #
#                                                                     #
#	It can also take in two optional arguments: a .txt file       #
#	designating the architecture of the network and the name      #
#	you want to call your model files. 			      #
#                                                                     #
#	It will train a keras model using the first 90% of each       #
#	ID in the dataset.                                            #
#                                                                     #
#	These will be saved in a json and h5 file in the current      #
#	directory and will be named according to the dataset name.    #
#                                                                     #
#######################################################################




import numpy as np
import pandas
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasRegressor
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import sys

inputfile = sys.argv[1]
resFolder = sys.argv[2]
if resFolder.rfind('/') != len(resFolder)-1:
        resFolder = resFolder+'/'

if len(sys.argv) == 4 and '.txt' not in sys.argv[3]:
	filename = resFolder+sys.argv[3]
elif len(sys.argv) == 5:
	if '.txt' not in sys.argv[3]:
		filename = resFolder+sys.argv[3]
	else:
		filename = resFolder+sys.argv[4]
else:
	if(inputfile.rfind('/')== -1):
        	filename =resFolder+"model90percent_"+ (inputfile[0:inputfile.rfind('.')])
	else:
        	filename =resFolder+"model90percent_"+ (inputfile[1+inputfile.rfind('/'):inputfile.rfind('.')])

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
for i in range (1,len(dataset)):
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
	
	for index in range(cutoff):
		i = dict[ID][index]
		x = []
		for j in range(0,1+features):
			if j!=0:
				s = dataset[i][j]
				x.append(float(s[(1+s.index(':')):]))
			else:
				Y.append(float(dataset[i][j]))
		X.append(x)	

# define base model
def baseline_model():
	# create model
	model = Sequential()
	model.add(Dense(5, input_dim=features, kernel_initializer='normal', activation='relu'))
	model.add(Dense(1, kernel_initializer='normal'))
	# Compile model
	model.compile(loss='mean_squared_error', optimizer='adam')
	return model
# fix random seed for reproducibility
seed = 7
np.random.seed(seed)
if len(sys.argv) ==3:
	train_model = baseline_model()
elif len(sys.argv) ==5 and '.txt' not in sys.argv[4] and '.txt' not in sys.argv[3]:
        train_model = baseline_model()
elif (len(sys.argv)== 4 and '.txt' not in sys.argv[3]):
	train_model = baseline_model()
else:
	if '.txt' in sys.argv[3]:
		i = 3
	else:
		i = 4
	reader = open(sys.argv[i], 'r') 
	architecture = reader.readline()
	reader.close()
	arch = architecture.split(' ')
	model = Sequential()
	model.add(Dense(int(arch[0]), input_dim=features, kernel_initializer='normal', activation='relu'))	
	for i in range(1,len(arch)):
		model.add(Dense(int(arch[i]),kernel_initializer='normal',activation = 'relu'))
	model.add(Dense(1, kernel_initializer='normal'))
	model.compile(loss='mean_squared_error', optimizer='adam')
	train_model = model

train_model.compile(loss='mean_squared_error', optimizer='adam')

# Fit the model

X = np.asarray(X)
#print(X[0,:])
#print(X.shape)

Y = np.asarray(Y)
#print(Y[0])
#print(Y.shape)



train_model.fit(X, Y, epochs=50, batch_size=1000,verbose=1)


# evaluate the model
scores = train_model.evaluate(X, Y, verbose=0)
print("\n\nThe mse is ",scores)

### save the model 
# serialize model to JSON
model_json = train_model.to_json()
with open(filename+".json", "w") as json_file:
    json_file.write(model_json)
# serialize weights to HDF5
train_model.save_weights(filename+".h5")
print("Saved model to disk")







# evaluate model with standardized dataset
#estimators = []
#estimators.append(('standardize', StandardScaler()))
#estimators.append(('mlp', KerasRegressor(build_fn=baseline_model, epochs=100, batch_size=5, verbose=0)))
#pipeline = Pipeline(estimators)
#kfold = KFold(n_splits=10, random_state=seed)
#results = cross_val_score(pipeline, X, Y, cv=kfold)
#print("Results: %.2f (%.2f) MSE" % (results.mean(), results.std()))

