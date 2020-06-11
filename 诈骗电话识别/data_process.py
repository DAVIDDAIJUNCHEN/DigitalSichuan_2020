#!/usr/bin/env python3

# import modules
import csv
import os
import numpy as np
import pickle

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
                output_dict[str(x_phone_no_m)] + [line[3]]
    return output_dict

# get model usable features from csv
def get_usable_data(file_user, file_voc, file_sms, method='idcard_cnt-avg_arpu'):
    """extract labels and features from given file"""
    # extract information from *_voc.csv
    if 'call_dur' in method:
        file_call_dur_dict = '../data/features/call_dur_dict.txt'
        # load or create dict (pickle)
        if not os.path.isfile(file_call_dur_dict):
            call_dur_dict = get_voc_info(file_voc, column='call_dur')
            with open(file_call_dur_dict, 'wb') as fout:
                pickle.dump(call_dur_dict, fout)
        else:
            with open(file_call_dur_dict, 'rb') as fin:
                call_dur_dict = pickle.load(fin)

    if 'called_people' in method:
        file_called_people_dict = '../data/features/called_people_dict.txt'
        # load or create dict (pickle)
        if not os.path.isfile(file_called_people_dict):
            called_people_dict = get_voc_info(file_voc, column='called_people')
            with open(file_called_people_dict, 'wb') as fout:
                pickle.dump(called_people_dict, fout)
        else:
            with open(file_called_people_dict, 'rb') as fin:
                called_people_dict = pickle.load(fin)

    if 'call_type' in method:
        file_call_type_dict = '../data/features/call_type_dict.txt'
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
        file_sms_people_dict = '../data/features/sms_people_dict.txt'
        # load or create dict (pickle)
        if not os.path.isfile(file_sms_people_dict):
            sms_people_dict = get_sms_info(file_sms, column='sms_people')
            with open(file_sms_people_dict, 'wb') as fout:
                pickle.dump(sms_people_dict, fout)
        else:
            with open(file_sms_people_dict, 'rb') as fin:
                sms_people_dict = pickle.load(fin)

    if 'sms_type' in method:
        file_sms_type_dict = '../data/features/sms_type_dict.txt'
        # load or create dict (pickle)
        if not os.path.isfile(file_sms_type_dict):
            sms_type_dict = get_sms_info(file_sms, column='sms_type')
            with open(file_sms_type_dict, 'wb') as fout:
                pickle.dump(sms_type_dict, fout)
        else:
            with open(file_sms_type_dict, 'rb') as fin:
                sms_type_dict = pickle.load(fin)

    with open(file_user, newline='', encoding='utf-8') as user_file:
        spamreader = csv.reader(user_file, delimiter=',', quotechar='|')
        label = []
        X = []
        for line in spamreader:
            if line[-1] == 'label' or len(''.join(line[4:-1])) == 0:
                pass
            else:
                # extract features: count of id cards + average arpu
                x_phone_no_m = line[0]
                x_idcar_cnt = float(line[3])
                x_avg_arpu = np.mean([float(num) for num in line[4:-1] if len(num) > 0])
                x_std_arpu = np.std([float(num) for num in line[4:-1] if len(num) > 0])
                label.append(int(line[-1]))
                if method == 'idcard_cnt-avg_arpu':
                    X.append([x_idcar_cnt, x_avg_arpu])
                elif method == 'idcard_cnt-avg_arpu-std_arpu':
                    X.append([x_idcar_cnt, x_avg_arpu, x_std_arpu])
                elif method == 'idcard_cnt-avg_arpu-std_arpu-call_dur':
                    if x_phone_no_m not in call_dur_dict.keys():
                        x_med_call_dur = 10 # if not found call_dur
                        x_std_call_dur = 1
                    else:
                        x_med_call_dur = np.median(call_dur_dict[x_phone_no_m])
                        x_std_call_dur = np.std(call_dur_dict[x_phone_no_m])
                    X.append([x_idcar_cnt, x_avg_arpu, x_std_arpu, x_med_call_dur, x_std_call_dur])
                elif method == 'idcard_cnt-avg_arpu-std_arpu-called_people':
                    if x_phone_no_m not in called_people_dict.keys():
                        x_num_called_people = 0
                    else:
                        x_num_called_people = len(set(called_people_dict[x_phone_no_m]))
                    X.append([x_idcar_cnt, x_avg_arpu, x_std_arpu, x_num_called_people])
                elif method == 'idcard_cnt-avg_arpu-std_arpu-call_dur-called_people':
                    if x_phone_no_m not in call_dur_dict.keys():
                        #x_med_call_dur = 10 # if not found call_dur
                        x_avg_call_dur = 10
                        x_std_call_dur = 1
                        x_num_called_people = 0
                    else:
                        #x_med_call_dur = np.median(call_dur_dict[x_phone_no_m])
                        x_avg_call_dur = np.mean(call_dur_dict[x_phone_no_m])
                        x_std_call_dur = np.std(call_dur_dict[x_phone_no_m])
                        x_num_called_people = float(len(set(called_people_dict[x_phone_no_m])))
                    X.append([x_idcar_cnt, x_avg_arpu, x_std_arpu, x_avg_call_dur, x_std_call_dur, x_num_called_people])
                elif method == 'idcard_cnt-avg_arpu-std_arpu-call_dur-call_type':
                    if x_phone_no_m not in call_dur_dict.keys():
                        #x_med_call_dur = 0 # if not found call_dur
                        x_avg_call_dur = 0
                        x_std_call_dur = 1
                        x_num_callout = 0
                        x_num_callin = 0
                        x_num_calltrans = 0
                    else:
                        #x_med_call_dur = np.median(call_dur_dict[x_phone_no_m])
                        x_avg_call_dur = np.mean(call_dur_dict[x_phone_no_m])
                        x_std_call_dur = np.std(call_dur_dict[x_phone_no_m])
                        x_num_callout = float(len([1 for i in call_type_dict[x_phone_no_m] if i=='1']))
                        x_num_callin = float(len([1 for i in call_type_dict[x_phone_no_m] if i=='2']))
                        x_num_calltrans = float(len([1 for i in call_type_dict[x_phone_no_m] if i=='3']))
                    X.append([x_idcar_cnt, x_avg_arpu, x_std_arpu, x_avg_call_dur, x_std_call_dur, x_num_callout, x_num_callin, x_num_calltrans])
                elif method == 'idcard_cnt-avg_arpu-std_arpu-call_dur-called_people-call_type':
                    if x_phone_no_m not in call_dur_dict.keys():
                        #x_med_call_dur = 0 # if not found call_dur
                        x_avg_call_dur = 0.0
                        x_std_call_dur = 1.0
                        x_num_called_people = 0.0
                        x_num_callout = 0.0
                        x_num_callin = 0.0
                        x_num_calltrans = 0.0
                    else:
                        #x_med_call_dur = np.median(call_dur_dict[x_phone_no_m])
                        x_avg_call_dur = np.mean(call_dur_dict[x_phone_no_m])
                        x_std_call_dur = np.std(call_dur_dict[x_phone_no_m])
                        x_num_called_people = float(len(set(called_people_dict[x_phone_no_m])))
                        x_num_callout = float(len([1 for i in call_type_dict[x_phone_no_m] if i == '1']))
                        x_num_callin = float(len([1 for i in call_type_dict[x_phone_no_m] if i == '2']))
                        x_num_calltrans = float(len([1 for i in call_type_dict[x_phone_no_m] if i == '3']))
                    X.append([x_idcar_cnt, x_avg_arpu, x_std_arpu, x_avg_call_dur, x_std_call_dur, x_num_called_people, x_num_callout, x_num_callin, x_num_calltrans])
                elif method == 'idcard_cnt-avg_arpu-std_arpu-call_dur-called_people-call_type-sms_people':
                    if x_phone_no_m not in call_dur_dict.keys():
                        #x_med_call_dur = 0 # if not found call_dur
                        x_avg_call_dur = 0.0
                        x_std_call_dur = 1.0
                        x_num_called_people = 0.0
                        x_num_callout = 0.0
                        x_num_callin = 0.0
                        x_num_calltrans = 0.0
                    else:
                        #x_med_call_dur = np.median(call_dur_dict[x_phone_no_m])
                        x_avg_call_dur = np.mean(call_dur_dict[x_phone_no_m])
                        x_std_call_dur = np.std(call_dur_dict[x_phone_no_m])
                        x_num_called_people = float(len(set(called_people_dict[x_phone_no_m])))
                        x_num_callout = float(len([1 for i in call_type_dict[x_phone_no_m] if i == '1']))
                        x_num_callin = float(len([1 for i in call_type_dict[x_phone_no_m] if i == '2']))
                        x_num_calltrans = float(len([1 for i in call_type_dict[x_phone_no_m] if i == '3']))

                    if x_phone_no_m not in sms_people_dict.keys():
                        x_num_sms_people = 0.0
                    else:
                        x_num_sms_people = float(len(set(sms_people_dict[x_phone_no_m])))

                    X.append([x_idcar_cnt, x_avg_arpu, x_std_arpu, x_avg_call_dur, x_std_call_dur, x_num_called_people,
                              x_num_callout, x_num_callin, x_num_calltrans, x_num_sms_people])
                elif method == 'idcard_cnt-avg_arpu-std_arpu-call_dur-called_people-call_type-sms_people-sms_type':
                    if x_phone_no_m not in call_dur_dict.keys():
                        # x_med_call_dur = 0 # if not found call_dur
                        x_avg_call_dur = 0.0
                        x_std_call_dur = 1.0
                        x_num_called_people = 0.0
                        x_num_callout = 0.0
                        x_num_callin = 0.0
                        x_num_calltrans = 0.0
                    else:
                        # x_med_call_dur = np.median(call_dur_dict[x_phone_no_m])
                        x_avg_call_dur = np.mean(call_dur_dict[x_phone_no_m])
                        x_std_call_dur = np.std(call_dur_dict[x_phone_no_m])
                        x_num_called_people = float(len(set(called_people_dict[x_phone_no_m])))
                        x_num_callout = float(len([1 for i in call_type_dict[x_phone_no_m] if i == '1']))
                        x_num_callin = float(len([1 for i in call_type_dict[x_phone_no_m] if i == '2']))
                        x_num_calltrans = float(len([1 for i in call_type_dict[x_phone_no_m] if i == '3']))

                    if x_phone_no_m not in sms_people_dict.keys():
                        x_num_smsout = 0.0
                        x_num_smsin = 0.0
                        x_num_sms_people = 0.0
                    else:
                        x_num_sms_people = float(len(set(sms_people_dict[x_phone_no_m])))
                        x_num_smsout = float(len([1 for i in sms_type_dict[x_phone_no_m] if i == '1']))
                        x_num_smsin = float(len([1 for i in sms_type_dict[x_phone_no_m] if i == '2']))
                    print(x_num_smsout, x_num_callout, x_num_smsin, x_num_smsin)

                    X.append([x_idcar_cnt, x_avg_arpu, x_std_arpu, x_avg_call_dur, x_std_call_dur, x_num_called_people,
                              x_num_callout, x_num_callin, x_num_calltrans, x_num_sms_people, x_num_smsout, x_num_smsin])
    label = np.array(label)
    X = np.array(X)

    return X, label
