#/usr/bin/env python3

import pandas as pd

def num_app(dataframe_phone_no, arguments):
    """return number of called people in given months"""
    # convert to datetime formatA
    app_dataframe = dataframe_phone_no['app']
    if len(app_dataframe) == 0:
        return arguments['represent_nan']

    num_apps = set(app_dataframe['busi_name'])
    return len(num_apps)

# debug part: To be deleted
def test():
    data_app = [['NaN', 8.33, '2019-11'], ['QQ', 13.527, '2019-03'],
                ['QQ', 15.22, '2019-04'], ['旺信', 10.22, '2019-03']]

    app_df = pd.DataFrame(data_app, columns=['busi_name', 'flow', 'month_id'])
    dataframe_phone_no = {"app": app_df}

    num_apps = num_app(dataframe_phone_no, {})

    print('input app dataframe for given phone number:\n ', app_df, '\n')
    print('number of apps:\n ', num_apps)

if __name__ == '__main__':
    test()
