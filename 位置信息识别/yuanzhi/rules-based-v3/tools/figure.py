import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd

# locationx	locationy
bjs = pd.read_csv('../data/figure/normal.csv', sep='\t')
lat = bjs['locationx']
lon = bjs['locationy']
label = bjs['street_num']
# lat = [116.23, 116.78, 116.90]
# lon = [31, 35, 34]


plt.rcParams['font.sans-serif'] = ['SimHei']
plt.scatter(lat, lon, alpha=0.3)
for i in range(len(lat)):
    plt.annotate(str(label[i]).replace('号', ''), xy=(lat[i], lon[i]))
plt.xlabel('longitude')
plt.ylabel('latitude')
# plt.xlim(124.890, 124.910)
# plt.ylim(46.614, 46.622)
plt.show()
