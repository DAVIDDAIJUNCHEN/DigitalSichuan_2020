import pandas as pd
rr2 = pd.read_csv('C:/Users/houwenkui/Documents/result/c1234GradientBoosting_all.csv')

rr = pd.read_csv('C:/Users/houwenkui/Documents/result/7778GradientBoosting_allmonths_newfeatures.csv')
vv2=rr2.values
vv=rr.values
n=0
# n1=0
# n2=0
# n3=0
# n4=0
# print(len(vv))
# for ii in range(len(vv)):
#     v=vv[ii]
#     v2=vv2[ii]
#     if v[1]==1 and v2[1]==1:
#         n1+=1
#     if v[1]==0 and v2[1]==1:
#         n2+=1
#     if v[1]==1:
#         n3+=1
#     if v2[1]==1:
#         n4+=1
#
# print(n1)
# print(n2)
# print(n3)
# print(n4)


import csv

with open('../test_results/' + 'and3.csv',
          'w', newline='', encoding='utf-8') as fout:
    field_names = ['phone_no_m', 'label']
    writer = csv.DictWriter(fout, fieldnames=field_names)
    writer.writeheader()

    for ii in range(len(vv)):
        m=vv[ii][0]
        p=vv[ii][1] | vv2[ii][1]
        if p==1:
            n+=1
        writer.writerow({'phone_no_m': m, 'label': p})
print(len(vv))
print(n)