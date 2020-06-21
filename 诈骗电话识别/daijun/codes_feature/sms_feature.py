#/usr/bin/env python3

import pandas as pd

def sms_people(sms_dataframe, months):
    """return number of sms people in given months"""
    # convert to datetime format
    sms_dataframe['request_datetime'] = pd.to_datetime(sms_dataframe['request_datetime'],
                                                     format='%Y%m%d %H:%M:%S')
    sms_dataframe['year_month_of_date'] = sms_dataframe.request_datetime.dt.to_period('M')
    sms_df_months = sms_dataframe.loc[lambda df: df['year_month_of_date'].dt.strftime('%Y-%m').isin(months), :]
    smsed_people = set(sms_df_months['opposite_no_m'])

    return len(smsed_people)

# debug part: To be deleted
data_sms = [['f0ebee98809cb1a9', 1, '2019-12-25 21:26:40'],
            ['dedd4a48c3a8f', 1, '2020-01-02 20:14:33']]
sms_df = pd.DataFrame(data_sms, columns=['opposite_no_m', 'calltype_id', 'request_datetime'])
num_smsed_people = sms_people(sms_df, months=['2019-12', '2020-01'])

print('input sms dataframe for given phone number:\n ', sms_df, '\n')
print('number of sms people:\n ', num_smsed_people)
