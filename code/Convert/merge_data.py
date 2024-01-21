import shutil
import os.path as osp
import os
import json
from glob import glob
from tqdm import tqdm
import random

def mkdir(data_path):
    if not osp.exists(data_path):
        os.makedirs(data_path, exist_ok=True)

# 클래스파일에 존재하는 클래스명과 숫자로 매칭
def class_dict(file_path):
    with open(file_path, encoding='utf-8') as f:
        classes = {}
        for i, j in enumerate(f):
            classes[j.split('\n')[0]] = i
    return classes

def move_all_data(src, image_dst, label_dst):
    for file in tqdm(glob(f'{src}/**/*.json',recursive=True),desc='json'):
        mkdir(label_dst)
        shutil.move(file, f'{label_dst}/{file.split("/")[-1]}')

    for file in tqdm(glob(f'{src}/**/*.jpg',recursive=True),desc='jpg'):
        mkdir(image_dst)
        shutil.move(file, f'{image_dst}/{file.split("/")[-1]}')

def split_train_val_test(src, image_dst, label_dst):
    move_all_data(src, image_dst, label_dst)
    data_list = os.listdir(image_dst)

    # Split_Data
    val_list = random.sample(data_list, int(len(data_list) * .2))
    test_list = random.sample(val_list, int(len(val_list) * .5))

    train = image_dst.replace(image_dst.split('/')[-1], 'train/images')
    val = image_dst.replace(image_dst.split('/')[-1], 'val/images')
    test = image_dst.replace(image_dst.split('/')[-1], 'test/images')

    for i in [train, val, test]:
        mkdir(i)
        mkdir(i.replace('images','labels'))
        mkdir(i.replace('images', 'jsons'))

    for i in tqdm(test_list, desc='test'):
        shutil.move(f'{image_dst}/{i}', f'{test}/{i}')
        shutil.move(f'{label_dst}/{i.replace(".jpg",".json")}', f'{test.replace("images","jsons")}/{i.replace(".jpg",".json")}')
    for i in tqdm(val_list, desc='val'):
        if osp.isfile(f'{image_dst}/{i}'):
            shutil.move(f'{image_dst}/{i}', f'{val}/{i}')
            shutil.move(f'{label_dst}/{i.replace(".jpg",".json")}',
                        f'{val.replace("images", "jsons")}/{i.replace(".jpg", ".json")}')
    for i in tqdm(data_list, desc='train'):
        if osp.isfile(f'{image_dst}/{i}'):
            shutil.move(f'{image_dst}/{i}', f'{train}/{i}')
            shutil.move(f'{label_dst}/{i.replace(".jpg",".json")}',
                        f'{train.replace("images", "jsons")}/{i.replace(".jpg", ".json")}')
    j_train, j_val, j_test = train.replace('images','jsons'), val.replace('images','jsons'), test.replace('images','jsons')
    return j_train, j_val, j_test