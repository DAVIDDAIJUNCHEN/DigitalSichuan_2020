
#!/usr/bin/env python3

# import global modules
import sys
import os
import csv
import numpy as np
import warnings
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
train_config_yml = '../configs/all_data_train.yml'
test_config_yml  = '../configs/all_data_test.yml'
# train_config_yml = '../configs/A1_2_4_5_7_9_10_12-30_36_37B1_3_4C1-6D1-3_config_train.yml'
# test_config_yml  = '../configs/A1_2_4_5_7_9_10_12-30_36_37B1_3_4C1-6D1-3_config_test.yml'
features_name = 'MMA1-2A4-5A7A9-10A12-24'

# get design matrix and label according to months
label_train_temp = get_label(train_file)
label_dev_temp = get_label(dev_file)
label_test_temp = get_label(test_file)
phone_no_m_blindtest = get_phone_no_m(test_user)


X_blindtest = get_features(test_user, test_voc, test_sms, test_app, test_config_yml)
X_blindtest_t=open('../../data/X_blindtest','wb')
pickle.dump(X_blindtest,X_blindtest_t)
## create test_results dir
if not os.path.exists('../test_results/'+features_name+'/'):
    os.mkdir('../test_results/'+features_name+'/')

# months_lst = [['2019-08'], ['2019-09'], ['2019-10'], ['2019-11'],
#                ['2019-12'], ['2020-01'], ['2020-02'], ['2020-03']]
#months_lst = [['2019-08'], ['2019-09'], ['2019-10'], ['2019-11'],['2020-01'],['2020-02'],['2020-03']]
months_lst = [['2019-08'], ['2019-09'], ['2019-10'], ['2019-11']]

months_test=[['2019-12']]
gradboost_blindAcc = {"2019-11_2019-12_2020-02_2020-03":0.9, '2019-08': 0.62, '2019-09': 0.66, '2019-10': 0.73, '2019-11': 0.75,
                 '2019-12': 0.78, '2020-01': 0.72, '2020-02': 0.76, '2020-03': 0.77}

clf_gradboostAcc_months = {}
X_train=[]
X_dev=[]
X_test=[]
label_train=[]
label_dev=[]
label_test=[]
for months in months_lst:
    print(months)
    # update the months in config_yaml file
    modify_months_config(train_config_yml, new_months=months)

    X_train_temp = get_features(train_file, train_voc, train_sms, train_app, train_config_yml)
    X_dev_temp = get_features(dev_file, train_voc, train_sms, train_app, train_config_yml)

    X_train +=X_train_temp;
    X_dev +=X_dev_temp

    label_train +=label_train_temp
    label_dev +=label_dev_temp
    if months!=['2019-12']:
        X_test_temp = get_features(test_file, train_voc, train_sms, train_app, train_config_yml)
        X_train += X_test_temp
        label_train += label_test_temp

for months in months_test:
    print(months)
    # update the months in config_yaml file
    modify_months_config(train_config_yml, new_months=months)
    X_test_temp = get_features(test_file, train_voc, train_sms, train_app, train_config_yml)
    X_test +=X_test_temp
    label_test +=label_test_temp

X_train+=X_dev;
label_train+=label_dev;

# X_train_t=open('../../data/X_train','wb')
# pickle.dump(X_train,X_train_t)
# label_train_t=open('../../data/label_train','wb')
# pickle.dump(label_train,label_train_t)
#
# X_test_t=open('../../data/X_test','wb')
# pickle.dump(X_test,X_test_t)
# label_test_t=open('../../data/label_test','wb')
# pickle.dump(label_test,label_test_t)

# model training and inference
## Model I: Logistic regression
clf_logistReg = LogisticRegression(random_state=0).fit(X_train, label_train)

### evaluate toy model on (X_dev, label_dev)
pred_dev = clf_logistReg.predict(X_dev).tolist()
evaluate(label_dev, pred_dev, model='Logistic Regression')

### evaluate toy model on (X_test, label_test)
pred_test = clf_logistReg.predict(X_test).tolist()
evaluate(label_test, pred_test, model='Logistic Regression')

## Model II: Logistic regression CV
clf_logistRegCV = LogisticRegressionCV(cv=5, random_state=0).fit(X_train, label_train)

### evaluate toy model on (X_dev, label_dev)
pred_dev = clf_logistRegCV.predict(X_dev).tolist()
evaluate(label_dev, pred_dev, model='Logistic Regression CV=5')

### evaluate toy model on (X_test, label_test)
pred_test = clf_logistRegCV.predict(X_test).tolist()
evaluate(label_test, pred_test, model='Logistic Regression CV=5')

## Model III: percepton
#from sklearn.linear_model import Perceptron
#clf_perceptron = Perceptron(tol=1e-3, random_state=0)
#clf_perceptron.fit(X_train, label_train)

# evaluate toy model on (X_dev, label_dev)
#pred_dev = clf_perceptron.predict(X_dev).tolist()
#evaluate(label_dev, pred_dev, model='Perceptron')

# evaluate toy model on (X_test, label_test)
#pred_test = clf_perceptron.predict(X_test).tolist()
#evaluate(label_test, pred_test, model='Perceptron')

## Model IV: RidgeClassifier
from sklearn.linear_model import RidgeClassifier
clf_ridgeClassifier = RidgeClassifier().fit(X_train, label_train)

