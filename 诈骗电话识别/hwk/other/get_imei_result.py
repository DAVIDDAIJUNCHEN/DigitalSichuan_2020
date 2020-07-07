import pandas as pd
import pickle
def get_imei_result():
    print('csn')




if __name__ == '__main__':

    voc_csv = pd.read_csv('../../data/test/test_voc.csv')
    vv = voc_csv.values
    imei_dict = {}
    for v in vv:
        if v[-1] not in imei_dict:
            imei_dict[v[-1]]=set()
        imei_dict[v[-1]].add(v[0])

    voc_csv_train = pd.read_csv('../../data/train/train_voc.csv')
    vv_train = voc_csv_train.values
    imei_train_dict = {}
    for v in vv_train:
        if v[-1] not in imei_train_dict:
            imei_train_dict[v[-1]]=set()
        imei_train_dict[v[-1]].add(v[0])

    imei_and=set(imei_dict.keys()) & set(imei_train_dict.keys())

    user_csv = pd.read_csv('../../data/test/test_user.csv')
    vv = user_csv.values
    id_lable_dict={}
    for v in vv:
        id_lable_dict[v[0]]=-1

    user_train_csv = pd.read_csv('../../data/train/train_user.csv')
    vv = user_train_csv.values
    id_lable_train_dict={}
    for v in vv:
        id_lable_train_dict[v[0]]=v[-1]

    result={}
    for im in imei_and:
        temp=imei_train_dict[im]
        sum=0
        cnt=0
        for tt in temp:
            cnt+=1
            sum+=id_lable_train_dict[tt]
            print(id_lable_train_dict[tt])
        print('\n')
        if sum/cnt>0.5:
            r=1
        else:
            r=0

        temp = imei_dict[im]
        for tt in temp:
            result[tt]=r

    imie_result = open('./imie_result', 'wb')
    pickle.dump(result, imie_result)




print(99)
    #get_imei_result()