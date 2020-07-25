#/usr/bin/env python3

import pandas as pd

def idcard_cnt(dataframe_phone_no, arguments):
    """return number of idcards for given phone_no"""
    user_dataframe = dataframe_phone_no['user']
    if len(user_dataframe) == 0:
        return arguments['represent_nan']

    return float(user_dataframe['idcard_cnt'])

# debug part: To be deleted
def test():
    data_user = [['f0ebee98809cb1a9', 3, '2019-12-25 21:26:40', 42, '成都', '武侯区', '0a0a319fdb33f9538']]
    user_df = pd.DataFrame(data_user, columns=['opposite_no_m', 'idcard_cnt', 'start_datetime',
                                     'call_dur', 'city_name', 'county_name', 'imei_m'])
    dataframe_phone_no = {'user': user_df}
    arguments = {}
    number_idcard = idcard_cnt(dataframe_phone_no, arguments)
    print('input voc dataframe for given phone number:\n ', user_df, '\n')
    print('number of idcards:\n ', number_idcard)

if __name__ == '__main__':
    test()
