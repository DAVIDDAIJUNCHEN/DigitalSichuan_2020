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


def first_call_time(dataframe_phone_no, arguments):
    months = arguments['months']
    stats = arguments['statistics']
    months_regex = '|'.join(months)
    voc_dataframe = dataframe_phone_no['voc']
    # 对应该月份的数据
    voc_df_months = voc_dataframe[voc_dataframe['start_datetime'].str.contains(months_regex)]

    timelist = list(voc_df_months['start_datetime'])
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
        return np.mean(list(earlylist.values()))
    elif stats == 'median':
        return np.median(list(earlylist.values()))
    elif stats == 'std':
        return np.std(list(earlylist.values()))

def last_call_time(dataframe_phone_no, arguments):
    months = arguments['months']
    stats = arguments['statistics']
    months_regex = '|'.join(months)
    voc_dataframe = dataframe_phone_no['voc']
    # 对应该月份的数据
    voc_df_months = voc_dataframe[voc_dataframe['start_datetime'].str.contains(months_regex)]

    timelist = list(voc_df_months['start_datetime'])
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
        return np.mean(list(lastlist.values()))
    elif stats == 'median':
        return np.median(list(lastlist.values()))
    elif stats == 'std':
        return np.std(list(lastlist.values()))


def calltype_per(dataframe_phone_no, arguments):
    months = arguments['months']
    months_regex = '|'.join(months)
    voc_dataframe = dataframe_phone_no['voc']
    voc_df_months = voc_dataframe[voc_dataframe['start_datetime'].str.contains(months_regex)]
    called_people = set(voc_df_months['opposite_no_m'])
    voc_df_type = voc_dataframe[voc_dataframe['calltype_id'] == 1]

    # print("------",voc_df_type,called_people)
    if len(called_people) == 0:
        return 0

    return len(voc_df_type) / len(called_people)


# debug part: To be deleted
def test():
    data_voc = [['f0ebee98809cb1a9', 1, '2019-12-25 21:26:40', 42, '成都', '武侯区', '0a0a319fdb33f9538'],
                ['dedd4a48c3a8f', 1, '2020-01-02 20:14:33', 111, '成都', '锦江区', '0a0a319fdb33f9538'],
                ['dedd4a48c3a8f', 1, '2019-12-02 20:14:33', 111, '成都', '锦江区', '0a0a319fdb33f9538'],
                ['sdfsd4a48c3a8f', 1, '2019-12-02 11:14:11', 111, '成都', '锦江区', '0a0a319fdb33f9538']]
    voc_df = pd.DataFrame(data_voc, columns=['opposite_no_m', 'calltype_id', 'start_datetime',
                                             'call_dur', 'city_name', 'county_name', 'imei_m'])
    dataframe_phone_no = {'voc': voc_df}
    arguments = {"months": ['2019-12'], 'statistics': 'min'}
    num_called_people = last_call_time(dataframe_phone_no, arguments)  # , '2020-01'])
    print(num_called_people)


if __name__ == '__main__':
    test()
