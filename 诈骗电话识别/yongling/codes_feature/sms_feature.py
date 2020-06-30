#/usr/bin/env python3

import pandas as pd

def sms_people(dataframe_phone_no, arguments):
    months = arguments['months']
    months_regex = '|'.join(months)
    sms_dataframe = dataframe_phone_no['sms']
    sms_df_months = sms_dataframe[sms_dataframe['request_datetime'].str.contains(months_regex)]
    smsed_people = set(sms_df_months['opposite_no_m'])
    return len(smsed_people)

# debug part: To be deleted
def test():
    data_sms = [['f0ebee98809cb1a9', 1, '2019-12-25 21:26:40'],
                ['dedd4a48c3a8f', 1, '2020-01-02 20:14:33']]
    sms_df = pd.DataFrame(data_sms, columns=['opposite_no_m', 'calltype_id', 'request_datetime'])
    dataframe_phone_no = {"sms": sms_df}
    arguments = {"months": ['2019-12', '2020-01']}
    num_smsed_people = sms_people(dataframe_phone_no, arguments)

    print('input sms dataframe for given phone number:\n ', sms_df, '\n')
    print('number of sms people:\n ', num_smsed_people)

if __name__ == '__main__':
    test()
