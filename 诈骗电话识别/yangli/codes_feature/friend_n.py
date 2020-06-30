#/usr/bin/env python3

import pandas as pd

def friends_n(dataframe_phone_no, arguments):
    """return number of friends in given months"""
    # convert to datetime format
    months = arguments['months']
    months_regex = '|'.join(months)
    voc_dataframe = dataframe_phone_no['voc']
    voc_df_months = voc_dataframe[voc_dataframe['start_datetime'].str.contains(months_regex)]
    called_people = list(voc_df_months['opposite_no_m'])
    called_people_dic={}
    for item_str in called_people:
        if item_str not in called_people_dic.keys():
           called_people_dic[item_str] = 1
        else:
           called_people_dic[item_str] += 1

    friends = []

    for k in called_people_dic.keys():
        if called_people_dic[k] > 4:
            friends.append(k)

    return len(friends)