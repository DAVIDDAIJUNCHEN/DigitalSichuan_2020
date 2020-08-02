import pandas as pd
import numpy as np
import time
import datetime
from scipy.stats import entropy
from collections import Counter
import statistics


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


def callout_range(dataframe_phone_no, arguments):
    """return the range of callout in given month"""
    months = arguments['months']
    months_regex = '|'.join(months)
    voc_dataframe = dataframe_phone_no['voc']
    voc_df_months = voc_dataframe[voc_dataframe['start_datetime'].str.contains(months_regex)]
    voc_df_months_callout = voc_df_months[voc_df_months['calltype_id']==1]
    sum_callout = len(voc_df_months_callout)

    if sum_callout == 0:
        return arguments['represent_nan']

    lst_split_datetime = list(voc_df_months_callout['start_datetime'].str.split())
    num_days = len(months)*30
    num_active = len(set([date[0] for date in lst_split_datetime]))
    lst_nonactive = [0]*(num_days - num_active)
    lst_nonactive.extend(list(Counter([date[0] for date in lst_split_datetime]).values()))

    return max(lst_nonactive) - min(lst_nonactive)


def callin_range(dataframe_phone_no, arguments):
    """return the range of callin in given month"""
    months = arguments['months']
    months_regex = '|'.join(months)
    voc_dataframe = dataframe_phone_no['voc']
    voc_df_months = voc_dataframe[voc_dataframe['start_datetime'].str.contains(months_regex)]
    voc_df_months_callout = voc_df_months[voc_df_months['calltype_id']==2]
    sum_callout = len(voc_df_months_callout)

    if sum_callout == 0:
        return arguments['represent_nan']

    lst_split_datetime = list(voc_df_months_callout['start_datetime'].str.split())
    num_days = len(months)*30
    num_active = len(set([date[0] for date in lst_split_datetime]))
    lst_nonactive = [0]*(num_days - num_active)
    lst_nonactive.extend(list(Counter([date[0] for date in lst_split_datetime]).values()))

    return max(lst_nonactive) - min(lst_nonactive)


def short_callout_num(dataframe_phone_no, arguments):
    """return the number of short callout in given month"""
    thres_dur = arguments['threshold_duration']
    months = arguments['months']
    months_regex = '|'.join(months)
    voc_dataframe = dataframe_phone_no['voc']
    voc_df_months = voc_dataframe[voc_dataframe['start_datetime'].str.contains(months_regex)]
    voc_df_months_callout = voc_df_months[voc_df_months['calltype_id']==1]
    short_callout = [1 for each in voc_df_months_callout['call_dur'] if each <= thres_dur]

    if len(short_callout) == 0:
        return arguments['represent_nan']
    else:
        return len(short_callout)


def short_callin_num(dataframe_phone_no, arguments):
    """return the number of short callin in given month"""
    thres_dur = arguments['threshold_duration']
    months = arguments['months']
    months_regex = '|'.join(months)
    voc_dataframe = dataframe_phone_no['voc']
    voc_df_months = voc_dataframe[voc_dataframe['start_datetime'].str.contains(months_regex)]
    voc_df_months_callin = voc_df_months[voc_df_months['calltype_id']==2]
    short_callin = [1 for each in voc_df_months_callin['call_dur'] if each <= thres_dur]

    if len(short_callin) == 0:
        return arguments['represent_nan']
    else:
        return len(short_callin)


def short_callout_range(dataframe_phone_no, arguments):
    """return the range of short callout in given month"""
    thres_dur = arguments['threshold_duration']
    months = arguments['months']
    months_regex = '|'.join(months)
    voc_dataframe = dataframe_phone_no['voc']
    voc_df_months = voc_dataframe[voc_dataframe['start_datetime'].str.contains(months_regex)]
    voc_df_months['start_datetime'] = pd.to_datetime(voc_df_months['start_datetime'], format='%Y-%m-%d %H:%M:%S')
    voc_df_months['start_day'] = voc_df_months['start_datetime'].dt.day
    voc_df_months_callout = voc_df_months[voc_df_months['calltype_id'] == 1]
    voc_df_months_short_callout = voc_df_months_callout[voc_df_months_callout['call_dur'] <= thres_dur]
    short_callout_num = []
    for k in range(1, 31):
        voc_df_months_short_callout_k = voc_df_months_short_callout[voc_df_months_short_callout['start_day'] == k]
        short_callout_K = list(voc_df_months_short_callout_k['start_day'])
        short_callout_num_k = len(short_callout_K)
        short_callout_num.append(short_callout_num_k)
    if max(short_callout_num) == 0:
        return arguments['represent_nan']
    else:
        return max(short_callout_num) - min(short_callout_num)


