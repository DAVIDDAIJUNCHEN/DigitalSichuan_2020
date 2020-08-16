import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['KaiTi'] # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题

def tt0():
    labels = ['G1', 'G2', 'G3', 'G4', 'G5']
    men_means = [20, 35, 30, 35, 27]
    women_means = [25, 32, 34, 20, 25]
    men_std = [2, 3, 4, 1, 2]
    women_std = [3, 5, 2, 3, 3]
    width = 0.35       # the width of the bars: can also be len(x) sequence
    fig, ax = plt.subplots()
    ax.bar(labels, men_means, width, yerr=men_std, label='Men')
    ax.bar(labels, women_means, width, yerr=women_std, bottom=men_means,
           label='Women')
    ax.set_ylabel('Scores')
    ax.set_title('Scores by group and gender')
    ax.legend()
    plt.show()

def app():
    # user_list= pd.read_csv('../../data/test_04/test_user_wLabel.csv').values
    user_list = pd.read_csv('../../data/train/train_user.csv').values
    id_lable_dict = {}
    total_fraud_num = 0
    total_normal_num = 0
    for v in user_list:
        id_lable_dict[v[0]] = v[-1]
        if v[-1] == 0:
            total_normal_num += 1
        else:
            total_fraud_num += 1

    # app_list = pd.read_csv('../../data/test_04/test_app.csv').values
    app_list = pd.read_csv('../../data/train/train_app.csv').values
    id_apps_dict = {}
    app_ids_dict = {}
    app_idCount_dict = {}
    for v in app_list:
        id = v[0]
        app = v[1]
        if type(app) != type(''):
            continue
        # if id not in id_apps_dict:
        #     id_apps_dict[id]=set()
        # id_apps_dict[id].add(app)
        if app not in app_ids_dict:
            app_ids_dict[app] = set()
        app_ids_dict[app].add(id)
    for app in app_ids_dict:
        app_idCount_dict[app] = len(app_ids_dict[app])

    app_idCount_list = sorted(app_idCount_dict.items(), key=lambda x: x[1], reverse=True)
    app_list = []
    app_rate_dict = {}
    for v in app_idCount_list:
        app_list.append(v[0])
    app_show = []
    fraud = []
    normal = []
    ii = 1
    for app in app_list:
        num_fraud = 0
        num_normal = 0
        for id in app_ids_dict[app]:
            if id_lable_dict[id] == 1:
                num_fraud += 1
            else:
                num_normal += 1
        if num_fraud + num_normal < 20:
            continue

        app_rate_dict[app] = num_fraud / (num_fraud + num_normal);

        #
        # fraud.append(num_fraud)
        # normal.append(num_normal)
        # app_show.append(app)
        # if len(fraud)==5:
        #     width = 0.35
        #     fig, ax = plt.subplots(figsize=(12, 4))
        #     ax.bar(app_show, normal, width, label='normal')
        #     ax.bar(app_show, fraud, width, bottom=normal, label='fraud')
        #     # ax.set_ylabel('Scores')
        #     # ax.set_title('Scores by group and gender')
        #     ax.legend()
        #     #plt.show()
        #     fig.savefig('bar_fig/' + str(ii)+ '.png')
        #     ii+=1
        #     print(app)
        #     print(num_fraud)
        #     print(num_normal)
        #     num_fraud = 0
        #     num_normal = 0
        #     app_show = []
        #     fraud = []
        #     normal = []
    app_rate_list = sorted(app_rate_dict.items(), key=lambda x: x[1], reverse=True)
    app = []
    rate = []
    count = []
    for app_rate in app_rate_list:
        app.append(app_rate[0])
        rate.append(app_rate[1])
        count.append(app_idCount_dict[app_rate[0]])
        # print(app,' ',rate,' ',count)
    data = pd.DataFrame({'app': app, 'rate': rate, 'count': count})
    data.to_csv('app比例名单.csv', encoding='utf_8_sig')

