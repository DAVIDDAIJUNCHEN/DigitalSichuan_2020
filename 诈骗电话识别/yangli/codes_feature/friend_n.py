#/usr/bin/env python3

import pandas as pd

def friends_n(dataframe_phone_no, arguments):
    """return number of friends in given months"""
    # convert to datetime format
    months = arguments['months']
    voc_dataframe = dataframe_phone_no['voc']
    voc_dataframe['start_datetime'] = pd.to_datetime(voc_dataframe['start_datetime'],
                                                     format='%Y%m%d %H:%M:%S')
    voc_dataframe['year_month_of_date'] = voc_dataframe.start_datetime.dt.to_period('M')
    voc_df_months = voc_dataframe.loc[lambda df: df['year_month_of_date'].dt.strftime('%Y-%m').isin(months), :]
    called_people = list(voc_df_months['opposite_no_m'])
    called_people_dic={}
    for item_str in called_people:
        if item_str not in called_people_dic:
           called_people_dic[item_str]=1
        else:
           called_people_dic[item_str]+=1
    friend=[]
    for k in called_people_dic:
        friend.append(k)
    for k in friend
        if called_people_dic[k]=1,2,3,4
          del friend[k]
    return len(friend)