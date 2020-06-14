#!/usr/bin/env python3

# import modules
import csv
import os
import numpy as np
import pickle
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

    # make dir
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

# get voc information by given header
def get_voc_info(file_voc, column='call_dur'):
    """get raw information from *_voc.csv file accroding to column"""
    with open(file_voc, newline='', encoding='utf-8') as voc_file:
        vocreader = csv.reader(voc_file, delimiter=',', quotechar='|')
        output_dict = {}
        for line in vocreader:
            if line[0] == 'phone_no_m':
                pass
            elif column == 'call_dur':
                x_phone_no_m = line[0]
                if x_phone_no_m not in output_dict.keys():
                    output_dict[str(x_phone_no_m)] = []
                output_dict[str(x_phone_no_m)] += [float(line[4])]
            elif column == 'called_people':
                x_phone_no_m = line[0]
                if x_phone_no_m not in output_dict.keys():
                    output_dict[str(x_phone_no_m)] = []
                output_dict[str(x_phone_no_m)] += [line[1]]
            elif column == 'call_type':
                x_phone_no_m = line[0]
                if x_phone_no_m not in output_dict.keys():
                    output_dict[str(x_phone_no_m)] = []
                output_dict[str(x_phone_no_m)] += [line[2]]

    return output_dict

# get sms information by given header
def get_sms_info(file_sms, column='sms_people'):
    """get raw information from *_sms.csv file according to column"""
    with open(file_sms, newline='', encoding='utf-8') as sms_file:
        smsreader = csv.reader(sms_file, delimiter=',', quotechar="|")
        output_dict = {}
        for line in smsreader:
            if line[0] == 'phone_no_m':
                pass
            elif column == 'sms_people':
                x_phone_no_m = line[0]
                if x_phone_no_m not in output_dict.keys():
                    output_dict[str(x_phone_no_m)] = []
                output_dict[str(x_phone_no_m)] += [line[1]]
            elif column == 'sms_type':
                x_phone_no_m = line[0]
                if x_phone_no_m not in output_dict.keys():
                    output_dict[str(x_phone_no_m)] = []
                output_dict[str(x_phone_no_m)] += [line[2]]
            elif column == 'sms_datetime':
                x_phone_no_m = line[0]
                if x_phone_no_m not in output_dict.keys():
                    output_dict[str(x_phone_no_m)] = []
                output_dict[str(x_phone_no_m)] += [line[3]]
    return output_dict