def address():
    print('address--------------------')
    user_list = pd.read_csv('../../data/train/train_user.csv').values
    id_lable_dict = {}
    city_ids_dict={}
    county_ids_dict={}

    for v in user_list:
        id_lable_dict[v[0]] = v[-1]
        id=v[0]
        city=v[1]
        if type(city)!=type(''):
            city='nan'
        county=v[2]
        if type(county)!=type(''):
            county='nan'
        lable=v[-1]
        if city not in city_ids_dict:
            city_ids_dict[city]=set()
        city_ids_dict[city].add(id)
        if county not in county_ids_dict:
            county_ids_dict[county]=set()
        county_ids_dict[county].add(id)
    city_count_dict={}
    county_count_dict={}
    for c in city_ids_dict:
        city_count_dict[c]=len(city_ids_dict[c])
    for c in county_ids_dict:
        county_count_dict[c]=len(county_ids_dict[c])

    city_count_list=sorted(city_count_dict.items(), key=lambda x: x[1], reverse=True)
    county_count_list = sorted(county_count_dict.items(), key=lambda x: x[1], reverse=True)
    city = []
    county=[]
    fraud = []
    normal = []
    ii = 1
    for v in city_count_list:
        ci=v[0]
        num_fraud = 0
        num_normal = 0
        ids=city_ids_dict[ci]
        for id in ids:
            if id_lable_dict[id]==1:
                num_fraud+=1
            else:
                num_normal+=1
        city.append(ci)
        fraud.append(num_fraud)
        normal.append(num_normal)

        if len(fraud)==5 or ci==city_count_list[-1][0]:
            width = 0.35
            fig, ax = plt.subplots(figsize=(12, 4))
            ax.bar(city, normal, width, label='normal')
            ax.bar(city, fraud, width, bottom=normal, label='fraud')
            ax.legend()
            fig.savefig('city_bar_fig/' + str(ii)+ '.png')
            ii+=1
            print(city)
            print(num_fraud)
            print(num_normal)
            num_fraud = 0
            num_normal = 0
            city = []
            fraud = []
            normal = []

    ii = 1
    for v in county_count_list:
        ci = v[0]
        num_fraud = 0
        num_normal = 0
        ids = county_ids_dict[ci]
        for id in ids:
            if id_lable_dict[id] == 1:
                num_fraud += 1
            else:
                num_normal += 1
        county.append(ci)
        fraud.append(num_fraud)
        normal.append(num_normal)

        if len(fraud) == 5 or ci == city_count_list[-1][0]:
            width = 0.35
            fig, ax = plt.subplots(figsize=(12, 4))
            ax.bar(county, normal, width, label='normal')
            ax.bar(county, fraud, width, bottom=normal, label='fraud')
            ax.legend()
            fig.savefig('county_bar_fig/' + str(ii) + '.png')
            ii += 1
            print(county)
            print(num_fraud)
            print(num_normal)
            num_fraud = 0
            num_normal = 0
            county = []
            fraud = []
            normal = []
    print(888)

def imei():
    print('imei-------------------')
    user_list = pd.read_csv('../../data/train/train_user.csv').values
    id_lable_dict = {}
    for v in user_list:
        id_lable_dict[v[0]] = v[-1]
    voc_list = pd.read_csv('../../data/train/train_voc.csv').values
    id_imeis_dict={}
    for v in voc_list:
        id=v[0]
        imei=v[-1]
        if id not in id_imeis_dict:
            id_imeis_dict[id]=set()
        id_imeis_dict[id].add(imei)

    imeicount_ids_dict={}
    for id in id_imeis_dict:
        c=len(id_imeis_dict[id])
        if c not in imeicount_ids_dict:
            imeicount_ids_dict[c]=set()
        imeicount_ids_dict[c].add(id)
    imeicount_idcount_dict={}
    for c in imeicount_ids_dict:
        imeicount_idcount_dict[c]=len(imeicount_ids_dict[c])
    imeicount_idcount_list = sorted(imeicount_idcount_dict.items(), key=lambda x: x[0], reverse=False)

    imei = []
    fraud = []
    normal = []
    ii = 1
    for v in imeicount_idcount_list:
        ci=v[0]
        num_fraud = 0
        num_normal = 0
        ids=imeicount_ids_dict[ci]
        for id in ids:
            if id_lable_dict[id]==1:
                num_fraud+=1
            else:
                num_normal+=1
        imei.append(str(ci))
        fraud.append(num_fraud)
        normal.append(num_normal)

        if len(fraud)==5 or ci==imeicount_idcount_list[-1][0]:
            width = 0.35
            fig, ax = plt.subplots(figsize=(12, 4))
            ax.bar(imei, normal, width, label='normal')
            ax.bar(imei, fraud, width, bottom=normal, label='fraud')
            ax.legend()
            fig.savefig('imei_bar_fig/' + str(ii)+ '.png')
            ii+=1
            print(imei)
            print(num_fraud)
            print(num_normal)
            num_fraud = 0
            num_normal = 0
            imei = []
            fraud = []
            normal = []

    print('888')

