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

user_csv = pd.read_csv('../../data/test/test_user.csv')
vv_user = user_csv.values


rr = pd.read_csv('C:/Users/houwenkui/Documents/result/7778GradientBoosting_allmonths_newfeatures.csv')
rr2 = pd.read_csv('C:/Users/houwenkui/Documents/result/c1234GradientBoosting_all.csv')
vv2=rr2.values
vv=rr.values
n=0
aa=0
test_ids=[]
print(len(vv))
change_set=set()
for ii in range(len(vv)):
    v=vv[ii]
    v2=vv2[ii]
    if v[1]==0 and v2[1]==1:
        n+=1
        test_ids+=v[0]
        print('\n')
        #print(vv_user[ii][1:])
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
        if vv_user[ii][3]<2 and flag<2 :
            aa+=1
            change_set.add(v[0])


print(n)
print(aa)
print(len(change_set))

n=0
xx_t= pd.read_csv('../test_results/and3.csv')
xx=xx_t.values
import csv

with open('../test_results/' + 'change4.csv',
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
