# /usr/bin/env python3

import pandas as pd
import numpy as np

day = 60 * 60 * 24


# 转换日期为整形数值
def convertTostemp(time):
    hhmmss = time.split(":")
    h = int(hhmmss[0]) * 60 * 60
    m = int(hhmmss[1]) * 60
    s = int(hhmmss[2])

    return h + m + s


# 获取列表每日最早通话时间
def get_early(datelist):
    earlylist = {}
    for date in datelist:
        early = 0
        for time in datelist[date]:
            if early == 0 or early > time:
                early = time / day
        earlylist[date] = early
    return earlylist


# 获取列表最晚通话时间
def get_late(datelist):
    latelist = {}
    for date in datelist:
        late = 0
        for time in datelist[date]:
            if late == 0 or late < time:
                late = time / day
        latelist[date] = late
    return latelist


def getMin(datelist):
    min = 0
    for time in datelist:
        if min == 0 or datelist[time] < min:
            min = datelist[time]
    return min


def getMax(datelist):
    max = 0
    for time in datelist:
        if max == 0 or datelist[time] > max:
            max = datelist[time]
    return max


def first_sms_time(dataframe_phone_no, arguments):
    months = arguments['months']
    stats = arguments['statistics']
    months_regex = '|'.join(months)
    sms_dataframe = dataframe_phone_no['sms']
    # 对应该月份的数据
    sms_df_months = sms_dataframe[sms_dataframe['request_datetime'].str.contains(months_regex)]

    timelist = list(sms_df_months['request_datetime'])
    datelist = {}
    for time in timelist:
        timesp = time.split(" ")
        if timesp[0] in datelist.keys():
            datelist.get(timesp[0]).append(convertTostemp(timesp[1]))
        else:
            datelist[timesp[0]] = [convertTostemp(timesp[1])]
    earlylist = get_early(datelist)

    if stats == 'min':
        return getMin(earlylist)
    elif stats == 'max':
        return getMax(earlylist)
    elif stats == 'mean':
        if len(earlylist) == 0:
            return 0.0
        return np.mean(list(earlylist.values()))
    elif stats == 'median':
        if len(earlylist) == 0:
            return 0.0
        return np.median(list(earlylist.values()))
    elif stats == 'std':
        # if no call in months, assign std to 0.01
        if len(earlylist) == 0:
            return 0.01
        return np.std(list(earlylist.values()))


def last_sms_time(dataframe_phone_no, arguments):
    months = arguments['months']
    stats = arguments['statistics']
    months_regex = '|'.join(months)
    sms_dataframe = dataframe_phone_no['sms']
    # 对应该月份的数据
    sms_df_months = sms_dataframe[sms_dataframe['request_datetime'].str.contains(months_regex)]

    timelist = list(sms_df_months['request_datetime'])
    datelist = {}
    for time in timelist:
        timesp = time.split(" ")
        if timesp[0] in datelist.keys():
            datelist.get(timesp[0]).append(convertTostemp(timesp[1]))
        else:
            datelist[timesp[0]] = [convertTostemp(timesp[1])]
    lastlist = get_late(datelist)

    if stats == 'min':
        return getMin(lastlist)
    elif stats == 'max':
        return getMax(lastlist)
    elif stats == 'mean':
        if len(lastlist) == 0:
            return 0.0
        return np.mean(list(lastlist.values()))
    elif stats == 'median':
        if len(lastlist) == 0:
            return 0.0
        return np.median(list(lastlist.values()))
    elif stats == 'std':
        if len(lastlist) == 0:
            return 0.01
        return np.std(list(lastlist.values()))



# debug part: To be deleted
def test():
    data_sms = [['f0ebee98809cb1a9', 1, '2019-12-25 21:26:40'],
                ['dedd4a48c3a8f', 1, '2020-01-02 20:14:33'],
                ['dedd4a48c3a8f', 1, '2019-12-02 20:14:33'],
                ['sdfsd4a48c3a8f', 1, '2019-12-02 11:14:11']]
    sms_df = pd.DataFrame(data_sms, columns=['opposite_no_m', 'calltype_id', 'request_datetime'])
    dataframe_phone_no = {"sms": sms_df}
    arguments = {"months": ['2019-12'], 'statistics': 'min'}
    num_smsed_people = last_sms_time(dataframe_phone_no, arguments)

    print('number of sms people:\n ', num_smsed_people)


if __name__ == '__main__':
    test()
