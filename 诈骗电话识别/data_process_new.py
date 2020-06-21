#!/usr/bin/env python3

# import modules
import csv
import os
import numpy as np
import yaml
import pandas as pd
import pickle
import time
from itertools import groupby

# split the data into train/dev/test
def split_data(origin_file, num_train, num_dev, num_test, replace=True):
    """split data into train/dev/test"""
    num_origin = num_train + num_dev + num_test
    ids_origin = np.arange(num_origin)
    np.random.shuffle(ids_origin)
    ids_train = ids_origin[:num_train]
    ids_dev   = ids_origin[num_train:num_dev+num_train]
    ids_test   = ids_origin[num_train+num_dev:num_origin]

    with open(origin_file, encoding='utf-8') as file_orig:
        lines = []
        for line in file_orig:
            if line.endswith('label\n'):
                header = line
            else:
                line = line.strip() + '\n'
                lines.append(line)
        # collect lines
        lines_train = [lines[i] for i in ids_train]
        lines_dev = [lines[i] for i in ids_dev]
        lines_test = [lines[i] for i in ids_test]

    dir = '/'.join(origin_file.split('/')[:-1]) + '/split/'
    name = origin_file.split('/')[-1]
    name = name.split('_')[-1]

    # make dir if not exist
    if not os.path.exists(dir):
        os.makedirs(dir)

    # output train/dev/test files.
    for cat, lines in [('train', lines_train), ('dev', lines_dev), ('test', lines_test)]:
        if (not os.path.isfile(dir+cat+'_'+name)) or (replace==True):
            with open(dir+cat+'_'+name, 'w', encoding='utf-8') as file_cat:
                file_cat.writelines(header)
                for line in lines[:-1]:
                    file_cat.writelines(line)
                file_cat.writelines(lines[-1].strip())

    return None

# get voc information by given header (take columns in file)
def get_columns_by_idphone(file_voc_sms_app, columns=['call_dur']):
    """get raw information from *_voc/sms/app.csv file according to column"""
    with open(file_voc_sms_app, newline='', encoding='utf-8') as voc_file:
        vocreader = csv.reader(voc_file, delimiter=',', quotechar='|')
        output_dict = {}
        for line in vocreader:
            # get header and indexes
            if line[0] == 'phone_no_m':
                assert len(columns) > 0
                header_voc = line
                indexes = [ind for ind in range(len(header_voc)) if header_voc[ind] in columns]
                pass
            # take columns (values) according to phone_no_m (key)
            x_phone_no_m = line[0]
            for ind in indexes:
                if x_phone_no_m not in output_dict.keys():
                    output_dict[str(x_phone_no_m)] = []
                output_dict[str(x_phone_no_m)] += [[line[ind] for ind in indexes]]

    return output_dict

# get user dictionary (run it each time)
def get_dict_user(file_user, file_user_dict, columns_user):
    user_csv = pd.read_csv(file_user)
    phone_no_m = user_csv['phone_no_m']
    dict_user = {}

    # load or create dict (pickle)
    for phone in phone_no_m:
        if len(columns_user) == 0:
            dict_user[phone] = pd.DataFrame([], columns=[])
        else:
            dict_user[phone] = user_csv[user_csv['phone_no_m'] == phone][columns_user]

    return dict_user

# get voc dictionary
def get_dict_voc(file_voc, file_voc_dict, columns_user):

    # load or create dict (pickle)
    if not os.path.isfile(file_voc_dict):
        voc_csv = pd.read_csv(file_voc)
        phone_no_m = voc_csv['phone_no_m']
        phone_no_m_uniq = set(phone_no_m.tolist())
        dict_voc = {}
        for phone in phone_no_m_uniq:
            if len(columns_user) == 0:
                dict_voc[phone] = pd.DataFrame([], columns=[])
            else:
                dict_voc[phone] = voc_csv[voc_csv['phone_no_m'] == phone][columns_voc]
        with open(file_voc_dict, 'wb') as fout:
            pickle.dump(dict_voc, fout)
    else:
        with open(file_voc_dict, 'rb') as fin:
            dict_voc = pickle.load(fin)
    return dict_voc

