#!/usr/bin/env python3

# import generic modules
import sys
import random
sys.path.append('../')
from hwk.data_process_hwk import *
from utils import evaluate
# import model modules
from models.LogisticRegression import LogisticRegression
from models.LogisticRegressionCV import LogisticRegressionCV
train_user_path = '../data/train/train_user.csv'
train_voc_path = '../data/train/train_voc.csv'

idcardMon_userInfo_dict=get_user_data(train_user_path)
idcardMon=list(idcardMon_userInfo_dict.keys())


# ids=range(len(idcardMon))
# random.shuffle(ids)

# set the data file parameters
num_total = len(idcardMon)
num_train = int(num_total * 0.8)
num_dev = int(num_total * 0.1)
num_test = num_total - num_train - num_dev

X_train=[]
lable_train=[]
for key in idcardMon[:num_train]:
    value=idcardMon_userInfo_dict[key]
    if value[0]=='':
        continue

    arpu=float(value[0])
    lable=int(value[1])
    X_train.append([arpu])
    lable_train.append(lable)

X_dev=[]
lable_dev=[]
for key in idcardMon[num_train:num_train+num_dev]:
    value=idcardMon_userInfo_dict[key]
    if value[0]=='':
        continue
    arpu=float(value[0])
    lable=int(value[1])
    X_dev.append([arpu])
    lable_dev.append(lable)

X_test=[]
lable_test=[]
for key in idcardMon[num_train+num_dev:num_train+num_dev+num_test]:
    value=idcardMon_userInfo_dict[key]
    if value[0]=='':
        continue
    arpu=float(value[0])
    lable=int(value[1])
    X_test.append([arpu])
    lable_test.append(lable)

label_train=lable_train;
label_dev=lable_dev;
label_test=lable_test;
# Model I: Logistic regression
clf_logistReg = LogisticRegression(random_state=0).fit(X_train, lable_train)

# evaluate toy model on (X_dev, label_dev)
pred_dev = clf_logistReg.predict(X_dev)
evaluate(label_dev, pred_dev, model='Logistic Regression')
# evaluate toy model on (X_test, label_test)
pred_test = clf_logistReg.predict(X_test)
evaluate(label_test, pred_test, model='Logistic Regression')

# Model II: Logistic regression CV
clf_logistRegCV = LogisticRegressionCV(cv=5, random_state=0).fit(X_train, label_train)

# evaluate toy model on (X_dev, label_dev)
pred_dev = clf_logistRegCV.predict(X_dev)
evaluate(label_dev, pred_dev, model='Logistic Regression CV=5')

# evaluate toy model on (X_test, label_test)
pred_test = clf_logistRegCV.predict(X_test)
evaluate(label_test, pred_test, model='Logistic Regression CV=5')

# Model III: percepton
from sklearn.linear_model import Perceptron
clf_perceptron = Perceptron(tol=1e-3, random_state=0)
clf_perceptron.fit(X_train, label_train)

# evaluate toy model on (X_dev, label_dev)
pred_dev = clf_perceptron.predict(X_dev)
evaluate(label_dev, pred_dev, model='Perceptron')

# evaluate toy model on (X_test, label_test)
pred_test = clf_perceptron.predict(X_test)
evaluate(label_test, pred_test, model='Perceptron')

# Model IV: RidgeClassifier
from sklearn.linear_model import RidgeClassifier
clf_ridgeClassifier = RidgeClassifier().fit(X_train, label_train)

# evaluate toy model on (X_dev, label_dev)
pred_dev = clf_ridgeClassifier.predict(X_dev)
evaluate(label_dev, pred_dev, model='Ridge Classification')

# evaluate toy model on (X_test, label_test)
pred_test = clf_ridgeClassifier.predict(X_test)
evaluate(label_test, pred_test, model='Ridge Classification')

#



print(666)