def short_callin_range(dataframe_phone_no, arguments):
    """return the range of short callout in given month"""
    thres_dur = arguments['threshold_duration']
    months = arguments['months']
    months_regex = '|'.join(months)
    voc_dataframe = dataframe_phone_no['voc']
    voc_df_months = voc_dataframe[voc_dataframe['start_datetime'].str.contains(months_regex)]
    voc_df_months['start_datetime'] = pd.to_datetime(voc_df_months['start_datetime'], format='%Y-%m-%d %H:%M:%S')
    voc_df_months['start_day'] = voc_df_months['start_datetime'].dt.day
    voc_df_months_callin = voc_df_months[voc_df_months['calltype_id'] == 2]
    voc_df_months_short_callin = voc_df_months_callin[voc_df_months_callin['call_dur'] <= thres_dur]
    short_callin_num = []
    for k in range(1, 31):
        voc_df_months_short_callin_k = voc_df_months_short_callin[voc_df_months_short_callin['start_day'] == k]
        short_callin_K = list(voc_df_months_short_callin_k['start_day'])
        short_callin_num_k = len(short_callin_K)
        short_callin_num.append(short_callin_num_k)
    if max(short_callin_num) == 0:
        return arguments['represent_nan']
    else:
        return max(short_callin_num) - min(short_callin_num)

def ratio_friends_callout(dataframe_phone_no, arguments):
    """return the ratio of callout number from friends"""
    months = arguments['months']
    thres_friend = arguments['threshold_friend']
    months_regex = '|'.join(months)
    voc_dataframe = dataframe_phone_no['voc']
    voc_df_months = voc_dataframe[voc_dataframe['start_datetime'].str.contains(months_regex)]
    called_people = list(voc_df_months['opposite_no_m'])
    called_people_dict = dict(Counter(called_people))
    friends = []
    for opposite_no_m, times in called_people_dict.items():
        if times >= thres_friend:
            friends.append(opposite_no_m)
    voc_df_months_callout = voc_df_months[voc_df_months['calltype_id'] == 1]
    callout = list(voc_df_months_callout['opposite_no_m'])
    friends_callout = [1 for each in voc_df_months_callout['opposite_no_m'] if each in friends]
    if len(callout) == 0:
        return arguments['represent_nan']
    else:
        return len(friends_callout)/len(callout)

def ratio_friends_callin(dataframe_phone_no, arguments):
    """return the ratio of callin number from friends"""
    months = arguments['months']
    thres_friend = arguments['threshold_friend']
    months_regex = '|'.join(months)
    voc_dataframe = dataframe_phone_no['voc']
    voc_df_months = voc_dataframe[voc_dataframe['start_datetime'].str.contains(months_regex)]
    called_people = list(voc_df_months['opposite_no_m'])
    called_people_dict = dict(Counter(called_people))
    friends = []
    for opposite_no_m, times in called_people_dict.items():
        if times >= thres_friend:
            friends.append(opposite_no_m)
    voc_df_months_callin = voc_df_months[voc_df_months['calltype_id'] == 2]
    callin = list(voc_df_months_callin['opposite_no_m'])
    friends_callin = [1 for each in voc_df_months_callin['opposite_no_m'] if each in friends]
    if len(callin) == 0:
        return arguments['represent_nan']
    else:
        return len(friends_callin)/len(callin)


