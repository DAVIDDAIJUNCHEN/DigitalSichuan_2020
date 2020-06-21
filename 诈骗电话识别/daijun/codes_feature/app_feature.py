#/usr/bin/env python3

import pandas as pd

def num_app(app_dataframe):
    """return number of called people in given months"""
    # convert to datetime format
    app_dataframe['month_id'] = pd.to_datetime(app_dataframe['month_id'], format='%Y-%m')
    num_apps = set(app_dataframe['busi_name'])

    return len(num_apps)

# debug part: To be deleted
data_app = [['NaN', 8.33, '2019-11'], ['QQ', 13.527, '2019-03'],
            ['QQ', 15.22, '2019-04'], ['旺信', 10.22, '2019-03']]

app_df = pd.DataFrame(data_app, columns=['busi_name', 'flow', 'month_id'])

num_apps = num_app(app_df)
print('input app dataframe for given phone number:\n ', app_df, '\n')
print('number of apps:\n ', num_apps)
