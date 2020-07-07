#/usr/bin/env python3

import pandas as pd

def called_people(voc_dataframe, months):
    """return number of called people in given months"""
    # convert to datetime format
    voc_dataframe['start_datetime'] = pd.to_datetime(voc_dataframe['start_datetime'],
                                                     format='%Y%m%d %H:%M:%S')
    voc_dataframe['year_month_of_date'] = voc_dataframe.start_datetime.dt.to_period('M')
    voc_df_months = voc_dataframe.loc[lambda df: df['year_month_of_date'].dt.strftime('%Y-%m').isin(months), :]
    called_people = set(voc_df_months['opposite_no_m'])

    return len(called_people)

def long_call(voc_dataframe, months):
    """return number of long call in given months"""
    # convert to datetime format
    voc_dataframe['start_datetime'] = pd.to_datetime(voc_dataframe['start_datetime'],
                                                     format='%Y%m%d %H:%M:%S')
    voc_dataframe['year_month_of_date'] = voc_dataframe.start_datetime.dt.to_period('M')
    voc_df_months = voc_dataframe.loc[lambda df: df['year_month_of_date'].dt.strftime('%Y-%m').isin(months), :]
    long_call_num=0
    for index,row in voc_df_months.iterrows():
        call_dur=float(row['call_dur'])
        if call_dur>=600:
            long_call_num+=1
    return long_call_num


def short_call(voc_dataframe, months):
    """return number of short call in given months"""
    # convert to datetime format
    voc_dataframe['start_datetime'] = pd.to_datetime(voc_dataframe['start_datetime'],
                                                     format='%Y%m%d %H:%M:%S')
    voc_dataframe['year_month_of_date'] = voc_dataframe.start_datetime.dt.to_period('M')
    voc_df_months = voc_dataframe.loc[lambda df: df['year_month_of_date'].dt.strftime('%Y-%m').isin(months), :]
    short_call_num=0
    for index,row in voc_df_months.iterrows():
        call_dur=float(row['call_dur'])
        if call_dur<=10:
            short_call_num+=1
    return short_call_num

# debug part: To be deleted
data_voc = [['f0ebee98809cb1a9', 1, '2019-12-25 21:26:40', 6, '成都', '武侯区', '0a0a319fdb33f9538'],
            ['dedd4a48c3a8f', 1, '2020-01-02 20:14:33', 111, '成都', '锦江区', '0a0a319fdb33f9538']]
voc_df = pd.DataFrame(data_voc, columns=['opposite_no_m', 'calltype_id', 'start_datetime',
                                 'call_dur', 'city_name', 'county_name', 'imei_m'])

num_long_call=long_call(voc_df, months=['2019-12']);
num_short_call=short_call(voc_df, months=['2019-12']);
num_called_people = called_people(voc_df, months=['2019-12'])#, '2020-01'])
print('input voc dataframe for given phone number:\n ', voc_df, '\n')
print('number of called people:\n ', num_called_people)
