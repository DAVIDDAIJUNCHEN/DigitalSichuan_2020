import pickle
import numpy as np
import sys
sys.path.append('../../')
from utils import evaluate
from tensorflow import keras
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import Sequential

X_train_t=open('../../data/X_train','rb')
X_train=pickle.load(X_train_t)

label_train_t=open('../../data/label_train','rb')
label_train=pickle.load(label_train_t)

label_train_2d=[]
for ii in label_train:
    if ii==1:
        label_train_2d.append([1,0])
    else:
        label_train_2d.append([0,1])



init_size=len(X_train[0])

X_train_array=np.array(X_train)
label_train_array=np.array(label_train_2d)

model=Sequential()
model.add(Dense(units=500,activation='relu',input_dim=init_size))
model.add(Dense(units=200,activation='relu',input_dim=500))
model.add(Dense(units=200,activation='relu',input_dim=200))
model.add(Dense(units=200,activation='relu',input_dim=200))
model.add(Dense(units=200,activation='relu',input_dim=200))
model.add(Dense(units=2,activation='softmax'))

model.compile(loss='categorical_crossentropy',optimizer='adam',metrics=['accuracy'])

model.fit(X_train_array,label_train_array,epochs=10,batch_size=256)

loss=model.evaluate(X_train_array,label_train_array,batch_size=32)
y=model.predict(X_train_array)
y_train=[]
for ii in y:
    if ii[0]>ii[1]:
        y_train.append(1)
    else:
        y_train.append(0)


evaluate(label_train, y_train, model='DNN')
print(loss)



