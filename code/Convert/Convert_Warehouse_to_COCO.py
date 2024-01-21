import os.path as osp
import json
from tqdm import tqdm
import cv2
import numpy as np
from glob import glob

# 폴리건 좌표에서 bbox좌표 값 출력
def getbbox(points):
    polygons = np.array(points)
    x,y = polygons[:,0], polygons[:,1]
    # bbox = [int(x.min()),int(y.min()), int(x.max()),int(y.max())]
    bbox = [int(x.min()), int(y.min()), int(x.max()) - int(x.min()), int(y.max() - int(y.min()))]
    # area = 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))
    area = (x.max()-x.min())*(y.max()-y.min())
    return bbox, area

# 물류창고 내 폴리건 클래스
def change_class(class_name):
    if class_name =='WO-08':
        return 0
    elif class_name =='SO-01':
        return 1
    elif class_name =='SO-05':
        return 2
    elif class_name =='SO-13':
        return 3
    elif class_name =='SO-14':
        return 4
    elif class_name =='SO-15':
        return 5

def convert_Warehouse2COCO(input_file, out_file, image_prefix, division):
    all_data = {}
    # 전체 json파일을 하나의 json파일로 만드는 작업
    for i in glob('../warehouse/{}/*.json'.format(division)):
        with open(i, encoding='utf-8') as j_file:
            json_data = json.load(j_file)
            all_data[json_data['Source data Info.']['source_data_ID'] + '.jpg'] = json_data
    with open('../warehouse/raw_{}.json'.format(division), 'w', encoding='utf-8') as new_file:
        json.dump(all_data, new_file, ensure_ascii=False, indent=1)

    # 전체 json값이 저장된 하나의 파일
    with open(input_file, encoding='utf-8') as json_file:
        json_info = json.load(json_file)

        annotations = []
        images = []
        obj_count = 0

        for idx, v in enumerate(tqdm(json_info.values())):
            filename = v['Source data Info.']['source_data_ID'] + '.jpg'
            img_path = osp.join(image_prefix, filename)
            height, width = cv2.imread(img_path).shape[:2]
            # Yolact coco_dataset
            images.append(dict(
                id=idx,
                file_name=filename,
                height=height,
                width=width
            ))

            for obj in v['Learning data info.']['annotation']:
                if obj['type'] == 'polygon' :#and obj['class_id'] =='SO-13':
                    poly = np.array(obj['data'])
                    bbox, area = getbbox(poly)
                    data_anno = dict(
                        image_id=idx,
                        id=obj_count,
                        category_id=change_class(obj['class_id']),
                        bbox= bbox,
                        area=area,
                        segmentation=[list(np.asarray(poly).flatten())],
                        iscrowd=0
                    )
                    annotations.append(data_anno)
                    obj_count += 1
        coco_format_json = dict(
            images=images,
            annotations=annotations,
            # categories=[{'id':0,'name':'SO-13'}]
            # 각 클래스에 맞게 클래스명과 숫자 매칭
            categories=[{'id': 0, 'name': 'WO-08'}, {'id': 1, 'name': 'SO-01'},
                        {'id': 2, 'name': 'SO-05'}, {'id': 3, 'name': 'SO-13'},
                        {'id': 4, 'name': 'SO-14'}, {'id': 5, 'name': 'SO-15'}]
        )
        with open(out_file, 'w', encoding='utf-8') as json_out_file:
            json.dump(coco_format_json, json_out_file, ensure_ascii=False, indent=1)


"""
    최종실행 방법 : 해당파일 내에 제일 마지막 convert_Warehouse2COCO('전체 json값이 들어있는 json파일', '최종 파일을 저장할 경로와 파일명', '이미지가 들어있는 폴더', 'train 혹은 val')
                  명령어로 실행

"""
# train폴더에 대한 컨버팅 실행
convert_Warehouse2COCO('../warehouse/raw_train.json',
                       '../warehouse/train.json',
                       '../warehouse/train', 'train')
# val폴더에 대한 컨버팅 실행
convert_Warehouse2COCO('../warehouse/raw_val.json',
                       '../warehouse/val.json',
                       '../warehouse/val', 'val')