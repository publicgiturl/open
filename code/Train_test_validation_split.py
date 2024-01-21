from sklearn.model_selection import train_test_split

X = []
# for i in aa['filename']:
#     X.append(i)
for i in glob('D:/ai_set/*.jpg'):
    X.append(i)

train_ratio = 0.75
validation_ratio = 0.15
test_ratio = 0.10


# train is now 75% of the entire data set
# the _junk suffix means that we drop that variable completely
# stratify= 정답값(Classification)
x_train, x_test = train_test_split(X, test_size=1 - train_ratio, shuffle=True, random_state = 42)

# test is now 10% of the initial data set
# validation is now 15% of the initial data set
x_val, x_test = train_test_split(x_test, test_size=test_ratio/(test_ratio + validation_ratio), shuffle=True, random_state = 42) 

for i in x_train:
    with open('C:/Users/HumanForest/Desktop/darknet/build/darknet/x64/data/ai_product/train.txt','a', encoding='utf-8') as f:
            f.write(i+'\n')
            f.close()
for i in x_val:
    with open('C:/Users/HumanForest/Desktop/darknet/build/darknet/x64/data/ai_product/val.txt','a', encoding='utf-8') as f:
            f.write(i+'\n')
            f.close()
for i in x_test:
    with open('C:/Users/HumanForest/Desktop/darknet/build/darknet/x64/data/ai_product/test.txt','a', encoding='utf-8') as f:
            f.write(i+'\n')
            f.close()
