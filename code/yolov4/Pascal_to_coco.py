### Convert_to_Yolo_AI_version
import json, os
from glob import glob
import argparse
import numpy as np
import xml.etree.ElementTree as ET
from collections import deque
import re

def convert(size, box):
    dw = 1./(size[0])
    dh = 1./(size[1])
    x = (box[0] + box[1])/2.0 - 1
    y = (box[2] + box[3])/2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = round(x*dw, 3)
    w = round(w*dw, 3)
    y = round(y*dh, 3)
    h = round(h*dh, 3)
    return (x,y,w,h)

# xml_list = glob('C:/Users/HF/Desktop/mingsu/object_detection/Tensorflow/workspace/images/**/*.xml', recursive=True)
# classes = ['Tony', 'Bruce', 'Natasha', 'Rogers', 'Thor']
# for x_file in xml_list:
#     # 저장할 파일 경로
#     out_file = open(x_file.replace('.xml', '.txt'), 'w', encoding='utf-8')
#     # xml파일 불러오기
#     root = ET.parse(x_file).getroot()
#     # img_size
#     size = root.find('size')
#     w = int(size.find('width').text)
#     h = int(size.find('height').text)
#     cls_bb = []
#
#     for obj in root.iter('object'):
#         difficult = obj.find('difficult').text
#         cls = obj.find('name').text
#         if cls not in classes or int(difficult) == 1:
#             continue
#         # box좌표 불러오기
#         bbox = obj.find('bndbox')
#         cls_id = classes.index(obj.find('name').text.strip())
#         b = (float(bbox.find('xmin').text), float(bbox.find('xmax').text), float(bbox.find('ymin').text),
#              float(bbox.find('ymax').text))
#         bb = convert((w, h), b)
#         bbb = list([a for a in bb])
#         bbb.insert(0, cls_id)
#         cls_bb.append(','.join(str(a) for a in bbb))
#
#     out_file.write(x_file.replace('.xml', '.jpg') + ' ' + re.sub("\[|\]|\'", "", str(cls_bb)).replace(', ',' '))

# TF_version
xml_list = glob('C:/Users/HF/Desktop/mingsu/object_detection/Tensorflow/workspace/images/**/*.xml', recursive=True)
classes = ['Tony', 'Bruce', 'Natasha', 'Rogers', 'Thor']
for x_file in xml_list:
    # 저장할 파일 경로
    out_file = open(x_file.replace('.xml', '.txt'), 'w', encoding='utf-8')
    # xml파일 불러오기
    root = ET.parse(x_file).getroot()
    # img_size
    # size = root.find('size')
    # w = int(size.find('width').text)
    # h = int(size.find('height').text)
    cls_bb = []

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult) == 1:
            continue
        # box좌표 불러오기
        bbox = obj.find('bndbox')
        cls_id = classes.index(obj.find('name').text.strip())
        b = [float(bbox.find('xmin').text), float(bbox.find('xmax').text), float(bbox.find('ymin').text),
             float(bbox.find('ymax').text)]
        # bb = convert((w, h), b)
        # bbb = list([a for a in bb])
        b.append(cls_id)

        # bbb.insert(0, cls_id)
        cls_bb.append(','.join(str(a) for a in b))

        # break
    out_file.write(x_file.replace('.xml', '.jpg') + ' ' + re.sub("\[|\]|\'", "", str(cls_bb)).replace(', ',' '))