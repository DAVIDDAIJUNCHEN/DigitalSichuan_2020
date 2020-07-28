import pandas as pd
import numpy as np
import time
import datetime
from collections import Counter
from scipy.stats import entropy


def call_in_total_time(dataframe_phone_no, arguments):
    """returne the total duration of call in calls"""
    months = arguments['months']
    months_regex = '|'.join(months)
    voc_dataframe = dataframe_phone_no['voc']
    voc_df_months = voc_dataframe[voc_dataframe['start_datetime'].str.contains(months_regex)]
    if len(voc_df_months) == 0:
        return arguments['represent_nan']

    voc_df_months_callin = voc_df_months.loc[voc_df_months['calltype_id'] == 2]
    return float(voc_df_months_callin['call_dur'].sum())


def call_in_time_avr(dataframe_phone_no, arguments):
    """returne the average duration of call in calls"""
    months = arguments['months']
    months_regex = '|'.join(months)
    voc_dataframe = dataframe_phone_no['voc']
    voc_df_months = voc_dataframe[voc_dataframe['start_datetime'].str.contains(months_regex)]
    voc_df_months_callin = voc_df_months.loc[voc_df_months['calltype_id'] == 2]
    total_time = float(voc_df_months_callin['call_dur'].sum())
    call_in_num = len(voc_df_months_callin['call_dur'])
    if call_in_num == 0:
        call_in_num = 1

    return total_time / call_in_num


def call_in_people(dataframe_phone_no, arguments):
    """return the number of call in people"""
    months = arguments['months']
    months_regex = '|'.join(months)
    voc_dataframe = dataframe_phone_no['voc']
    voc_df_months = voc_dataframe[voc_dataframe['start_datetime'].str.contains(months_regex)]
    voc_df_months_callin = voc_df_months.loc[voc_df_months['calltype_id'] == 2]
    call_in_people = set(voc_df_months_callin['opposite_no_m'])
    if len(voc_df_months) == 0:
        return arguments['represent_nan']

    return len(call_in_people)


def call_out_total_time(dataframe_phone_no, arguments):
    """returne the total duration of call out calls"""
    months = arguments['months']
    months_regex = '|'.join(months)
    voc_dataframe = dataframe_phone_no['voc']
    voc_df_months = voc_dataframe[voc_dataframe['start_datetime'].str.contains(months_regex)]
    voc_df_months_callout = voc_df_months.loc[voc_df_months['calltype_id'] == 1]
    if len(voc_df_months_callout) == 0:
        return arguments['represent_nan']

    return float(voc_df_months_callout['call_dur'].sum())


def call_out_time_avr(dataframe_phone_no, arguments):
    """returne the average duration of call out calls"""
    months = arguments['months']
    months_regex = '|'.join(months)
    voc_dataframe = dataframe_phone_no['voc']
    voc_df_months = voc_dataframe[voc_dataframe['start_datetime'].str.contains(months_regex)]
    voc_df_months_callout = voc_df_months.loc[voc_df_months['calltype_id'] == 1]
    if len(voc_df_months_callout) == 0:
        return arguments['represent_nan']

    total_time = float(voc_df_months_callout['call_dur'].sum())
    call_out_num = len(voc_df_months_callout['call_dur'])
    return total_time / call_out_num


def call_out_people(dataframe_phone_no, arguments):
    """return the number of call in people"""
    months = arguments['months']
    months_regex = '|'.join(months)
    voc_dataframe = dataframe_phone_no['voc']
    voc_df_months = voc_dataframe[voc_dataframe['start_datetime'].str.contains(months_regex)]
    if len(voc_df_months) == 0:
        return arguments['represent_nan']

    voc_df_months_callout = voc_df_months.loc[voc_df_months['calltype_id'] == 1]
    call_out_people = set(voc_df_months_callout['opposite_no_m'])
    return len(call_out_people)


