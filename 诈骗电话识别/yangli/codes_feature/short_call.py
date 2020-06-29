#/usr/bin/env python3

import pandas as pd

def called_people(dataframe_phone_no, arguments):
    """return number of short call in given months"""
    # convert to datetime format
    months = arguments['months']
    voc_dataframe = dataframe_phone_no['voc']
    voc_dataframe['start_datetime'] = pd.to_datetime(voc_dataframe['start_datetime'],
                                                     format='%Y%m%d %H:%M:%S')
    voc_dataframe['year_month_of_date'] = voc_dataframe.start_datetime.dt.to_period('M')
    voc_df_months = voc_dataframe.loc[lambda df: df['year_month_of_date'].dt.strftime('%Y-%m').isin(months), :]
    short_call=voc_df_months.df[[each<6 for each in voc_df_months['call_dur'] ]]

    return len(short_call)