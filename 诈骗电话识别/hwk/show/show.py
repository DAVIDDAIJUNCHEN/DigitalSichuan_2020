import pickle
import numpy as np
import matplotlib.pyplot as plt
#!/usr/bin/env python3

# import global modules
import sys
import os
import csv
import numpy as np
import warnings
import pandas as pd
import pickle
warnings.filterwarnings('ignore')
sys.path.append('../../')
sys.path.append('../codes_feature/')
sys.path.append('../other')

# import local modules
from utils import evaluate, modify_months_config
from data_process_new import split_data, get_features, get_label, get_phone_no_m
from models.LogisticRegression import LogisticRegression
from models.LogisticRegressionCV import LogisticRegressionCV
from models.ensemble_model import ensemble
from sklearn.preprocessing import normalize
#from get_imei_result import get_imei_result

imie_result = open('../other/imie_result', 'rb')
result=pickle.load(imie_result)

# prepare data and parameter
## original csv files
train_user = '../../data/train/train_user.csv'
train_voc = '../../data/train/train_voc.csv'
train_sms = '../../data/train/train_sms.csv'
train_app = '../../data/train/train_app.csv'

test_user = '../../data/test/test_user.csv'
test_voc = '../../data/test/test_voc.csv'
test_sms = '../../data/test/test_sms.csv'
test_app = '../../data/test/test_app.csv'

## split train/dev/test csv files (with label)
train_file = '../../data/train/split/train_user.csv'
dev_file = '../../data/train/split/dev_user.csv'
test_file = '../../data/train/split/test_user.csv'

## set the data file parameters （in splitting）
num_total = 6106
num_train = int(num_total * 0.8)
num_dev = int(num_total * 0.1)
num_test = num_total - num_train - num_dev

## split data to train/dev/test (only for train_user.csv)
split_data(train_user, num_train, num_dev, num_test, replace=False)

## define features in train_config_yml and test_config_yml
train_config_yml = '../configs/show.yml'

# get design matrix and label according to months
label_train = get_label(train_file)
label_dev = get_label(dev_file)
label_test = get_label(test_file)

user_train_csv = pd.read_csv('../../data/train/train_user.csv')

clf_gradboostAcc_months = {}



X_train = get_features(train_file, train_voc, train_sms, train_app, train_config_yml)
X_dev = get_features(dev_file, train_voc, train_sms, train_app, train_config_yml)
X_test = get_features(test_file, train_voc, train_sms, train_app, train_config_yml)

X_all=X_train+X_dev+X_test
label_all=label_train+label_dev+label_test
#诈骗
X_ZP=[]
#非诈骗
X_NZP=[]
for ii in range(len(X_all)):
    if label_all[ii]==1:
        X_ZP.append(X_all[ii])
    else:
        X_NZP.append(X_all[ii])

X_ZP_array=np.array(X_ZP)
X_NZP_array=np.array(X_NZP)

zp=X_ZP_array[:,0]
nzp=X_NZP_array[:,0]
plt.figure(1)
plt.boxplot(zp)
plt.figure(2)
plt.boxplot(nzp)
plt.show()