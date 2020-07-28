#!/usr/bin/env python3

# import global modules
import sys
import os
import csv
import numpy as np
from sklearn import metrics
import joblib
from sklearn.grid_search import GridSearchCV
# from sklearn.preprocessing import normalize
sys.path.append('../../')

# import local modules
from utils import evaluate, modify_months_config
from data_process_new import split_data, get_features, get_label, get_phone_no_m
from models.LogisticRegression import LogisticRegression
from models.LogisticRegressionCV import LogisticRegressionCV
from models.ensemble_model import ensemble

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
train_config_yml = '../configs/A1_2_4_5_7_9_10_12-30_36-42B1_3-9_11-13C1-6D1-3_config_train.yml'
blindTest_config_yml = '../configs/A1_2_4_5_7_9_10_12-30_36-42B1_3-9_11-13C1-6D1-3_config_blind_test.yml'
extTest_config_yml = '../configs/A1_2_4_5_7_9_10_12-30_36-42B1_3-9_11-13C1-6D1-3_config_ext_test.yml'

# set months of internal test data
inter_test_months = ['2019-11']
modify_months_config(train_config_yml, new_months=inter_test_months)

features_name = 'A1_2_4_5_7_9_10_12-30_36-42B1_3-9_11-13C1-6D1-3'

# get design matrix and label according to months
label_train = get_label(train_file)
num_train_positive = len([1 for i in label_train if i==1])
ind_train_positive = [i for i, n in enumerate(label_train) if n == 1]
label_train.extend([1]*num_train_positive)

label_dev = get_label(dev_file)
label_inter_test = get_label(inter_test_file)
label_exter_test = get_label(exter_test_user)

phone_no_m_blindtest = get_phone_no_m(blind_test_user)

print('size of training data: ', len(label_train))
print('1 in training data: ', len([1 for i in label_train if i==1]))
print('0 in training data: ', len([0 for i in label_train if i==0]))

# all data in training
label_train_all = label_train
label_train_all.extend(label_dev)
label_train_all.extend(label_inter_test)

print('size of all training data: ', len(label_train_all))
print('1 in all training data: ', len([1 for i in label_train_all if i==1]))
print('0 in all training data: ', len([0 for i in label_train_all if i==0]))

X_blindtest = get_features(blind_test_user, blind_test_voc, blind_test_sms, blind_test_app, blindTest_config_yml)
X_inter_test = get_features(inter_test_file, train_voc, train_sms, train_app, train_config_yml)
X_exter_test = get_features(exter_test_user, exter_test_voc, exter_test_sms, exter_test_app, extTest_config_yml)

## create test_results dir
if not os.path.exists('../test_results/'+features_name+'/'):
    os.mkdir('../test_results/'+features_name+'/')

months_lst = [['2019-08', '2019-09', '2019-10', '2019-11', '2020-01', '2020-02', '2020-03'],
              ['2019-08'], ['2019-09'], ['2019-10'], ['2019-11'], ['2019-12'], ['2020-01'], 
              ['2020-02'], ['2020-03']]

gradboost_blindAcc = {"2019-08_2019-09_2019-10_2019-11_2020-01_2020-02_2020-03": 0.01,
                      '2019-08': 0.62, '2019-09': 0.8, '2019-10': 0.8, '2019-11': 0.75,
                      '2019-12': 0.78, '2020-01': 0.72, '2020-02': 0.76, '2020-03': 0.77}

clf_gradboostAcc_months = {}

