#/usr/bin/env python3

import pandas as pd
import numpy as np
import math

def idcard_cnt(dataframe_phone_no, arguments):
    """return number of idcards for given phone_no"""
    user_dataframe = dataframe_phone_no['user']
    return float(user_dataframe['idcard_cnt'])

def arpu_mean(dataframe_phone_no, arguments):
    user_dataframe = dataframe_phone_no['user']
    user_columns = list(user_dataframe.keys())
    arpu_columns = [col for col in user_columns if 'arpu_' in col]
    arpu_lst = list(user_dataframe[arpu_columns].values[0])
    mean_arpu = np.mean([float(arpu) for arpu in arpu_lst if arpu != ''])
    if math.isnan(mean_arpu):
        return 45.
    return mean_arpu

def arpu_mean2(dataframe_phone_no, arguments):
    user_dataframe = dataframe_phone_no['user']
    kk=list(user_dataframe.keys());
    vv=user_dataframe.values[0]

    month_arpu_dict={}
    for ii in range(len(kk)-3):
        mm=kk[ii+3][5:]
        month_arpu_dict[mm]=vv[ii+3]

    months = arguments['months']
    arpu_sum=0
    month_count=0
    for mm in months:
        k=mm[:4]+mm[5:]
        if k in month_arpu_dict:
            if  not np.isnan(month_arpu_dict[k]):
                month_count+=1
                arpu_sum+=float(month_arpu_dict[k])

    if month_count==0:
        return -1
    else:
        if np.isnan(arpu_sum/month_count):
            print(vv)
        return arpu_sum/month_count

def arpu_std(dataframe_phone_no, arguments):
    user_dataframe = dataframe_phone_no['user']
    user_columns = list(user_dataframe.keys())
    arpu_columns = [col for col in user_columns if 'arpu_' in col]
    arpu_lst = list(user_dataframe[arpu_columns].values[0])
    std_arpu = np.std([float(arpu) for arpu in arpu_lst if arpu != ''])
    if math.isnan(std_arpu):
        return 0.01
    return std_arpu

# debug part: To be deleted
def test():
    data_user = [['7bcf933547b6776b1','','45.0','45.0','45.0','45.0','45.0','45','45.0']]
    user_df = pd.DataFrame(data_user, columns=['opposite_no_m', 'arpu_201908','arpu_201909','arpu_201910','arpu_201911','arpu_201912','arpu_202001','arpu_202002','arpu_202003'])
    dataframe_phone_no = {'user': user_df}
    arguments = {"months": ['2019-08']}
    am = arpu_mean(dataframe_phone_no, arguments)
    print(am)
    print('input voc dataframe for given phone number:\n ', user_df, '\n')


if __name__ == '__main__':
    test()
