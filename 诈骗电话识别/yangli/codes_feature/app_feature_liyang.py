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

    suspect_app = {'HuaWei PushMessage', '学习啦', '萤石', '阿里公共流量', '屈臣氏购物网', '百词斩', 'ip查询', 'BeiDian', 'MiniWorld', '语文迷', '花瓣网', '豆瓣阅读'
'看看新闻网', '磨基移动广告', 'Dingyueads', '新浪云存储', '微乐游戏', 'Shobserver', '作业帮', '糖果网站', '爪机书屋', 'Thecover', '家长帮', '糖豆广场舞'
'晋江小说阅读', '腾讯公共流量', 'PingAnHaoCheZhu', '车主无忧', 'Nibaguai', '人民日报', '途虎', '网易16163游戏网', '别踩白块儿', 'A0Bi', '中国搜索', '联想手机商城'
'快看漫画', '丁香通', '考试吧学习通', 'Cyol', '三国杀', '优她网', '金蝶医疗', '查查吧', 'Taopiaopiao', '太平洋亲子网', '183Me', '广州聘大信息科技有限责任公司官网'
'e互助', 'QiMaoReader', 'HuaSheng100', '奥迪官网', '凯立德导航', '5068儿童网', '球迷宝', 'Radmin远程桌面', 'IPIP', '共享盘', '猿辅导', 'DuoDian'
'360Tpcdn', '小天才', 'ChaoXingXueXiTong', '大福星', 'Cpta', '猎文网', '典欧灯饰', '粉粉日记', 'YouLiShiPin', '51AiWan', '欧朋Opera手机浏览器官网', '超级教练'
'学而思网校', '唯一图库', '惠锁屏', '掌游天下', 'Mygolbs', '7Sef', 'YourFreedom', '兔展', '趣点点赚钱', 'HuanXiDouDiZhu', 'QuDuoPai', '一下科技'
'CSDN软件开发网', '财联社', '必要-', 'Smarthome', '互动作业', 'MaMaWangYunYu', '齐鲁壹点', '彩视', '商助官网', '新京报', '美洽客服', 'CheLunJiaKaoTong'
'游娱社区', '美食杰', '北京创变网络科技有限公司', '中文万维', 'Agoda', '懒人模板', 'Swrve', 'WhosHere', '各种广告', '魔力相册', 'MiDuReader', '趣头条'
'Onegreen', '上海费睿网络官网', 'TianTianLeXue', 'Tapad', '艾媒网', '直播吧', '乐居', 'Scedu', '地铁跑酷', '新东方在线官网', '北京乐影网', '广州市鸿亿防伪产品有限公司官网'
'MengHuanHuaYuan', '投票吧', 'Book118', 'GeDeng', '网上泰康人寿保险', 'JJ斗地主', '风灵创景网', '车轮查违章', '顶点小说', '育碧', '格力电器官网以及App流量', 'WeiLiNovel'
'Dreamstime', '7Net', '9553下载', '新商盟依', 'KaKaZY', '卡妞微秀', '育儿网', 'XueAnQuan', '步步高下载中心', '51Talk', 'APUS'
'乐教乐学', '18Guanjia', 'Snmi', '猿题库', '棉花糖小说网', 'TaoXinWen', '豪客来官网', '魅图网络科技', 'Hi现场', 'Sqreader', 'HuaDongChuanMei', 'KuaiDuiZuoYe'
'WuLiZiXun', 'QingQu', '至诚财经网', '斐波那契', '大象就医', '正保远程教育', '樊登读书会官网', '当当云阅读', '乐阅读', '智慧树网', 'YouPinWei', '中国知网'
'EClicks', '手机电视MBBMS', '妈妈帮', '西瓜视频', '孩子王', '中华会计网校', '风灵创景科技有限公司官网', '凤凰网', '178游戏网', '3DMGAME', '升学e网通', 'JiaZhangTong'
'Laqddc', 'iFood', 'CNN', '人人', '233XiaoYouXi', '日历官网', 'Aiclicash', 'Vcgame', '获取奖学金公益网', '万年历', 'XiaoMiYunDong', '酷酷游戏'
'Ikea', '智慧树', 'Gopher网络协议', '汤姆猫跑酷', 'JiLiGuaLa', '小伙伴', 'PeanutDiary', 'VpnMaster', 'Szzbmy', '一起作业学生端', '小年糕', 'Cd120'
'WeiLiKanKan', 'Shenghuoquan', '我的安吉拉', '亿启酷动', '薄荷科技', '1010Jiajiao', 'YouJianKang', '网易公开课', '北京文青博业科技', 'NBA', 'ZhangShangDianLi',
'美乐乐家具网', 'Tangdou_HTTP_Video', 'CN人才网', '工程师爸爸', '东方输入法', '西安文明网', '作业盒子', '红薯中文网', '农产品移动电商平台', '视源股份', 'Stickyadstv',
'Applifier', 'Fring', 'HuiTouTiao', 'TalkingTomGoldRun', '新东方网', 'TianTianDouDiZhu', '大家找算命网', 'ZhongYangTianQiYuBao', '运满满', '养生之道', 'Suishenyun',
'Sgcc', '百度公共流量', '学霸君', '可可简笔画', '5Read', '游道易', '猫酷', 'Scgh114', 'XiaoHeiBan', '咕咚运动', '百度影音', 'ErGeDianDian', 'WeiDianGo', '61info',
'AnQuanShouHu2', '乐堂动漫', '故事大全', 'WebToon', '酷划', '书链', 'YiLan', '初中作文网', '笔趣阁小说网', 'BoBoShiPin', 'Cmge',
'VIPKID', 'APUS Launcher', '凯叔讲故事', 'UIAndroid', 'HiLaiDian_Browsing', 'Appcloudbox', 'RightPaddle', '张力卓个人网站'}


    num_suspect_app = [1 for each in app_dataframe['busi_name'] if each in suspect_app]

    return len(num_suspect_app)