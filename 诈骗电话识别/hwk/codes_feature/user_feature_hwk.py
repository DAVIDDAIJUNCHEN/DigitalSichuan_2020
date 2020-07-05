#/usr/bin/env python3

import pandas as pd
import numpy as np

def idcard_cnt(dataframe_phone_no, arguments):
    """return number of idcards for given phone_no"""
    user_dataframe = dataframe_phone_no['user']
    return float(user_dataframe['idcard_cnt'])

def arpu_mean(dataframe_phone_no, arguments):
    user_dataframe = dataframe_phone_no['user']
    kk=list(user_dataframe.keys());
    vv=user_dataframe.values[0]

    month_arpu_dict={}
    for ii in range(len(kk)-1):
        mm=kk[ii+1][5:]
        month_arpu_dict[mm]=vv[ii+1]

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





# debug part: To be deleted
def test():
    data_user = [['7bcf933547b6776b1','','45.0','45.0','45.0','45.0','45.0','45','45.0']]
    user_df = pd.DataFrame(data_user, columns=['opposite_no_m', 'arpu_201908','arpu_201909','arpu_201910','arpu_201911','arpu_201912','arpu_202001','arpu_202002','arpu_202003'])
    dataframe_phone_no = {'user': user_df}
    arguments = {"months": ['2019-08']}
    am= arpu_mean(dataframe_phone_no, arguments)
    print('input voc dataframe for given phone number:\n ', user_df, '\n')


if __name__ == '__main__':
    test()
