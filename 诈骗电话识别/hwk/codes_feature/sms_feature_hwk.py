#/usr/bin/env python3

import pandas as pd
import numpy as np
import math

def sms_people(dataframe_phone_no, arguments):
    months = arguments['months']
    months_regex = '|'.join(months)
    sms_dataframe = dataframe_phone_no['sms']
    sms_df_months = sms_dataframe[sms_dataframe['request_datetime'].str.contains(months_regex)]
    if len(sms_df_months) == 0:
        return arguments['represent_nan']

    smsed_people = set(sms_df_months['opposite_no_m'])
    return len(smsed_people)

def sms_interval_meantime(dataframe_phone_no, arguments):
    # convert to datetime format
    months = arguments['months']
    months_regex = '|'.join(months)
    sms_dataframe = dataframe_phone_no['sms']
    sms_df_months = sms_dataframe[sms_dataframe['request_datetime'].str.contains(months_regex)]

    day_startTimeList_dict={}
    interavl_list=[]
    vv=sms_df_months.values
    for v in vv:
        start_time=v[2]
        day=start_time[0:10]
        t=float(start_time[11:13])*3600+float(start_time[14:16])*60+float(start_time[17:19]);
        if day not in day_startTimeList_dict:
            day_startTimeList_dict[day]=[]
        day_startTimeList_dict[day].append(t)

    for day in day_startTimeList_dict:
        startTimeList=day_startTimeList_dict[day]
        startTimeList.sort(reverse=True)
        if len(startTimeList)<2:
            continue
        for ii in range(len(startTimeList)-1):
            interavl_list.append(startTimeList[ii]-startTimeList[ii+1])

    if math.isnan(np.mean(interavl_list)):
        return arguments['represent_nan']

    return np.mean(interavl_list)

# debug part: To be deleted
def test():
    data_sms = [['f0ebee98809cb1a9', 1, '2019-12-25 21:26:40'],
                ['dedd4a48c3a8f', 1, '2019-12-25 20:14:33']]
    sms_df = pd.DataFrame(data_sms, columns=['opposite_no_m', 'calltype_id', 'request_datetime'])
    dataframe_phone_no = {"sms": sms_df}
    arguments = {"months": ['2019-12']}
    t=sms_interval_meantime(dataframe_phone_no, arguments)
    num_smsed_people = sms_people(dataframe_phone_no, arguments)

    print('input sms dataframe for given phone number:\n ', sms_df, '\n')
    print('number of sms people:\n ', num_smsed_people)

if __name__ == '__main__':
    test()
