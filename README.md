# KerasModel

### Installation steps

1. Download and Unzip KerasModel package.

Create a working directory called 'KerasModel' where all scripts, programs and databases will reside:
```
  cd ~
  mkdir KerasModel
```
Download the KerasModel code:
```
  git clone https://github.com/s-liuyl/KerasModel.git
```
2. Install numpy, sklearn, keras, theano, matplotlib, and pandas.

Create python virtual environment (if not installed)
```
  cd ~/KerasModel/  
  virtualenv keras_python
  source keras_python/bin/activate
  pip install --upgrade pip
```
Install appropriate libraries
```
  pip install keras
  pip install numpy
  pip install sklearn
  pip install numpy
  pip install panda
  pip install matplotlib
  pip install glob
```
3. Modify ~/keras/keras.json to use theano as the backend.
```
  {
  "epsilon": 1e-07,
  "floatx": "float32",
  "image_dim_ordering":"tf",
  "image_data_format": "channels_last",
  "backend": "theano"
  }
```

### Data, models, graphs, and results
1. Create a directory for data, results, and models
```
  cd ~/KerasModel/ 
  mkdir results
  mkdir models
  mkdir data
  mkdir graphs
```  

### Spliting a dataset into two files
1. To split a dataset file into two files: the first 90% of targets and the last 10% of targets. The files will be saved in the same directory as the dataset file.

For example,
```
  python split9010.py data/CASPdata/QA_score_CASP8_9_10_11_features_singlemodel_20190530.txt

```

### Training the model
1. In order to train the model, it requires 2 arguments: the dataset and the directory for saving the model. 

There are two optional arguments: the architecture as a .txt file and the name you would like your models to have. 

For example, 
```
  python train_QA_90per.py data/CASPdata/QA_score_CASP8_9_10_11_features_singlemodel_20190530_first90.txt DeepCluster_QA_models/ arch.txt

```
The architecture file will contain the number of nodes per hidden layer, separated by a space.

For example, in order to have 3 hidden layers, with 20, 10, and 5 nodes, respectively, the  .txt file will look as such:
```
20 10 5
```

### Predicting with a model
There are two ways to run the prediction code:
1. The first way requires 4 arguments: the dataset, the directory to save the results, the model's json file and the model's h5 file.

For example, 
```
  python predict_QA90percent.py data/CASPdata/QA_score_CASP12_features_singlemodel_20190530.txt results/ DeepCluster_QA_models/model90percent_QA_score_CASP8_9_10_11_features_singlemodel_20190530.json DeepCluster_QA_models/model90percent_QA_score_CASP8_9_10_11_features_singlemodel_20190530.h5
```
2. The second way requires 3 arguments: the dataset, the directory to save the results, and the directory with the model's h5 and json files. The directory, however, can only have one json and one h5 file.

For example, 
```
  python predict_QA90per.py data/QA_score_CASP12_features_singlemodel_20190530.txt results/ DeepCluster_QA_models/
```


### Evaluating the features 
1.  In order to evaluate the features, it requires 2 arguments: the dataset and the directory to save the results.

For example, 
```
  python eval_feats_bar_graph.py data/CASPdata/QA_score_CASP8_9_10_11_features_singlemodel_20190530.txt graphs/
```