def segement_call_duration(dataframe_phone_no, arguments):
    """return the segement call duration of given month"""
    months = arguments['months']
    months_regex = '|'.join(months)
    voc_dataframe = dataframe_phone_no['voc']
    voc_df_months = voc_dataframe[voc_dataframe['start_datetime'].str.contains(months_regex)]
    datetime = voc_df_months.start_datetime.str.split().tolist()
    voc_df_months['time'] = [time[1] for time in datetime]
    voc_df_months['time'] = pd.to_datetime(voc_df_months['time'], format='%H:%M:%S')
    voc_df_months['time'] = voc_df_months['time'].dt.hour
    voc_df_months_0_8 = voc_df_months.loc[0 <= voc_df_months['time']].loc[voc_df_months['time'] <= 7]
    voc_df_months_8_10 = voc_df_months.loc[8 <= voc_df_months['time']].loc[voc_df_months['time'] <= 9]
    voc_df_months_10_12 = voc_df_months.loc[10 <= voc_df_months['time']].loc[voc_df_months['time'] <= 11]
    voc_df_months_12_14 = voc_df_months.loc[12 <= voc_df_months['time']].loc[voc_df_months['time'] <= 13]
    voc_df_months_14_16 = voc_df_months.loc[14 <= voc_df_months['time']].loc[voc_df_months['time'] <= 15]
    voc_df_months_16_18 = voc_df_months.loc[16 <= voc_df_months['time']].loc[voc_df_months['time'] <= 17]
    voc_df_months_18_20 = voc_df_months.loc[18 <= voc_df_months['time']].loc[voc_df_months['time'] <= 19]
    voc_df_months_20_22 = voc_df_months.loc[20 <= voc_df_months['time']].loc[voc_df_months['time'] <= 21]
    voc_df_months_22_24 = voc_df_months.loc[22 <= voc_df_months['time']].loc[voc_df_months['time'] <= 23]
    segement_call_duration = {}
    segement_call_duration['call_duratiom_0_8'] = float(voc_df_months_0_8['call_dur'].sum())
    segement_call_duration['call_duratiom_8_10'] = float(voc_df_months_8_10['call_dur'].sum())
    segement_call_duration['call_duratiom_10_12'] = float(voc_df_months_10_12['call_dur'].sum())
    segement_call_duration['call_duratiom_12_14'] = float(voc_df_months_12_14['call_dur'].sum())
    segement_call_duration['call_duratiom_14_16'] = float(voc_df_months_14_16['call_dur'].sum())
    segement_call_duration['call_duratiom_16_18'] = float(voc_df_months_16_18['call_dur'].sum())
    segement_call_duration['call_duratiom_18_20'] = float(voc_df_months_18_20['call_dur'].sum())
    segement_call_duration['call_duratiom_20_22'] = float(voc_df_months_20_22['call_dur'].sum())
    segement_call_duration['call_duratiom_22_24'] = float(voc_df_months_22_24['call_dur'].sum())
    return segement_call_duration


def voc_active_day_num(dataframe_phone_no, arguments):
    """return the number of active days in given months"""
    months = arguments['months']
    months_regex = '|'.join(months)
    voc_dataframe = dataframe_phone_no['voc']
    voc_df_months = voc_dataframe[voc_dataframe['start_datetime'].str.contains(months_regex)]
    lst_split_datetime = list(voc_df_months['start_datetime'].str.split())
    active_days = set([date[0] for date in lst_split_datetime])

    return len(active_days)


def voc_active_interval(dataframe_phone_no, arguments):
    """return the active interval"""
    months = arguments['months']
    months_regex = '|'.join(months)
    voc_dataframe = dataframe_phone_no['voc']
    voc_df_months = voc_dataframe[voc_dataframe['start_datetime'].str.contains(months_regex)]

    lst_split_datetime = list(voc_df_months['start_datetime'].str.split())
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


def voc_active_avr(dataframe_phone_no, arguments):
    """return the active interval"""
    months = arguments['months']
    months_regex = '|'.join(months)
    voc_dataframe = dataframe_phone_no['voc']
    voc_df_months = voc_dataframe[voc_dataframe['start_datetime'].str.contains(months_regex)]

    lst_split_datetime = list(voc_df_months['start_datetime'].str.split())
    active_days = set([date[0] for date in lst_split_datetime])
    num_call = len(voc_df_months)

    if len(active_days) == 0:
        return arguments['represent_nan']
    else:
        return num_call / len(active_days)


