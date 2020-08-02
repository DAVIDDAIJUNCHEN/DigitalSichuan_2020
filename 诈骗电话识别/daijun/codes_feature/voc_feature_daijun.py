#/usr/bin/env python3

import pandas as pd
from scipy.stats import entropy
import time
import math


def called_people(dataframe_phone_no, arguments):
    """return number of called people in given months"""
    months = arguments['months']
    months_regex = '|'.join(months)
    voc_dataframe = dataframe_phone_no['voc']
    voc_df_months = voc_dataframe[voc_dataframe['start_datetime'].str.contains(months_regex)]
    called_people = set(voc_df_months['opposite_no_m'])

    if math.isnan(len(called_people)):
        return arguments['represent_nan']
    else:
        return len(called_people)


def mean_call_dur(dataframe_phone_no, arguments):
    """return mean of call duration in given months"""
    months = arguments['months']
    months_regex = '|'.join(months)
    voc_dataframe = dataframe_phone_no['voc']
    voc_df_months = voc_dataframe[voc_dataframe['start_datetime'].str.contains(months_regex)]
    call_dur_df = voc_df_months['call_dur']

    if len(call_dur_df) == 0:
        return arguments['represent_nan']
    else:
        return float(call_dur_df.mean())


def std_call_dur(dataframe_phone_no, arguments):
    """return mean of call duration in given months"""
    months = arguments['months']
    months_regex = '|'.join(months)
    voc_dataframe = dataframe_phone_no['voc']
    voc_df_months = voc_dataframe[voc_dataframe['start_datetime'].str.contains(months_regex)]
    call_dur_df = voc_df_months['call_dur']
    if len(call_dur_df) == 0:
        return arguments['represent_nan']
    else:
        std_call_dur = call_dur_df.std()
        # if there is only one element, then assign std to 0.001
        if math.isnan(float(std_call_dur)):
            std_call_dur = arguments['represent_nan']
        return float(std_call_dur)

def entropy_called_people(dataframe_phone_no, arguments):
    """return entropy of called people"""
    months = arguments['months']
    months_regex = '|'.join(months)
    voc_dataframe = dataframe_phone_no['voc']
    voc_df_months = voc_dataframe[voc_dataframe['start_datetime'].str.contains(months_regex)]
    calltype1_df_months = voc_df_months[voc_df_months['calltype_id']==1]

    opposite_lst_months = list(calltype1_df_months['opposite_no_m'])
    num_call = len(opposite_lst_months)
    prob_opposite = [opposite_lst_months.count(item)/num_call for item in set(opposite_lst_months)]

    if len(prob_opposite) in [0, 1]:
        return arguments['represent_nan']
    else:
        return entropy(prob_opposite)

def ratio_zero_calldur(dataframe_phone_no, arguments):
    """return ratio of calls with zero call duration"""
    months = arguments['months']
    months_regex = '|'.join(months)
    voc_dataframe = dataframe_phone_no['voc']
    voc_df_months = voc_dataframe[voc_dataframe['start_datetime'].str.contains(months_regex)]
    num_zerodur_months = len([1 for dur in voc_df_months['call_dur'] if dur==0])
    num_call_months = len(voc_df_months)
    if num_call_months == 0:
        return arguments['represent_nan']
    else:
        return num_zerodur_months / num_call_months

def ratio_nonzero_calldur(dataframe_phone_no, arguments):
    """return ratio of calls with non-zero call duration"""
    months = arguments['months']
    months_regex = '|'.join(months)
    voc_dataframe = dataframe_phone_no['voc']
    voc_df_months = voc_dataframe[voc_dataframe['start_datetime'].str.contains(months_regex)]
    num_nonzerodur_months = len([1 for dur in voc_df_months['call_dur'] if dur > 0]) # len(voc_df_months[voc_df_months['call_dur']>0])
    num_call_months = len(voc_df_months)
    if num_call_months == 0:
        return arguments['represent_nan']
    else:
        return num_nonzerodur_months / num_call_months

def num_callout(dataframe_phone_no, arguments):
    """return number of callout"""
    months = arguments['months']
    months_regex = '|'.join(months)
    voc_dataframe = dataframe_phone_no['voc']
    voc_df_months = voc_dataframe[voc_dataframe['start_datetime'].str.contains(months_regex)]
    if len(voc_df_months) == 0:
        return arguments['represent_nan']

    num_callout = len([1 for id in voc_df_months['calltype_id'] if id==1])
    return num_callout

def num_callin(dataframe_phone_no, arguments):
    """return number of callin"""
    months = arguments['months']
    months_regex = '|'.join(months)
    voc_dataframe = dataframe_phone_no['voc']
    voc_df_months = voc_dataframe[voc_dataframe['start_datetime'].str.contains(months_regex)]
    if len(voc_df_months) == 0:
        return arguments['represent_nan']

    num_callin = len([1 for id in voc_df_months['calltype_id'] if id==2])
    return num_callin

