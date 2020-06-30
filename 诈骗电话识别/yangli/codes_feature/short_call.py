#/usr/bin/env python3

import pandas as pd

def called_people(dataframe_phone_no, arguments):
    """return number of short call in given months"""
    # convert to datetime format
    months = arguments['months']
    months_regex = '|'.join(months)
    voc_dataframe = dataframe_phone_no['voc']
    voc_df_months = voc_dataframe[voc_dataframe['start_datetime'].str.contains(months_regex)]
    short_call = [1 for each in voc_df_months['call_dur'] if each < 6]
    return len(short_call)