def vocin_active_avr(dataframe_phone_no, arguments):
    """return the active interval"""
    months = arguments['months']
    months_regex = '|'.join(months)
    voc_dataframe = dataframe_phone_no['voc']
    voc_df_months = voc_dataframe[voc_dataframe['start_datetime'].str.contains(months_regex)]

    lst_split_datetime = list(voc_df_months['start_datetime'].str.split())
    active_days = set([date[0] for date in lst_split_datetime])
    num_callin = len(voc_df_months['calltype_id']==2)

    if len(active_days) == 0:
        return arguments['represent_nan']
    else:
        return num_callin / len(active_days)


def vocout_active_avr(dataframe_phone_no, arguments):
    """return the active interval"""
    months = arguments['months']
    months_regex = '|'.join(months)
    voc_dataframe = dataframe_phone_no['voc']
    voc_df_months = voc_dataframe[voc_dataframe['start_datetime'].str.contains(months_regex)]

    lst_split_datetime = list(voc_df_months['start_datetime'].str.split())
    active_days = set([date[0] for date in lst_split_datetime])
    num_callout = len(voc_df_months['calltype_id']==1)

    if len(active_days) == 0:
        return arguments['represent_nan']
    else:
        return num_callout / len(active_days)


def ratio_callout_callin(dataframe_phone_no, arguments):
    """return the ratio of callout with callin"""
    months = arguments['months']
    months_regex = '|'.join(months)
    voc_dataframe = dataframe_phone_no['voc']
    voc_df_months = voc_dataframe[voc_dataframe['start_datetime'].str.contains(months_regex)]
    voc_df_months_callout = voc_df_months[voc_df_months['calltype_id']==1]
    voc_df_months_callin = voc_df_months[voc_df_months['calltype_id']==2]

    if len(voc_df_months_callin) == 0:
        return arguments['represent_nan']
    else:
        return len(voc_df_months_callout) / len(voc_df_months_callin)


def voc_entropy_active_day(dataframe_phone_no, arguments):
    """return entropy of active day"""
    months = arguments['months']
    months_regex = '|'.join(months)
    voc_dataframe = dataframe_phone_no['voc']
    voc_df_months = voc_dataframe[voc_dataframe['start_datetime'].str.contains(months_regex)]
    sum_call = len(voc_df_months)

    if sum_call == 0:
        return arguments['represent_nan']

    lst_split_datetime = list(voc_df_months['start_datetime'].str.split())
    num_days = len(months)*30
    num_active = len(set([date[0] for date in lst_split_datetime]))
    lst_nonactive = [0]*(num_days - num_active)
    lst_nonactive.extend(list(Counter([date[0] for date in lst_split_datetime]).values()))
    lst_day_call_prob = [cnt/sum_call for cnt in lst_nonactive]

    return entropy(lst_day_call_prob)

# debug part: To be deleted
def test():
    data_voc = [['f0ebee98809cb1a9', 1, '2020-01-02 21:26:40', 742, '成都', '武侯区', '0a0a319fdb33f9538'],
                ['dedd4a48c3a8f', 2, '2020-01-02 20:14:33', 111, '成都', '锦江区', '0a0a319fdb33f9538'],
                ['dedd4a48c3a8f', 1, '2020-01-02 21:14:33', 11, '成都', '锦江区', '0a0a319fdb33f9538']]
    voc_df = pd.DataFrame(data_voc, columns=['opposite_no_m', 'calltype_id', 'start_datetime',
                                             'call_dur', 'city_name', 'county_name', 'imei_m'])
    dataframe_phone_no = {'voc': voc_df}
    print(voc_entropy_active_day(dataframe_phone_no, {'months': ['2020-01'], 'represent_nan': -10}))


if __name__ == '__main__':
    test()