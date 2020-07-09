# -*- coding: utf-8 -*-
"""
Created on Wed Jul  8 07:21:01 2020

@author: Kyle
"""
# =============================================================================
# 1、设置参数
# 2、划分数据
# 3、提取特征
# 4、导入模型
# 5、训练模型
# 6、超参选择
# 7、模型评估
# =============================================================================
import sys
import os
import csv

from pathlib import Path
RELATIVEPATH = Path(__file__).parent.parent.parent
sys.path.append(str(RELATIVEPATH))

from utils import evaluate, modify_months_config
from data_process_new import split_data, get_features, get_label, get_phone_no_m
import models 
from models.ensemble_model import ensemble
from sklearn.preprocessing import normalize
from functools import partial
from sklearn.metrics import f1_score
from sklearn import decomposition



class ModelEngine(object):
    
    def __init__(self):
        
        # 模型相关变量
        self.raw_models = {}
        self.fited_models = {}
        # 模型预测标签结果
        self.pred_vec = {}
        self.pred_test = {}
        
        # 配置变量
        self.train_yml = None
        self.test_yml = None
        self.features_name = None
        
        # 导入默认划分比例
        self.set_num_split(6106, 0.8, 0.1)
        
        # 设置相关路径
        self.set_origin_file()
        self.set_split_file()
        
        # 测试集用户名单
        self.users_no_blindtest = get_phone_no_m(self.origin_test_user)
        
        # 主观划分数据
        self.has_splited = False
        # 是否提取过特征
        self.has_get_features = False
        
        # 提醒
        print('\033[1;31;43m记得导入数据,使用set_config(name, train_yml, test_yml)\033[0m')
    
    def run(self, model_list):
        
        # 检查模型是否都已导入
        self.check_model(model_list)
        
        # 相关变量清零
        self.clear_variables()
        
        # 初始化划分函数
        self._init_features_fun()
        
        # 划分数据
        self.split_data()
        
        # 提取特征
        self.get_split_features()
        
        # 提取标签
        self.get_split_labels()
        
        # 导入模型
        self.set_models(model_list)
        
        # 训练模型
        self.fit_models()
        
        # 预测模型
        self.pred_models()
        
        # 评估模型
        self.eval_models()
      
        # 写入结果
        pass

    def run_months(self, model_list, months_lst, gradboost_blindAcc, method_list):
        self.fited_models_months = {}
        for months in months_lst:
            # 分月修改配置文件
            modify_months_config(train_config_yml, new_months=months)
            # 运行策略
            print(f'\033[1;32;44m月份{months}开始运行\033[0m','#'*45)
            self.run(model_list)
            # 获取相关
            for model_name, fited_model in self.fited_models.items():
                if model_name not in self.fited_models_months:
                    self.fited_models_months[model_name] = {}
                self.fited_models_months[model_name]['_'.join(months)] = \
                    (fited_model, gradboost_blindAcc['_'.join(months)])
        
        for method in method_list:
            # 模型预测
            self.pred_models_months(method)
            # 评估模型
            print(f'\033[1;32;41m{method}方法分月份合并预测', '*'*79+'\033[0m')
            self.eval_models()
            
                
    # 预测结果    
    def pred_models_months(self, method):
        for model_name, fited_model in self.fited_models_months.items():
            self.pred_vec[model_name] = ensemble(fited_model, self.split_X_dev, method=method)
            self.pred_test[model_name] = ensemble(fited_model, self.split_X_test, method=method) 
            
    def clear_variables(self):
        # 模型相关变量
        self.raw_models = {}
        self.fited_models = {}
        # 模型预测标签结果
        self.pred_vec = {}
        self.pred_test = {}
        
    def set_config(self, name, train_yml, test_yml):
        # 导入人工参数文件
        self.train_yml = train_yml
        self.test_yml = test_yml
        self.features_name = name
        self.has_get_features = False
        
    def set_num_split(self, num_total, num_train, num_dev):
        if 0 < num_train < 1:
            num_train = num_total*num_train
        if 0 < num_dev < 1:
            num_dev = num_total*num_dev
            
        self.num_total = 6106
        self.num_train = int(num_train)
        self.num_dev = int(num_dev)
        self.num_test = int(num_total - num_train - num_dev)
        
        print(f'已设置划分比例：(num_total,num_train, num_dev, \
num_test)={(self.num_total, self.num_train,self.num_dev, self.num_test)}')
        self.has_splited = False
                   
    # 主观划分训练集 
    def split_data(self):
        if not self.has_splited:
            split_data(self.origin_train_user, self.num_train, 
                       self.num_dev, self.num_test, replace=False)
            self.has_splited = True
            print('数据划分完成')
        else:
            print('数据已划分，继续执行操作')
    
    # 设置原始训练集/测试集的数据路径               
    def set_origin_file(self):
        parent_path = RELATIVEPATH / 'data'
        file_title = 'origin'
        set_names = ['train', 'test']
        set_class_names = ['user', 'voc', 'sms', 'app']  
        for set_name in set_names:
            for class_name in set_class_names:
                name_path = str(parent_path / f'{set_name}/{set_name}_{class_name}.csv')
                setattr(self, f'{file_title}_{set_name}_{class_name}',name_path)
    
    # 设置主观划分训练集数据为训练集，验证集，测试集的路径
    def set_split_file(self): 
        parent_path = RELATIVEPATH / 'data/train/split'
        file_title = 'split'
        set_names = ['train', 'dev','test']
        set_class_names = ['user']  
        for set_name in set_names:
            for class_name in set_class_names:
                name_path = str(parent_path/ f'{set_name}_{class_name}.csv')
                setattr(self, f'{file_title}_{set_name}_{class_name}',name_path)
        
    # 初始化特征函数和标签函数
    def _init_features_fun(self):
        if not self.train_yml:
            raise Exception('未添加配置文件')
        keys = ('file_voc', 'file_sms', 'file_app', 'config_yml')
        train_values = (self.origin_train_voc,
                        self.origin_train_sms,
                        self.origin_train_app,
                        self.train_yml)
        train_dict = dict(zip(keys, train_values))
        self.train_get_features = partial(get_features, **train_dict)
        test_values = (self.origin_test_voc,
                        self.origin_test_sms,
                        self.origin_test_app,
                        self.test_yml)
        test_dict = dict(zip(keys, test_values))
        self.test_get_features = partial(get_features, **test_dict)
    # 提取特征
    def get_split_features(self):
        if not self.has_get_features:
            self.split_X_train = self.train_get_features(self.split_train_user)
            self.split_X_dev = self.train_get_features(self.split_dev_user)
            self.split_X_test = self.train_get_features(self.split_test_user)
            
            # 添加pca
            pca = decomposition.PCA(n_components = 0.7)   # n_components默认为1，'mls'表示自动确定保留数
            
            self.split_X_train = pca.fit_transform(self.split_X_train)
            num_pca = len(pca.explained_variance_)
            pca = decomposition.PCA(n_components = num_pca)
            print(f'pca特征数为{num_pca}')
            self.split_X_dev = pca.fit_transform(self.split_X_dev)
            self.split_X_test = pca.fit_transform(self.split_X_test)
            
            
            self.has_get_features = True
    # 提取标签 
    def get_split_labels(self):
        self.split_L_train = get_label(self.split_train_user)
        self.split_L_dev = get_label(self.split_dev_user)
        self.split_L_test = get_label(self.split_test_user)
        
    # 设置模型
    def set_models(self, model_list):
        
        for model_name, params in model_list:
            raw_model = getattr(models, model_name)(**params)
            if model_name in self.raw_models:
                model_name = model_name + "_p" 
            self.raw_models[model_name] = raw_model
    
    # 训练模型
    def fit_models(self):
        for model_name, raw_model in self.raw_models.items():
            fited_model = raw_model.fit(self.split_X_train, self.split_L_train)
            self.fited_models[model_name] = fited_model
            print(f'{model_name}训练完成')
    
    # 预测结果    
    def pred_models(self):
        
        for model_name, fited_model in self.fited_models.items():
            self.pred_vec[model_name] = fited_model.predict(self.split_X_dev).tolist()
            self.pred_test[model_name] = fited_model.predict(self.split_X_test).tolist()
            
    # 评估模型
    def eval_models(self):
        for model_name in self.raw_models.keys():
            F1_dev = f1_score(self.split_L_dev, self.pred_vec[model_name])
            F1_test = f1_score(self.split_L_test, self.pred_test[model_name])
            print('='*79)
            print(f'\033[1;34;47m{model_name}验证集评估:F1 score is {F1_dev}\033[0m')
            print(f'\033[1;35;47m{model_name}测试集评估:F1 score is {F1_test}\033[0m')
    
    def check_model(self, model_list):
        is_error = False
        model_names = [i[0] for i in model_list]
        for model_name in model_names:
            if not hasattr(models, model_name):
                print(f'models文件夹的__init__.py中未导入模型{model_name}')
                is_error = True
        if is_error:
            raise Exception('请导入缺失模型')
            
    # 写入excel
    def blindtest(self, model_names, filename):
        if model_names == str:
            model_names = [model_names]
            
        X_blindtest = self.test_get_features(self.origin_test_user)
        for model_name in model_names:
            pred_blindtest = self.fited_models[model_name].predict(X_blindtest).tolist()
            
            csv_filename = filename + model_name
            with open(csv_filename, 'w', newline='', encoding='utf-8') as fout:
                field_names = ['phone_no_m', 'label']
                writer = csv.DictWriter(fout, fieldnames=field_names)
                writer.writeheader()
                   
                for phone, pred in zip(self.users_no_blindtest, pred_blindtest):
                    writer.writerow({'phone_no_m': phone, 'label': pred})
    
