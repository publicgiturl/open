import json
from tqdm import tqdm
import numpy as np
import os
from glob import glob

# 클래스파일에 존재하는 클래스명과 숫자로 매칭
def class_dict(file_path):
    with open(file_path, encoding='utf-8') as f:
        classes = {}
        for i, j in enumerate(f):
            classes[j.split('\n')[0]] = i
    return classes

# 전체 json폴더 내에 있는 json파일 불러와서 convert
def convert_Warehouse2YOLO(input_path, output_path, class_path):
    box_class = class_dict(class_path)

    num = 0
    yolo_dir = open(output_path, 'a', encoding='utf-8')
    if not os.path.exists(os.path.join('/'.join(output_path.split('/')[:-1]), 'coor')):
        os.mkdir(os.path.join('/'.join(output_path.split('/')[:-1]), 'coor'))

    new_path = os.path.join('/'.join(output_path.split('/')[:-1]), 'coor')
    for j_file in tqdm(glob(input_path+'/*.json', recursive=True)):
        with open(j_file, encoding='utf-8') as json_file:
            json_data = json.load(json_file)
            width,height =(1920, 1080)

            # json파일 내 이미지명 추출

            img_name = json_data['Source Data Info.']['source_data_ID'] + '.jpg'

            # convert된 yolo_data_set저장 경로
            yolo_set = open(new_path+'/'+img_name.replace('.jpg','.txt'), 'w', encoding='utf-8')


            # annotations 값 추출
            annotations = json_data['Learning Data Info.']['annotation']
            # file_path = j_file.replace('.json', '.jpg').replace('\\','/')
            file_path = ''

            # annotations된 객체들 반복
            for ann in annotations:
                # if ann['type'] == 'box':
                  if 'box' in ann.keys():
                    # yolo형식에 맞게 자료 변환
                    x1 = ann['box'][0]
                    y1 = ann['box'][1]
                    x2 = ann['box'][2]
                    y2 = ann['box'][3]

                    dw = 1. / width
                    dh = 1. / height
                    x = (float(x1) + float(x1) + float(x2)) / 2.0
                    y = (float(y1) + float(y1) + float(y2)) / 2.0
                    w = float(x2)
                    h = float(y2)

                    x = round(x * dw, 6)
                    w = round(w * dw, 6)
                    y = round(y * dh, 6)  # 6자리 표시
                    h = round(h * dh, 6)

                    obj = (str(box_class[ann['class_id']]) + ' '
                              + str(x) + ' '
                              + str(y) + ' '
                              + str(w) + ' '
                              + str(h)
                            )
                    # path값 설정
                    file_path += obj+'\n'

            yolo_set.write(file_path)
            yolo_set.close()
            yolo_dir.write('data/img/'+img_name+'\n')
    yolo_dir.close()

"""
    최종실행 방법 : 해당파일 내에 convert_Warehouse2YOLO('json파일들이 들어있는 경로', 'yolo_set을 저장할 경로 및 파일명', '클래스들이 저장되어 있는 파일명(.txt, .name)')
                  명령어로 실행                  
"""

convert_Warehouse2YOLO('C:/Users/User/Desktop/AI_hub_Project/Convert/JSON/labels', 'C:/Users/User/Desktop/AI_hub_Project/Convert/YOLO/train.txt', 'C:/Users/User/Desktop/AI_hub_Project/Convert/NAME/box.names.txt')
