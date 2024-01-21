from glob import glob
from tqdm import tqdm
import json
import numpy as np
from datetime import datetime, date


class ConvertEncoder(json.JSONEncoder):
    """ Special json encoder for numpy types """

    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, (datetime, date)):
            return obj.isoformat()
        return json.JSONEncoder.default(self, obj)


# for j_file in tqdm(glob('D:/download/annotations/instances_default.json', recursive=True)):
#     file_path = 'D:/download/annotations'
#     with open(j_file, encoding='utf-8') as json_file:
#         json_data = json.load(json_file)
#
#         for img in json_data['images']:
#             width = img['width']
#             height = img['height']
#             img_id = img['id']
#
#             obj_num = 1
#             annotations = []
#             for ann in json_data['annotations']:
#                 if img_id == ann['image_id']:
#                     annotations.append(dict(
#                         id=obj_num,
#                         image_id=1,
#                         category_id=ann['category_id'],
#                         segmentation=ann['segmentation'],
#                         area=ann['area'],
#                         bbox=ann['bbox'],
#                         iscrowd=ann['iscrowd'],
#                         attributes=ann['attributes']
#                     ))
#                     obj_num += 1
#             new_json = dict(
#                 info=json_data['info'],
#                 licenses=[json_data['licenses']],
#                 categories=[
#                     {
#                         "id": 1,
#                         "name": "빌딩",
#                         "supercategory": ""
#                     },
#                     {
#                         "id": 2,
#                         "name": "사람",
#                         "supercategory": ""
#                     },
#                     {
#                         "id": 3,
#                         "name": "트럭",
#                         "supercategory": ""
#                     },
#                     {
#                         "id": 4,
#                         "name": "승용차",
#                         "supercategory": ""
#                     },
#                     {
#                         "id": 5,
#                         "name": "버스",
#                         "supercategory": ""
#                     },
#                     {
#                         "id": 6,
#                         "name": "차선",
#                         "supercategory": ""
#                     },
#                     {
#                         "id": 7,
#                         "name": "노면표시",
#                         "supercategory": ""
#                     }
#                 ],
#                 images=[dict(
#                     id=1,
#                     width=width,
#                     height=height,
#                     file_name=img['file_name'],
#                     license=0,
#                     flickr_url='',
#                     coco_url='',
#                     date_captured=0
#                 )],
#                 annotations=annotations)
#             with open(f'{file_path}/{img["file_name"].replace(".PNG", ".json")}', 'w',
#                       encoding='utf-8') as new_file:
#                 json.dump(new_json, new_file, indent=2, ensure_ascii=False, cls=ConvertEncoder)

for j_file in tqdm(glob('D:/download/annotations/ind/*.json', recursive=True)):
    new_ann = []
    area_dict = {}
    with open(j_file, encoding='utf-8') as json_file:
        json_data = json.load(json_file)

        for idx, ann in enumerate(json_data['annotations']):
            if ann['area'] not in area_dict.keys():
                area_dict[ann['area']] = 1
                new_ann.append(ann)
            else:
                continue

    new_json = dict(
                    info=json_data['info'],
                    licenses=[json_data['licenses']],
                    categories=[
                        {
                            "id": 1,
                            "name": "빌딩",
                            "supercategory": ""
                        },
                        {
                            "id": 2,
                            "name": "사람",
                            "supercategory": ""
                        },
                        {
                            "id": 3,
                            "name": "트럭",
                            "supercategory": ""
                        },
                        {
                            "id": 4,
                            "name": "승용차",
                            "supercategory": ""
                        },
                        {
                            "id": 5,
                            "name": "버스",
                            "supercategory": ""
                        },
                        {
                            "id": 6,
                            "name": "차선",
                            "supercategory": ""
                        },
                        {
                            "id": 7,
                            "name": "노면표시",
                            "supercategory": ""
                        }
                    ],
                    images=json_data['images'],
                    annotations=new_ann)
    with open(j_file, 'w', encoding='utf-8') as new_file:
        json.dump(new_json, new_file, indent=2, ensure_ascii=False, cls=ConvertEncoder)

# new_ann = []
# area_dict = {}
# with open('D:/download/annotations/ind/frame_000126.json', encoding='utf-8') as json_file:
#     json_data = json.load(json_file)
#
#     for idx, ann in enumerate(json_data['annotations']):
#         if ann['area'] not in area_dict.keys():
#             new_ann.append(ann)
#         else:
#             continue
# print(area_dict)