if __name__ == '__main__':
    model_list = [
        ('LogisticRegression', dict(random_state=0)),
        ('LogisticRegressionCV',dict(cv=5, random_state=0)),
        ('AdaBoostClassifier',dict(n_estimators=100, random_state=0)),
        ('GradientBoostingClassifier',dict(max_depth=2, random_state=0))
        ]  

    train_config_yml = '../configs/A1-2A4-5A7A9-10A12-24_config_train.yml'
    test_config_yml = '../configs/A1-2A4-5A7A9-10A12-24_config_test.yml'
    features_name = 'Z2'
    
    months_lst = [['2019-08'], ['2019-09']]

    gradboost_blindAcc = {'2019-08': 0.62, '2019-09': 0.66, '2019-10': 0.73, '2019-11': 0.75,
                     '2019-12': 0.78, '2020-01': 0.72, '2020-02': 0.76, '2020-03': 0.77}
    
    method_list = ['vote', 'avg_unif', 'avg_softmax']
    
    #%% 模型单独测试
    engine = ModelEngine() 
    engine.set_config(features_name, train_config_yml, test_config_yml)
    engine.run(model_list)
   
    #%% 分月测试
    # engine.run_months(model_list, months_lst, gradboost_blindAcc, method_list)
        
                   
                   
                   
                   
                   
                   
                   