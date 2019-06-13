# KerasModel

### Installation Steps

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

### Data, Models, and Results
1. Create a directory for data, results, and models
```
  cd ~/KerasModel/ 
  mkdir results
  mkdir models
  mkdir data
```  
The trained model including its weights will be stored in the models directory after train_QA_90per.py is run.

The results for evaluating the features will appear as bar graph png in the results directory after eval_feats_bar_graph.py is run.

### Training the Model
1. In order to train the model, it requires 2 arguments: the dataset and the directory for saving the model. The third argument is optional and is the architecture as a .txt file. 

For example, 
```
  python train_QA_90per.py data/QA_score_CASP8_9_10_11_features_singlemodel_20190530.txt models/ arch.txt

```
The architecture file will contain the number of nodes per hidden layer, separated by a space.

For example, in order to have 3 hidden layers, with 20, 10, and 5 nodes, respectively, the  .txt file will look as such:
```
20 10 5
```

### Predicting with a Model
There are two ways to run the prediction code:
1. The first way requires 4 arguments: the dataset, the directory to save the results, the model's json file and the model's h5 file.

For example, 
```
  python predict_QA90per.py data/QA_score_CASP8_9_10_11_features_singlemodel_20190530.txt results/models/model90percent_QA_score_CASP8_9_10_11_features_singlemodel_20190530.json models/model90percent_QA_score_CASP8_9_10_11_features_singlemodel_20190530.h5
```
2. The second way requires 3 arguments: the dataset, the directory to save the results, and the directory with the model's h5 and json files. The directory, however, can only have one json and one h5 file.

For example, 
```
  python predict_QA90per.py data/QA_score_CASP8_9_10_11_features_singlemodel_20190530.txt results/ models/
```


### Evaluating the Features 
1.  In order to evaluate the features, it requires 2 arguments: the dataset and the directory to save the results.

For example, 
```
  python eval_feats_bar_graph.py data/QA_score_CASP8_9_10_11_features_singlemodel_20190530.txt results/
```
