#/usr/bin/env python3

import pandas as pd
import numpy as np
import math


def idcard_cnt(dataframe_phone_no, arguments):
    """return number of idcards for given phone_no"""
    user_dataframe = dataframe_phone_no['user']
    if len(user_dataframe) == 0:
        return arguments['represent_nan']

    return float(user_dataframe['idcard_cnt'])


def isempty_last_arpu(dataframe_phone_no, arguments):
    """return 1 if latest arpu is empty else 0"""
    user_dataframe = dataframe_phone_no['user']
    user_columns = list(user_dataframe.keys())
    arpu_columns = [col for col in user_columns if 'arpu_' in col]

    arpu_last = user_dataframe[[arpu_columns[-1]]].values[0][0]

    if math.isnan(arpu_last):
        return 1
    else:
        return 0


# debug part: To be deleted
def test():
    data_user = [['672ddbf02a5544d32e4ecc9433','绵阳','江油分公司', 1, 46.06, 45, 45, 45, 45, 45, 45, 45, 0],
                 ['5e1272273', '德阳', '旌阳分公司', 1, 79, 79.2, 79.1, 79.3, 41.4, 34.1, 59.4, 60, 0]]

    user_df = pd.DataFrame(data_user, columns=['phone_no_m', 'city_name', 'county_name', 'idcard_cnt', 'arpu_201908',
                                               'arpu_201909', 'arpu_201910', 'arpu_201911', 'arpu_201912', 'arpu_202001',
                                               'arpu_202002', 'arpu_202003', 'label'])
    dataframe_phone_no = {'user': user_df}
    arguments = {}
    number_idcard = isempty_last_arpu(dataframe_phone_no, arguments)
    print(number_idcard)

if __name__ == '__main__':
    test()

