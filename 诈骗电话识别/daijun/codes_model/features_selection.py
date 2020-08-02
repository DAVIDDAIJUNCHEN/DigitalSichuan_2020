#!/usr/bin/env python3
# import modules
import sys
from sklearn.svm import SVC
from sklearn.model_selection import StratifiedKFold
from sklearn.feature_selection import RFECV
from sklearn.feature_selection import RFE
import matplotlib.pyplot as plt
from sklearn.preprocessing import normalize

sys.path.append('../../')

# import local modules
from utils import evaluate, modify_months_config
from data_process_new import split_data, get_features, get_label, get_phone_no_m

# prepare data and parameter
## train/blind_test/external test user/voc/sms/app files
train_user = '../../data/train/train_user.csv'
train_voc = '../../data/train/train_voc.csv'
train_sms = '../../data/train/train_sms.csv'
train_app = '../../data/train/train_app.csv'

blind_test_user = '../../data/test/test_user.csv'
blind_test_voc = '../../data/test/test_voc.csv'
blind_test_sms = '../../data/test/test_sms.csv'
blind_test_app = '../../data/test/test_app.csv'

exter_test_user = '../../data/test_04/test_user_wLabel.csv'
exter_test_voc = '../../data/test_04/test_voc.csv'
exter_test_sms = '../../data/test_04/test_sms.csv'
exter_test_app = '../../data/test_04/test_app.csv'

## split train_user into train/dev/internal test csv files
train_file = '../../data/train/split/train_user.csv'
dev_file = '../../data/train/split/dev_user.csv'
inter_test_file = '../../data/train/split/test_user.csv'

## set the data file parameters （in splitting）
num_total = 6106
num_train = int(num_total * 0.8)
num_dev = int(num_total * 0.1)
num_test = num_total - num_train - num_dev

# ensemble top K models in each month
num_ensemble = 4

## split data to train/dev/test (only for train_user.csv)
split_data(train_user, num_train, num_dev, num_test, replace=False)

## define features in train_config_yml and blind/external test_config_yml
train_config_yml = '../configs/distinguished_config_train.yml'
blindTest_config_yml = '../configs/distinguished_config_blind_test.yml'
extTest_config_yml = '../configs/distinguished_config_ext_test.yml'

# set months of internal test data
inter_test_months = ['2019-12']
modify_months_config(train_config_yml, new_months=inter_test_months)

features_name = 'distinguished'

# get design matrix and label according to months
label_train = get_label(train_file)
num_train_positive = len([1 for i in label_train if i==1])
ind_train_positive = [i for i, n in enumerate(label_train) if n == 1]

label_dev = get_label(dev_file)
label_inter_test = get_label(inter_test_file)
label_exter_test = get_label(exter_test_user)

# all data in training
label_train_all = label_train.copy()
label_train_all.extend(label_dev)
label_train_all.extend(label_inter_test)

print('size of training data: ', len(label_train))
print('1 in training data: ', len([1 for i in label_train if i==1]))
print('0 in training data: ', len([0 for i in label_train if i==0]))

print('size of all training data: ', len(label_train_all))
print('1 in all training data: ', len([1 for i in label_train_all if i==1]))
print('0 in all training data: ', len([0 for i in label_train_all if i==0]))

#X_blindtest = get_features(blind_test_user, blind_test_voc, blind_test_sms, blind_test_app, blindTest_config_yml)
#X_inter_test = get_features(inter_test_file, train_voc, train_sms, train_app, train_config_yml)
#X_exter_test = get_features(exter_test_user, exter_test_voc, exter_test_sms, exter_test_app, extTest_config_yml)

months_lst = [['2019-08'], ['2019-09'], ['2019-10'], ['2019-11'], ['2019-12'], ['2020-01'], ['2020-02'], ['2020-03']]

for months in months_lst:
    # update the months in config_yaml file
    modify_months_config(train_config_yml, new_months=months)

    X_train = get_features(train_file, train_voc, train_sms, train_app, train_config_yml)

    X_dev = get_features(dev_file, train_voc, train_sms, train_app, train_config_yml)
    X_dev = normalize(X_dev)
    # train final model on all data files
    X_test_internal = get_features(inter_test_file, train_voc, train_sms, train_app, train_config_yml)

    X_train_all = X_train.copy()
    X_train_all.extend(X_dev)
    X_train_all.extend(X_test_internal)

    # Create the RFE object and rank each pixel
    svc = SVC(kernel="linear", C=1)
    rfe = RFE(estimator=svc, n_features_to_select=1, step=1)
    rfe.fit(X_dev, label_dev)
    ranking = rfe.ranking_#.reshape([8, 8])
    print(ranking)
    # Plot pixel ranking
    # plt.matshow(ranking, cmap=plt.cm.Blues)
    # plt.colorbar()
    # plt.title("Ranking of pixels with RFE")
    # plt.show()

    # The "accuracy" scoring is proportional to the number of correct
    # classifications
    rfecv = RFECV(estimator=svc, step=1, cv=StratifiedKFold(2), scoring='accuracy')
    rfecv.fit(X_dev, label_dev)

    print("Optimal number of features : %d" % rfecv.n_features_)

    # Plot number of features VS. cross-validation scores
    plt.figure()
    plt.xlabel("Number of features selected")
    plt.ylabel("Cross validation score (nb of correct classifications)")
    plt.plot(range(1, len(rfecv.grid_scores_) + 1), rfecv.grid_scores_)
    plt.show()



