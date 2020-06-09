#!/usr/bin/env python3

# import generic modules
from data_process import split_data, get_usable_data
from utils import evaluate

# import model modules
from models.LogisticRegression import LogisticRegression
from models.LogisticRegressionCV import LogisticRegressionCV

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

# Features I: x_idcard_cnt + average_arpu
X_train, label_train = get_usable_data(train_file, method='idcard_cnt-avg_arpu')
X_dev, label_dev = get_usable_data(dev_file, method='idcard_cnt-avg_arpu')
X_test, label_test = get_usable_data(test_file, method='idcard_cnt-avg_arpu')


# Model I: Logistic regression
clf_logistReg = LogisticRegression(random_state=0).fit(X_train, label_train)

# evaluate toy model on (X_dev, label_dev)
label_dev = label_dev.tolist()
pred_dev = clf_logistReg.predict(X_dev).tolist()
evaluate(label_dev, pred_dev, model='Logistic Regression')

# evaluate toy model on (X_test, label_test)
label_test = label_test.tolist()
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
from sklearn.linear_model import Perceptron
clf_perceptron = Perceptron(tol=1e-3, random_state=0)
clf_perceptron.fit(X_train, label_train)

# evaluate toy model on (X_dev, label_dev)
pred_dev = clf_perceptron.predict(X_dev).tolist()
evaluate(label_dev, pred_dev, model='Perceptron')

# evaluate toy model on (X_test, label_test)
pred_test = clf_perceptron.predict(X_test).tolist()
evaluate(label_test, pred_test, model='Perceptron')

# Model IV: RidgeClassifier
from sklearn.linear_model import RidgeClassifier
clf_ridgeClassifier = RidgeClassifier().fit(X_train, label_train)

# evaluate toy model on (X_dev, label_dev)
pred_dev = clf_ridgeClassifier.predict(X_dev).tolist()
evaluate(label_dev, pred_dev, model='Ridge Classification')

# evaluate toy model on (X_test, label_test)
pred_test = clf_ridgeClassifier.predict(X_test).tolist()
evaluate(label_test, pred_test, model='Ridge Classification')

#