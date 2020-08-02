#/usr/bin/env python3
import pandas as pd
import math

def num_app(dataframe_phone_no, arguments):
    """return number of called people in given months"""
    # convert to datetime formatA
    app_dataframe = dataframe_phone_no['app']
    if len(app_dataframe) == 0:
        return arguments['represent_nan']

    num_apps = set(app_dataframe['busi_name'])
    return len(num_apps)


def appstore_num(dataframe_phone_no, arguments):
    """return the number of appstore"""
    appstore = {'小米应用商店', 'AppStore', '华为应用市场', '魅族应用中心', 'VIVO应用商店', '酷派应用商店', '中兴应用商店',
                  '三星应用商店', 'oppo应用商店', '一加手机官网', '联想乐商店', '锤子应用商店'}
    months = arguments['months']
    months_regex = '|'.join(months)
    app_dataframe = dataframe_phone_no['app']
    if app_dataframe['month_id'].isnull().values.all():
        return arguments['represent_nan']
    else:
        app_df_months = app_dataframe[app_dataframe['month_id'].str.contains(months_regex)]
    app = list(app_df_months['busi_name'])
    app_set = set([entry for entry in app if not entry != entry])

    num_appstore = app_set & appstore

    return len(num_appstore)

# debug part: To be deleted
def test():
    data_app = [['NaN', 8.33, '2019-11'], ['QQ', 13.527, '2019-03'],
                ['QQ', 15.22, '2019-04'], ['联想乐商店', 10.22, '2019-03']]

    app_df = pd.DataFrame(data_app, columns=['busi_name', 'flow', 'month_id'])
    dataframe_phone_no = {"app": app_df}

    num_apps = appstore_num(dataframe_phone_no, {})

    print('input app dataframe for given phone number:\n ', app_df, '\n')
    print('number of apps:\n ', num_apps)

if __name__ == '__main__':
    test()
