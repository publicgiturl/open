import os, shutil
from tqdm import tqdm
from glob import glob

# class Getallfiles:
#     def __init__(self):
#         pass
#     def getFiles(self,dir):
#         x = 0
#         for pack in os.walk(dir):
#             for f in pack[2]:
#                 if f.endswith('.json'):
#                     x+=1
#         print(('Dir: %s, 전체 파일수 : %s')%(dir,str(x)))
# if __name__ =='__main__':
#     f= Getallfiles()
#     f.getFiles('Z:/학습데이터')
#     f.getFiles('Z:/학습데이터/middle classification_01')
#     f.getFiles('Z:/학습데이터/middle classification_02')
#     f.getFiles('Z:/학습데이터/middle classification_03_06')
#     f.getFiles('Z:/학습데이터/middle classification_07')
#

# for img in tqdm(glob('H:/Data/08_vehicle_exterior/**/*.jpg', recursive=True)):
#     file_name = img.split('\\')[-1]
#     shutil.move(img, f'H:/Data/08_vehicle_exterior/images/{file_name}')
#
# for img in tqdm(glob('H:/Data/08_vehicle_exterior/**/*.json', recursive=True)):
#     file_name = img.split('\\')[-1]
#     shutil.move(img, f'H:/Data/08_vehicle_exterior/label/{file_name}')

import json
import numpy as np
img_dummy = []
dummy_list = []

with open('H:/Data/04_Industrial_safety/fire/label/S3-N1202MF03614.json', encoding='utf-8-sig') as json_file:
    json_data = json.load(json_file)

    img_name = json_data["image"]["filename"]
    img_path = '04_Industrial_safety/fire/image'

    width, height = json_data["image"]["resolution"][0], json_data["image"]["resolution"][1]
    location = None
    # print(json_data)
    img_dummy.append([img_name, img_path, width, height, location])

    # if json_data["image"]["filename"] != 'H:/Data/04_Industrial_safety/fire/label/S3-N0816MS18839.json'.split('\\')[-1].replace('.json', '.jpg'):
    #     print('H:/Data/04_Industrial_safety/fire/label/S3-N0816MS18839.json')

    obj_idx = 1

    for ann in json_data['annotations']:
        px = []
        py = []
        print(ann['class'])
        if ann["class"] == "01":  # 검정색 연기
            db_code = 28
        elif ann["class"] == "02":  # 회색연기
            db_code = 30
        elif ann["class"] == "03":  # 흰색연기
            db_code = 29
        elif ann["class"] == "04":  # 불꽃
            db_code = 33
        elif ann["class"] == "05":  # 구름
            db_code = 31
        elif ann["class"] == "06":  # 안개 연무
            db_code = 34
        elif ann["class"] == "07":  # 조명
            db_code = 32
        elif ann["class"] == "08":  # 햇빛
            db_code = 35
        elif ann['class'] in ['11', '09', '10']:
            continue

        if 'box' in ann.keys():
            anno = 'box'
            xmin = ann["box"][0]
            ymin = ann["box"][1]
            xmax = ann["box"][2]
            ymax = ann["box"][3]
            x_arr = None
            y_arr = None

        if 'polygon' in ann.keys():
            anno = 'polygon'
            poly_point = np.array(ann['polygon'])
            x_arr = poly_point[:, 0].flatten().tolist()
            y_arr = poly_point[:, 1].flatten().tolist()
            xmax = poly_point[:, 0].max()
            xmin = poly_point[:, 0].min()
            ymin = poly_point[:, 1].min()
            ymax = poly_point[:, 1].max()
            print(y_arr)
            print('-'*30)
            print(x_arr)
        dummy_list.append([img_name, obj_idx, db_code, anno, xmin, ymin, xmax, ymax, x_arr, y_arr])
        obj_idx += 1
# print(img_dummy)
print(dummy_list)