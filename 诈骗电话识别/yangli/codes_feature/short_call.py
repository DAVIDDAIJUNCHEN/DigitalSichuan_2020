#/usr/bin/env python3

import pandas as pd

def num_shortcall(dataframe_phone_no, arguments):
    """return number of short calls in given months"""
    # convert to datetime format
    months = arguments['months']
    months_regex = '|'.join(months)
    thres_calldur = arguments['threshold_duration']
    voc_dataframe = dataframe_phone_no['voc']
    voc_df_months = voc_dataframe[voc_dataframe['start_datetime'].str.contains(months_regex)]
    short_call = [1 for each in voc_df_months['call_dur'] if each <= thres_calldur]

    return len(short_call)

def ratio_shortcall(dataframe_phone_no, arguments):
    """return ratio of short calls in given months"""
    # convert to datetime format
    months = arguments['months']
    months_regex = '|'.join(months)
    thres_calldur = arguments['threshold_duration']
    voc_dataframe = dataframe_phone_no['voc']
    voc_df_months = voc_dataframe[voc_dataframe['start_datetime'].str.contains(months_regex)]
    num_short_call = len([1 for dur in voc_df_months['call_dur'] if dur < thres_calldur])
    if len(voc_df_months) == 0:
        return 0.0
    return num_short_call / len(voc_df_months)

# debug part: To be deleted
def test():
    data_voc = [['f0ebee98809cb1a9', 2, '2019-12-25 21:26:40', 42, '成都', '武侯区', '0a0a319fdb33f9538'],
                ['dedd4a48c3a8f', 3, '2020-01-02 20:14:33', 111, '成都', '锦江区', '0a0a319fdb33f9538']]#,
                #['dedd4a48c3a8f', 1, '2020-01-02 20:14:33', 90, '成都', '锦江区', '0a0a319fdb33f9538']]
    voc_df = pd.DataFrame(data_voc, columns=['opposite_no_m', 'calltype_id', 'start_datetime',
                                     'call_dur', 'city_name', 'county_name', 'imei_m'])
    dataframe_phone_no = {'voc': voc_df}
    arguments = {"months": ['2019-12', '2020-01'], "threshold_duration": 50}
    ratio_shortcall(dataframe_phone_no, arguments)

if __name__ == '__main__':
    test()