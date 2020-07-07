import pickle
import pandas as pd
# X_blindtest_t=open('../../data/X_blindtest','rb')
# X_blindtest=pickle.load(X_blindtest_t)

# with open('../../data/features/test/voc_dict.txt', 'rb') as fin:
#     dict_voc = pickle.load(fin)

voc_csv = pd.read_csv('../../data/test/test_voc.csv')
vv=voc_csv.values
imei_set=set()
for v in vv:
    imei_set.add(v[-1])

voc_csv_train = pd.read_csv('../../data/train/train_voc.csv')
vv_train=voc_csv_train.values
imei_train_set=set()
for v in vv_train:
    imei_train_set.add(v[-1])

tt=imei_set&imei_train_set
print(len(tt))