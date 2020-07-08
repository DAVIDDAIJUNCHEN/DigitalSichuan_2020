import pandas as pd
import numpy as np

def call_in_total_time(dataframe_phone_no, arguments):
    """returne the total duration of call in calls"""
    months = arguments['months']
    months_regex = '|'.join(months)
    voc_dataframe = dataframe_phone_no['voc']
    voc_df_months = voc_dataframe[voc_dataframe['start_datetime'].str.contains(months_regex)]
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

    return total_time/call_in_num

def call_in_people(dataframe_phone_no, arguments):
    """return the number of call in people"""
    months = arguments['months']
    months_regex = '|'.join(months)
    voc_dataframe = dataframe_phone_no['voc']
    voc_df_months = voc_dataframe[voc_dataframe['start_datetime'].str.contains(months_regex)]
    voc_df_months_callin = voc_df_months.loc[voc_df_months['calltype_id'] == 2]
    call_in_people = set(voc_df_months_callin['opposite_no_m'])

    return len(call_in_people)

def call_out_total_time(dataframe_phone_no, arguments):
    """returne the total duration of call out calls"""
    months = arguments['months']
    months_regex = '|'.join(months)
    voc_dataframe = dataframe_phone_no['voc']
    voc_df_months = voc_dataframe[voc_dataframe['start_datetime'].str.contains(months_regex)]
    voc_df_months_callout = voc_df_months.loc[voc_df_months['calltype_id'] == 1]

    return float(voc_df_months_callout['call_dur'].sum())

def call_out_time_avr(dataframe_phone_no, arguments):
    """returne the average duration of call out calls"""
    months = arguments['months']
    months_regex = '|'.join(months)
    voc_dataframe = dataframe_phone_no['voc']
    voc_df_months = voc_dataframe[voc_dataframe['start_datetime'].str.contains(months_regex)]
    voc_df_months_callout = voc_df_months.loc[voc_df_months['calltype_id'] == 1]
    total_time = float(voc_df_months_callout['call_dur'].sum())
    call_out_num = len(voc_df_months_callout['call_dur'])
    if call_out_num == 0:
        call_out_num = 1

    return total_time/call_out_num

def call_out_people(dataframe_phone_no, arguments):
    """return the number of call in people"""
    months = arguments['months']
    months_regex = '|'.join(months)
    voc_dataframe = dataframe_phone_no['voc']
    voc_df_months = voc_dataframe[voc_dataframe['start_datetime'].str.contains(months_regex)]
    voc_df_months_callout = voc_df_months.loc[voc_df_months['calltype_id'] == 1]
    call_out_people = set(voc_df_months_callout['opposite_no_m'])

    return len(call_out_people)





# debug part: To be deleted
def test():
    data_voc = [['f0ebee98809cb1a9', 1, '2020-01-25 21:26:40', 742, '成都', '武侯区', '0a0a319fdb33f9538'],
                ['dedd4a48c3a8f', 1, '2020-01-02 20:14:33', 111, '成都', '锦江区', '0a0a319fdb33f9538'],
                ['dedd4a48c3a8f', 1, '2020-01-02 21:14:33', 11, '成都', '锦江区', '0a0a319fdb33f9538']]
    voc_df = pd.DataFrame(data_voc, columns=['opposite_no_m', 'calltype_id', 'start_datetime',
                                     'call_dur', 'city_name', 'county_name', 'imei_m'])
    dataframe_opposite_phone_no = {'voc': voc_df}