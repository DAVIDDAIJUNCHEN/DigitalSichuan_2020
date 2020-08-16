import pandas as pd
import numpy as np
import math
from scipy.stats import norm


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


def normal90_app_num(dataframe_phone_no, arguments):
    """return the number of suspected app"""

    app_dataframe = dataframe_phone_no['app']

    if len(app_dataframe) == 0:
        return arguments['represent_nan']

    suspect_app = {"Omge","Vipkid","凯叔讲故事","UIAndroid","酷酷游戏","APUSLauncher","百度影音","TalkingTomGoldRun","178游戏网",
                   "ErGeDianDian","TianTianDouDiZhu","农产品移动电商平台","KuaiDuiZuoYe","了堂动漫","故事大全","超级教练","Gopher网络协议",
                   "书链","DuoDian","YiLan","info","PeanutDiary","VpnMaster","笔趣阁小说网","初中作文网","Cd120","新东方在线官网","妈妈帮",
                   "百度公共流量","西瓜视频","WeiLiKanKan","新东方网","正保远程教育","RightPaddle","Appcloudbox","酷划","0Ikea","红薯中文网",
                   "一起作业学生端","新京报","51talk","WuLiZiXun","糖豆广场舞","小年糕","WebToon","北京乐影网","卡妞微秀","腾讯公共流量",
                   "养生之道","AnQuanShouHu2","CNN"}

    num_suspect_app = [1 for each in app_dataframe['busi_name'] if each in suspect_app]

    return len(num_suspect_app)

def normal90_app_contain(dataframe_phone_no, arguments):
    """return the number of suspected app"""

    app_dataframe = dataframe_phone_no['app']

    if len(app_dataframe) == 0:
        return arguments['represent_nan']

    suspect_app = {"Omge","Vipkid","凯叔讲故事","UIAndroid","酷酷游戏","APUSLauncher","百度影音","TalkingTomGoldRun","178游戏网",
                   "ErGeDianDian","TianTianDouDiZhu","农产品移动电商平台","KuaiDuiZuoYe","了堂动漫","故事大全","超级教练","Gopher网络协议",
                   "书链","DuoDian","YiLan","info","PeanutDiary","VpnMaster","笔趣阁小说网","初中作文网","Cd120","新东方在线官网","妈妈帮",
                   "百度公共流量","西瓜视频","WeiLiKanKan","新东方网","正保远程教育","RightPaddle","Appcloudbox","酷划","0Ikea","红薯中文网",
                   "一起作业学生端","新京报","51talk","WuLiZiXun","糖豆广场舞","小年糕","WebToon","北京乐影网","卡妞微秀","腾讯公共流量",
                   "养生之道","AnQuanShouHu2","CNN"}

    num_suspect_app = [1 for each in app_dataframe['busi_name'] if each in suspect_app]

    if len(num_suspect_app) == 0:
        return 0
    else:
        return 1



def normal100_app_num(dataframe_phone_no, arguments):
    """return the number of suspected app"""

    app_dataframe = dataframe_phone_no['app']

    if len(app_dataframe) == 0:
        return arguments['represent_nan']

    suspect_app = {"语文迷","张力卓个人网站","ErGeDianDian","61info","WeiDianGo","花瓣网","WeiLiNovel","HuaDongChuanMei",
                   "家长帮","乐视云盘","趣配音","EumAppdynamics","Tan8","四川大学华西第二医院","中公教育","东奥会计在线",
                   "SiteScout","奥数网","古诗文网","查字典","听力课堂","晋江原创网","浙江阿里巴巴云计算有限公司","中大网视",
                   "Gywb","法语助手","医生站","银联商务有限公司","汤圆创作","Fotoable","口语100","Dtscout","北京触控科技有限公司",
                   "DigitalOcean","易企微官网","微信公众平台","ChaoJiKeChengBiao","学堂在线","八百方网上药店","微车违章查询",
                   "LaoYouZhiBo","A9VG电玩部落","最游戏","Skout+","Socdm","Xg4ken","上海新易传媒广告有限公司csbew系统",
                   "爱套网","华讯财经","海报时尚网","911查询","Tinypic","Jovetech","Tisgame","Postitial","Autodesk"}

    num_suspect_app = [1 for each in app_dataframe['busi_name'] if each in suspect_app]

    return len(num_suspect_app)

