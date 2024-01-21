# /home/ms/Downloads/jeju/53/annotations/instances_default.json
# 20221103_W_T0293_NI_01405.JPG 132
# /home/ms/Downloads/jeju/53/annotations/instances_default.json
# 20221103_W_T0296_NI_00699.JPG 133
# import pandas as pd
import os

aa = ['20221103_W_T0293_NI_01405.JPG','20221103_W_T0296_NI_00699.JPG']
import random
from glob import glob
import json
from tqdm import tqdm
import pymysql
import cv2

# host_name = '192.168.0.13'
# user_name = 'land'
# paswd = 'land' \
#         '2021!@'
# db = 'landdb'
#
#
# conn=pymysql.connect(host=host_name, user=user_name,password=paswd, db=db, port=3306)
#
# sql = """
# select IMG_NAME
# from ai_image_tbl;
# """
# cursor = conn.cursor()
# cursor.execute(sql)
# rows = cursor.fetchall()
# cursor.close()
# file_lst = []
# for i in rows:
#     file_lst.append(i[0])
#
# dup_list = []
# num = 0
# for temp_file in tqdm(glob('D:/download/Landmarks/**/*.png', recursive=True)):
#     file_name = temp_file.split('\\')[1]+'-'+temp_file.split('\\')[2] + '-'+temp_file.split('\\')[-1]
#     if file_name not in file_lst:
#         dup_list.append(file_name)
#         num+=1
# print(dup_list)
# print(num)

def random_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return (r, g, b)

# 15가지 랜덤 색상 추출
num_colors = 15
color_maps = {idx: random_color() for idx, _ in enumerate(range(num_colors))}
cls_dict = {0:'young_man',
1:'young_woman',
2:'middle_aged_man',
3:'middle_aged_woman',
4:'old_aged_man',
5:'old_aged_woman',
6:'face',
7:'opened_eyes',
8:'closed_eyes',
9:'cigar',
10:'phone',
11:'mask',
12:'bottle',
13:'dog',
14:'seat_belt'}

for txt_file in tqdm(glob('/data/save_900/**/*.txt', recursive=True)):
    img_file = txt_file.replace('labels','images').replace('.txt','.png')
    save_file = img_file.replace('images','resutls')
    os.makedirs('/'.join(save_file.split('/')[:-1]), exist_ok=True)
    img = cv2.imread(img_file)
    img_h, img_w = img.shape[:-1]
    with open(txt_file) as t_file:
        for ann in t_file:
            cls, x,y,w,h = [float(coord) for coord in ann.split()]

            x_min = int((x - w / 2) * img_w)
            y_min = int((y - h / 2) * img_h)

            # 꼭짓점 좌표 계산
            x_max = int(x_min + (w * img_w))
            y_max = int(y_min + (h * img_h))

            cv2.rectangle(img, (x_min, y_min), (x_max, y_max), color_maps[int(cls)],2)
            cv2.putText(img, cls_dict[int(cls)], (x_min,y_min), cv2.FONT_HERSHEY_COMPLEX, 2, (0,0,200), 2)

    cv2.imwrite(save_file, img)
