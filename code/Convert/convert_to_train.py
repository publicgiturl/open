import os
from sklearn.model_selection import train_test_split

X = []
with open('E:/data_set_TF.txt', 'r', encoding='utf-8') as f:
    for i in f:
        X.append(i.split('\n')[0])

train_ratio = 0.75
validation_ratio = 0.15
test_ratio = 0.10


# train is now 75% of the entire data set
# the _junk suffix means that we drop that variable completely
x_train, x_test = train_test_split(X, test_size=1 - train_ratio)

# test is now 10% of the initial data set
# validation is now 15% of the initial data set
x_val, x_test = train_test_split(x_test, test_size=test_ratio/(test_ratio + validation_ratio)) 

for i in x_train:
    with open('E:/yolov4_TF/data/dataset/train.txt','a', encoding='utf-8') as f:
            f.write(i+'\n')
            f.close()
for i in x_val:
    with open('E:/yolov4_TF/data/dataset/val.txt','a', encoding='utf-8') as f:
            f.write(i+'\n')
            f.close()
for i in x_test:
    with open('E:/yolov4_TF/data/dataset/test.txt','a', encoding='utf-8') as f:
            f.write(i+'\n')
            f.close()
