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
    thres_dur = arguments['threshold_duration']
    voc_dataframe = dataframe_phone_no['voc']
    voc_df_months = voc_dataframe[voc_dataframe['start_datetime'].str.contains(months_regex)]
    num_long_call = len([1 for dur in voc_df_months['call_dur'] if dur >= thres_dur])

    return num_long_call

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
    """return total call time in given months"""
    # convert to datetime format
    months = arguments['months']
    months_regex = '|'.join(months)
    voc_dataframe = dataframe_phone_no['voc']
    voc_df_months = voc_dataframe[voc_dataframe['start_datetime'].str.contains(months_regex)]

    return float(voc_df_months['call_dur'].sum())

def morning_call_time_rate(dataframe_phone_no, arguments):
    months = arguments['months']
    months_regex = '|'.join(months)
    voc_dataframe = dataframe_phone_no['voc']
    voc_df_months = voc_dataframe[voc_dataframe['start_datetime'].str.contains(months_regex)]
    total_time=0
    morning_time=0
    vv = voc_df_months.values
    for v in vv:
        start_time = v[2]
        day = start_time[0:10]
        t = float(start_time[11:13])*3600+float(start_time[14:16])*60+float(start_time[17:19]);
        total_time+=float(v[3])
        if 3600*8<t<3600*18:
            morning_time+=float(v[3])
    #return morning_time
    if total_time==0:
        return -1
    else:
        return morning_time



def call_interval_meantime(dataframe_phone_no, arguments):
    """return mean of time between two neighbor calls in given months"""
    # convert to datetime format
    months = arguments['months']
    months_regex = '|'.join(months)
    voc_dataframe = dataframe_phone_no['voc']
    voc_df_months = voc_dataframe[voc_dataframe['start_datetime'].str.contains(months_regex)]
    day_startTimeList_dict = {}
    interavl_list = []
    vv = voc_df_months.values
    for v in vv:
        start_time = v[2]
        day = start_time[0:10]
        t = float(start_time[11:13])*3600+float(start_time[14:16])*60+float(start_time[17:19]);
        if day not in day_startTimeList_dict:
            day_startTimeList_dict[day] = []
        day_startTimeList_dict[day].append(t)

    for day in day_startTimeList_dict:
        startTimeList = day_startTimeList_dict[day]
        startTimeList.sort(reverse=True)
        if len(startTimeList) < 2:
            continue
        for ii in range(len(startTimeList) - 1):
            interavl_list.append(startTimeList[ii] - startTimeList[ii+1])
    if len(interavl_list) == 0:
        return -1
    return np.mean(interavl_list)

def imei_num(dataframe_phone_no, arguments):
    months = arguments['months']
    months_regex = '|'.join(months)
    voc_dataframe = dataframe_phone_no['voc']
    voc_df_months = voc_dataframe[voc_dataframe['start_datetime'].str.contains(months_regex)]
    imei_set=set()
    vv = voc_df_months.values
    for v in vv:
        imei_set.add(v[-1])
    return len(imei_set)

# debug part: To be deleted
def test():
    data_voc = [['f0ebee98809cb1a9', 1, '2020-01-25 21:26:40', 742, '成都', '武侯区', '0a0a319fdb33f9538'],
                ['dedd4a48c3a8f', 1, '2020-01-02 20:14:33', 111, '成都', '锦江区', '0a0a319fdb33f9538'],
                ['dedd4a48c3a8f', 1, '2020-01-02 21:14:33', 11, '成都', '锦江区', '0a0a319fdb33f9538']]
    voc_df = pd.DataFrame(data_voc, columns=['opposite_no_m', 'calltype_id', 'start_datetime',
                                     'call_dur', 'city_name', 'county_name', 'imei_m'])
    dataframe_phone_no = {'voc': voc_df}
    arguments = {"months": ['2020-01'], 'threshold_duration': 100}
    t=call_interval_meantime(dataframe_phone_no, arguments)
    var = day_call_var(dataframe_phone_no, arguments)
    num_called_people = called_people(dataframe_phone_no, arguments)#, '2020-01'])
    long_call_num = total_call_time(dataframe_phone_no, arguments)
    print('input voc dataframe for given phone number:\n ', voc_df, '\n')
    print('number of called people:\n ', long_call_num)

if __name__ == '__main__':
    test()