def normal100_app_contain(dataframe_phone_no, arguments):
    """return the number of suspected app"""

    app_dataframe = dataframe_phone_no['app']

    if len(app_dataframe) == 0:
        return arguments['represent_nan']

    suspect_app = {"语文迷","张力卓个人网站","ErGeDianDian","61info","WeiDianGo","花瓣网","WeiLiNovel","HuaDongChuanMei",
                   "家长帮","乐视云盘","趣配音","EumAppdynamics","Tan8","四川大学华西第二医院","中公教育","东奥会计在线",
                   "SiteScout","奥数网","古诗文网","查字典","听力课堂","晋江原创网","浙江阿里巴巴云计算有限公司","中大网视",
                   "Gywb","法语助手","医生站","银联商务有限公司","汤圆创作","Fotoable","口语100","Dtscout","北京触控科技有限公司",
                   "DigitalOcean","易企微官网","微信公众平台","ChaoJiKeChengBiao","学堂在线","八百方网上药店","微车违章查询",
                   "LaoYouZhiBo","A9VG电玩部落","最游戏","Skout+","Socdm","Xg4ken","上海新易传媒广告有限公司csbew系统",
                   "爱套网","华讯财经","海报时尚网","911查询","Tinypic","Jovetech","Tisgame","Postitial","Autodesk"}

    num_suspect_app = [1 for each in app_dataframe['busi_name'] if each in suspect_app]

    if len(num_suspect_app) == 0:
        return 0
    else:
        return 1


def fraud90_app_num(dataframe_phone_no, arguments):
    """return the number of suspected app"""

    app_dataframe = dataframe_phone_no['app']

    if len(app_dataframe) == 0:
        return arguments['represent_nan']

    suspect_app = {"XianJinBashi80","Gcontent","借贷宝"}

    num_suspect_app = [1 for each in app_dataframe['busi_name'] if each in suspect_app]

    return len(num_suspect_app)


def fraud90_app_contain(dataframe_phone_no, arguments):
    """return the number of suspected app"""

    app_dataframe = dataframe_phone_no['app']

    if len(app_dataframe) == 0:
        return arguments['represent_nan']

    suspect_app = {"XianJinBashi80", "Gcontent", "借贷宝"}

    num_suspect_app = [1 for each in app_dataframe['busi_name'] if each in suspect_app]

    if len(num_suspect_app) == 0:
        return 0
    else:
        return 1


def fraud100_app_num(dataframe_phone_no, arguments):
    """return the number of suspected app"""

    app_dataframe = dataframe_phone_no['app']

    if len(app_dataframe) == 0:
        return arguments['represent_nan']

    suspect_app = {"海康威视","微托帮网络","VyprVPN","51卡农、Jwpsrv","深圳航空","ChinaPress","捞月狗","缘来婚恋交友",
                   "ZiDanDuanXin","Letgo","Osta","杭州狂想网络科技有限公司官网","Mycolordiary","X224","Elex",
                   "Casinomodule","DirectConnect","Mycom","Ctmail","XiaoBaiLaiHua","Ghs","Travelyh",
                   "美国航空","基金批发网站","环球黑卡","DURecorder","Xda_developers","福步外贸网","天天农场官网"}

    num_suspect_app = [1 for each in app_dataframe['busi_name'] if each in suspect_app]

    return len(num_suspect_app)


def fraud100_app_contain(dataframe_phone_no, arguments):
    """return the number of suspected app"""

    app_dataframe = dataframe_phone_no['app']

    if len(app_dataframe) == 0:
        return arguments['represent_nan']

    suspect_app = {"海康威视","微托帮网络","VyprVPN","51卡农、Jwpsrv","深圳航空","ChinaPress","捞月狗","缘来婚恋交友",
                   "ZiDanDuanXin","Letgo","Osta","杭州狂想网络科技有限公司官网","Mycolordiary","X224","Elex",
                   "Casinomodule","DirectConnect","Mycom","Ctmail","XiaoBaiLaiHua","Ghs","Travelyh",
                   "美国航空","基金批发网站","环球黑卡","DURecorder","Xda_developers","福步外贸网","天天农场官网"}

    num_suspect_app = [1 for each in app_dataframe['busi_name'] if each in suspect_app]

    if len(num_suspect_app) == 0:
        return 0
    else:
        return 1


