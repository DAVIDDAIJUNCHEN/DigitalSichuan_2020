#!/usr/bin/env python3

# import generic modules
from data_process import split_data, get_usable_data
from utils import evaluate

# import model modules
from models.logisticReg import LogisticRegression

# csv files
origin_file = 'data/train/train_user.csv'
train_file = 'data/train/split/train_user.csv'
dev_file = 'data/train/split/dev_user.csv'
test_file = 'data/train/split/test_user.csv'

# set the data file parameters
num_total = 6106
num_train = int(num_total * 0.8)
num_dev = int(num_total * 0.1)
num_test = num_total - num_train - num_dev

# split data to train/dev/test (only for train_user.csv)
split_data(origin_file, num_train, num_dev, num_test, replace=False)

# features I: x_idcar_cnt + average arpu
X_train, label_train = get_usable_data(train_file)
X_dev, label_dev = get_usable_data(dev_file)
X_test, label_test = get_usable_data(test_file)

# Logistic regression
clf = LogisticRegression(random_state=0).fit(X_train, label_train)

# evaluate toy model on (X_dev, label_dev)
label_dev = label_dev.tolist()
pred_dev = clf.predict(X_dev).tolist()
evaluate(label_dev, pred_dev)

# evaluate toy model on (X_test, label_test)
label_test = label_test.tolist()
pred_test = clf.predict(X_test).tolist()
evaluate(label_test, pred_test)
