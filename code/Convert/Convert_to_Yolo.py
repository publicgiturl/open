import json
from tqdm import tqdm
import numpy as np
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
    # convert된 yolo_data_set저장 경로
    yolo_set = open(output_path, 'a', encoding='utf-8')

    for j_file in tqdm(glob(input_path+'/*.json', recursive=True)):
        with open(j_file, encoding='utf-8') as json_file:
            json_data = json.load(json_file)
            # json파일 내 이미지명 추출
            img_name = json_data['Source data Info.']['source_data_ID'] + '.jpg'

            # annotations 값 추출
            annotations = json_data['Learning data info.']['annotation']
            file_path = j_file.replace('.json', '.jpg').replace('\\','/')

            # annotations된 객체들 반복
            for ann in annotations:
                if ann['type'] == 'box':
                    # yolo형식에 맞게 자료 변환
                    obj = (str(int(ann['data'][0])) + ','
                              + str(int(ann['data'][1])) + ','
                              + str(int(ann['data'][2])) + ','
                              + str(int(ann['data'][3])) + ','
                              + str(box_class[ann['class_id']]))
                    # path값 설정
                    file_path += ' ' + obj

            yolo_set.write(file_path+'\n')
    yolo_set.close()

"""
    최종실행 방법 : 해당파일 내에 convert_Warehouse2YOLO('json파일들이 들어있는 경로', 'yolo_set을 저장할 경로 및 파일명', '클래스들이 저장되어 있는 파일명(.txt, .name)')
                  명령어로 실행
                  
"""

convert_Warehouse2YOLO('F:/2021/작업안전/sample/json_data', 'F:/2021/작업안전/yolo_.txt', 'F:/2021/작업안전/class/warehouse_bbox.txt')