import pandas as pd
import pickle
user_train_csv = pd.read_csv('../../data/train/train_user.csv')
vv = user_train_csv.values
id_lable_train_dict = {}
zpn=0
zpid=set()
nzpid=set()
for v in vv:
    id_lable_train_dict[v[0]] = v[-1]
    if v[-1]==1:
        zpid.add(v[0])
    else:
        nzpid.add(v[0])
    # if v[-1]==1:
    #     zpn+=1
    #     print(v)


with open('../../data/features/train/voc_dict.txt', 'rb') as fin:
    dict_voc = pickle.load(fin)

for ii in list(nzpid)[2:4]:
    temp=dict_voc[ii]
    for t in temp.values:
        print(t[1:-1])
    print('\n\n')

# voc_train_csv = pd.read_csv('../../data/train/train_voc.csv')
# vv = voc_train_csv.values
# sms_people=set()
# max_time=0
# for v in vv[3000:10000]:
#     if v[0] in zpid:
#         # if v[2]==2:
#         #     continue
#         if v[4]>max_time:
#             max_time=v[4]
#         if v[4]>600:
#             print([v[2:-1]])


        #print(v[2:-1])




print(66)