def long_callout(dataframe_phone_no, arguments):
    """return the number of long callout in given month"""
    months = arguments['months']
    months_regex = '|'.join(months)
    thres_dur = arguments['threshold_duration']
    voc_dataframe = dataframe_phone_no['voc']
    voc_df_months = voc_dataframe[voc_dataframe['start_datetime'].str.contains(months_regex)]
    voc_df_months_callout = voc_df_months[voc_df_months['calltype_id'] == 1]
    long_callout = [1 for dur in voc_df_months_callout['call_dur'] if dur >= thres_dur]

    if len(long_callout) == 0:
        return arguments['represent_nan']
    else:
        return len(long_callout)


def long_callin(dataframe_phone_no, arguments):
    """return the number of long callout in given month"""
    months = arguments['months']
    months_regex = '|'.join(months)
    thres_dur = arguments['threshold_duration']
    voc_dataframe = dataframe_phone_no['voc']
    voc_df_months = voc_dataframe[voc_dataframe['start_datetime'].str.contains(months_regex)]
    voc_df_months_callin = voc_df_months[voc_df_months['calltype_id'] == 2]
    long_callin = [1 for dur in voc_df_months_callin['call_dur'] if dur >= thres_dur]

    if len(long_callin) == 0:
        return arguments['represent_nan']
    else:
        return len(long_callin)


def range_long_callout(dataframe_phone_no, arguments):
    """return the range of long callout in given month"""
    months = arguments['months']
    months_regex = '|'.join(months)
    thres_dur = arguments['threshold_duration']
    voc_dataframe = dataframe_phone_no['voc']
    voc_df_months = voc_dataframe[voc_dataframe['start_datetime'].str.contains(months_regex)]
    voc_df_months['start_datetime'] = pd.to_datetime(voc_df_months['start_datetime'], format='%Y-%m-%d %H:%M:%S')
    voc_df_months['start_day'] = voc_df_months['start_datetime'].dt.day
    voc_df_months_callout = voc_df_months[voc_df_months['calltype_id'] == 1]
    voc_df_months_long_callout = voc_df_months_callout[voc_df_months_callout['call_dur'] >= thres_dur]
    long_callout_num = []
    for k in range(1, 31):
        voc_df_months_long_callout_k = voc_df_months_long_callout[voc_df_months_long_callout['start_day'] == k]
        long_callout_K = list(voc_df_months_long_callout_k['start_day'])
        long_callout_num_k = len(long_callout_K)
        long_callout_num.append(long_callout_num_k)
    if max(long_callout_num) == 0:
        return arguments['represent_nan']
    else:
        return max(long_callout_num) - min(long_callout_num)


def range_long_callin(dataframe_phone_no, arguments):
    """return the range of long callin in given month"""
    months = arguments['months']
    months_regex = '|'.join(months)
    thres_dur = arguments['threshold_duration']
    voc_dataframe = dataframe_phone_no['voc']
    voc_df_months = voc_dataframe[voc_dataframe['start_datetime'].str.contains(months_regex)]
    voc_df_months['start_datetime'] = pd.to_datetime(voc_df_months['start_datetime'], format='%Y-%m-%d %H:%M:%S')
    voc_df_months['start_day'] = voc_df_months['start_datetime'].dt.day
    voc_df_months_callin = voc_df_months[voc_df_months['calltype_id'] == 2]
    voc_df_months_long_callin = voc_df_months_callin[voc_df_months_callin['call_dur'] >= thres_dur]
    long_callin_num = []
    for k in range(1, 31):
        voc_df_months_long_callin_k = voc_df_months_long_callin[voc_df_months_long_callin['start_day'] == k]
        long_callin_K = list(voc_df_months_long_callin_k['start_day'])
        long_callin_num_k = len(long_callin_K)
        long_callin_num.append(long_callin_num_k)
    if max(long_callin_num) == 0:
        return arguments['represent_nan']
    else:
        return max(long_callin_num) - min(long_callin_num)


