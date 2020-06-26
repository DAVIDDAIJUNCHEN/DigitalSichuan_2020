#/usr/bin/env python3

import pandas as pd
import time

# def called_people(dataframe_phone_no, arguments):
#     """return number of called people in given months"""
#     # convert to datetime format
#     t0 = time.time()
#     months = arguments['months']
#     months = pd.DataFrame(months, columns=['year_month_of_date'])
#     months['year_month_of_date'] = pd.to_datetime(months['year_month_of_date'],
#                                                   format='%Y-%m')
#     months['year_month_of_date'] = months.year_month_of_date.dt.to_period('M')
#
#     voc_dataframe = dataframe_phone_no['voc']
#     voc_dataframe['start_datetime'] = pd.to_datetime(voc_dataframe['start_datetime'],
#                                                      format='%Y%m%d %H:%M:%S')
#
#     voc_dataframe['year_month_of_date'] = voc_dataframe.start_datetime.dt.to_period('M')
#     check = voc_dataframe['year_month_of_date'].isin(months['year_month_of_date'])
#     print('t0:', time.time() - t0)
#     voc_df_months = voc_dataframe[check]
#
#     #voc_df_months = voc_dataframe.loc[lambda df: df['year_month_of_date'].dt.strftime('%Y-%m').isin(months), :]
#     called_people = set(voc_df_months['opposite_no_m'])
#
#     return len(called_people)

def called_people(dataframe_phone_no, arguments):
    months = arguments['months']
    months_regex = '|'.join(months)
    voc_dataframe = dataframe_phone_no['voc']
    voc_df_months = voc_dataframe[voc_dataframe['start_datetime'].str.contains(months_regex)]
    called_people = set(voc_df_months['opposite_no_m'])
    return len(called_people)

# debug part: To be deleted
def test():
    data_voc = [['f0ebee98809cb1a9', 1, '2019-12-25 21:26:40', 42, '成都', '武侯区', '0a0a319fdb33f9538'],
                ['dedd4a48c3a8f', 1, '2020-01-02 20:14:33', 111, '成都', '锦江区', '0a0a319fdb33f9538']]
    voc_df = pd.DataFrame(data_voc, columns=['opposite_no_m', 'calltype_id', 'start_datetime',
                                     'call_dur', 'city_name', 'county_name', 'imei_m'])
    dataframe_phone_no = {'voc': voc_df}
    arguments = {"months": ['2019-12']}
    num_called_people = called_people(dataframe_phone_no, arguments)#, '2020-01'])
    print('input voc dataframe for given phone number:\n ', voc_df, '\n')
    print('number of called people:\n ', num_called_people)

if __name__ == '__main__':
    test()
