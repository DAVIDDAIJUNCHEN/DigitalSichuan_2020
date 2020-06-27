#/usr/bin/env python3

import pandas as pd

def called_people(dataframe_phone_no, arguments):
    months = arguments['months']
    months_regex = '|'.join(months)
    voc_dataframe = dataframe_phone_no['voc']
    voc_df_months = voc_dataframe[voc_dataframe['start_datetime'].str.contains(months_regex)]
    called_people = set(voc_df_months['opposite_no_m'])
    return len(called_people)



def long_call(dataframe_phone_no, arguments):
    """return number of long call in given months"""
    # convert to datetime format
    months = arguments['months']
    months_regex = '|'.join(months)
    voc_dataframe = dataframe_phone_no['voc']
    voc_df_months = voc_dataframe[voc_dataframe['start_datetime'].str.contains(months_regex)]
    long_call_num=0
    for index,row in voc_df_months.iterrows():
        call_dur=float(row['call_dur'])
        if call_dur>=1500:
            long_call_num+=1
    return long_call_num



# debug part: To be deleted
def test():
    data_voc = [['f0ebee98809cb1a9', 1, '2019-12-25 21:26:40', 742, '成都', '武侯区', '0a0a319fdb33f9538'],
                ['dedd4a48c3a8f', 1, '2020-01-02 20:14:33', 111, '成都', '锦江区', '0a0a319fdb33f9538']]
    voc_df = pd.DataFrame(data_voc, columns=['opposite_no_m', 'calltype_id', 'start_datetime',
                                     'call_dur', 'city_name', 'county_name', 'imei_m'])
    dataframe_phone_no = {'voc': voc_df}
    arguments = {"months": ['2019-12']}


    num_called_people = called_people(dataframe_phone_no, arguments)#, '2020-01'])
    long_call_num = long_call(dataframe_phone_no, arguments)
    print('input voc dataframe for given phone number:\n ', voc_df, '\n')
    print('number of called people:\n ', num_called_people)

if __name__ == '__main__':
    test()
