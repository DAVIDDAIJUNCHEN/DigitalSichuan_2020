import pandas as pd


def payapp_num(dataframe_phone_no, arguments):
    """return the number of app about pay"""

    app_dataframe = dataframe_phone_no['app']
    if len(app_dataframe) == 0:
        return arguments['represent_nan']

    payapp = {'支付宝', '中国建设银行', '和包', '招商银行', '财付通', '农行掌上银行', '翼支付', '银联网上银行', 'ShouQianBa',
                  '360JieTiao', 'WeiXin_Pay_Action', '1Qianbao', '喔噻', 'Ppdai', 'Scrcu', '交通银行', '民生银行',
                 '百度钱包', '哆啦宝', 'ICBCRongELian', '凤凰金融', '京东金融', 'WangShangYinHang', '中国银行手机银行',
                 '中国工商银行', '农行掌上银行', '兴业银行', '平安口袋银行', '网银在线', '易宝支付', '联动优势', 'Qingsongchou',
                 '51信用卡', '融360', '光大银行', '财付通', '中国银联', 'JingDongQianBao', 'Paypal', '2DFire', '挖财记账',
                 'QuanMinShengHuo', '华夏银行', '银联钱包', 'CITIC_DongKaKongJian', 'XiaoYingKaDai'}

    num_payapp = [1 for each in app_dataframe['busi_name'] if each in payapp]

    return len(num_payapp)


def suspect_app_num(dataframe_phone_no, arguments):
    """return the number of suspected app"""

    app_dataframe = dataframe_phone_no['app']
    if len(app_dataframe) == 0:
        return arguments['represent_nan']

    suspect_app = {'信析宝', '友盟+', 'MySpace', '领英', '七牛', 'JPush', 'AdMaster精硕科技', '个推', '聚胜万合', 'ShareSDK',
                    'ShareSDK', '兔展', 'MmStat', '武汉安天信息技术有限责任公司', 'Leancloud', '53Kf', '华扬联众官方网站',
                      '玩咖欢聚', '国双', 'Shuzilm', 'Teddymobile', '艾客信息咨询', 'appjiagu网', 'Growingio', '非凡时代传媒科技网',
                      'CNZZ统计', 'DoubleClick广告', 'NetBios', 'NTP', 'HTTP2', 'DNS', 'STUN', 'Crashlytics网络协议',
                    'BaiDuTongJi', 'WangYiQiYu', 'Openinstall', 'Tanx', 'Izatcloud', 'SSL', 'Jabber', '有赞网', '麦客',
                      'Qchannel', 'SIGMOB', 'RTP', 'Brightcove', 'RTMFP', 'eMule', 'Other VoIP', 'Cloudflare', '对吧',
                      '易企秀', 'Akamaihd', 'Omtrdc', 'HuaWei PushMessage', 'TiqCDN', '35HuLian', 'Imtmp', 'Mookie1',
                      'Swrve', '易观集团', 'Bootcss', 'IpApi', 'I单击', 'Qnssl', '上海宏路数据技术股份有限公司', '极验验证码',
                      '加和科技', 'MIS系统', '悠易互通广告', 'Zoosnet', '兑吧', 'Growingio', 'Kochava', 'Google Analytics',
                      'TalkingData', 'Crashlytics网络协议', 'ScorecardResearch', 'AndroidConCheck', 'Demdex', 'Sephora_KSA',
                     '融云即时通讯云', 'ICY', 'Behavior', 'Easemob', '触宝', '微盟', '彩信', '网宿科技', '我要啦', 'Ipinfo',
                      'AD调查', 'APICloud 柚子科技有限公司', '电话邦', 'Ifconfig', '灵集科技', '3Gmimo', 'IP地址查询网',
                      '新数网络', '乐变', '千帆', '上海宏路数据技术股份有限公司', '深圳维京人网络科技有限公司', '精硕科技', '51YES流量统计',
                      'APP林子', '查询580', 'Find My Friends', 'SPDY', 'MS Common', 'Ksmobile', 'TengYunTianXia', 'RTCP',
                      'etoote', 'SIP Control', 'ServingSys', 'Digicert证书校验网站', 'GlobalSign', 'MIS系统', 'ChinaGovSites',
                      'Plcdn', 'Kakao Talk', '品友互动', '璧合科技', 'Lomark', 'Adsymptotic', '吆喝科技官网', 'GoogleAdsense',
                      '钞针系统', 'Demdex', 'Ptvyun', 'Tealiumiq', 'Holla', 'Usertrust', 'Maxjia', 'Zoosnet', 'Lenzmx',
                      'Siftscience', 'IOS PushMessage', '钞针系统', 'XYCDN_Other', 'FengKongCloud', 'NeiXin', 'FXLTSBL',
                      'TongDun', 'TianYiCloudService', 'RTMP', '720Static', 'VERYYS', '77CDN', '720Yun', ',appjiagu网',
                      'InMobi广告', 'Appsflyer', 'Exelator', 'Taboola', 'Crwdcntrl', 'Pimg'}

    num_suspect_app = [1 for each in app_dataframe['busi_name'] if each in suspect_app]

    return len(num_suspect_app)