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
    zerodur_df_months = len(voc_df_months[voc_df_months['call_dur']==0])
    num_call_months = len(voc_df_months)
    if num_call_months in [0, 1]:
        return 0.0
    else:
        return zerodur_df_months / num_call_months

# debug part: To be deleted
def test():
    data_voc = [['f0ebee98809cb1a9', 1, '2019-12-25 21:26:40', 42, '成都', '武侯区', '0a0a319fdb33f9538'],
                ['dedd4a48c3a8f', 1, '2020-01-02 20:14:33', 111, '成都', '锦江区', '0a0a319fdb33f9538']]#,
                #['dedd4a48c3a8f', 1, '2020-01-02 20:14:33', 90, '成都', '锦江区', '0a0a319fdb33f9538']]
    voc_df = pd.DataFrame(data_voc, columns=['opposite_no_m', 'calltype_id', 'start_datetime',
                                     'call_dur', 'city_name', 'county_name', 'imei_m'])
    dataframe_phone_no = {'voc': voc_df}
    arguments = {"months": ['2019-12', '2020-01']}
    std_call_duration = entropy_called_people(dataframe_phone_no, arguments)#, '2020-01'])
    print('input voc dataframe for given phone number:\n ', voc_df, '\n')
    print('std of call duration:\n ', std_call_duration)

if __name__ == '__main__':
    test()
