import pandas as pd
import math

def city_name(dataframe_phone_no, arguments):
    """return the city of user"""

    user_dataframe = dataframe_phone_no['user']
    city = list(user_dataframe['city_name'])

    if '成都' in city:
        return -1
    elif '天府新区' in city:
        return -2
    elif '乐山' in city:
        return 1
    elif '内江' in city:
        return 2
    elif '凉山' in city:
        return 3
    elif '南充' in city:
        return 4
    elif '宜宾' in city:
        return 5
    elif '巴中' in city:
        return 6
    elif '广元 ' in city:
        return 7
    elif '广安' in city:
        return 8
    elif '德阳' in city:
        return 9
    elif '攀枝花' in city:
        return 10
    elif '泸州' in city:
        return 11
    elif '甘孜' in city:
        return 12
    elif '眉山' in city:
        return 13
    elif '绵阳' in city:
        return 14
    elif '自贡' in city:
        return 15
    elif '资阳' in city:
        return 16
    elif '达州' in city:
        return 17
    elif '遂宁' in city:
        return 18
    elif '阿坝' in city:
        return 19
    elif '雅安' in city:
        return 20
    else:
        return arguments['represent_nan']

def arpu_nan(dataframe_phone_no, arguments):
    """check whether arpu is Nan"""
    user_dataframe = dataframe_phone_no['user']
    months = arguments('arpu_201908', 'arpu_201909', 'arpu_201910', 'arpu_201910', 'arpu_201911',
                       'arpu_201912', 'arpu_202001', 'arpu_202002', 'arpu_202003', 'arpu_202004',
                       'arpu_202005')
    arpu = user_dataframe[months]
    if len(arpu) == 0:
        return 0
    else:
        return 1