def appstore():
    print('appstore-----------------------------')
    stores=['AppStore','魅族应用中心','小米应用商店','联想乐商店','锤子应用商店','中兴应用商店','三星应用商店','VIVO应用商店','oppo应用商店','华为应用市场']
    stores_set=set(stores)
    user_list = pd.read_csv('../../data/train/train_user.csv').values
    id_lable_dict = {}
    for v in user_list:
        id_lable_dict[v[0]] = v[-1]

    app_list = pd.read_csv('../../data/train/train_app.csv').values
    id_apps_dict = {}
    app_ids_dict = {}

    for v in app_list:
        id = v[0]
        app = v[1]
        if app not in stores_set:
            continue
        if id not in id_apps_dict:
            id_apps_dict[id]=set()
        id_apps_dict[id].add(app)
        if app not in app_ids_dict:
            app_ids_dict[app] = set()
        app_ids_dict[app].add(id)

    app_idCount_dict = {}
    for app in app_ids_dict:
        app_idCount_dict[app] = len(app_ids_dict[app])

    appcount_ids_dict={}
    for id in id_apps_dict:
        c=len(id_apps_dict[id])
        if c not in appcount_ids_dict:
            appcount_ids_dict[c]=set()
        appcount_ids_dict[c].add(id)

    appcount_idcount_dict={}
    for c in appcount_ids_dict:
        appcount_idcount_dict[c]=len(appcount_ids_dict[c])
    appcount_idcount_list = sorted(appcount_idcount_dict.items(), key=lambda x: x[0], reverse=False)

    app = []
    fraud = []
    normal = []
    ii = 1
    for v in appcount_idcount_list:
        ci=v[0]
        num_fraud = 0
        num_normal = 0
        ids=appcount_ids_dict[ci]
        for id in ids:
            if id_lable_dict[id]==1:
                num_fraud+=1
            else:
                num_normal+=1
        app.append(str(ci))
        fraud.append(num_fraud)
        normal.append(num_normal)

        if len(fraud)==5 or ci==appcount_idcount_list[-1][0]:
            width = 0.35
            fig, ax = plt.subplots(figsize=(12, 4))
            ax.bar(app, normal, width, label='normal')
            ax.bar(app, fraud, width, bottom=normal, label='fraud')
            ax.legend()
            fig.savefig('appstore_bar_fig/' + str(ii)+ '.png')
            ii+=1
            print(app)
            print(num_fraud)
            print(num_normal)
            num_fraud = 0
            num_normal = 0
            app = []
            fraud = []
            normal = []


    print('8888')

def appflow():
    user_list = pd.read_csv('../../data/train/train_user.csv').values
    id_lable_dict = {}
    total_fraud_num = 0
    total_normal_num = 0
    for v in user_list:
        id_lable_dict[v[0]] = v[-1]

    app_list = pd.read_csv('../../data/train/train_app.csv').values

    app_fraudflows_dict={}
    app_normalflows_dict = {}
    app_ids_dict = {}
    app_idCount_dict = {}
    for v in app_list:
        id = v[0]
        app = v[1]
        flow=v[2]
        if type(flow)!=type(1.0):
            continue
        if type(app) != type(''):
            continue

        if app not in app_fraudflows_dict:
            app_fraudflows_dict[app] = []
        if app not in app_normalflows_dict:
            app_normalflows_dict[app] = []

        if id_lable_dict[id]==1:
            app_fraudflows_dict[app].append(flow)
        else:
            app_normalflows_dict[app].append(flow)

        if app not in app_ids_dict:
            app_ids_dict[app] = set()
        app_ids_dict[app].add(id)

    for app in app_ids_dict:
        app_idCount_dict[app] = len(app_ids_dict[app])


    app_idCount_list = sorted(app_idCount_dict.items(), key=lambda x: x[1], reverse=True)
    app_list = []
    app_rate_dict = {}
    for v in app_idCount_list:
        app_list.append(v[0])
    app_show = []
    fraud = []
    normal = []
    fraud_var = []
    normal_var = []
    ii = 1
    for app in app_list:
        num_fraud = 0
        num_normal = 0
        for id in app_ids_dict[app]:
            if id_lable_dict[id] == 1:
                num_fraud += 1
            else:
                num_normal += 1
        if num_fraud + num_normal < 20:
            continue
        app_show.append(app)
        normalflows=app_normalflows_dict[app]
        fraudflows=app_fraudflows_dict[app]
        normal.append(np.mean(normalflows))
        fraud.append(np.mean(fraudflows))
        normal_var.append(np.var(normalflows))
        fraud_var.append(np.var(fraudflows))
    data = pd.DataFrame({'app': app_show, 'normalflow_mean': normal, 'fraudflow_mean': fraud, 'normalflow_var': normal_var, 'fraudflow_var': fraud_var})
    data.to_csv('app流量.csv', encoding='utf_8_sig')



    print(777)

if __name__ == '__main__':


    appflow()
    print(9999)

    #test()
