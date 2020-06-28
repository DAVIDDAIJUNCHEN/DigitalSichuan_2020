#!/usr/bin/env python3

# import modules
from sklearn.metrics import f1_score
import yaml

def evaluate(golden_truth, pred, model=None):
    """wrap up evaluation methods and print information"""
    f1 = f1_score(golden_truth, pred, average='micro')
    if model == None:
        print('F1 score is {}'.format(f1))
    else:
        assert type(model) == str
        print(model + ': F1 score is {}'.format(f1))

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

if __name__ == '__main__':
    modify_months_config('./daijun/configs/A1_B1_C1_config_train_backup.yml')