def range_call_dur(dataframe_phone_no, arguments):
    """return the range of call duration of everyday in given month"""
    months = arguments['months']
    months_regex = '|'.join(months)
    voc_dataframe = dataframe_phone_no['voc']
    voc_df_months = voc_dataframe[voc_dataframe['start_datetime'].str.contains(months_regex)]
    voc_df_months['start_datetime'] = pd.to_datetime(voc_df_months['start_datetime'], format='%Y-%m-%d %H:%M:%S')
    voc_df_months['start_day'] = voc_df_months['start_datetime'].dt.day
    call_dur = []
    for k in range(1,31):
        voc_df_months_k = voc_df_months[voc_df_months['start_day'] == k]
        call_dur_k = list(voc_df_months_k['call_dur'])
        dur_k = sum(call_dur_k)
        call_dur.append(dur_k)
    if max(call_dur) == 0:
        return arguments['represent_nan']
    else:
        return max(call_dur) - min(call_dur)


def range_callout_dur(dataframe_phone_no, arguments):
    """return the range of callout duration of everyday in given month"""
    months = arguments['months']
    months_regex = '|'.join(months)
    voc_dataframe = dataframe_phone_no['voc']
    voc_df_months = voc_dataframe[voc_dataframe['start_datetime'].str.contains(months_regex)]
    voc_df_months['start_datetime'] = pd.to_datetime(voc_df_months['start_datetime'], format='%Y-%m-%d %H:%M:%S')
    voc_df_months['start_day'] = voc_df_months['start_datetime'].dt.day
    voc_df_months_callout = voc_df_months[voc_df_months['calltpye_id'] == 1]
    callout_dur = []
    for k in range(1,31):
        voc_df_months_callout_k = voc_df_months_callout[voc_df_months_callout['start_day'] == k]
        callout_dur_k = list(voc_df_months_callout_k['call_dur'])
        dur_k = sum(callout_dur_k)
        callout_dur.append(dur_k)
    if max(callout_dur) == 0:
        return arguments['represent_nan']
    else:
        return max(callout_dur) - min(callout_dur)


def range_callin_dur(dataframe_phone_no, arguments):
    """return the range of callin duration of everyday in given month"""
    months = arguments['months']
    months_regex = '|'.join(months)
    voc_dataframe = dataframe_phone_no['voc']
    voc_df_months = voc_dataframe[voc_dataframe['start_datetime'].str.contains(months_regex)]
    voc_df_months['start_datetime'] = pd.to_datetime(voc_df_months['start_datetime'], format='%Y-%m-%d %H:%M:%S')
    voc_df_months['start_day'] = voc_df_months['start_datetime'].dt.day
    voc_df_months_callin = voc_df_months[voc_df_months['calltpye_id'] == 2]
    callin_dur = []
    for k in range(1,31):
        voc_df_months_callin_k = voc_df_months_callin[voc_df_months_callin['start_day'] == k]
        callin_dur_k = list(voc_df_months_callin_k['call_dur'])
        dur_k = sum(callin_dur_k)
        callin_dur.append(dur_k)
    if max(callin_dur) == 0:
        return arguments['represent_nan']
    else:
        return max(callin_dur) - min(callin_dur)


def callout_active_avr(dataframe_phone_no, arguments):
    """return the value of callout number divided by active day"""
    months = arguments['months']
    months_regex = '|'.join(months)
    voc_dataframe = dataframe_phone_no['voc']
    voc_df_months = voc_dataframe[voc_dataframe['start_datetime'].str.contains(months_regex)]
    voc_df_months['start_datetime'] = pd.to_datetime(voc_df_months['start_datetime'], format='%Y-%m-%d %H:%M:%S')
    voc_df_months['start_day'] = voc_df_months['start_datetime'].dt.day
    voc_df_months_callout = voc_df_months[voc_df_months['calltype_id'] == 1]
    active_day = set(voc_df_months_callout['start_day'])
    callout_list = list(voc_df_months_callout['start_day'])

    if len(active_day) == 0:
        return arguments['represent_nan']
    else:
        return len(callout_list)/len(active_day)


