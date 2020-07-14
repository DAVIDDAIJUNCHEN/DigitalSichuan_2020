import pandas as pd
import numpy as np
user_csv = pd.read_csv('../../data/test/test_user.csv')
vv_user = user_csv.values

voc_csv_train = pd.read_csv('../../data/test/test_voc.csv')
vv_train = voc_csv_train.values
imei_id_train_dict = {}
id_imei_train_dict={}
for v in vv_train:
    if v[-1] not in imei_id_train_dict:
        imei_id_train_dict[v[-1]] = set()
    imei_id_train_dict[v[-1]].add(v[0])

    if v[0] not in id_imei_train_dict:
        id_imei_train_dict[v[0]]=set()
    id_imei_train_dict[v[0]].add(v[-1])


xx_t= pd.read_csv('../test_results/change4.csv')
vv=xx_t.values
xx=xx_t.values
change_set=set()
for ii in range(len(vv)):
    v=vv[ii]

    if v[1]==1 :

        # print('\n')
        # print(vv[ii][1:])
        flag=1
        if v[0] in id_imei_train_dict:
            temp_set=set()
            kk=id_imei_train_dict[v[0]]
            for k in kk:
                bb=imei_id_train_dict[k]
                for b in bb:
                    temp_set.add(b)
            #print(len(id_imei_train_dict[v[0]]))
            #print(len(temp_set))
            flag=len(temp_set)
        if vv_user[ii][3]==1 and flag==1:
            if vv_user[ii][4]<19:
                 continue
            if np.isnan(vv_user[ii][4]):
                continue
            if vv_user[ii][4]>200:
                 continue

            change_set.add(v[0])
            print(vv_user[ii][3])
            print(flag)
            print(vv_user[ii][1:])
            print('\n')

print(len(change_set))



n=0
import csv

with open('../test_results/' + 'change6.csv',
          'w', newline='', encoding='utf-8') as fout:
    field_names = ['phone_no_m', 'label']
    writer = csv.DictWriter(fout, fieldnames=field_names)
    writer.writeheader()

    for ii in range(len(xx)):
        m=xx[ii][0]
        p=xx[ii][1]
        if m in change_set:
            n+=1
            p=0
        writer.writerow({'phone_no_m': m, 'label': p})
print(n)
