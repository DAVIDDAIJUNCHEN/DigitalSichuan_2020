import pandas as pd

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

#rr = pd.read_csv('C:/Users/houwenkui/Documents/result/and.csv')
rr = pd.read_csv('../test_results/and3.csv')
vv=rr.values
init_bad_set=set()
for v in vv:
    if v[1]==1:
        init_bad_set.add(v[0])

bad1=set()
for id in init_bad_set:
    if id not in id_imei_train_dict:
        continue
    kk=id_imei_train_dict[id]
    for k in kk:
        tt=imei_id_train_dict[k]
        for t in tt:
            #print(t)
            if t not in init_bad_set:
                bad1.add(t)
print(len(bad1))

bad2=set()
for id in bad1:
    if id not in id_imei_train_dict:
        continue
    kk=id_imei_train_dict[id]
    for k in kk:
        tt=imei_id_train_dict[k]
        for t in tt:
            #print(t)
            if t not in init_bad_set:
                if t not in bad1:
                    bad2.add(t)
print(len(bad2))

# import csv
#
# with open('../test_results/' + 'hahaha.csv',
#           'w', newline='', encoding='utf-8') as fout:
#     field_names = ['phone_no_m', 'label']
#     writer = csv.DictWriter(fout, fieldnames=field_names)
#     writer.writeheader()
#
#     for ii in range(len(vv)):
#         v=vv[ii]
#         if v[-1]==0 and v[1] in bad1:
#             v[-1]=1
#         writer.writerow({'phone_no_m': v[0], 'label': v[-1]})