def num_calltrans(dataframe_phone_no, arguments):
    """return number of callin"""
    months = arguments['months']
    months_regex = '|'.join(months)
    voc_dataframe = dataframe_phone_no['voc']
    voc_df_months = voc_dataframe[voc_dataframe['start_datetime'].str.contains(months_regex)]
    if len(voc_df_months) == 0:
        return arguments['represent_nan']

    num_calltrans = len([1 for id in voc_df_months['calltype_id'] if id==3])
    return num_calltrans

def ratio_longcall(dataframe_phone_no, arguments):
    """return ratio of long call in given months"""
    months = arguments['months']
    months_regex = '|'.join(months)
    thres_dur = arguments['threshold_duration']
    voc_dataframe = dataframe_phone_no['voc']
    voc_df_months = voc_dataframe[voc_dataframe['start_datetime'].str.contains(months_regex)]
    if len(voc_df_months) == 0:
        return arguments['represent_nan']

    num_long_call = len([1 for dur in voc_df_months['call_dur'] if dur>=thres_dur])
    return num_long_call / len(voc_df_months['call_dur'])

def num_callback(dataframe_phone_no, arguments):
    """return number of calling back"""
    months = arguments['months']
    months_regex = '|'.join(months)
    voc_dataframe = dataframe_phone_no['voc']
    voc_df_months = voc_dataframe[voc_dataframe['start_datetime'].str.contains(months_regex)]

    if len(voc_df_months) == 0:
        return 1.0

    #voc_df_months['start_datetime'] = pd.to_datetime(voc_df_months['start_datetime'], format='%Y-%m-%d %H:%M:%S')
    phone_no_callout_df = voc_df_months[voc_df_months['calltype_id']==1]
    phone_no_callin_df = voc_df_months[voc_df_months['calltype_id']==2]
    num_callback = 0
    for _, row_out in phone_no_callout_df.iterrows():
        datetime_out = row_out['start_datetime']
        row_in_candidate = phone_no_callin_df[phone_no_callin_df['start_datetime'] > datetime_out]
        if row_out['opposite_no_m'] in list(row_in_candidate['opposite_no_m']):
            num_callback += 1
    return num_callback

def ratio_callback(dataframe_phone_no, arguments):
    """return number of calling back"""
    months = arguments['months']
    months_regex = '|'.join(months)
    voc_dataframe = dataframe_phone_no['voc']
    voc_df_months = voc_dataframe[voc_dataframe['start_datetime'].str.contains(months_regex)]
    if len(voc_df_months) == 0:
        return 1.0
    #voc_df_months['start_datetime'] = pd.to_datetime(voc_df_months['start_datetime'], format='%Y-%m-%d %H:%M:%S')
    phone_no_callout_df = voc_df_months[voc_df_months['calltype_id']==1]
    phone_no_callin_df = voc_df_months[voc_df_months['calltype_id']==2]

    num_callback = 0
    for _, row_out in phone_no_callout_df.iterrows():
        datetime_out = row_out['start_datetime']
        row_in_candidate = phone_no_callin_df[phone_no_callin_df['start_datetime'] > datetime_out]
        if row_out['opposite_no_m'] in list(row_in_candidate['opposite_no_m']):
            num_callback += 1
    if len(phone_no_callout_df) == 0:
        return 1.0
    return num_callback / len(phone_no_callout_df)


def imei_num(dataframe_phone_no, arguments):
    """return the number of IMEI"""
    months = arguments['months']
    months_regex = '|'.join(months)
    voc_dataframe = dataframe_phone_no['voc']
    voc_df_months = voc_dataframe[voc_dataframe['start_datetime'].str.contains(months_regex)]
    if len(voc_df_months) == 0:
        return arguments['represent_nan']
    else:
        imei = set(voc_df_months['imei_m'])
        return len(imei)


# debug part: To be deleted
def test():
    data_voc = [['f0ebee98809cb1a9', 1, '2020-01-02 20:14:33', 9, '成都', '武侯区', '0a0a319fdb33f9538'],
                ['dedd4a48c3a8f', 2, '2020-01-02 20:14:33', 111, '成都', '锦江区', '0a0a319fdb33f9538'],
                ['f0ebee98809cb1a9', 2, '2020-02-02 20:14:38', 0, '成都', '锦江区', '0a0a319fdb33f958']]
    voc_df = pd.DataFrame(data_voc, columns=['opposite_no_m', 'calltype_id', 'start_datetime',
                                     'call_dur', 'city_name', 'county_name', 'imei_m'])
    dataframe_phone_no = {'voc': voc_df}
    arguments = {"months": ['2019-12', '2020-01'], "threshold_duration": 150., 'represent_nan': -10}
    print(std_call_dur(dataframe_phone_no, arguments))


if __name__ == '__main__':
    test()
