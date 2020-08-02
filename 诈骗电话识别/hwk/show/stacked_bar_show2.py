import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['KaiTi'] # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题

# def test():
#     labels = ['G1', 'G2', 'G3', 'G4', 'G5']
#     men_means = [20, 35, 30, 35, 27]
#     women_means = [25, 32, 34, 20, 25]
#     men_std = [2, 3, 4, 1, 2]
#     women_std = [3, 5, 2, 3, 3]
#     width = 0.35       # the width of the bars: can also be len(x) sequence
#     fig, ax = plt.subplots()
#     ax.bar(labels, men_means, width, yerr=men_std, label='Men')
#     ax.bar(labels, women_means, width, yerr=women_std, bottom=men_means,
#            label='Women')
#     ax.set_ylabel('Scores')
#     ax.set_title('Scores by group and gender')
#     ax.legend()
#     plt.show()

if __name__ == '__main__':
    #user_list= pd.read_csv('../../data/test_04/test_user_wLabel.csv').values
    user_list = pd.read_csv('../../data/train/train_user.csv').values
    id_lable_dict={}
    total_fraud_num=0
    total_normal_num=0
    for v in user_list:
        id_lable_dict[v[0]]=v[-1]
        if v[-1]==0:
            total_normal_num+=1
        else:
            total_fraud_num+=1

    #app_list = pd.read_csv('../../data/test_04/test_app.csv').values
    app_list = pd.read_csv('../../data/train/train_app.csv').values
    id_apps_dict={}
    app_ids_dict={}
    app_idCount_dict={}
    app_fraudflow_dict={}
    app_normalflow_dict={}
    for v in app_list:
        id=v[0]
        app=v[1]
        if type(app)!=type(''):
            continue
        if v[2]=='':
            flow=0
        else:
            flow=float(v[2])
        if id_lable_dict[id]==1:
            if app not in app_fraudflow_dict:
                app_fraudflow_dict[app]=0
            app_fraudflow_dict[app]+=flow
        else:
            if app not in app_normalflow_dict:
                app_normalflow_dict[app]=0
            app_normalflow_dict[app]+=flow

        if id not in id_apps_dict:
            id_apps_dict[id]=set()
        id_apps_dict[id].add(app)
        if app not in app_ids_dict:
            app_ids_dict[app]=set()
        app_ids_dict[app].add(id)

    for app in app_ids_dict:
        app_idCount_dict[app]=len(app_ids_dict[app])

    app_idCount_list=sorted(app_idCount_dict.items(), key=lambda x: x[1], reverse=True)
    app_list=[]
    app_rate_dict={}
    for v in app_idCount_list:
        app_list.append(v[0])
    app_show=[]
    fraud=[]
    normal=[]
    ii=1
    for app in app_list:
        num_fraud=0
        num_normal=0
        for id in app_ids_dict[app]:
            if id_lable_dict[id]==1:
                num_fraud+=1
            else:
                num_normal+=1
        if num_fraud+num_normal<20:
            continue

        app_rate_dict[app]=num_fraud/(num_fraud+num_normal);

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
    fraudflow=[]
    normalflow=[]
    for app_rate in app_rate_list:
        app.append(app_rate[0])
        rate.append(app_rate[1])
        if app_rate[0] not in app_fraudflow_dict:
            fraudflow.append(0)
        else:
            fraudflow.append(app_fraudflow_dict[app_rate[0]])
        if app_rate[0] not in app_normalflow_dict:
            normalflow.append(0)
        else:
            normalflow.append(app_normalflow_dict[app_rate[0]])
        count.append(app_idCount_dict[app_rate[0]])
        # print(app,' ',rate,' ',count)
    data = pd.DataFrame({'app': app, 'rate':rate, 'count':count,'fraudflow':fraudflow,'normalflow':normalflow})
    data.to_csv('app比例名单withFlow.csv',encoding='utf_8_sig')

    print(9999)

    #test()
