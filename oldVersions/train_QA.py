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
for i in range(len(dataset)):
	x = []
	for j in range(0,1+features):
		if j!=0:
			s = dataset[i][j]
			x.append(float(s[(1+s.index(":")):]))
		else:
			Y.append(float(dataset[i][j]))
	X.append(x)
# define base model
def baseline_model():
	# create model
	model = Sequential()
	model.add(Dense(26, input_dim=26, kernel_initializer='normal', activation='relu'))
	# model.add(Dense(13,kernel_initializer='normal',activation = 'relu'))
	model.add(Dense(1, kernel_initializer='normal'))
	# Compile model
	model.compile(loss='mean_squared_error', optimizer='adam')
	return model
# fix random seed for reproducibility
seed = 7
np.random.seed(seed)

train_model = baseline_model()
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
with open("model.json", "w") as json_file:
    json_file.write(model_json)
# serialize weights to HDF5
train_model.save_weights("model.h5")
print("Saved model to disk")







# evaluate model with standardized dataset
#estimators = []
#estimators.append(('standardize', StandardScaler()))
#estimators.append(('mlp', KerasRegressor(build_fn=baseline_model, epochs=100, batch_size=5, verbose=0)))
#pipeline = Pipeline(estimators)
#kfold = KFold(n_splits=10, random_state=seed)
#results = cross_val_score(pipeline, X, Y, cv=kfold)
#print("Results: %.2f (%.2f) MSE" % (results.mean(), results.std()))