# get model usable features from csv
def get_usable_data(file_user, file_voc, file_sms, method='idcard_cnt-avg_arpu', get_label=True, get_phone_no=False, num_month=8):
    """extract labels and features from given file"""
    # extract information from *_voc.csv
    if 'train' in file_voc:
        output_dir = '../data/features/train/'
    elif 'test' in file_voc:
        output_dir = '../data/features/test/'

    if 'call_dur' in method:
        file_call_dur_dict = output_dir + 'call_dur_dict.txt'
        # load or create dict (pickle)
        if not os.path.isfile(file_call_dur_dict):
            call_dur_dict = get_voc_info(file_voc, column='call_dur')
            with open(file_call_dur_dict, 'wb') as fout:
                pickle.dump(call_dur_dict, fout)
        else:
            with open(file_call_dur_dict, 'rb') as fin:
                call_dur_dict = pickle.load(fin)

    if 'called_people' in method:
        file_called_people_dict = output_dir + 'called_people_dict.txt'
        # load or create dict (pickle)
        if not os.path.isfile(file_called_people_dict):
            called_people_dict = get_voc_info(file_voc, column='called_people')
            with open(file_called_people_dict, 'wb') as fout:
                pickle.dump(called_people_dict, fout)
        else:
            with open(file_called_people_dict, 'rb') as fin:
                called_people_dict = pickle.load(fin)

    if 'call_type' in method:
        file_call_type_dict = output_dir + 'call_type_dict.txt'
        # load or create dict (pickle)
        if not os.path.isfile(file_call_type_dict):
            call_type_dict = get_voc_info(file_voc, column='call_type')
            with open(file_call_type_dict, 'wb') as fout:
                pickle.dump(call_type_dict, fout)
        else:
            with open(file_call_type_dict, 'rb') as fin:
                call_type_dict = pickle.load(fin)
 
    # extract information from *_sms.csv
    if 'sms_people' in method:
        file_sms_people_dict = output_dir + 'sms_people_dict.txt'
        # load or create dict (pickle)
        if not os.path.isfile(file_sms_people_dict):
            sms_people_dict = get_sms_info(file_sms, column='sms_people')
            with open(file_sms_people_dict, 'wb') as fout:
                pickle.dump(sms_people_dict, fout)
        else:
            with open(file_sms_people_dict, 'rb') as fin:
                sms_people_dict = pickle.load(fin)

    if 'sms_type' in method:
        file_sms_type_dict = output_dir + 'sms_type_dict.txt'
        # load or create dict (pickle)
        if not os.path.isfile(file_sms_type_dict):
            sms_type_dict = get_sms_info(file_sms, column='sms_type')
            with open(file_sms_type_dict, 'wb') as fout:
                pickle.dump(sms_type_dict, fout)
        else:
            with open(file_sms_type_dict, 'rb') as fin:
                sms_type_dict = pickle.load(fin)

    if 'sms_datetime' in method:
        file_sms_datetime_dict = output_dir + 'sms_datetime_dict.txt'
        # load or create dict (pickle)
        if not os.path.isfile(file_sms_datetime_dict):
            sms_datetime_dict = get_sms_info(file_sms, column='sms_datetime')
            with open(file_sms_datetime_dict, 'wb') as fout:
                pickle.dump(sms_datetime_dict, fout)
        else:
            with open(file_sms_datetime_dict, 'rb') as fin:
                sms_datetime_dict = pickle.load(fin)

    with open(file_user, newline='', encoding='utf-8') as user_file:
        spamreader = csv.reader(user_file, delimiter=',', quotechar='|')
        if get_label:
            label = []
        X = []
        phone_no_m = []

        for line in spamreader:
            if ('train' in file_voc) and (line[0] == 'phone_no_m' or len(''.join(line[4:-1])) == 0):
                pass
            elif ('test' in file_voc) and (line[0] == 'phone_no_m'):
                pass
            else:
                # extract features: count of id cards + average arpu
                x_phone_no_m = line[0]
                phone_no_m.append(x_phone_no_m)
                x_idcar_cnt = float(line[3])

                if 'train' in file_voc:
                    x_avg_arpu = np.mean([float(num) for num in line[4:-1] if len(num) > 0])
                    x_std_arpu = np.std([float(num) for num in line[4:-1] if len(num) > 0])
                elif 'test' in file_voc:
                    if len(line[4]) > 0:
                        x_avg_arpu = float(line[4])
                    else:
                        x_avg_arpu = 50.0 # ??
                    x_std_arpu = 0.0

                if get_label:
                    label.append(int(line[-1]))

                if method == 'idcard_cnt-avg_arpu':
                    X.append([x_idcar_cnt, x_avg_arpu])
                elif method == 'idcard_cnt-avg_arpu-std_arpu':
                    X.append([x_idcar_cnt, x_avg_arpu, x_std_arpu])
                elif method == 'idcard_cnt-avg_arpu-std_arpu-call_dur':
                    if x_phone_no_m not in call_dur_dict.keys():
                        x_med_call_dur = 0.0 # if not found call_dur
                        x_std_call_dur = 0.0
                    else:
                        x_med_call_dur = np.median(call_dur_dict[x_phone_no_m])
                        x_std_call_dur = np.std(call_dur_dict[x_phone_no_m])
                    X.append([x_idcar_cnt, x_avg_arpu, x_std_arpu, x_med_call_dur, x_std_call_dur])
                elif method == 'idcard_cnt-avg_arpu-std_arpu-called_people':
                    if x_phone_no_m not in called_people_dict.keys():
                        x_num_called_people = 0.
                    else:
                        x_num_called_people = 1./num_month * len(set(called_people_dict[x_phone_no_m]))
                    X.append([x_idcar_cnt, x_avg_arpu, x_std_arpu, x_num_called_people])
                elif method == 'idcard_cnt-avg_arpu-std_arpu-call_dur-called_people':
                    if x_phone_no_m not in call_dur_dict.keys():
                        #x_med_call_dur = 10 # if not found call_dur
                        x_avg_call_dur = 0.0
                        x_std_call_dur = 1.
                        x_num_called_people = 0.
                    else:
                        #x_med_call_dur = np.median(call_dur_dict[x_phone_no_m])
                        x_avg_call_dur = np.mean(call_dur_dict[x_phone_no_m])
                        x_std_call_dur = np.std(call_dur_dict[x_phone_no_m])
                        x_num_called_people = 1./num_month * float(len(set(called_people_dict[x_phone_no_m])))
                    X.append([x_idcar_cnt, x_avg_arpu, x_std_arpu, x_avg_call_dur, x_std_call_dur, x_num_called_people])
                elif method == 'idcard_cnt-avg_arpu-std_arpu-call_dur-call_type':
                    if x_phone_no_m not in call_dur_dict.keys():
                        #x_med_call_dur = 0 # if not found call_dur
                        x_avg_call_dur = 0.
                        x_std_call_dur = 0.0
                        x_num_callout = 0.
                        x_num_callin = 0.
                        x_num_calltrans = 0.
                    else:
                        #x_med_call_dur = np.median(call_dur_dict[x_phone_no_m])
                        x_avg_call_dur = np.mean(call_dur_dict[x_phone_no_m])
                        x_std_call_dur = np.std(call_dur_dict[x_phone_no_m])
                        x_num_callout = 1./num_month * float(len([1 for i in call_type_dict[x_phone_no_m] if i=='1']))
                        x_num_callin = 1./num_month * float(len([1 for i in call_type_dict[x_phone_no_m] if i=='2']))
                        x_num_calltrans = 1./num_month * float(len([1 for i in call_type_dict[x_phone_no_m] if i=='3']))
                    X.append([x_idcar_cnt, x_avg_arpu, x_std_arpu, x_avg_call_dur, x_std_call_dur, x_num_callout, x_num_callin, x_num_calltrans])
                elif method == 'idcard_cnt-avg_arpu-std_arpu-call_dur-called_people-call_type':
                    if x_phone_no_m not in call_dur_dict.keys():
                        #x_med_call_dur = 0 # if not found call_dur
                        x_avg_call_dur = 0.0
                        x_std_call_dur = 0.0
                        x_num_called_people = 0.0
                        x_num_callout = 0.0
                        x_num_callin = 0.0
                        x_num_calltrans = 0.0
                    else:
                        #x_med_call_dur = np.median(call_dur_dict[x_phone_no_m])
                        x_avg_call_dur = np.mean(call_dur_dict[x_phone_no_m])
                        x_std_call_dur = np.std(call_dur_dict[x_phone_no_m])
                        x_num_called_people = 1./num_month * float(len(set(called_people_dict[x_phone_no_m])))
                        x_num_callout = 1./num_month * float(len([1 for i in call_type_dict[x_phone_no_m] if i == '1']))
                        x_num_callin = 1./num_month * float(len([1 for i in call_type_dict[x_phone_no_m] if i == '2']))
                        x_num_calltrans = 1./num_month * float(len([1 for i in call_type_dict[x_phone_no_m] if i == '3']))
                    X.append([x_idcar_cnt, x_avg_arpu, x_std_arpu, x_avg_call_dur, x_std_call_dur, x_num_called_people, x_num_callout, x_num_callin, x_num_calltrans])
                elif method == 'idcard_cnt-avg_arpu-std_arpu-call_dur-called_people-call_type-sms_people':
                    if x_phone_no_m not in call_dur_dict.keys():
                        #x_med_call_dur = 0 # if not found call_dur
                        x_avg_call_dur = 0.0
                        x_std_call_dur = 0.0
                        x_num_called_people = 0.0
                        x_num_callout = 0.0
                        x_num_callin = 0.0
                        x_num_calltrans = 0.0
                    else:
                        #x_med_call_dur = np.median(call_dur_dict[x_phone_no_m])
                        x_avg_call_dur = np.mean(call_dur_dict[x_phone_no_m])
                        x_std_call_dur = np.std(call_dur_dict[x_phone_no_m])
                        x_num_called_people = 1./num_month * float(len(set(called_people_dict[x_phone_no_m])))
                        x_num_callout = 1./num_month * float(len([1 for i in call_type_dict[x_phone_no_m] if i == '1']))
                        x_num_callin = 1./num_month * float(len([1 for i in call_type_dict[x_phone_no_m] if i == '2']))
                        x_num_calltrans = 1./num_month * float(len([1 for i in call_type_dict[x_phone_no_m] if i == '3']))

                    if x_phone_no_m not in sms_people_dict.keys():
                        x_num_sms_people = 0.0
                    else:
                        x_num_sms_people = 1./num_month * float(len(set(sms_people_dict[x_phone_no_m])))

                    X.append([x_idcar_cnt, x_avg_arpu, x_std_arpu, x_avg_call_dur, x_std_call_dur, x_num_called_people,
                              x_num_callout, x_num_callin, x_num_calltrans, x_num_sms_people])
                elif method == 'idcard_cnt-avg_arpu-std_arpu-call_dur-called_people-call_type-sms_people-sms_type':
                    if x_phone_no_m not in call_dur_dict.keys():
                        # x_med_call_dur = 0 # if not found call_dur
                        x_avg_call_dur = 0.0
                        x_std_call_dur = 0.0
                        x_num_called_people = 0.0
                        x_num_callout = 0.0
                        x_num_callin = 0.0
                        x_num_calltrans = 0.0
                    else:
                        # x_med_call_dur = np.median(call_dur_dict[x_phone_no_m])
                        x_avg_call_dur = np.mean(call_dur_dict[x_phone_no_m])
                        x_std_call_dur = np.std(call_dur_dict[x_phone_no_m])
                        x_num_called_people = 1./num_month * float(len(set(called_people_dict[x_phone_no_m])))
                        x_num_callout = 1./num_month * float(len([1 for i in call_type_dict[x_phone_no_m] if i == '1']))
                        x_num_callin = 1./num_month * float(len([1 for i in call_type_dict[x_phone_no_m] if i == '2']))
                        x_num_calltrans = 1./num_month * float(len([1 for i in call_type_dict[x_phone_no_m] if i == '3']))

                    if x_phone_no_m not in sms_people_dict.keys():
                        x_num_smsout = 0.0
                        x_num_smsin = 0.0
                        x_num_sms_people = 0.0
                    else:
                        x_num_sms_people = 1./num_month * float(len(set(sms_people_dict[x_phone_no_m])))
                        x_num_smsout = 1./num_month * float(len([1 for i in sms_type_dict[x_phone_no_m] if i == '1']))
                        x_num_smsin = 1./num_month * float(len([1 for i in sms_type_dict[x_phone_no_m] if i == '2']))

                    X.append([x_idcar_cnt, x_avg_arpu, x_std_arpu, x_avg_call_dur, x_std_call_dur, x_num_called_people,
                              x_num_callout, x_num_callin, x_num_calltrans, x_num_sms_people, x_num_smsout, x_num_smsin])
                elif method == 'idcard_cnt-avg_arpu-std_arpu-call_dur-called_people-call_type-sms_people-sms_type-sms_datetime':
                    if x_phone_no_m not in call_dur_dict.keys():
                        # x_med_call_dur = 0 # if not found call_dur
                        x_avg_call_dur = 0.0
                        x_std_call_dur = 0.0
                        x_num_called_people = 0.0
                        x_num_callout = 0.0
                        x_num_callin = 0.0
                        x_num_calltrans = 0.0
                    else:
                        # x_med_call_dur = np.median(call_dur_dict[x_phone_no_m])
                        x_avg_call_dur = np.mean(call_dur_dict[x_phone_no_m])
                        x_std_call_dur = np.std(call_dur_dict[x_phone_no_m])
                        x_num_called_people = 1./num_month * float(len(set(called_people_dict[x_phone_no_m])))
                        x_num_callout = 1./num_month * float(len([1 for i in call_type_dict[x_phone_no_m] if i == '1']))
                        x_num_callin = 1./num_month * float(len([1 for i in call_type_dict[x_phone_no_m] if i == '2']))
                        x_num_calltrans = 1./num_month * float(len([1 for i in call_type_dict[x_phone_no_m] if i == '3']))

                    if x_phone_no_m not in sms_people_dict.keys():
                        x_num_smsout = 0.0
                        x_num_smsin = 0.0
                        x_num_sms_people = 0.0
                        x_num_sms_days = 0.0
                        x_avg_sms_perday = 0.0
                        x_std_sms_perday = 0.0
                    else:
                        x_num_sms_people = 1./num_month * float(len(set(sms_people_dict[x_phone_no_m])))
                        x_num_smsout = 1./num_month * float(len([1 for i in sms_type_dict[x_phone_no_m] if i == '1']))
                        x_num_smsin = 1./num_month * float(len([1 for i in sms_type_dict[x_phone_no_m] if i == '2']))
                        days = [datetime.split(' ')[0] for datetime in sms_datetime_dict[x_phone_no_m]]
                        x_num_sms_days = 1./num_month * float(len(set(days)))
                        x_avg_sms_perday = float(np.mean([len(list(group)) for key, group in groupby(days)]))
                        x_std_sms_perday = float(np.std([len(list(group)) for key, group in groupby(days)]))

                    X.append([x_idcar_cnt, x_avg_arpu, x_std_arpu, x_avg_call_dur, x_std_call_dur, x_num_called_people,
                              x_num_callout, x_num_callin, x_num_calltrans, x_num_sms_people, x_num_smsout, x_num_smsin,
                              x_num_sms_days, x_avg_sms_perday, x_std_sms_perday])
                elif method == 'idcard_cnt-call_dur-called_people-call_type-sms_people-sms_type-sms_datetime':
                    if x_phone_no_m not in call_dur_dict.keys():
                        # x_med_call_dur = 0 # if not found call_dur
                        x_avg_call_dur = 0.0
                        x_std_call_dur = 0.0
                        x_num_called_people = 0.0
                        x_num_callout = 0.0
                        x_num_callin = 0.0
                        x_num_calltrans = 0.0
                    else:
                        # x_med_call_dur = np.median(call_dur_dict[x_phone_no_m])
                        x_avg_call_dur = np.mean(call_dur_dict[x_phone_no_m])
                        x_std_call_dur = np.std(call_dur_dict[x_phone_no_m])
                        x_num_called_people = 1./num_month * float(len(set(called_people_dict[x_phone_no_m])))
                        x_num_callout = 1./num_month * float(len([1 for i in call_type_dict[x_phone_no_m] if i == '1']))
                        x_num_callin = 1./num_month * float(len([1 for i in call_type_dict[x_phone_no_m] if i == '2']))
                        x_num_calltrans = 1./num_month * float(len([1 for i in call_type_dict[x_phone_no_m] if i == '3']))

                    if x_phone_no_m not in sms_people_dict.keys():
                        x_num_smsout = 0.0
                        x_num_smsin = 0.0
                        x_num_sms_people = 0.0
                        x_num_sms_days = 0.0
                        x_avg_sms_perday = 0.0
                        x_std_sms_perday = 0.0
                    else:
                        x_num_sms_people = 1./num_month * float(len(set(sms_people_dict[x_phone_no_m])))
                        x_num_smsout = 1./num_month * float(len([1 for i in sms_type_dict[x_phone_no_m] if i == '1']))
                        x_num_smsin = 1./num_month * float(len([1 for i in sms_type_dict[x_phone_no_m] if i == '2']))
                        days = [datetime.split(' ')[0] for datetime in sms_datetime_dict[x_phone_no_m]]
                        x_num_sms_days = 1./num_month * float(len(set(days)))
                        x_avg_sms_perday = float(np.mean([len(list(group)) for key, group in groupby(days)]))
                        x_std_sms_perday = float(np.std([len(list(group)) for key, group in groupby(days)]))

                    X.append([x_idcar_cnt, x_avg_call_dur, x_std_call_dur, x_num_called_people,
                              x_num_callout, x_num_callin, x_num_calltrans, x_num_sms_people, x_num_smsout, x_num_smsin,
                              x_num_sms_days, x_avg_sms_perday, x_std_sms_perday])
    X = np.array(X)

    if get_label and get_phone_no:
        label = np.array(label)
        return X, label, phone_no_m
    elif get_label and not get_phone_no:
        label = np.array(label)
        return X, label
    elif not get_label and get_phone_no:
        return X, phone_no_m
    elif not get_label and not get_phone_no:
        return X