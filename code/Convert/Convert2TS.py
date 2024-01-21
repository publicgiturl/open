import random
from glob import glob
import os
import os.path as osp
import shutil
from tqdm import tqdm


for idx, file_name in tqdm(enumerate(glob('E:/2021/TS/2D BB GT/val/labels/*.txt'))):
    if osp.isfile('E:/2021/TS/2D BB GT/data/{}'.format(file_name.split('\\')[-1].replace('.txt','.png'))):
        shutil.move('E:/2021/TS/2D BB GT/data/{}'.format(file_name.split('\\')[-1].replace('.txt','.png')),
                                                         'E:/2021/TS/2D BB GT/val/images/{}'.format(file_name.split('\\')[-1].replace('.txt','.png')))
    elif osp.isfile('E:/2021/TS/2D BB GT/data/{}'.format(file_name.split('\\')[-1].replace('.txt','.jpg'))):
        shutil.move('E:/2021/TS/2D BB GT/data/{}'.format(file_name.split('\\')[-1].replace('.txt', '.jpg')),
                    'E:/2021/TS/2D BB GT/val/images/{}'.format(file_name.split('\\')[-1].replace('.txt', '.jpg')))
    # file_path = osp.join(file_name.split('\\')[0])
    # os.rename(file_name,file_path+'/{}.png'.format(idx+1796))


# file_list = os.listdir('E:/2021/TS/2D BB GT/labels')
# val_list = random.sample(file_list, int(len(file_list)*.2))
# test_list = random.sample(val_list, int(len(val_list)*.5))
# for i in tqdm(test_list):
#     shutil.move('E:/2021/TS/2D BB GT/labels/{}'.format(i), 'E:/2021/TS/2D BB GT/test/labels/{}'.format(i))
# for i in tqdm(val_list):
#     if osp.isfile('E:/2021/TS/2D BB GT/labels/{}'.format(i)):
#         shutil.move('E:/2021/TS/2D BB GT/labels/{}'.format(i), 'E:/2021/TS/2D BB GT/val/labels/{}'.format(i))