# normal app
normal90_app = ["管理后台登录页面","双开助手官","Uuu9","巨人征途","草花手游中心","每日瑜伽官网","FTP","随手记","Roblox","东亚银行","傲世堂",
"土巴兔装修网","ZhangShangDaoJuCheng","游民星空","HuoLaLa","Study","114啦网址导航","Coolapk","QingMang",
"开迅视频","战网","Speedtest","火猫TV","金太阳","抱抱","Weico微博客户端","腕表之家","上海贪玩信息技术有限公司",
"37游戏","手机加速","澎湃新闻","ABC","全民飞机大战","126邮箱","NowYingShi","Telegram_Messenger","77CDN",
"中通快递官网","活动行","QQ桌面管家","英雄互娱","Adobe","7k7k小游戏","IJunHai","保利威视","Ford","QQWiFiManager",
"播视网","360奇酷商城","OWA","四川航空","寺库","QQ炫舞","花椒直播","健客网","HaiNanLiSheng_Streaming","词典翻译金山词霸",
"Snapchat","拉勾网","安卓壁纸","今日军事网","游戏狗","沪江开心词场","SnapVPN","AiKuCun","Qbb6","糗事百科","HuaDongChuanMei"
"喜马拉雅听","飞卢中文网","天天爱消除","海信传媒网络技术有限公司官网","英伟达","蜻蜓FM","东方博雅","动漫之家","搜狗手机助手",
"龙珠直播","360News","可可英语","折800","沪江CC课堂","Popcap","凯励程官网","熊猫看书","Minecraft","凤凰山下",
"漫画岛","什么值得买","360云盘","100Bt","美国艺电","易班网","爪机书屋","晋江小说阅读","Nibaguai","惠锁屏","财联社",
"Onegreen","风灵创景网","KaKaZY","Sqreader","樊登读书会官网","中华会计网校","风灵创景科技有限公司官网","升学e网通",
"糖豆广场舞","233XiaoYouXi","日历官网","XiaoMiYunDong","JiLiGuaLa","PeanutDiary","一起作业学生端","CheLunJiaKaoTong",
"WeiLiKanKan","Tangdou_HTTP_Video","Fring","HuiTouTiao","ZhongYangTianQiYuBao","运满满","5Read","XiaoHeiBan",
"北京乐影网","WebToon","书链","VIPKID","ErGeDianDian","WeiDianGo","61info","花瓣网","家长帮","格力电器官网以及App流量"]

# fraud app
fraud90_app = ["Qpgame","Ipinfo","小象优品","XiaYiDao2","Icanhazip","腾讯房产","Bigo","Showself","六间房",
"中国移动无线城市","中彩网","欢聚云官网","Jabber","惠普公司","观察者","香哈菜谱","Hockeyapp","ShiGuangXiangCe",
"N300","AliBaBaCaiGou","西祠胡同社区","好豆菜谱","Oovoo","DJ总站","蘑菇街","Playrix","QiE_FM",
"Juicyads","云系统","BaiShanYun","Happyelements","掌游天下","新京报","我的安吉拉","亿启酷动"]


def fraud90_flow(dataframe_phone_no, arguments):
    """return total flow of apps that fraud flow >90%"""
    months = arguments['months']

    months_regex = '|'.join(months)
    app_dataframe = dataframe_phone_no['app']
    flow = 0

    try:
        app_df_months = app_dataframe.copy()# app_dataframe[app_dataframe['month_id'].str.contains(months_regex)]
        app = set(app_df_months['busi_name'])
        app_used = app & set(fraud90_app)

        if len(app_used) > 0:
            for app in app_used:
                flow += float(app_df_months[app_df_months['busi_name'] == app]['flow'].sum())

        return flow
    except:
        return arguments['represent_nan']