for months in months_lst:
    # update the months in config_yaml file
    modify_months_config(train_config_yml, new_months=months)

    X_train = get_features(train_file, train_voc, train_sms, train_app, train_config_yml)
    X_train.extend((np.array(X_train)[ind_train_positive]).tolist())

    X_dev = get_features(dev_file, train_voc, train_sms, train_app, train_config_yml)

    # train final model on all data files
    X_test_internal = get_features(inter_test_file, train_voc, train_sms, train_app, train_config_yml)

    X_train_all = X_train
    X_train_all.extend(X_dev)
    X_train_all.extend(X_test_internal)

    # model: accuracy
    dict_model_acc_dev = {}
    dict_model_acc_test = {}

    # model training and inference
    ## Model I: Logistic regression

    clf_logistReg = LogisticRegression(random_state=0).fit(X_train, label_train)

    y_predprob = clf_logistReg.predict_proba(X_inter_test)[:, 1]
    print('AUC score (Train) of logistic regression: %f' % metrics.roc_auc_score(label_inter_test, y_predprob))

    ### evaluate toy model on (X_dev, label_dev)
    pred_dev = clf_logistReg.predict(X_dev).tolist()

    ### evaluate toy model on (X_test, label_test)
    pred_inter_test = clf_logistReg.predict(X_inter_test).tolist()
    pred_exter_test = clf_logistReg.predict(X_exter_test).tolist()

    clf_logistReg = LogisticRegression(random_state=0).fit(X_train_all, label_train_all)
    dict_model_acc_dev['logistReg'] = (clf_logistReg, evaluate(label_dev, pred_dev, model='Logistic Regression'))
    dict_model_acc_test['logistReg'] = (clf_logistReg, evaluate(label_inter_test, pred_inter_test, model='Logistic Regression'))
    evaluate(label_exter_test, pred_exter_test, model='Logistic Regression')
    
    ## Model II: Logistic regression CV
    clf_logistRegCV = LogisticRegressionCV(cv=5, random_state=0).fit(X_train, label_train)

    y_predprob = clf_logistRegCV.predict_proba(X_inter_test)[:, 1]
    print('AUC score (Train) of logistic regression CV: %f' % metrics.roc_auc_score(label_inter_test, y_predprob))

    ### evaluate toy model on (X_dev, label_dev)
    pred_dev = clf_logistRegCV.predict(X_dev).tolist()

    ### evaluate toy model on (X_test, label_test)
    pred_inter_test = clf_logistRegCV.predict(X_inter_test).tolist()
    pred_exter_test = clf_logistRegCV.predict(X_exter_test).tolist()

    clf_logistRegCV = LogisticRegressionCV(cv=5, random_state=0).fit(X_train_all, label_train_all)
    dict_model_acc_dev['logistRegCV'] = (clf_logistRegCV, evaluate(label_dev, pred_dev, model='Logistic Regression CV=5'))
    dict_model_acc_test['logistRegCV'] = (clf_logistRegCV, evaluate(label_inter_test, pred_inter_test, model='Logistic Regression CV=5'))
    evaluate(label_exter_test, pred_exter_test, model='Logistic Regression CV=5')

    ## Model IV: RidgeClassifier
    from sklearn.linear_model import RidgeClassifier
    clf_ridgeClassifier = RidgeClassifier().fit(X_train, label_train)

    ### evaluate toy model on (X_dev, label_dev)
    pred_dev = clf_ridgeClassifier.predict(X_dev).tolist()

    ### evaluate toy model on (X_test, label_test)
    pred_inter_test = clf_ridgeClassifier.predict(X_inter_test).tolist()
    pred_exter_test = clf_ridgeClassifier.predict(X_exter_test).tolist()

    clf_ridgeClassifier = RidgeClassifier().fit(X_train_all, label_train_all)
    dict_model_acc_dev['ridgeClassifier'] = (clf_ridgeClassifier, evaluate(label_dev, pred_dev, model='Ridge Classification'))
    dict_model_acc_test['ridgeClassifier'] = (clf_ridgeClassifier, evaluate(label_inter_test, pred_inter_test, model='Ridge Classification'))
    evaluate(label_exter_test, pred_exter_test, model='Ridge Classification')

    ## Model V: AdaBoostClassifier
    from sklearn.ensemble import AdaBoostClassifier
    clf_AdaBoost = AdaBoostClassifier(n_estimators=100, random_state=0)
    clf_AdaBoost.fit(X_train, label_train)

    ### evaluate toy model on (X_dev, label_dev)
    pred_dev = clf_AdaBoost.predict(X_dev).tolist()

    ### evaluate toy model on (X_test, label_test)
    pred_inter_test = clf_AdaBoost.predict(X_inter_test).tolist()
    pred_exter_test = clf_AdaBoost.predict(X_exter_test).tolist()

    clf_AdaBoost = AdaBoostClassifier(n_estimators=100, random_state=0)
    clf_AdaBoost.fit(X_train_all, label_train_all)
    dict_model_acc_dev['Adaboost'] = (clf_AdaBoost, evaluate(label_dev, pred_dev, model='Adaboost'))
    dict_model_acc_test['Adaboost'] = (clf_AdaBoost, evaluate(label_inter_test, pred_inter_test, model='Adaboost'))
    evaluate(label_exter_test, pred_exter_test, model='Adaboost')

    ## Model VI: BaggingClassifier
    from sklearn.ensemble import BaggingClassifier
    from sklearn.svm import SVC
    clf_Bagging = BaggingClassifier(base_estimator=SVC(), n_estimators=10, random_state=0)
    clf_Bagging.fit(X_train, label_train)

    ### evaluate toy model on (X_dev, label_dev)
    pred_dev = clf_Bagging.predict(X_dev).tolist()

    ### evaluate toy model on (X_test, label_test)
    pred_inter_test = clf_Bagging.predict(X_inter_test).tolist()
    pred_exter_test = clf_Bagging.predict(X_exter_test).tolist()

    clf_Bagging = BaggingClassifier(base_estimator=SVC(), n_estimators=10, random_state=0)
    clf_Bagging.fit(X_train_all, label_train_all)
    dict_model_acc_dev['Bagging_SVC'] = (clf_Bagging, evaluate(label_dev, pred_dev, model='Bagging_SVC'))
    dict_model_acc_test['Bagging_SVC'] = (clf_Bagging, evaluate(label_inter_test, pred_inter_test, model='Bagging_SVC'))
    evaluate(label_exter_test, pred_exter_test, model='Bagging_SVC')

    ## Model VII: random forest
    from sklearn.ensemble import RandomForestClassifier
    # tune parameters for random forest
    #para_test1 = {'min_samples_leaf': list(range(10, 60, 10)), 'max_features': list(range(2, 20, 2))}
    #para_test1 = {'n_estimators': list(range(20, 200, 10))}
    #para_test1 = {'max_depth': list(range(3, 14, 2)), 'min_samples_split': list(range(50, 201, 20))}
    #gsearch1 = GridSearchCV(estimator=RandomForestClassifier(n_estimators=160, min_samples_leaf=10, max_features=10,
    #                                                         max_depth=5, min_samples_split=50, random_state=10),
    #                        param_grid=para_test1, scoring='roc_auc', iid=False, cv=5)

    #gsearch1.fit(X_test, label_test)
    #print(gsearch1.grid_scores_, gsearch1.best_params_, gsearch1.best_score_)

    # fit random forest model
    clf_randforest = RandomForestClassifier(n_estimators=160, max_features=10, min_samples_leaf=10, max_depth=5,
                                            min_samples_split=50, random_state=10)

    clf_randforest.fit(X_train, label_train)

    y_predprob = clf_randforest.predict_proba(X_inter_test)[:, 1]
    print('AUC score (Train) of random forest: %f' % metrics.roc_auc_score(label_inter_test, y_predprob))

    ### evaluate toy model on (X_dev, label_dev)
    pred_dev = clf_randforest.predict(X_dev).tolist()

    ### evaluate toy model on (X_test, label_test)
    pred_inter_test = clf_randforest.predict(X_inter_test).tolist()
    pred_exter_test = clf_randforest.predict(X_exter_test).tolist()

    clf_randforest = RandomForestClassifier(n_estimators=160, max_features=10, min_samples_leaf=10, max_depth=5,
                                            min_samples_split=50, random_state=10)

    clf_randforest.fit(X_train_all, label_train_all)
    dict_model_acc_dev['Random_forest'] = (clf_randforest, evaluate(label_dev, pred_dev, model='Random forest'))
    dict_model_acc_test['Random_forest'] = (clf_randforest, evaluate(label_inter_test, pred_inter_test, model='Random forest'))
    evaluate(label_exter_test, pred_exter_test, model='Random forest')

    ## Model VIII: Gradientboosting
    from sklearn.ensemble import GradientBoostingClassifier
    # tune parameters for gradient boosting
    #para_test1 = {'min_samples_leaf': list(range(10, 60, 10)), 'max_features': list(range(2, 20, 2))}
    #para_test1 = {'n_estimators': list(range(20, 200, 10))}
    #para_test1 = {'max_depth': list(range(3, 14, 2)), 'min_samples_split': list(range(50, 201, 20))}
    #gsearch1 = GridSearchCV(estimator=GradientBoostingClassifier(n_estimators=90, max_features=8, min_samples_leaf=20,
    #                                                             max_depth=11, min_samples_split=50, random_state=10),
    #                        param_grid=para_test1, scoring='roc_auc', iid=False, cv=5)

    #gsearch1.fit(X_test, label_test)
    #print(gsearch1.grid_scores_, gsearch1.best_params_, gsearch1.best_score_)

    clf_gradboost = GradientBoostingClassifier(n_estimators=90, max_features=8, min_samples_leaf=20, max_depth=11,
                                               min_samples_split=50, random_state=10)
    clf_gradboost.fit(X_train_all, label_train_all)
    y_predprob = clf_gradboost.predict_proba(X_inter_test)[:, 1]
    print('AUC score (Train) of gradient boosting: %f' % metrics.roc_auc_score(label_inter_test, y_predprob))

    ### evaluate toy model on (X_dev, label_dev)
    pred_dev = clf_gradboost.predict(X_dev).tolist()

    ### evaluate toy model on (X_test, label_test)
    pred_inter_test = clf_gradboost.predict(X_inter_test).tolist()
    pred_exter_test = clf_gradboost.predict(X_exter_test).tolist()

    #clf_gradboost = GradientBoostingClassifier(n_estimators=90, max_features=8, min_samples_leaf=20, max_depth=11,
    #                                           min_samples_split=50, random_state=10)
    #clf_gradboost.fit(X_train_all, label_train_all)
    dict_model_acc_dev['Gradient_boosting'] = (clf_gradboost, evaluate(label_dev, pred_dev, model='Gradient boosting'))
    dict_model_acc_test['Gradient_boosting'] = (clf_gradboost, evaluate(label_inter_test, pred_inter_test, model='Gradient boosting'))
    evaluate(label_exter_test, pred_exter_test, model='Gradient boosting')

    ### collect models in months
    clf_gradboostAcc_months['_'.join(months)] = (clf_gradboost, gradboost_blindAcc['_'.join(months)])

    ## Model IX: MLP Classifier
    from sklearn.neural_network import MLPClassifier
    clf_mlp = MLPClassifier(random_state=1, max_iter=300).fit(X_train, label_train)

    y_predprob = clf_mlp.predict_proba(X_inter_test)[:, 1]
    print('AUC score (Train) of mlp: %f' % metrics.roc_auc_score(label_inter_test, y_predprob))

    ### evaluate toy model on (X_dev, label_dev)
    pred_dev = clf_mlp.predict(X_dev).tolist()

    ### evaluate toy model on (X_test, label_test)
    pred_inter_test = clf_mlp.predict(X_inter_test).tolist()
    pred_exter_test = clf_mlp.predict(X_exter_test).tolist()

    clf_mlp = MLPClassifier(random_state=1, max_iter=300).fit(X_train_all, label_train_all)
    dict_model_acc_dev['MLP'] = (clf_mlp, evaluate(label_dev, pred_dev, model='MLP'))
    dict_model_acc_test['MLP'] = (clf_mlp, evaluate(label_inter_test, pred_inter_test, model='MLP'))
    evaluate(label_exter_test, pred_exter_test, model='MLP')

    ## Model X: SVM
    from sklearn.svm import LinearSVC
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler

    clf_svm = make_pipeline(StandardScaler(), LinearSVC(random_state=0, tol=1e-5))
    clf_svm.fit(X_train, label_train)

    ### evaluate toy model on (X_dev, label_dev)
    pred_dev = clf_svm.predict(X_dev).tolist()

    ### evaluate toy model on (X_test, label_test)
    pred_inter_test = clf_svm.predict(X_inter_test).tolist()
    pred_exter_test = clf_svm.predict(X_exter_test).tolist()

    clf_svm = make_pipeline(StandardScaler(), LinearSVC(random_state=0, tol=1e-5))
    clf_svm.fit(X_train_all, label_train_all)
    dict_model_acc_dev['SVM'] = (clf_svm, evaluate(label_dev, pred_dev, model='SVM'))
    dict_model_acc_test['SVM'] = (clf_svm, evaluate(label_inter_test, pred_inter_test, model='SVM'))
    evaluate(label_exter_test, pred_exter_test, model='SVM')

    ## model ensemble (top K accuracy models ensemble)
    ### construct dictionary with topK models: {'model1': accuracy1, ... , 'modelK': accuracyK}
    dict_topK_model_acc_dev = dict(sorted(dict_model_acc_dev.items(), key=lambda x: x[1][1], reverse=True)[:num_ensemble])
    dict_topK_model_acc_test = dict(sorted(dict_model_acc_test.items(), key=lambda x: x[1][1], reverse=True)[:num_ensemble])

    ### evaluate ensemble model on (X_dev, label_dev)
    pred_dev = ensemble(dict_topK_model_acc_dev, X_dev, method='vote')
    evaluate(label_dev, pred_dev, model='topK_vote')

    ### evaluate ensemble model on (X_test, label_test)
    pred_inter_test = ensemble(dict_topK_model_acc_test, X_inter_test, method='vote')
    evaluate(label_inter_test, pred_inter_test, model='topK_vote')
    pred_exter_test = ensemble(dict_topK_model_acc_test, X_exter_test, method='vote')
    evaluate(label_exter_test, pred_exter_test, model='topK_vote')

    ### evaluate ensemble model on (X_dev, label_dev)
    if 'Bagging_SVC' in dict_topK_model_acc_dev.keys():
        dict_topK_model_acc_dev.pop('Bagging_SVC')

    if 'Bagging_SVC' in dict_topK_model_acc_test.keys():
        dict_topK_model_acc_test.pop('Bagging_SVC')

    if 'SVM' in dict_topK_model_acc_dev.keys():
        dict_topK_model_acc_dev.pop('SVM')

    if 'SVM' in dict_topK_model_acc_test.keys():
        dict_topK_model_acc_test.pop('SVM')

    if 'ridgeClassifier' in dict_topK_model_acc_dev.keys():
        dict_topK_model_acc_dev.pop('ridgeClassifier')

    if 'ridgeClassifier' in dict_topK_model_acc_test.keys():
        dict_topK_model_acc_test.pop('ridgeClassifier')


    pred_dev = ensemble(dict_topK_model_acc_dev, X_dev, method='avg_unif')
    evaluate(label_dev, pred_dev, model='topK_avg_unif')

    ### evaluate ensemble model on (X_test, label_test)
    pred_inter_test = ensemble(dict_topK_model_acc_test, X_inter_test, method='avg_unif')
    evaluate(label_inter_test, pred_inter_test, model='topK_avg_unif')
    pred_exter_test = ensemble(dict_topK_model_acc_test, X_exter_test, method='avg_unif')
    evaluate(label_exter_test, pred_exter_test, model='topK_avg_unif')

    ### evaluate ensemble model on (X_dev, label_dev)
    pred_dev = ensemble(dict_topK_model_acc_dev, X_dev, method='avg_softmax')
    evaluate(label_dev, pred_dev, model='topK_avg_softmax')

    ### evaluate ensemble model on (X_test, label_test)
    pred_inter_test = ensemble(dict_topK_model_acc_test, X_inter_test, method='avg_softmax')
    evaluate(label_inter_test, pred_inter_test, model='topK_avg_softmax')
    pred_exter_test = ensemble(dict_topK_model_acc_test, X_exter_test, method='avg_softmax')
    evaluate(label_exter_test, pred_exter_test, model='topK_avg_softmax')

    # predict labels on blind test set and write to xlsx file for submitting
    ## ensemble classifier (topK_avg_softmax)
    pred_blindtest = ensemble(dict_topK_model_acc_test, X_blindtest, method='avg_softmax')
    month_train = '_'.join(months)
    with open('../test_results/' + features_name + '/' + 'topK_avg_softmax_' + month_train + '.csv',
              'w', newline='', encoding='utf-8') as fout:
        field_names = ['phone_no_m', 'label']
        writer = csv.DictWriter(fout, fieldnames=field_names)
        writer.writeheader()

        for phone, pred in zip(phone_no_m_blindtest, pred_blindtest):
            writer.writerow({'phone_no_m': phone, 'label': pred})

    ## ensemble classifier (topK_vote)
    pred_blindtest = ensemble(dict_topK_model_acc_test, X_blindtest, method='vote')
    month_train = '_'.join(months)
    with open('../test_results/' + features_name + '/' + 'topK_vote_' + month_train + '.csv',
              'w', newline='', encoding='utf-8') as fout:
        field_names = ['phone_no_m', 'label']
        writer = csv.DictWriter(fout, fieldnames=field_names)
        writer.writeheader()

        for phone, pred in zip(phone_no_m_blindtest, pred_blindtest):
            writer.writerow({'phone_no_m': phone, 'label': pred})

    ## ensemble classifier (topK_avg_unif)
    pred_blindtest = ensemble(dict_topK_model_acc_test, X_blindtest, method='avg_unif')
    month_train = '_'.join(months)
    with open('../test_results/' + features_name + '/' + 'topK_avg_unif_' + month_train + '.csv',
              'w', newline='', encoding='utf-8') as fout:
        field_names = ['phone_no_m', 'label']
        writer = csv.DictWriter(fout, fieldnames=field_names)
        writer.writeheader()

        for phone, pred in zip(phone_no_m_blindtest, pred_blindtest):
            writer.writerow({'phone_no_m': phone, 'label': pred})

    ## gradboost classifier
    pred_blindtest = clf_gradboost.predict(X_blindtest).tolist()

    month_train = '_'.join(months)    # month_train should be the same as in config_train.yml

    with open('../test_results/' + features_name + '/' + 'GradientBoosting_' + month_train + '.csv',
              'w', newline='', encoding='utf-8') as fout:
        field_names = ['phone_no_m', 'label']
        writer = csv.DictWriter(fout, fieldnames=field_names)
        writer.writeheader()

        for phone, pred in zip(phone_no_m_blindtest, pred_blindtest):
            writer.writerow({'phone_no_m': phone, 'label': pred})

