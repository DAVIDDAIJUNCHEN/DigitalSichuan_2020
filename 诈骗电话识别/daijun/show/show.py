import pickle
import numpy as np
import yaml
import matplotlib.pyplot as plt
#!/usr/bin/env python3

# import global modules
import sys
import os
import csv
import numpy as np
import warnings
import pandas as pd
import pickle
warnings.filterwarnings('ignore')
sys.path.append('../../')
sys.path.append('../codes_feature/')
sys.path.append('../other')

# import local modules
from utils import evaluate, modify_months_config
from data_process_new import split_data, get_features, get_label, get_phone_no_m

#from get_imei_result import get_imei_result


def get_design_months(name_months_dict, config_yml, user_file, voc_file, sms_file, app_file):
    """return dict: {name_months: design_matrix_months}"""

    name_design_dict = {}

    for months_name in name_months_dict.keys():
        months = name_months_dict[months_name]
        modify_months_config(config_yml, new_months=months)
        X_months = get_features(user_file, voc_file, sms_file, app_file, config_yml)

        name_design_dict[months_name] = X_months

    return name_design_dict


def get_subdesign(name_design_dict, index):
    """return design matrix according to index"""
    name_subdesign = {}

    for name in name_design_dict.keys():
        X_name = name_design_dict[name]
        X_ind_array = np.array(X_name)[index]
        name_subdesign[name] = X_ind_array

    return name_subdesign


def train_design_months(name_months_dict, label_train, train_config_yml, user_train, voc_train, sms_train, app_train):
    """return {'normal': name_design_normal, 'fraud': name_design_fraud}"""
    name_design_dict = get_design_months(name_months_dict, train_config_yml, user_train, voc_train, sms_train, app_train)

    index_train_fraud = [ind for ind, label in enumerate(label_train) if label == 1]
    index_train_normal = [ind for ind, label in enumerate(label_train) if label == 0]

    name_design_normal = get_subdesign(name_design_dict, index_train_normal)
    name_design_fraud = get_subdesign(name_design_dict, index_train_fraud)

    return {'normal': name_design_normal, 'fraud': name_design_fraud}


def test_design_months(name_months_dict, test_config_yml, user_test, voc_test, sms_test, app_test):
    """return {name: design_test} """
    name_design_dict = get_design_months(name_months_dict, test_config_yml, user_test, voc_test, sms_test, app_test)
    for name in name_design_dict.keys():
        name_design_dict[name] = np.array(name_design_dict[name])

    return name_design_dict


def plot_features(feature_tag, feature_name, col, train_design_months, test_design_months, out_dir):
    train_design_months_normal = train_design_months['normal']
    train_design_months_fraud = train_design_months['fraud']

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    for name in train_design_months_normal.keys():
        # plot boxplot and hist gram
        col_fraud = train_design_months_fraud[name][:, col].tolist()
        col_normal = train_design_months_normal[name][:, col].tolist()
        col_all_train = col_fraud + col_normal

        fig = plt.figure(feature_name+'_'+name)

        try:
            min_bin = np.percentile(col_all_train, 0)
            max_bin = np.percentile(col_all_train, 90)
            interv = (max_bin - min_bin) / 10
            bins = np.arange(min_bin, max_bin, interv)
        except:
            bins = 10

        # plot box-plot and hist-gram of test data
        col_test = test_design_months['all_months'][:, col].tolist()

        ax1 = plt.subplot(241)
        plt.boxplot(col_test, vert=False, showmeans=True)
        plt.title('Test', fontsize='large')

        ax2 = plt.subplot(242)
        plt.boxplot(col_all_train, vert=False, showmeans=True)
        plt.title('Train', fontsize='large')

        ax3 = plt.subplot(243)
        plt.boxplot(col_fraud, vert=False, showmeans=True)
        plt.title('Fraud', fontsize='large')

        ax4 = plt.subplot(244, sharey=ax3, sharex=ax3)
        plt.boxplot(col_normal, vert=False, showmeans=True)
        plt.title('Normal', fontsize='large')

        ax5 = plt.subplot(245)
        plt.hist(col_test, bins, density=True, facecolor='g')
        plt.grid(True)

        ax6 = plt.subplot(246, sharey=ax5, sharex=ax5)
        plt.hist(col_all_train, bins, density=True, facecolor='g')
        plt.grid(True)

        ax7 = plt.subplot(247, sharey=ax5, sharex=ax5)
        plt.hist(col_fraud, bins, density=True, facecolor='g')
        plt.grid(True)

        ax8 = plt.subplot(248, sharey=ax5, sharex=ax5)
        plt.hist(col_normal, bins, density=True, facecolor='g')
        plt.grid(True)

        plt.suptitle(feature_name + '_' + name, fontsize='x-large')
        fig.set_figheight(10)
        fig.set_figwidth(30)
        fig.savefig(out_dir+'/'+feature_tag+'_'+name+'.png')

if __name__ == '__main__':
    #imie_result = open('../other/imie_result', 'rb')
    #result = pickle.load(imie_result)

    # prepare data and parameter
    train_user = '../../data/train/train_user.csv'
    train_voc = '../../data/train/train_voc.csv'
    train_sms = '../../data/train/train_sms.csv'
    train_app = '../../data/train/train_app.csv'

    test_user = '../../data/test/test_user.csv'
    test_voc = '../../data/test/test_voc.csv'
    test_sms = '../../data/test/test_sms.csv'
    test_app = '../../data/test/test_app.csv'

    train_file = '../../data/train/train_user.csv'
    test_file = '../../data/test/test.user.csv'

    ## define features in train_config_yml and test_config_yml
    train_config_yml = '../configs/show_train.yml'
    test_config_yml = '../configs/show_test.yml'

    with open(train_config_yml) as file:
        def_para = yaml.load(file)
        def_para_columns = {}
        def_para_features = {}
        for item in def_para['features']:
            def_para_features[list(item.keys())[0]] = list(item.values())[0]

    features_lst = list(def_para_features.keys())
    features_name = [def_para_features[feature][0]['name'] for feature in features_lst]

    # get design matrix and label according to months
    label_train = get_label(train_file)

    ## get testing design matrix
    train_name_months_dict = {'all_months': ['2019-08', '2019-09', '2019-10', '2019-11', '2019-12',
                                             '2020-01', '2020-02', '2020-03']}#,
                              #'2019-08': ['2019-08'], '2019-09': ['2019-09'], '2019-10': ['2019-10'],
                              #'2019-11': ['2019-11'], '2019-12': ['2019-12'], '2020-01': ['2020-01'],
                              #'2020-02': ['2020-02'], '2020-03': ['2020-03']}

    test_name_months_dict = {'all_months': ['2020-04']}

    train_design = train_design_months(train_name_months_dict, label_train, train_config_yml,
                                       train_user, train_voc, train_sms, train_app)

    test_design = test_design_months(test_name_months_dict, test_config_yml, test_user,
                                     test_voc, test_sms, test_app)
    out_dir = './figures'

    for col, feature in enumerate(features_name):

        plot_features(features_lst[col], feature, col, train_design, test_design, out_dir)