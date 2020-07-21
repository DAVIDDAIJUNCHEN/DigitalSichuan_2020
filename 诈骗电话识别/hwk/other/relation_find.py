import pandas as pd

user_train_csv = pd.read_csv('../../data/train/train_user.csv')
vv = user_train_csv.values
id_lable_train_dict ={}
for v in vv:
    id_lable_train_dict[v[0] ] =v[-1]

voc_csv_train = pd.read_csv('../../data/train/train_voc.csv')
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

init_bad_set=set()
for id in id_lable_train_dict:
    if id_lable_train_dict[id]==1:
        init_bad_set.add(id)

print(len(init_bad_set))

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
bad2 = set()
for id in bad1:
    if id not in id_imei_train_dict:
        continue
    kk = id_imei_train_dict[id]
    for k in kk:
        tt = imei_id_train_dict[k]
        for t in tt:
            if t not in init_bad_set:
                if t not in bad1:
                    bad2.add(t)

print(len(bad2))