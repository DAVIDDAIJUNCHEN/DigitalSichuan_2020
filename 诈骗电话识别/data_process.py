#!/usr/bin/env python3

# import modules
import csv
import os
import numpy as np
from utils import evaluate

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

# get model usable data from csv
def get_usable_data(file):
    """extract labels and features from given file"""

    with open(file, newline='', encoding='utf-8') as csv_file:
        spamreader = csv.reader(csv_file, delimiter=',', quotechar='|')
        label = []
        X = []
        for line in spamreader:
            if line[-1] == 'label' or len(''.join(line[4:-1])) == 0:
                pass
            else:
                # extract features: count of id cards + average arpu
                x_idcar_cnt = float(line[3])
                x_avg_arpu = np.mean([float(num) for num in line[4:-1] if len(num) > 0])
                label.append(int(line[-1]))
                X.append([x_idcar_cnt, x_avg_arpu])

    label = np.array(label)
    X = np.array(X)

    return X, label
