#!/usr/bin/env python3

# import global modules
import sys
import os
import csv
sys.path.append('../../')

# import local modules
from utils import evaluate
from data_process_new import split_data, get_features, get_label, get_phone_no_m
from models.LogisticRegression import LogisticRegression
from models.LogisticRegressionCV import LogisticRegressionCV
from sklearn.preprocessing import normalize


# original csv files
train_user = '../../data/train/train_user.csv'
train_voc = '../../data/train/train_voc.csv'
train_sms = '../../data/train/train_sms.csv'
train_app = '../../data/train/train_app.csv'

test_user = '../../data/test/test_user.csv'
test_voc = '../../data/test/test_voc.csv'
test_sms = '../../data/test/test_sms.csv'
test_app = '../../data/test/test_app.csv'

# split train/dev/test csv files (with label)
train_file = '../../data/train/split/train_user.csv'
dev_file = '../../data/train/split/dev_user.csv'
test_file = '../../data/train/split/test_user.csv'

# set the data file parameters
num_total = 6106
num_train = int(num_total * 0.8)
num_dev = int(num_total * 0.1)
num_test = num_total - num_train - num_dev

# split data to train/dev/test (only for train_user.csv)
split_data(train_user, num_train, num_dev, num_test, replace=False)

# define features in config_yml
train_config_yml = '../configs/A1_B1_C1_config_train.yml'
test_config_yml = '../configs/A1_B1_C1_config_test.yml'
features_name = 'A1_B1_C1'

# get design matrix and label
X_train = get_features(train_file, train_voc, train_sms, train_app, train_config_yml)
label_train = get_label(train_file)

X_dev = get_features(dev_file, train_voc, train_sms, train_app, train_config_yml)
label_dev = get_label(dev_file)

X_test = get_features(test_file, train_voc, train_sms, train_app, train_config_yml)
label_test = get_label(test_file)

X_blindtest = get_features(test_user, test_voc, test_sms, test_app, test_config_yml)
phone_no_m_blindtest = get_phone_no_m(test_user)

if not os.path.exists('../test_results/'+features_name+'/'):
    os.mkdir('../test_results/'+features_name+'/')

# Model I: Logistic regression
clf_logistReg = LogisticRegression(random_state=0).fit(X_train, label_train)

# evaluate toy model on (X_dev, label_dev)
pred_dev = clf_logistReg.predict(X_dev).tolist()
evaluate(label_dev, pred_dev, model='Logistic Regression')

# evaluate toy model on (X_test, label_test)
pred_test = clf_logistReg.predict(X_test).tolist()
evaluate(label_test, pred_test, model='Logistic Regression')

# Model II: Logistic regression CV
clf_logistRegCV = LogisticRegressionCV(cv=5, random_state=0).fit(X_train, label_train)

# evaluate toy model on (X_dev, label_dev)
pred_dev = clf_logistRegCV.predict(X_dev).tolist()
evaluate(label_dev, pred_dev, model='Logistic Regression CV=5')

# evaluate toy model on (X_test, label_test)
pred_test = clf_logistRegCV.predict(X_test).tolist()
evaluate(label_test, pred_test, model='Logistic Regression CV=5')

# Model III: percepton
#from sklearn.linear_model import Perceptron
#clf_perceptron = Perceptron(tol=1e-3, random_state=0)
#clf_perceptron.fit(X_train, label_train)

# evaluate toy model on (X_dev, label_dev)
#pred_dev = clf_perceptron.predict(X_dev).tolist()
#evaluate(label_dev, pred_dev, model='Perceptron')

# evaluate toy model on (X_test, label_test)
#pred_test = clf_perceptron.predict(X_test).tolist()
#evaluate(label_test, pred_test, model='Perceptron')

# Model IV: RidgeClassifier
from sklearn.linear_model import RidgeClassifier
clf_ridgeClassifier = RidgeClassifier().fit(X_train, label_train)

# evaluate toy model on (X_dev, label_dev)
pred_dev = clf_ridgeClassifier.predict(X_dev).tolist()
evaluate(label_dev, pred_dev, model='Ridge Classification')