def callin_active_avr(dataframe_phone_no, arguments):
    """return the value of callin number divided by active day"""
    months = arguments['months']
    months_regex = '|'.join(months)
    voc_dataframe = dataframe_phone_no['voc']
    voc_df_months = voc_dataframe[voc_dataframe['start_datetime'].str.contains(months_regex)]
    voc_df_months['start_datetime'] = pd.to_datetime(voc_df_months['start_datetime'], format='%Y-%m-%d %H:%M:%S')
    voc_df_months['start_day'] = voc_df_months['start_datetime'].dt.day
    voc_df_months_callin = voc_df_months[voc_df_months['calltype_id'] == 2]
    active_day = set(voc_df_months_callin['start_day'])
    callin_list = list(voc_df_months_callin['start_day'])

    if len(active_day) == 0:
        return arguments['represent_nan']
    else:
        return len(callin_list)/len(active_day)


def callout_active_day_num(dataframe_phone_no, arguments):
    """return the number of callout active days in given months"""
    months = arguments['months']
    months_regex = '|'.join(months)
    voc_dataframe = dataframe_phone_no['voc']
    voc_df_months = voc_dataframe[voc_dataframe['start_datetime'].str.contains(months_regex)]
    voc_df_months_callout = voc_df_months[voc_df_months['calltype_id'] == 1]
    lst_split_datetime = list(voc_df_months_callout['start_datetime'].str.split())
    callout_active_days = set([date[0] for date in lst_split_datetime])
    return len(callout_active_days)


def callin_active_day_num(dataframe_phone_no, arguments):
    """return the number of callin active days in given months"""
    months = arguments['months']
    months_regex = '|'.join(months)
    voc_dataframe = dataframe_phone_no['voc']
    voc_df_months = voc_dataframe[voc_dataframe['start_datetime'].str.contains(months_regex)]
    voc_df_months_callin = voc_df_months[voc_df_months['calltype_id'] == 2]
    lst_split_datetime = list(voc_df_months_callin['start_datetime'].str.split())
    callin_active_days = set([date[0] for date in lst_split_datetime])
    return len(callin_active_days)


def callout_active_interval(dataframe_phone_no, arguments):
    """return the active interval"""
    months = arguments['months']
    months_regex = '|'.join(months)
    voc_dataframe = dataframe_phone_no['voc']
    voc_df_months = voc_dataframe[voc_dataframe['start_datetime'].str.contains(months_regex)]
    voc_df_months_callout = voc_df_months[voc_df_months['calltype_id'] == 1]
    lst_split_datetime = list(voc_df_months_callout['start_datetime'].str.split())
    callout_active_days = set(date[0] for date in lst_split_datetime)

    if len(callout_active_days) == 0:
        return arguments['represent_nan']
    else:
        last_day_lst = max(callout_active_days).split('-')
        first_day_lst = min(callout_active_days).split('-')
        last_day = datetime.date(int(last_day_lst[0]), int(last_day_lst[1]), int(last_day_lst[2]))
        first_day = datetime.date(int(first_day_lst[0]), int(first_day_lst[1]), int(first_day_lst[2]))
        interval = last_day - first_day

        return float(interval.days)


def callin_active_interval(dataframe_phone_no, arguments):
    """return the active interval"""
    months = arguments['months']
    months_regex = '|'.join(months)
    voc_dataframe = dataframe_phone_no['voc']
    voc_df_months = voc_dataframe[voc_dataframe['start_datetime'].str.contains(months_regex)]
    voc_df_months_callin = voc_df_months[voc_df_months['calltype_id'] == 2]
    lst_split_datetime = list(voc_df_months_callin['start_datetime'].str.split())
    callin_active_days = set([date[0] for date in lst_split_datetime])

    if len(callin_active_days) == 0:
        return arguments['represent_nan']
    else:
        last_day_lst = max(callin_active_days).split('-')
        first_day_lst = min(callin_active_days).split('-')
        last_day = datetime.date(int(last_day_lst[0]), int(last_day_lst[1]), int(last_day_lst[2]))
        first_day = datetime.date(int(first_day_lst[0]), int(first_day_lst[1]), int(first_day_lst[2]))
        interval = last_day - first_day

        return float(interval.days)

