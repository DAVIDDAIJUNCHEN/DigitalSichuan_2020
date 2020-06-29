#/usr/bin/env python3

import pandas as pd

def num_app(dataframe_phone_no, arguments):
    """return number of called people in given months"""
    # convert to datetime formatA
    app_dataframe = dataframe_phone_no['app']
    num_apps = set(app_dataframe['busi_name'])

    return len(num_apps)


def video_audio_flow(dataframe_phone_no,arguments):
    """return number of video_audio_flow in given months"""
    # convert to datetime format
    months = arguments['months']
    months_regex = '|'.join(months)
    app_dataframe = dataframe_phone_no['app']
    # tt=app_dataframe['month_id'].str
    # print(app_dataframe['month_id'].str)
    # app_df_months = app_dataframe[app_dataframe['month_id'].str.contains(months_regex)]
    try:
        app_df_months = app_dataframe[app_dataframe['month_id'].str.contains(months_regex)]
    except:
        #tt=app_dataframe['month_id']
        #aa=app_dataframe['month_id'].str.contains(months_regex)
        return -1
    flow=0

    video_app_set=set(['哔哩哔哩动画','腾讯视频','优酷','爱奇艺视频','芒果TV','搜狐视频','土豆视频','咪咕视频','酷6视频','央视影音','YouTube视频','皮皮影视'])
    audio_app_set=set(['唱吧','全民K歌','QQ音乐','酷我音乐','虾米音乐','酷狗音乐','百度音乐','凤凰电台','蜻蜓FM','网易云音乐'])
    short_video_app_set=set(['快手','抖音','火山小视频','微视','斗鱼直播','虎牙直播','UC影音']);
    video_audio_app_set = video_app_set | audio_app_set | short_video_app_set;

    for index, row in app_df_months.iterrows():
        #print(row)
        if row['busi_name'] in video_audio_app_set:
            flow+=row['flow']
    return flow



def social_flow(dataframe_phone_no,arguments):
    """return number of video_audio_flow in given months"""
    # convert to datetime format
    months = arguments['months']
    months_regex = '|'.join(months)
    app_dataframe = dataframe_phone_no['app']
    try:
        app_df_months = app_dataframe[app_dataframe['month_id'].str.contains(months_regex)]
    except:
        return -1
    flow=0

    social_app_set = set(['QQ','微信','旺信','陌陌','钉钉','探探']);

    for index, row in app_df_months.iterrows():
        #print(row)
        if row['busi_name'] in social_app_set:
            flow+=row['flow']
    return flow

def tool_flow(dataframe_phone_no,arguments):
    """return number of video_audio_flow in given months"""
    # convert to datetime format
    months = arguments['months']
    months_regex = '|'.join(months)
    app_dataframe = dataframe_phone_no['app']
    try:
        app_df_months = app_dataframe[app_dataframe['month_id'].str.contains(months_regex)]
    except:
        return -1
    flow=0

    tool_app_set = set(['高德导航','苹果地图','腾讯地图','百度地图','360安全卫士','迅雷','支付宝',
                        '腾讯云','阿里云','华为云','滴滴出行','美团','百度网盘','微云','华为网盘',
                        '金山云','有道词典']);

    for index, row in app_df_months.iterrows():
        #print(row)
        if row['busi_name'] in tool_app_set:
            flow+=row['flow']
    return flow

def surf_flow(dataframe_phone_no,arguments):
    """return number of video_audio_flow in given months"""
    # convert to datetime format
    months = arguments['months']
    months_regex = '|'.join(months)
    app_dataframe = dataframe_phone_no['app']
    try:
        app_df_months = app_dataframe[app_dataframe['month_id'].str.contains(months_regex)]
    except:
        return -1
    flow=0

    surf_app_set = set(['知乎','微博','百度贴吧','手机百度','腾讯网','网易网','百度搜索','腾讯新闻',
                        '搜狗搜索','今日头条','百度新闻','QQ浏览器','网页浏览','UC浏览器','神马搜索','新浪网',
                        '新浪微博','百度百科','人民网','中华网']);

    for index, row in app_df_months.iterrows():
        #print(row)
        if row['busi_name'] in surf_app_set:
            flow+=row['flow']
    return flow


def total_flow(dataframe_phone_no,arguments):
    """return number of video_audio_flow in given months"""
    # convert to datetime format
    months = arguments['months']
    months_regex = '|'.join(months)
    app_dataframe = dataframe_phone_no['app']
    try:
        app_df_months = app_dataframe[app_dataframe['month_id'].str.contains(months_regex)]
    except:
        return -1
    flow=0

    for index, row in app_df_months.iterrows():

        flow+=row['flow']
    return flow

# debug part: To be deleted
def test():
    data_app = [['NaN', 8.33, '2019-11'], ['QQ', 13.527, '2019-03'],
                ['QQ', 15.22, '2019-04'], ['旺信', 10.22, '2019-03'],
                ['腾讯视频', 40, '2019-12'], ['优酷', 90, '2019-12']]

    app_df = pd.DataFrame(data_app, columns=['busi_name', 'flow', 'month_id'])
    dataframe_phone_no = {"app": app_df}
    arguments = {"months": ['2019-12']}
    flow = video_audio_flow(dataframe_phone_no, arguments);
    print(flow)
    num_apps = num_app(dataframe_phone_no,{})

    print('input app dataframe for given phone number:\n ', app_df, '\n')
    print('number of apps:\n ', num_apps)

if __name__ == '__main__':
    test()
