# -*- coding: utf-8 -*-
"""
Created on Sat Jul  4 15:37:21 2020

@author: Kyle
"""
import pandas as pd
from scipy.stats import entropy
import time
import math

def entropy_smsed_people(dataframe_phone_no, arguments):
    # 读取相应月份数据
    months = arguments['months']
    months_regex = '|'.join(months)
    sms_dataframe = dataframe_phone_no['sms']
    sms_df_months = sms_dataframe[sms_dataframe['request_datetime'].str.contains(months_regex)]
    
    # 筛选短信上行号码
    sms_up = sms_df_months[sms_df_months['calltype_id'] == 1]
    
    # 筛选短信下行号码
    sms_dn = list(sms_up['opposite_no_m'])
    
    # 求算频率
    num_sms = len(sms_dn)
    prob_opposite = [sms_dn.count(item)/num_sms for item in set(sms_dn)]
    
    return entropy(prob_opposite)