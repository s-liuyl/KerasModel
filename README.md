# KerasModel

### Installation Steps

1. Download and Unzip KerasModel package
Create a working directory called 'KerasModel' where all scripts, programs and databases will reside:
```
  cd ~
  mkdir KerasModel
```
Download the KerasModel code:

  git clone https://github.com/s-liuyl/KerasModel.git
  
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

### Data and Results
1. Create a directory for results
```
  cd ~/KerasModel/ 
  mkdir results
```  
The results for evaluating the features will appear as bar graph png in the results directory after eval_feats_bar_graph.py is run.

### Running the code
1. In order to run the code, the directory for the datasets must be an argument.
For example, 
```
  python train_QA_90per.py data/QA_score_CASP8_9_10_11_features_singlemodel_20190530.txt
```
