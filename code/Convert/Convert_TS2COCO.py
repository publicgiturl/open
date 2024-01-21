import os.path as osp
import json
from tqdm import tqdm
import numpy as np
import cv2
from glob import glob

all_data = {}
for i in glob('/data/ai_dataSet/Data_Set/2DSS/test/*.json'):
    with open(i, encoding='utf-8') as j_file:
        json_data = json.load(j_file)
        all_data[json_data['image']] = json_data

with open('/data/ai_dataSet/Data_Set/2DSS/test/raw_test.json', 'w', encoding='utf-8') as new_file:
    json.dump(all_data, new_file, ensure_ascii=False, indent=1)


def change_class(class_path):
    with open(class_path,encoding='utf-8') as f:
        cls_dict = []
        for idx, cls in enumerate(f):
            cls_dict.append(dict(id=idx+1,name=cls.split('\n')[0]))
    return cls_dict

def convert_TS2COCO(input_file, out_file, image_prefix):
    with open(input_file, encoding='utf-8') as json_file:
        json_info = json.load(json_file)

        annotations = []
        images = []
        obj_count = 0

        for idx, v in enumerate(tqdm(json_info.values())):
            filename = v['image']
            img_path = osp.join(image_prefix, filename)
            height, width = cv2.imread(img_path).shape[:2]

            images.append(dict(
                id=idx,
                file_name=filename,
                height=height,
                width=width
            ))

            # bboxes = []
            # labels = []
            # masks = []
            for obj in v['annotations']:
                try:
                    data_anno = dict(
                        image_id=idx,
                        id=obj_count,
                        category_id=obj['category_id'],
                        bbox= obj['bbox'],
                        area=obj['area'],
                        segmentation=obj['segmentation'],
                        iscrowd=0
                    )
                    annotations.append(data_anno)
                    obj_count += 1
                except Exception as e:
                    print(filename)
                    pass

        coco_format_json = dict(
            images=images,
            annotations=annotations,
            categories=change_class('/data/ai_dataSet/Data_Set/2DSS/ts_class.names')
        )

        with open(out_file, 'w', encoding='utf-8') as json_out_file:
            json.dump(coco_format_json, json_out_file, ensure_ascii=False, indent=1)
convert_TS2COCO('/data/ai_dataSet/Data_Set/2DSS/test/raw_test.json', '/data/ai_dataSet/Data_Set/2DSS/test/test.json', '/data/ai_dataSet/Data_Set/2DSS/val')
