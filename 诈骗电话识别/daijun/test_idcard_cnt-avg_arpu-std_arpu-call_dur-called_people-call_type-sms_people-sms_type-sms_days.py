#!/usr/bin/env python3

# import generic modules
import sys
import os
import csv
sys.path.append('../')
from data_process import get_usable_data
from utils import evaluate

# import model modules
from models.LogisticRegression import LogisticRegression
from models.LogisticRegressionCV import LogisticRegressionCV

# csv files
train_voc = '../data/train/train_voc.csv'
train_sms = '../data/train/train_sms.csv'
test_voc = '../data/test/test_voc.csv'
test_sms = '../data/test/test_sms.csv'

train_file = '../data/train/train_user.csv'
dev_file = '../data/train/split/dev_user.csv'
test_file = '../data/test/test_user.csv'


# Features I: x_idcard_cnt + average_arpu + std_arpu
X_train, label_train = get_usable_data(train_file, train_voc, train_sms, method='idcard_cnt-avg_arpu-std_arpu-call_dur-called_people-call_type-sms_people-sms_type-sms_datetime')
X_dev, label_dev = get_usable_data(dev_file, train_voc, train_sms, method='idcard_cnt-avg_arpu-std_arpu-call_dur-called_people-call_type-sms_people-sms_type-sms_datetime')
X_test, phone_no_m = get_usable_data(test_file, test_voc, test_sms, get_label=False, num_month=1, get_phone_no=True, method='idcard_cnt-avg_arpu-std_arpu-call_dur-called_people-call_type-sms_people-sms_type-sms_datetime')

feauture_name = 'idcard_cnt-avg_arpu-std_arpu-call_dur-called_people-call_type-sms_people-sms_type-sms_datetime'

if not os.path.exists('./test_results/'+feauture_name+'/'):
    os.makedirs('./test_results/'+feauture_name+'/')

# Model I: Logistic regression
clf_logistReg = LogisticRegression(random_state=0).fit(X_train, label_train)

# evaluate toy model on (X_dev, label_dev)
label_dev = label_dev.tolist()
pred_dev = clf_logistReg.predict(X_dev).tolist()
evaluate(label_dev, pred_dev, model='Logistic Regression')

# evaluate toy model on (X_test, label_test)
pred_test = clf_logistReg.predict(X_test).tolist()

with open('./test_results/'+feauture_name+'/'+'logisticRegression.csv', 'w', newline='', encoding='utf-8') as fout:
    field_names = ['phone_no_m', 'label']
    writer = csv.DictWriter(fout, fieldnames=field_names)
    writer.writeheader()
    for phone, pred in zip(phone_no_m, pred_test):
        writer.writerow({'phone_no_m': phone, 'label': pred})

# Model VIII: Gradientboosting
from sklearn.ensemble import GradientBoostingClassifier
clf_gradboost = GradientBoostingClassifier(max_depth=2, random_state=0)
clf_gradboost.fit(X_train, label_train)

# evaluate toy model on (X_dev, label_dev)
pred_dev = clf_gradboost.predict(X_dev).tolist()
evaluate(label_dev, pred_dev, model='Gradient boosting')

# evaluate toy model on (X_test, label_test)
pred_test = clf_gradboost.predict(X_test).tolist()

with open('./test_results/'+feauture_name+'/'+'Gradientboosting.csv', 'w', newline='', encoding='utf-8') as fout:
    field_names = ['phone_no_m', 'label']
    writer = csv.DictWriter(fout, fieldnames=field_names)
    writer.writeheader()
    for phone, pred in zip(phone_no_m, pred_test):
        writer.writerow({'phone_no_m': phone, 'label': pred})
