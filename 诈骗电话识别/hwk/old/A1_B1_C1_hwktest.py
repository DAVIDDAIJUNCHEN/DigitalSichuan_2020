#!/usr/bin/env python3

# import global modules
import sys
sys.path.append('../../')

# import local modules
from utils import evaluate
from data_process_new import split_data, get_features, get_label
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
config_yml = '../configs/A1_B1_C1_config.yml'

# get design matrix and label
X_train = get_features(train_file, train_voc, train_sms, train_app, config_yml)
label_train = get_label(train_file)

X_dev = get_features(dev_file, train_voc, train_sms, train_app, config_yml)
label_dev = get_label(dev_file)

X_test = get_features(test_file, train_voc, train_sms, train_app, config_yml)
label_test = get_label(test_file)

# Model I: Logistic regression
clf_logistReg = LogisticRegression(random_state=0).fit(X_train, label_train)

# evaluate toy model on (X_dev, label_dev)
#label_dev = label_dev.tolist()
pred_dev = clf_logistReg.predict(X_dev).tolist()
evaluate(label_dev, pred_dev, model='Logistic Regression')

# evaluate toy model on (X_test, label_test)
#label_test = label_test.tolist()
pred_test = clf_logistReg.predict(X_test).tolist()
evaluate(label_test, pred_test, model='Logistic Regression')
