#!/usr/bin/env python3

# import generic modules
import sys
import random
sys.path.append('../')
from hwk.old.data_process_hwk import *
from utils import evaluate
# import model modules
from models.LogisticRegression import LogisticRegression
from models.LogisticRegressionCV import LogisticRegressionCV
train_user_path = '../data/train/train_user.csv'
train_voc_path = '../data/train/train_voc.csv'
train_sms_path = '../data/train/train_sms.csv'
idcardMon_smsInfo_dict=get_sms_data(train_sms_path)
idcardMon_vocInfo_dict=get_voc_data(train_voc_path)

idcardMon_userInfo_dict=get_user_data(train_user_path)
idcardMon=list(idcardMon_userInfo_dict.keys())
idcardSet=set();
for im in idcardMon:
    idcardSet.add(im[0])
idcardList=list(idcardSet)
random.shuffle(idcardList)


# ids=range(len(idcardMon))
# random.shuffle(ids)

# set the data file parameters
num_total = len(idcardList)
num_train = int(num_total * 0.8)
num_dev = int(num_total * 0.1)
num_test = num_total - num_train - num_dev

idcard_train=set(idcardList[:num_train]);
idcard_dev=set(idcardList[num_train:num_train+num_dev]);
idcard_test=set(idcardList[num_train+num_dev:num_train+num_dev+num_test]);


X_train=[]
lable_train=[]
X_dev=[]
lable_dev=[]
X_test=[]
lable_test=[]

for key in idcardMon:
    if key not in idcardMon_vocInfo_dict:
        FrequentContactsNum=-1
        ContactsNum=-1
        ShortCallNum=-1
        LongCallNum = -1
    else:
        voc_value=idcardMon_vocInfo_dict[key]
        FrequentContactsNum=get_voc_FrequentContactsNum(voc_value)
        ContactsNum = get_voc_ContactsNum(voc_value)
        ShortCallNum=get_voc_ShortCallNum(voc_value)
        LongCallNum = get_voc_LongCallNum(voc_value)

    if key not in idcardMon_smsInfo_dict:
        SmsNum=-1

    else:
        sms_value=idcardMon_smsInfo_dict[key]
        SmsNum = get_sms_SmsNum(sms_value)

    value=idcardMon_userInfo_dict[key]
    arpu=float(value[-2])
    idcard_cnt=float(value[2])
    feature=[idcard_cnt,arpu,FrequentContactsNum,ContactsNum,ShortCallNum,SmsNum]
    lable=int(value[-1])
    if key[0] in  idcard_train:
        X_train.append(feature)
        lable_train.append(lable)
    if key[0] in  idcard_dev:
        X_dev.append(feature)
        lable_dev.append(lable)
    if key[0] in  idcard_test:
        X_test.append(feature)
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
# Model V: AdaBoostClassifier
from sklearn.ensemble import AdaBoostClassifier
clf_AdaBoost = AdaBoostClassifier(n_estimators=100, random_state=0)
clf_AdaBoost.fit(X_train, label_train)

# evaluate toy model on (X_dev, label_dev)
pred_dev = clf_AdaBoost.predict(X_dev)
evaluate(label_dev, pred_dev, model='Adaboost')

# evaluate toy model on (X_test, label_test)
pred_dev = clf_AdaBoost.predict(X_test)
evaluate(label_test, pred_test, model='Adaboost')


# Model VII: random forest
from sklearn.ensemble import RandomForestClassifier
clf_randforest = RandomForestClassifier(max_depth=2, random_state=0)
clf_randforest.fit(X_train, label_train)

# evaluate toy model on (X_dev, label_dev)
pred_dev = clf_randforest.predict(X_dev)
evaluate(label_dev, pred_dev, model='Random forest')

# evaluate toy model on (X_test, label_test)
pred_test = clf_randforest.predict(X_test).tolist()
evaluate(label_test, pred_test, model='Random forest')
print(666)