def fraud90_flow_normalization(dataframe_phone_no, arguments):
    """return total flow of apps that fraud flow >90%"""
    months = arguments['months']

    months_regex = '|'.join(months)
    app_dataframe = dataframe_phone_no['app']

    flow_csv = pd.read_csv('../../data/app_flow.csv')
    ratios = []
    try:
        app_df_months = app_dataframe.copy() # app_dataframe[app_dataframe['month_id'].str.contains(months_regex)]
        app = set(app_df_months['busi_name'])
        app_used = app & set(fraud90_app)

        if len(app_used) > 0:
            for app in app_used:
                app_flow_csv = flow_csv[flow_csv['app']==app]
                flow = float(app_df_months[app_df_months['busi_name']==app]['flow'].sum())
                normal_bias = (flow - float(app_flow_csv['normalflow_mean'])) / math.sqrt(float(app_flow_csv['normalflow_var'])+0.0001)
                fraud_bias = (flow - float(app_flow_csv['fraudflow_mean'])) / math.sqrt(float(app_flow_csv['fraudflow_var'])+0.0001)
                normal_prob = 1 - abs(norm.cdf(normal_bias) - norm.cdf(-normal_bias))
                fraud_prob = 1 - abs(norm.cdf(fraud_bias) - norm.cdf(-fraud_bias))
                if (normal_prob==0) and (fraud_prob==0):
                    continue
                else:
                    ratios.append(fraud_prob / (fraud_prob + normal_prob))
            if not math.isnan(np.max(ratios)):
                return np.max(ratios)
            else:
                return arguments['represent_nan']
        else:
            return arguments['represent_nan']
    except:
        return arguments['represent_nan']


def normal90_flow(dataframe_phone_no, arguments):
    """return total flow of apps that normal flow >90%"""
    months = arguments['months']

    months_regex = '|'.join(months)
    app_dataframe = dataframe_phone_no['app']
    flow = 0

    try:
        app_df_months = app_dataframe.copy() # app_dataframe[app_dataframe['month_id'].str.contains(months_regex)]
        app = set(app_df_months['busi_name'])
        app_used = app & set(normal90_app)

        if len(app_used) > 0:
            for app in app_used:
                flow += float(app_df_months[app_df_months['busi_name']==app]['flow'].sum())

        return flow
    except:
        return arguments['represent_nan']

def normal90_flow_normalization(dataframe_phone_no, arguments):
    """return total flow of apps that fraud flow >90%"""
    months = arguments['months']

    months_regex = '|'.join(months)
    app_dataframe = dataframe_phone_no['app']

    flow_csv = pd.read_csv('../../data/app_flow.csv')
    ratios = []
    try:
        app_df_months = app_dataframe.copy() #app_dataframe[app_dataframe['month_id'].str.contains(months_regex)]
        app = set(app_df_months['busi_name'])
        app_used = app & set(normal90_app)

        if len(app_used) > 0:
            for app in app_used:
                app_flow_csv = flow_csv[flow_csv['app']==app]
                flow = float(app_df_months[app_df_months['busi_name']==app]['flow'].sum())
                normal_bias = (flow - float(app_flow_csv['normalflow_mean'])) / (math.sqrt(float(app_flow_csv['normalflow_var']))+0.0001)
                fraud_bias = (flow - float(app_flow_csv['fraudflow_mean'])) / (math.sqrt(float(app_flow_csv['fraudflow_var']))+0.0001)
                normal_prob = 1 - abs(norm.cdf(normal_bias) - norm.cdf(-normal_bias))
                fraud_prob = 1 - abs(norm.cdf(fraud_bias) - norm.cdf(-fraud_bias))
                if (normal_prob==0) and (fraud_prob==0):
                    continue
                else:
                    ratios.append(normal_prob / (fraud_prob + normal_prob))
            if not math.isnan(np.max(ratios)):
                return np.max(ratios)
            else:
                return arguments['represent_nan']
        else:
            return arguments['represent_nan']
    except:
        return arguments['represent_nan']


# debug part: To be deleted
def test():
    data_app = [['什么值得买', 8.33, '2019-03'], ["书链", 13.527, '2019-03'],
                ["飞卢中文网", 15.22, '2019-03'], ["Qpgame", 10.22, '2019-03']]

    app_df = pd.DataFrame(data_app, columns=['busi_name', 'flow', 'month_id'])
    dataframe_phone_no = {"app": app_df}

    num_apps = fraud90_flow_normalization(dataframe_phone_no, {'months':'2019-03', 'represent_nan':-1})

    print('input app dataframe for given phone number:\n ', app_df, '\n')
    print('number of apps:\n ', num_apps)


if __name__ == '__main__':
    test()