# ensemble model (vote/avg_unif/avg_softmax)
## vote
dict_model_acc = clf_gradboostAcc_months
pred_vote_blindtest = ensemble(dict_model_acc, X_blindtest, method='vote')

month_train = '201908-202003'    # month should be the same as in config_train.yml

with open('../test_results/' + features_name + '/' + 'vote_gradboost_' + month_train + '.csv',
          'w', newline='', encoding='utf-8') as fout:
    field_names = ['phone_no_m', 'label']
    writer = csv.DictWriter(fout, fieldnames=field_names)
    writer.writeheader()

    for phone, pred in zip(phone_no_m_blindtest, pred_vote_blindtest):
        writer.writerow({'phone_no_m': phone, 'label': pred})

## avg_unif
pred_avgunif_blindtest = ensemble(dict_model_acc, X_blindtest, method='avg_unif')

with open('../test_results/' + features_name + '/' + 'avgunif_gradboost_' + month_train + '.csv',
          'w', newline='', encoding='utf-8') as fout:
    field_names = ['phone_no_m', 'label']
    writer = csv.DictWriter(fout, fieldnames=field_names)
    writer.writeheader()

    for phone, pred in zip(phone_no_m_blindtest, pred_avgunif_blindtest):
        writer.writerow({'phone_no_m': phone, 'label': pred})

## avg_softmax
pred_avgsoftmax_blindtest = ensemble(dict_model_acc, X_blindtest, method='avg_softmax')

with open('../test_results/' + features_name + '/' + 'avgsoftmax_gradboost_' + month_train + '.csv',
          'w', newline='', encoding='utf-8') as fout:
    field_names = ['phone_no_m', 'label']
    writer = csv.DictWriter(fout, fieldnames=field_names)
    writer.writeheader()

    for phone, pred in zip(phone_no_m_blindtest, pred_avgsoftmax_blindtest):
        writer.writerow({'phone_no_m': phone, 'label': pred})
