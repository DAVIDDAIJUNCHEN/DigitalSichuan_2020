import pandas as pd
import numpy as np
import time
from collections import Counter
import datetime
from scipy.stats import entropy


def smsin_num(dataframe_phone_no, arguments):
    """return the number of smsout in given month"""
    months = arguments['months']
    months_regex = '|'.join(months)
    sms_dataframe = dataframe_phone_no['sms']
    sms_df_months = sms_dataframe[sms_dataframe['request_datetime'].str.contains(months_regex)]
    sms_df_months_in = sms_df_months[sms_df_months['calltype_id']==2]

    return len(sms_df_months_in)


def smsout_num(dataframe_phone_no, arguments):
    """return the number of smsout in given month"""
    months = arguments['months']
    months_regex = '|'.join(months)
    sms_dataframe = dataframe_phone_no['sms']
    sms_df_months = sms_dataframe[sms_dataframe['request_datetime'].str.contains(months_regex)]
    sms_df_months_out = sms_df_months[sms_df_months['calltype_id']==1]

    return len(sms_df_months_out)


def sms_active_day_num(dataframe_phone_no, arguments):
    """return the number of active days in given months"""
    months = arguments['months']
    months_regex = '|'.join(months)
    sms_dataframe = dataframe_phone_no['sms']
    sms_df_months = sms_dataframe[sms_dataframe['request_datetime'].str.contains(months_regex)]
    lst_split_datetime = list(sms_df_months['request_datetime'].str.split())
    active_days = set([date[0] for date in lst_split_datetime])

    return len(active_days)

def sms_active_interval(dataframe_phone_no, arguments):
    """return the active interval"""
    months = arguments['months']
    months_regex = '|'.join(months)
    sms_dataframe = dataframe_phone_no['sms']
    sms_df_months = sms_dataframe[sms_dataframe['request_datetime'].str.contains(months_regex)]

    lst_split_datetime = list(sms_df_months['request_datetime'].str.split())
    active_days = set([date[0] for date in lst_split_datetime])

    if len(active_days) == 0:
        return arguments['represent_nan']
    else:
        last_day_lst = max(active_days).split('-')
        first_day_lst = min(active_days).split('-')
        last_day = datetime.date(int(last_day_lst[0]), int(last_day_lst[1]), int(last_day_lst[2]))
        first_day = datetime.date(int(first_day_lst[0]), int(first_day_lst[1]), int(first_day_lst[2]))
        interval = last_day - first_day

    return float(interval.days)


def sms_active_avr(dataframe_phone_no, arguments):
    """return the active interval"""
    months = arguments['months']
    months_regex = '|'.join(months)
    sms_dataframe = dataframe_phone_no['sms']
    sms_df_months = sms_dataframe[sms_dataframe['request_datetime'].str.contains(months_regex)]

    lst_split_datetime = list(sms_df_months['request_datetime'].str.split())
    active_days = set([date[0] for date in lst_split_datetime])
    num_sms = len(sms_df_months)

    if len(active_days) == 0:
        return arguments['represent_nan']
    else:
        return num_sms / len(active_days)


def smsin_active_avr(dataframe_phone_no, arguments):
    """return the active interval"""
    months = arguments['months']
    months_regex = '|'.join(months)
    sms_dataframe = dataframe_phone_no['sms']
    sms_df_months = sms_dataframe[sms_dataframe['request_datetime'].str.contains(months_regex)]

    lst_split_datetime = list(sms_df_months['request_datetime'].str.split())
    active_days = set([date[0] for date in lst_split_datetime])
    num_smsin = len(sms_df_months[sms_df_months['calltype_id']==2])

    if len(active_days) == 0:
        return arguments['represent_nan']
    else:
        return num_smsin / len(active_days)


def smsout_active_avr(dataframe_phone_no, arguments):
    """return the active interval"""
    months = arguments['months']
    months_regex = '|'.join(months)
    sms_dataframe = dataframe_phone_no['sms']
    sms_df_months = sms_dataframe[sms_dataframe['request_datetime'].str.contains(months_regex)]

    lst_split_datetime = list(sms_df_months['request_datetime'].str.split())
    active_days = set([date[0] for date in lst_split_datetime])
    num_smsout = len(sms_df_months[sms_df_months['calltype_id']==1])

    if len(active_days) == 0:
        return arguments['represent_nan']
    else:
        return num_smsout / len(active_days)


def ratio_smsout_smsin(dataframe_phone_no, arguments):
    """return the ratio of callout with callin"""
    months = arguments['months']
    months_regex = '|'.join(months)
    sms_dataframe = dataframe_phone_no['sms']
    sms_df_months = sms_dataframe[sms_dataframe['request_datetime'].str.contains(months_regex)]
    sms_df_months_smsout = sms_df_months[sms_df_months['calltype_id']==1]
    sms_df_months_smsin = sms_df_months[sms_df_months['calltype_id']==2]

    if len(sms_df_months_smsin) == 0:
        return arguments['represent_nan']
    else:
        return len(sms_df_months_smsout) / len(sms_df_months_smsin)


def sms_entropy_active_day(dataframe_phone_no, arguments):
    """return entropy of active day"""
    months = arguments['months']
    months_regex = '|'.join(months)
    sms_dataframe = dataframe_phone_no['sms']
    sms_df_months = sms_dataframe[sms_dataframe['request_datetime'].str.contains(months_regex)]
    sum_sms = len(sms_df_months)

    if sum_sms == 0:
        return arguments['represent_nan']

    lst_split_datetime = list(sms_df_months['request_datetime'].str.split())
    num_days = len(months)*30
    num_active = len(set([date[0] for date in lst_split_datetime]))
    lst_nonactive = [0]*(num_days - num_active)
    lst_nonactive.extend(list(Counter([date[0] for date in lst_split_datetime]).values()))
    lst_day_sms_prob = [cnt/sum_sms for cnt in lst_nonactive]

    return entropy(lst_day_sms_prob)


# debug part: To be deleted
def test():
    data_sms = [['f0ebee98809cb1a9', 1, '2020-01-01 21:26:40'],
                ['dedd4a48c3a8f', 1, '2020-01-03 20:14:33'],
                ['dedd4a48c3a8f', 1, '2020-01-02 20:14:33'],
                ['dedd4a48c3a8f', 1, '2020-01-02 20:14:33']]
    sms_df = pd.DataFrame(data_sms, columns=['opposite_no_m', 'calltype_id', 'request_datetime'])
    dataframe_phone_no = {"sms": sms_df}
    arguments = {"months": ['2019-12', '2020-01'], 'represent_nan': -10}
    print(sms_entropy_active_day(dataframe_phone_no, arguments))


if __name__ == '__main__':
    test()
