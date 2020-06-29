#!/usr/bin/env python3

# import modules
import csv
import os
import numpy as np
from utils import evaluate
aa=3;
# split the data into train/dev/test

def get_voc_FrequentContactsNum(voc_value):
    contact_num_dict={}
    for v in voc_value:
        if v[0] not in contact_num_dict:
            contact_num_dict[v[0]]=0
        contact_num_dict[v[0]] =contact_num_dict[v[0]] +1
    num=0
    for c in contact_num_dict.keys():
        if contact_num_dict[c]>2:
            num=num+1
    return num

def get_voc_ContactsNum(voc_value):
    contact_num_dict={}
    for v in voc_value:
        if v[0] not in contact_num_dict:
            contact_num_dict[v[0]]=0
        contact_num_dict[v[0]] =contact_num_dict[v[0]] +1
    return len(contact_num_dict)

def get_voc_ShortCallNum(voc_value):
    n=0
    for v in voc_value:
        if float(v[3])<20:
            n=n+1
    return n

def get_voc_LongCallNum(voc_value):
    n=0
    for v in voc_value:
        if float(v[3])>600:
            n=n+1
    return n



def get_sms_SmsNum(sms_value):
    return len(sms_value)

def get_user_data(user_data_path):
    idcardMon_userInfo_dict = {};
    with open(user_data_path, encoding='utf-8') as file_orig:
        lines = []
        for line in file_orig:
            if line.startswith('phone_no_m'):
                header = line[:-1]
                header=line.split(',')
            else:
                line=line[:-1]
                line=line.split(',')
                for ii in range(4,12):
                    if line[ii]=='':
                        continue
                    mon=header[ii]
                    mon=mon[5:]
                    key=(line[0],mon)
                    value=line[1:4]+[line[ii],line[-1]]
                    idcardMon_userInfo_dict[key]=value
    return idcardMon_userInfo_dict


def get_voc_data(voc_data_path):
    idcardMon_vocInfo_dict = {};
    with open(voc_data_path, encoding='utf-8') as file_orig:
        for line in file_orig:
            if line.startswith('phone_no_m'):
                header = line[:-1]
                header=line.split(',')
            else:
                line=line[:-1]
                line=line.split(',')
                start_datetime=line[3]
                mon=start_datetime[:4]+start_datetime[5:7];
                value=line[1:]
                key=(line[0],mon)
                if key not in idcardMon_vocInfo_dict:
                    idcardMon_vocInfo_dict[key]=[]
                idcardMon_vocInfo_dict[key].append(value)

    return idcardMon_vocInfo_dict

def get_sms_data(sms_data_path):
    idcardMon_smsInfo_dict = {};
    with open(sms_data_path, encoding='utf-8') as file_orig:
        for line in file_orig:
            if line.startswith('phone_no_m'):
                header = line[:-1]
                header=line.split(',')
            else:
                line=line[:-1]
                line=line.split(',')
                start_datetime=line[3]
                mon=start_datetime[:4]+start_datetime[5:7];
                value=line[1:]
                key=(line[0],mon)
                if key not in idcardMon_smsInfo_dict:
                    idcardMon_smsInfo_dict[key]=[]
                idcardMon_smsInfo_dict[key].append(value)

    return idcardMon_smsInfo_dict


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
    """get information from *_voc.csv file"""
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


# get model usable data from csv
def get_usable_data(file_user, file_voc, method='idcard_cnt-avg_arpu'):
    """extract labels and features from given file"""
    # extract infor from train_voc.csv
    if 'call_dur' in method:
        call_dur_dict = get_voc_info(file_voc, column='call_dur')

    if 'called_people' in method:
        called_people_dict = get_voc_info(file_voc, column='called_people')

    if 'call_type' in method:
        call_type_dict = get_voc_info(file_voc, column='call_type')

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

    label = np.array(label)
    X = np.array(X)

    return X, label