def call_var(dataframe_phone_no, arguments):
    """return the variance of call number in given months"""
    months = arguments['months']
    months_regex = '|'.join(months)
    voc_dataframe = dataframe_phone_no['voc']
    voc_df_months = voc_dataframe[voc_dataframe['start_datetime'].str.contains(months_regex)]
    voc_df_months['start_datetime'] = pd.to_datetime(voc_df_months['start_datetime'], format='%Y-%m-%d %H:%M:%S')
    voc_df_months['start_day'] = voc_df_months['start_datetime'].dt.day
    call_num = []
    for k in range(1, 31):
        voc_df_months_k = voc_df_months[voc_df_months['start_day'] == k]
        call_k = list(voc_df_months_k['start_day'])
        call_num_k = len(call_k)
        call_num.append(call_num_k)
    if max(call_num) == 0:
        return arguments['represent_nan']
    else:
        return statistics.variance(call_num)

def callout_var(dataframe_phone_no, arguments):
    """return the variance of callout number in given months"""
    months = arguments['months']
    months_regex = '|'.join(months)
    voc_dataframe = dataframe_phone_no['voc']
    voc_df_months = voc_dataframe[voc_dataframe['start_datetime'].str.contains(months_regex)]
    voc_df_months['start_datetime'] = pd.to_datetime(voc_df_months['start_datetime'], format='%Y-%m-%d %H:%M:%S')
    voc_df_months['start_day'] = voc_df_months['start_datetime'].dt.day
    voc_df_months_callout = voc_df_months[voc_df_months['calltapy_id'] == 1]
    callout_num = []
    for k in range(1, 31):
        voc_df_months_k = voc_df_months_callout[voc_df_months_callout['start_day'] == k]
        callout_k = list(voc_df_months_k['start_day'])
        callout_num_k = len(callout_k)
        callout_num.append(callout_num_k)
    if max(callout_num) == 0:
        return arguments['represent_nan']
    else:
        return statistics.variance(callout_num)

def callin_var(dataframe_phone_no, arguments):
    """return the variance of callout number in given months"""
    months = arguments['months']
    months_regex = '|'.join(months)
    voc_dataframe = dataframe_phone_no['voc']
    voc_df_months = voc_dataframe[voc_dataframe['start_datetime'].str.contains(months_regex)]
    voc_df_months['start_datetime'] = pd.to_datetime(voc_df_months['start_datetime'], format='%Y-%m-%d %H:%M:%S')
    voc_df_months['start_day'] = voc_df_months['start_datetime'].dt.day
    voc_df_months_callin = voc_df_months[voc_df_months['calltapy_id'] == 2]
    callin_num = []
    for k in range(1, 31):
        voc_df_months_k = voc_df_months_callin[voc_df_months_callin['start_day'] == k]
        callin_k = list(voc_df_months_k['start_day'])
        callin_num_k = len(callin_k)
        callin_num.append(callin_num_k)
    if max(callin_num) == 0:
        return arguments['represent_nan']
    else:
        return statistics.variance(callin_num)




# debug part: To be deleted
def test():
    data_voc = [['f0ebee98809cb1a9', 1, '2020-01-25 21:26:40', 742, '成都', '武侯区', '0a0a319fdb33f9538'],
                ['dedd4a48c3a8f', 1, '2020-02-02 20:14:33', 111, '成都', '锦江区', '0a0a319fdb33f9538'],
                ['dedd4a48c3a8f', 1, '2020-02-02 21:14:33', 11, '成都', '锦江区', '0a0a319fdb33f9538']]
    voc_df = pd.DataFrame(data_voc, columns=['opposite_no_m', 'calltype_id', 'start_datetime',
                                             'call_dur', 'city_name', 'county_name', 'imei_m'])
    dataframe_phone_no = {'voc': voc_df}
    arguments = {'months': ['2020-02'], 'represent_nan': -1, 'threshold_duration': 300}
    print(short_callout_num(dataframe_phone_no, arguments))


if __name__ == '__main__':
    test()
