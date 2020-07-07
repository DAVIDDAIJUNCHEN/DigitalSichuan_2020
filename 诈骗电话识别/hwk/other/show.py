import pickle
import numpy as np
import matplotlib.pyplot as plt
X_train_t=open('../../data/X_train','rb')
X_train=pickle.load(X_train_t)
X_train_array=np.array(X_train)

t=X_train_array[:,5]
plt.boxplot(t)
plt.show()
print(88)