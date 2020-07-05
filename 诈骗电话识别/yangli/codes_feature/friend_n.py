#/usr/bin/env python3

import pandas as pd
from collections import Counter

def ratio_friends(dataframe_phone_no, arguments):
    """return number of friends in given months"""
    # convert to datetime format
    months = arguments['months']
    thres_friend = arguments['threshold_friend']
    months_regex = '|'.join(months)
    voc_dataframe = dataframe_phone_no['voc']
    voc_df_months = voc_dataframe[voc_dataframe['start_datetime'].str.contains(months_regex)]
    called_people = list(voc_df_months['opposite_no_m'])
    called_people_dict = dict(Counter(called_people))
    num_friend = 0

    for opposite_phone, times in called_people_dict.items():
        if times >= thres_friend:
            num_friend += 1
    # if no called people in these months, assign 100%
    if len(called_people) == 0:
        return 1.0

    return num_friend / len(called_people_dict)

def test():
    data_voc = [['f0ebee98809cb1a9', 1, '2019-12-25 21:26:40', 42, '成都', '武侯区', '0a0a319fdb33f9538'],
                ['dedd4a48c3a8f', 1, '2020-01-02 20:14:33', 111, '成都', '锦江区', '0a0a319f db33f9538'],
                ['dedd4a48c3a8f', 1, '2020-01-02 20:14:33', 90, '成都', '锦江区', '0a0a319fdb33f9538']]

    voc_df = pd.DataFrame(data_voc, columns=['opposite_no_m', 'calltype_id', 'start_datetime',
                                     'call_dur', 'city_name', 'county_name', 'imei_m'])
    dataframe_phone_no = {'voc': voc_df}
    arguments = {"months": ['2019-12', '2020-01'], 'threshold_friend': 2}
    print(ratio_friends(dataframe_phone_no, arguments))

if __name__ == '__main__':
    test()