### evaluate toy model on (X_dev, label_dev)
pred_dev = clf_ridgeClassifier.predict(X_dev).tolist()

evaluate(label_dev, pred_dev, model='Ridge Classification')

### evaluate toy model on (X_test, label_test)
pred_test = clf_ridgeClassifier.predict(X_test).tolist()
evaluate(label_test, pred_test, model='Ridge Classification')

## Model V: AdaBoostClassifier
from sklearn.ensemble import AdaBoostClassifier
clf_AdaBoost = AdaBoostClassifier(n_estimators=100, random_state=0)

clf_AdaBoost.fit(X_train, label_train)

### evaluate toy model on (X_dev, label_dev)
pred_dev = clf_AdaBoost.predict(X_dev).tolist()
evaluate(label_dev, pred_dev, model='Adaboost')

### evaluate toy model on (X_test, label_test)
pred_test = clf_AdaBoost.predict(X_test).tolist()
evaluate(label_test, pred_test, model='Adaboost')

# ## Model VI: BaggingClassifier
# from sklearn.ensemble import BaggingClassifier
# from sklearn.svm import SVC
# clf_Bagging = BaggingClassifier(base_estimator=SVC(), n_estimators=10, random_state=0)
# clf_Bagging.fit(X_train, label_train)
#
# ### evaluate toy model on (X_dev, label_dev)
# pred_dev = clf_Bagging.predict(X_dev).tolist()
# evaluate(label_dev, pred_dev, model='Bagging_SVC')
#
# ### evaluate toy model on (X_test, label_test)
# pred_test = clf_Bagging.predict(X_test).tolist()
# evaluate(label_test, pred_test, model='Bagging_SVC')

## Model VII: random forest
from sklearn.ensemble import RandomForestClassifier
#clf_randforest = RandomForestClassifier(max_depth=2, random_state=0)
clf_randforest = RandomForestClassifier(n_estimators=160, max_features=10, min_samples_leaf=10, max_depth=5,
                                        min_samples_split=50, random_state=10)
clf_randforest.fit(X_train, label_train)

### evaluate toy model on (X_dev, label_dev)
pred_dev = clf_randforest.predict(X_dev).tolist()
evaluate(label_dev, pred_dev, model='Random forest')

### evaluate toy model on (X_test, label_test)
pred_test = clf_randforest.predict(X_test).tolist()
evaluate(label_test, pred_test, model='Random forest')

## Model VIII: Gradientboosting
from sklearn.ensemble import GradientBoostingClassifier
#clf_gradboost = GradientBoostingClassifier(max_depth=2, random_state=0)
clf_gradboost = GradientBoostingClassifier(n_estimators=90, max_features=8, min_samples_leaf=20, max_depth=11,
                                           min_samples_split=50, random_state=10)
clf_gradboost.fit(X_train, label_train)

### evaluate toy model on (X_dev, label_dev)
pred_dev = clf_gradboost.predict(X_dev).tolist()
evaluate(label_dev, pred_dev, model='Gradient boosting')

### evaluate toy model on (X_test, label_test)
pred_test = clf_gradboost.predict(X_test).tolist()
evaluate(label_test, pred_test, model='Gradient boosting')

### collect models in months
clf_gradboostAcc_months['_'.join(months)] = (clf_gradboost, gradboost_blindAcc['_'.join(months)])

## Model IX: MLP Classifier
from sklearn.neural_network import MLPClassifier
clf_mlp = MLPClassifier(hidden_layer_sizes=(100,100,50), max_iter=300).fit(X_train, label_train)

### evaluate toy model on (X_dev, label_dev)
pred_dev = clf_mlp.predict(X_dev).tolist()
evaluate(label_dev, pred_dev, model='MLP')

### evaluate toy model on (X_test, label_test)
pred_test = clf_mlp.predict(X_test).tolist()
evaluate(label_test, pred_test, model='MLP')

## Model X: SVM
from sklearn.svm import LinearSVC
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

clf_svm = make_pipeline(StandardScaler(), LinearSVC(random_state=0, tol=1e-5))
clf_svm.fit(X_train, label_train)

### evaluate toy model on (X_dev, label_dev)
pred_dev = clf_svm.predict(X_dev).tolist()
evaluate(label_dev, pred_dev, model='SVM')

### evaluate toy model on (X_test, label_test)
pred_test = clf_svm.predict(X_test).tolist()
evaluate(label_test, pred_test, model='SVM')


# predict labels on blind test set and write to xlsx file for submitting
## gradboost classifier
pred_blindtest = clf_gradboost.predict(X_blindtest).tolist()

month_train = '_'.join(months)    # month_train should be the same as in config_train.yml

with open('../test_results/' + features_name + '/' + 'GradientBoosting_'  + 'all.csv',
          'w', newline='', encoding='utf-8') as fout:
    field_names = ['phone_no_m', 'label']
    writer = csv.DictWriter(fout, fieldnames=field_names)
    writer.writeheader()

    for phone, pred in zip(phone_no_m_blindtest, pred_blindtest):
        if phone in result and result[phone]!=pred:
            writer.writerow({'phone_no_m': phone, 'label': result[phone]})
            print('换掉啦啦')
        else:
            writer.writerow({'phone_no_m': phone, 'label': pred})
