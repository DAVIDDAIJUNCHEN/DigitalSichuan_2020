#/usr/bin/env python3

import pandas as pd
from scipy.stats import entropy
import time
import math

def called_people(dataframe_phone_no, arguments):
    """return number of called people  in given months"""
    months = arguments['months']
    months_regex = '|'.join(months)
    voc_dataframe = dataframe_phone_no['voc']
    voc_df_months = voc_dataframe[voc_dataframe['start_datetime'].str.contains(months_regex)]
    called_people = set(voc_df_months['opposite_no_m'])
    return len(called_people)

def mean_call_dur(dataframe_phone_no, arguments):
    """return mean of call duration in given months"""
    months = arguments['months']
    months_regex =  '|'.join(months)
    voc_dataframe = dataframe_phone_no['voc']
    voc_df_months = voc_dataframe[voc_dataframe['start_datetime'].str.contains(months_regex)]
    call_dur_df = voc_df_months['call_dur']

    if len(call_dur_df) == 0:
        return 0.0
    else:
        mean_call_dur = call_dur_df.mean()
        return float(mean_call_dur)

def std_call_dur(dataframe_phone_no, arguments):
    """return mean of call duration in given months"""
    months = arguments['months']
    months_regex = '|'.join(months)
    voc_dataframe = dataframe_phone_no['voc']
    voc_df_months = voc_dataframe[voc_dataframe['start_datetime'].str.contains(months_regex)]
    call_dur_df = voc_df_months['call_dur']
    if len(call_dur_df) == 0:
        return 0.0
    else:
        std_call_dur = call_dur_df.std()
        if math.isnan(float(std_call_dur)):
            std_call_dur = 0.0
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

    return entropy(prob_opposite)

def ratio_zero_calldur(dataframe_phone_no, arguments):
    """return ratio of calls with zero call duration"""
    months = arguments['months']
    months_regex = '|'.join(months)
    voc_dataframe = dataframe_phone_no['voc']
    voc_df_months = voc_dataframe[voc_dataframe['start_datetime'].str.contains(months_regex)]
    num_zerodur_months = len(voc_df_months[voc_df_months['call_dur']==0])
    num_call_months = len(voc_df_months)
    if len(num_call_months) == 0.0:
        return 0.0
    else:
        return num_zerodur_months / num_call_months

def ratio_nonzero_calldur(dataframe_phone_no, arguments):
    """return ratio of calls with non-zero call duration"""
    months = arguments['months']
    months_regex = '|'.join(months)
    voc_dataframe = dataframe_phone_no['voc']
    voc_df_months = voc_dataframe[voc_dataframe['start_datetime'].str.contains(months_regex)]
    num_nonzerodur_months = len(voc_df_months[voc_df_months['call_dur']>0])
    num_call_months = len(voc_df_months)
    if len(num_call_months) == 0:
        return 1.0
    else:
        return num_nonzerodur_months / num_call_months

def num_callout(dataframe_phone_no, arguments):
    """return number of callout"""
    months = arguments['months']
    months_regex = '|'.join(months)
    voc_dataframe = dataframe_phone_no['voc']
    voc_df_months = voc_dataframe[voc_dataframe['start_datetime'].str.contains(months_regex)]
    num_callout = len(voc_df_months[voc_df_months['calltype_id']==1])
    print(num_callout)
    return num_callout

def num_callin(dataframe_phone_no, arguments):
    """return number of callin"""
    months = arguments['months']
    months_regex = '|'.join(months)
    voc_dataframe = dataframe_phone_no['voc']
    voc_df_months = voc_dataframe[voc_dataframe['start_datetime'].str.contains(months_regex)]
    num_callin = len(voc_df_months[voc_df_months['calltype_id']==2])
    print(num_callin)
    return num_callin

def num_calltrans(dataframe_phone_no, arguments):
    """return number of callin"""
    months = arguments['months']
    months_regex = '|'.join(months)
    voc_dataframe = dataframe_phone_no['voc']
    voc_df_months = voc_dataframe[voc_dataframe['start_datetime'].str.contains(months_regex)]
    num_calltrans = len(voc_df_months[voc_df_months['calltype_id']==3])
    print(num_calltrans)
    return num_calltrans

def ratio_longcall(dataframe_phone_no, arguments):
    """return ratio of long call in given months"""
    # convert to datetime format
    months = arguments['months']
    months_regex = '|'.join(months)
    thres_dur = arguments['threshold_duration']
    voc_dataframe = dataframe_phone_no['voc']
    voc_df_months = voc_dataframe[voc_dataframe['start_datetime'].str.contains(months_regex)]
    num_long_call = len(voc_df_months[voc_df_months['call_dur']>=thres_dur])
    print(num_long_call / len(voc_df_months['call_dur']))
    return num_long_call / len(voc_df_months['call_dur'])





# debug part: To be deleted
def test():
    data_voc = [['f0ebee98809cb1a9', 2, '2019-12-25 21:26:40', 42, '成都', '武侯区', '0a0a319fdb33f9538'],
                ['dedd4a48c3a8f', 3, '2020-01-02 20:14:33', 111, '成都', '锦江区', '0a0a319fdb33f9538']]#,
                #['dedd4a48c3a8f', 1, '2020-01-02 20:14:33', 90, '成都', '锦江区', '0a0a319fdb33f9538']]
    voc_df = pd.DataFrame(data_voc, columns=['opposite_no_m', 'calltype_id', 'start_datetime',
                                     'call_dur', 'city_name', 'county_name', 'imei_m'])
    dataframe_phone_no = {'voc': voc_df}
    arguments = {"months": ['2019-12', '2020-01'], "threshold_duration": 150}
    ratio_longcall(dataframe_phone_no, arguments)

if __name__ == '__main__':
    test()