# get sms dictionary
def get_dict_sms(file_sms, file_sms_dict, columns_sms):
    # load or create dict (pickle)
    if not os.path.isfile(file_sms_dict):
        sms_csv = pd.read_csv(file_sms)
        phone_no_m = sms_csv['phone_no_m']
        phone_no_m_uniq = set(phone_no_m.tolist())
        dict_sms = {}
        for phone in phone_no_m_uniq:
            if len(columns_sms) == 0:
                dict_sms[phone] = pd.DataFrame([], columns=[])
            else:
                dict_sms[phone] = sms_csv[sms_csv['phone_no_m'] == phone][columns_sms]
        with open(file_sms_dict, 'wb') as fout:
            pickle.dump(dict_sms, fout)
    else:
        with open(file_sms_dict, 'rb') as fin:
            dict_sms = pickle.load(fin)

    return dict_sms

# get app dictionary
def get_dict_app(file_sms, file_app_dict, columns_app):
    if not os.path.isfile(file_app_dict):
        app_csv = pd.read_csv(file_app)
        phone_no_m = app_csv['phone_no_m']
        phone_no_m_uniq = set(phone_no_m.tolist())
        dict_app = {}
        for phone in phone_no_m_uniq:
            if len(columns_app) == 0:
                dict_app[phone] = pd.DataFrame([], columns=[])
            else:
                dict_app[phone] = app_csv[app_csv['phone_no_m'] == phone][columns_app]
        with open(file_app_dict, 'wb') as fout:
            pickle.dump(dict_app, fout)
    else:
        with open(file_app_dict, 'rb') as fin:
            dict_app = pickle.load(fin)

    return dict_app

# get model features from csv
def get_features(file_user, file_voc, file_sms, file_app, config_yml):
    """extract labels and features from given file and configuration file"""
    # take parameters from config_yml file
    with open(config_yml) as file:
        def_para = yaml.load(file)
        def_para_columns = {}
        def_para_features = {}

        def_para_name = def_para['name']
        def_para_columns = def_para['columns'][0]
        for item in def_para['features']:
            def_para_features[list(item.keys())[0]] = list(item.values())[0]

        ## get columns parameter
        columns_user = def_para_columns['user']
        columns_voc = def_para_columns['voc']
        columns_sms = def_para_columns['sms']
        columns_app = def_para_columns['app']

        ## get features parameter
        features = []
        for key in def_para_features.keys():
            feature = def_para_features[key][0]
            features.append(feature)

    # get the output directory
    if 'train' in file_voc:
        output_dir = './data/features/train/'
    elif 'test' in file_voc:
        output_dir = './data/features/test/'

    # take columns from *_user/_call/_sms/_app.csv to get dictionary
    ## from *_user.csv
    print(time.time())
    file_user_dict = output_dir + 'user_dict.txt'
    dict_user = get_dict_user(file_user, file_user_dict, columns_user)
    print(time.time())
    ## from *_voc.csv
    file_voc_dict = output_dir + 'voc_dict.txt'
    dict_voc = get_dict_voc(file_voc, file_voc_dict, columns_voc)
    print(time.time())
    ## from *_sms.csv
    file_sms_dict = output_dir + 'sms_dict.txt'
    dict_sms = get_dict_sms(file_sms, file_sms_dict, columns_sms)
    print(time.time())
    ## from *_app.csv
    file_app_dict = output_dir + 'app_dict.txt'
    dict_app = get_dict_app(file_app, file_app_dict, columns_app)
    print(time.time())
    # generate features
    X = []
    for user_phone_no in dict_user.keys():
        for feature in features:
            name_feature = feature['name']
            columns_feature = feature['columns'][0]
            columns_feature = dict([(key, [key+'_'+column for column in columns_feature[key]]) for key in columns_feature.keys()])

            ## take columns form dict
            print(dict_app[user_phone_no])
            for key in columns_feature.keys():
                exec('dict_%s_phone_no = dict_%s["%s"]' % (key, key, user_phone_no))
                for col in columns_feature[key]:
                    exec('%s = %s["%s"]' % (col, 'dict_'+key+'_phone_no', col.split(key+'_')[1]))
                    print('%s = %s["%s"]' % (col, 'dict_'+key+'_phone_no', col.split(key+'_')[1]))
    #     formulae = feature['formulae']
    #     x_feature = exec(formulae)
    #     X.features.append(x_feature)


# Debug Part
file_user = './data/train/train_user.csv'
file_voc = './data/train/train_voc.csv'
file_sms = './data/train/train_sms.csv'
file_app = './data/train/train_app.csv'
config_yml = './daijun/configs/A1_B1_C1_config.yml'

get_features(file_user, file_voc, file_sms, file_app, config_yml)
