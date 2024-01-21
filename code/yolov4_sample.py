from glob import glob
import os, json


train_list = []
test_list = []
with open('./train_list.txt', encoding='utf-8') as f:
    for i in f:
        train_list.append(i.split('\n')[0])
with open('./test_list.txt', encoding='utf-8') as f:
    for i in f:
        test_list.append(i.split('\n')[0])

try :
    for i in glob('/data/ai_dataSet/02_상품/**/*.jpg', recursive=True):
        if i.split('\\')[-1] in train_list:
            with open('./train_img.txt', 'a', encoding='utf-8') as f:
                f.write(i)
                f.write('\n')
            f.close()
        elif i.split('\\')[-1] in test_list:
            with open('./test_img.txt', 'a', encoding='utf-8') as f:
                f.write(i)
                f.write('\n')
            f.close()
except Exception as ex:
    print(ex)
    pass