# evaluate toy model on (X_test, label_test)
pred_test = clf_ridgeClassifier.predict(X_test).tolist()
evaluate(label_test, pred_test, model='Ridge Classification')

# Model V: AdaBoostClassifier
from sklearn.ensemble import AdaBoostClassifier
clf_AdaBoost = AdaBoostClassifier(n_estimators=100, random_state=0)
clf_AdaBoost.fit(X_train, label_train)

# evaluate toy model on (X_dev, label_dev)
pred_dev = clf_AdaBoost.predict(X_dev).tolist()
evaluate(label_dev, pred_dev, model='Adaboost')

# evaluate toy model on (X_test, label_test)
pred_test = clf_AdaBoost.predict(X_test).tolist()
evaluate(label_test, pred_test, model='Adaboost')

# Model VI: BaggingClassifier
from sklearn.ensemble import BaggingClassifier
from sklearn.svm import SVC
clf_Bagging = BaggingClassifier(base_estimator=SVC(), n_estimators=10, random_state=0)
clf_Bagging.fit(X_train, label_train)

# evaluate toy model on (X_dev, label_dev)
pred_dev = clf_Bagging.predict(X_dev).tolist()
evaluate(label_dev, pred_dev, model='Bagging_SVC')

# evaluate toy model on (X_test, label_test)
pred_test = clf_Bagging.predict(X_test).tolist()
evaluate(label_test, pred_test, model='Bagging_SVC')

# Model VII: random forest
from sklearn.ensemble import RandomForestClassifier
clf_randforest = RandomForestClassifier(max_depth=2, random_state=0)
clf_randforest.fit(X_train, label_train)

# evaluate toy model on (X_dev, label_dev)
pred_dev = clf_randforest.predict(X_dev).tolist()
evaluate(label_dev, pred_dev, model='Random forest')

# evaluate toy model on (X_test, label_test)
pred_test = clf_randforest.predict(X_test).tolist()
evaluate(label_test, pred_test, model='Random forest')

# Model VIII: Gradientboosting
from sklearn.ensemble import GradientBoostingClassifier
clf_gradboost = GradientBoostingClassifier(max_depth=2, random_state=0)
clf_gradboost.fit(X_train, label_train)

# evaluate toy model on (X_dev, label_dev)
pred_dev = clf_gradboost.predict(X_dev).tolist()
evaluate(label_dev, pred_dev, model='Gradient boosting')

# evaluate toy model on (X_test, label_test)
pred_test = clf_gradboost.predict(X_test).tolist()
evaluate(label_test, pred_test, model='Gradient boosting')

# evaluate toy model on (X_blindtest)
pred_blindtest = clf_gradboost.predict(X_blindtest).tolist()

month_train = '201911'
with open('../test_results/' + features_name + '/' + 'GradientBoosting_' + month_train + '.csv',
          'w', newline='', encoding='utf-8') as fout:
    field_names = ['phone_no_m', 'label']
    writer = csv.DictWriter(fout, fieldnames=field_names)
    writer.writeheader()
    for phone, pred in zip(phone_no_m_blindtest, pred_blindtest):
        writer.writerow({'phone_no_m': phone, 'label': pred})

# Model IX: MLP Classifier
from sklearn.neural_network import MLPClassifier
clf_mlp = MLPClassifier(random_state=1, max_iter=300).fit(X_train, label_train)

# evaluate toy model on (X_dev, label_dev)
pred_dev = clf_mlp.predict(X_dev).tolist()
evaluate(label_dev, pred_dev, model='MLP')

# evaluate toy model on (X_test, label_test)
pred_test = clf_mlp.predict(X_test).tolist()
evaluate(label_test, pred_test, model='MLP')

# Model X: SVM
from sklearn.svm import LinearSVC
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

clf_svm = make_pipeline(StandardScaler(), LinearSVC(random_state=0, tol=1e-5))
clf_svm.fit(X_train, label_train)

# evaluate toy model on (X_dev, label_dev)
pred_dev = clf_svm.predict(X_dev).tolist()
evaluate(label_dev, pred_dev, model='SVM')

# evaluate toy model on (X_test, label_test)
pred_test = clf_svm.predict(X_test).tolist()
evaluate(label_test, pred_test, model='SVM')