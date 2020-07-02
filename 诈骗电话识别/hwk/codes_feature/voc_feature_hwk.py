#/usr/bin/env python3

import pandas as pd
import numpy as np

def called_people(dataframe_phone_no, arguments):
    months = arguments['months']
    months_regex = '|'.join(months)
    voc_dataframe = dataframe_phone_no['voc']
    voc_df_months = voc_dataframe[voc_dataframe['start_datetime'].str.contains(months_regex)]
    called_people = set(voc_df_months['opposite_no_m'])
    return len(called_people)

def long_call(dataframe_phone_no, arguments):
    """return number of long call in given months"""
    # convert to datetime format
    months = arguments['months']
    months_regex = '|'.join(months)
    voc_dataframe = dataframe_phone_no['voc']
    voc_df_months = voc_dataframe[voc_dataframe['start_datetime'].str.contains(months_regex)]
    long_call_num=0
    for index,row in voc_df_months.iterrows():
        call_dur=float(row['call_dur'])
        if call_dur>=1500:
            long_call_num+=1
    return long_call_num

def day_call_var(dataframe_phone_no, arguments):
    """return number of long call in given months"""
    # convert to datetime format
    months = arguments['months']
    months_regex = '|'.join(months)
    voc_dataframe = dataframe_phone_no['voc']
    voc_df_months = voc_dataframe[voc_dataframe['start_datetime'].str.contains(months_regex)]
    day_calls_dict={}
    vv=voc_df_months.values
    for v in vv:
        if v[2]=='NaN':
            return -1

        day=v[2][:10]
        if day not in day_calls_dict:
            day_calls_dict[day]=[]
        day_calls_dict[day].append(float(v[3]))
    call_ed=[]

    for day in day_calls_dict.keys():
        call_ed.append(len(day_calls_dict[day]))
    call_ed =call_ed+[0]*(30-len(call_ed))
    call_ed_var=np.var(call_ed)
    if np.isnan(call_ed_var):
        return -1
    return call_ed_var

def total_call_time(dataframe_phone_no, arguments):
    """return number of long call in given months"""
    # convert to datetime format
    months = arguments['months']
    months_regex = '|'.join(months)
    voc_dataframe = dataframe_phone_no['voc']
    voc_df_months = voc_dataframe[voc_dataframe['start_datetime'].str.contains(months_regex)]
    t=0
    vv=voc_df_months.values
    for v in vv:
        t+=float(v[3])
    return t

# debug part: To be deleted
def test():
    data_voc = [['f0ebee98809cb1a9', 1, '2020-01-25 21:26:40', 742, '成都', '武侯区', '0a0a319fdb33f9538'],
                ['dedd4a48c3a8f', 1, '2020-01-02 20:14:33', 111, '成都', '锦江区', '0a0a319fdb33f9538'],
                ['dedd4a48c3a8f', 1, '2020-01-02 21:14:33', 11, '成都', '锦江区', '0a0a319fdb33f9538']]
    voc_df = pd.DataFrame(data_voc, columns=['opposite_no_m', 'calltype_id', 'start_datetime',
                                     'call_dur', 'city_name', 'county_name', 'imei_m'])
    dataframe_phone_no = {'voc': voc_df}
    arguments = {"months": ['2020-01']}
    t=total_call_time(dataframe_phone_no, arguments)
    var = day_call_var(dataframe_phone_no, arguments)
    num_called_people = called_people(dataframe_phone_no, arguments)#, '2020-01'])
    long_call_num = long_call(dataframe_phone_no, arguments)
    print('input voc dataframe for given phone number:\n ', voc_df, '\n')
    print('number of called people:\n ', num_called_people)

if __name__ == '__main__':
    test()
