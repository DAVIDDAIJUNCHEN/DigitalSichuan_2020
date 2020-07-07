#/usr/bin/env python3

import pandas as pd

def num_app(app_dataframe):
    """return number of called people in given months"""
    # convert to datetime format
    app_dataframe['month_id'] = pd.to_datetime(app_dataframe['month_id'], format='%Y-%m')
    num_apps = set(app_dataframe['busi_name'])
    return len(num_apps)

def video_audio_flow(app_dataframe,months):
    """return number of video_audio_flow in given months"""
    # convert to datetime format
    app_dataframe['month_id'] = pd.to_datetime(app_dataframe['month_id'], format='%Y-%m')
    app_df_months = app_dataframe.loc[lambda df: df['month_id'].isin(months),:]
    flow=0
    video_audio_app_set=set()
    video_audio_app_set.add('腾讯视频')
    video_audio_app_set.add('优酷')

    for index, row in app_df_months.iterrows():
        print(row)
        if row['busi_name'] in video_audio_app_set:
            flow+=row['flow']
    return flow






# debug part: To be deleted
data_app = [['NaN', 8.33, '2019-11'], ['QQ', 13.527, '2019-03'],
            ['QQ', 15.22, '2019-04'], ['旺信', 10.22, '2019-03'],
            ['腾讯视频',40,'2019-12'],['优酷',90,'2019-12']]

app_df = pd.DataFrame(data_app, columns=['busi_name', 'flow', 'month_id'])

flow=video_audio_flow(app_df,months=['2019-12']);

num_apps = num_app(app_df)
print('input app dataframe for given phone number:\n ', app_df, '\n')
print('number of apps:\n ', num_apps)
