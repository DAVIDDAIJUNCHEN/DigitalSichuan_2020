import pandas as pd
from collections import Counter

def ratio_sms_friends(dataframe_phone_no, arguments):
    """return number of friends in given months"""
    # convert to datetime format
    months = arguments['months']
    thres_friend = arguments['threshold_friend']
    months_regex = '|'.join(months)
    sms_dataframe = dataframe_phone_no['sms']
    sms_df_months = sms_dataframe[sms_dataframe['request_datetime'].str.contains(months_regex)]

    smsed_people = list(sms_df_months['opposite_no_m'])
    smsed_people_dict = dict(Counter(smsed_people))
    if len(smsed_people_dict) == 0:
        return arguments['represent_nan']

    sms_friend = 0
    for opposite_phone, times in smsed_people_dict.items():
        if times >= thres_friend:
            sms_friend += 1

    return sms_friend / len(smsed_people_dict)

def test():
    data_sms = [['f0ebee98809cb1a9', 1, '2019-12-25 21:26:40'],
                ['dedd4a48c3a8f', 1, '2020-01-02 20:14:33'],
                ['dedd4a48c3a8f', 1, '2020-01-02 20:14:33']]

    sms_df = pd.DataFrame(data_sms, columns=['opposite_no_m','calltype_id','request_datetime'])
    dataframe_phone_no = {'sms': sms_df}
    arguments = {"months": ['2019-12', '2020-01'], 'threshold_friend': 2}
    print(ratio_sms_friends(dataframe_phone_no, arguments))

if __name__ == '__main__':
    test()