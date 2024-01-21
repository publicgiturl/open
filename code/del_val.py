import os
from glob import glob
aa = []
with open('del_val.txt') as f:
    for i in f:
       aa.append(i.split('\n')[0])
for i in glob('Train/image/*.jpg'):
    if i.split('/')[-1] in aa:
        print(i)
        os.remove(i)