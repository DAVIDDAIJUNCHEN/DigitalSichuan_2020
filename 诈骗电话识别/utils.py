#!/usr/bin/env python3

# import modules
from sklearn.metrics import f1_score
import yaml


def evaluate(golden_truth, pred, model=None):
    """wrap up evaluation methods and print information"""
    f1 = f1_score(golden_truth, pred, average='micro')
    if model == None:
        print('F1 score is {}'.format(f1))
        return f1
    else:
        assert type(model) == str
        print(model + ': F1 score is {}'.format(f1))
        return f1


def modify_months_config(config_yml, new_months=['2020-01', '2020-02']):
    """modify date in the config yaml file"""
    # parsing config_yml
    with open(config_yml) as fin:
        def_para = yaml.load(fin)
        def_para_feature = def_para['features']

    # modify moths in function parameter
    for feature in def_para_feature:
        feature_entry = list(feature.values())[0][0]
        function = feature_entry['function'][0]
        parameter = function['para']
        if 'months' in parameter.keys():
            parameter['months'] = new_months

        function['para'] = dict(parameter)
    # output config_yml
    with open(config_yml, 'w') as fout:
        data = yaml.dump(def_para, fout)

    return None


def insert_label(user_file_in, label_file, user_file_out):
    """insert test label into test user file"""
    dct_label = {}
    with open(label_file, 'r', encoding='utf-8') as fin:
        for line in fin:
            line_splt = line.split(',')
            phone_no_m = line_splt[0]
            label = line_splt[-1]
            dct_label[phone_no_m] = label

    new_lines = []
    with open(user_file_in, 'r', encoding='utf-8') as fin:
        for line in fin:
            line_splt = line.split(',')
            phone_no_m = line_splt[0]
            if phone_no_m in dct_label.keys():
                line = line.strip('\n')
                new_line = line + ',' + dct_label[phone_no_m]
            new_lines.append(new_line)

    with open(user_file_out, 'w', encoding='utf-8') as fout:
        for line in new_lines:
            fout.writelines(line)

    return None


if __name__ == '__main__':
    insert_label('./data/test_04/test_user.csv', './data/test_04/labelsAB.csv',
                 './data/test_04/test_user_wLabel.csv')
    #modify_months_config('./daijun/configs/A1_B1_C1_config_train_backup.yml')