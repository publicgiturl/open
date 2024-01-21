# -*- coding: UTF-8 -*-
import os
import json
import pandas as pd
import numpy as np
from tqdm import tqdm
pd.set_option('mode.chained_assignment', None)

# cls_dict = {'potted plant' :155,  'tv':156 ,'chair':157, 'person':158, 'microwave':159, 'refrigerator':160, 'book':161,
#  'clock':162, 'vase':163, 'dining table':164, 'bear':165, 'bed':166, 'stop sign':167, 'truck':25, 'car':6,
#  'teddy bear':0, 'skis':0, 'oven':0, 'sports ball':0, 'baseball glove':0, 'tennis racket':0,
#  'handbag':0, 'backpack':0, 'bird':171, 'boat':0, 'cell phone':168, 'train':172, 'sandwich':0, 'bowl':0,
#  'surfboard':0, 'laptop':169, 'mouse':0, 'keyboard':0, 'bus':24, 'cat':170, 'airplane':173, 'zebra':0,
#  'tie':0, 'traffic light':18, 'apple':0, 'baseball bat':0, 'knife':0, 'cake':0, 'wine glass':0,
#  'cup':0, 'spoon':0, 'banana':0, 'donut':0, 'bottle':0, 'sink':0, 'toilet':0, 'broccoli':0,
#  'skateboard':0, 'fork':0, 'carrot':0, 'couch':0, 'remote':0, 'scissors':0, 'bicycle':20,
#  'sheep':0, 'bench':0, 'orange':0, 'elephant':0, 'frisbee':0, 'umbrella':122, 'horse':0, 'dog':174,
#  'motorcycle':5, 'kite':0, 'pizza':0, 'fire hydrant':0, 'suitcase':0, 'hot dog':0, 'cow':0,
#  'giraffe':0, 'snowboard':0, 'parking meter':0, 'toothbrush':0, 'toaster':0, 'hair drier':0,}

# def start():
#     for (path, dir, files) in os.walk(main_path):  # for (path,dir,files) in os.walk(beforepath) beforepath에 있는 디렉토리 탐색
#         for fileName in files:  # 디렉토리 탐색 중 파일을 검색
#             if fileName.endswith('.json'):  # .json 확장자를 탐색
#                 try:
#                     with open(os.path.join(path, fileName),encoding='utf-8') as json_file:  # 파일 열기
#                         jsonData = json.load(json_file)  # 디스크에 있는 포맷 데이터를 파이썬으로 읽어 오기
#
#                         for arr in range(len(jsonData["annotations"])):
#                             jsonData["annotations"][arr]['flags'] = {} # "flags" 의 value를 {}변환
#
#                     with open(os.path.join(path,fileName), 'w', encoding='utf-8') as json_change:
#                         json.dump(jsonData, json_change, ensure_ascii=False, indent=4)
#
#                 finally:
#                     json_file.close()
#
#
# if __name__ == '__main__':
#     start()


# df = pd.read_csv('D:/download/coco_val_convert_cls.csv', encoding='utf-8')
# img_resolution = {}
# with open('D:/download/annotations_trainval2017/annotations/instances_val2017.json') as j_file:
#  json_data = json.load(j_file)
#  for img in json_data['images']:
#   img_resolution[img['file_name']] =  [img['width'], img['height']]
#
# with open('D:/download/annotations_trainval2017/annotations/img_resl.json', 'w', encoding='utf-8') as new_json:
#  json.dump(img_resolution, new_json, ensure_ascii=False, indent=2)

aa = {"segmentation": [[285.84,353.8,341.93,247.01,366.74,213.57,380.76,196.31,398.02,179.06,382.92,154.25,381.84,126.2,404.49,89.53,415.28,73.35,454.11,78.74,476.76,102.47,487.55,163.96,509.12,173.66,516.67,199.55,513.44,264.27,489.71,283.69,405.57,267.51,379.69,257.8,368.9,257.8,346.25,262.11,337.62,275.06],[413.12,389.39,480.0,344.09,486.47,353.8,487.55,385.08,442.25,396.94]],"area": 25664.856200000002,"iscrowd": 0,"image_id": 8690,"bbox": [285.84,73.35,230.83,323.59],"category_id": 1,"id": 200151}

print(aa['segmentation'])