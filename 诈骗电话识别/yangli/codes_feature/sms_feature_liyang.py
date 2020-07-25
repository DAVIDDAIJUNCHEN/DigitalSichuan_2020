import pandas as pd
import numpy as np
import time
import datetime
from scipy.stats import entropy
def smeout_num(dataframe_phone_no, arguments):
    """return the number of smsout in given month"""
    months = arguments['months']
    months_regex = '|'.join(months)
    sms_dataframe = dataframe_phone_no['sms']
    sms_df_months = sms_dataframe[sms_dataframe['request_datetime'].str.contains(months_regex)]
    sms_df_months_out = sms_df_months['calltype_id' == 1]
    smsout = list(sms_df_months_out['calltype_id'])
    return len(smsout)

def sms_active_day_num (dataframe_phone_no, arguments):
    """return the number of active days in given months"""
    months = arguments['months']
    months_regex = '|'.join(months)
    sms_dataframe = dataframe_phone_no['sms']
    sms_df_months = sms_dataframe[sms_dataframe['request_datetime'].str.contains(months_regex)]
    sms_df_months['request_datetime'] = pd.to_datetime(sms_df_months['request_datetime'], format='%Y-%m-%d %H:%M:%S')
    sms_df_months['request_day'] = sms_df_months['request_datetime'].dt.day
    active_day = set(sms_df_months['request_day'])
    return len(active_day)
def sms_active_interval (dataframe_phone_no, arguments):
    """return the active interval"""
    months = arguments['months']
    months_regex = '|'.join(months)
    sms_dataframe = dataframe_phone_no['sms']
    sms_df_months = sms_dataframe[sms_dataframe['request_datetime'].str.contains(months_regex)]
    sms_df_months['request_datetime'] = pd.to_datetime(sms_df_months['request_datetime'], format='%Y-%m-%d %H:%M:%S')
    sms_df_months['request_day'] = sms_df_months['request_datetime'].dt.day
    active_day = set(sms_df_months['request_day'])
    if len(active_day) == 0:
        return len(active_day)
    else:
        last_day = max(active_day)
        first_day = min(active_day)
        return last_day - first_day

def sms_entropy_active_day(dataframe_phone_no, arguments):
    """return entropy of active day"""
    months = arguments['months']
    months_regex = '|'.join(months)
    sms_dataframe = dataframe_phone_no['sms']
    sms_df_months = sms_dataframe[sms_dataframe['request_datetime'].str.contains(months_regex)]
    sms_df_months['request_datetime'] = pd.to_datetime(sms_df_months['request_datetime'], format='%Y-%m-%d %H:%M:%S')
    sms_df_months['request_day'] = sms_df_months['request_datetime'].dt.day
    sms_day = []
    for k in range(1,31):
        sms_df_months_k = sms_df_months.loc[sms_df_months['request_day'] == k]
        sms_k = list(sms_df_months_k['request_day'])
        sms_num_k = len(sms_k)
        sms_day.append(sms_num_k)
    total_sms = sum(sms_day)
    return entropy([day_sms / total_sms for day_sms in sms_day])