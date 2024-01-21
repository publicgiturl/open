import json
from datetime import datetime, date
from glob import glob

import numpy as np
from tqdm import tqdm


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


info = {
    "contributor": "",
    "date_created": "",
    "description": "",
    "url": "",
    "version": "",
    "year": ""
}
licenses = [{
    "name": "",
    "id": 0,
    "url": ""
}]
categories = [
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
]
images = []
annotations = []
num = 1
# #
# for img_idx, j_file in enumerate(tqdm(glob('D:/download/annotations/ind/*.json'), desc='Merge')):
#     with open(j_file, encoding='utf-8') as json_file:
#         json_data = json.load(json_file)
#         file_name = json_data['images'][0]['file_name']
#         for img in json_data['images']:
#             images.append(dict(
#                 id=img_idx + 1,
#                 width=img['width'],
#                 height=img['height'],
#                 # file_name=img['file_name'],
#                 file_name=file_name,
#                 license=0,
#                 flickr_url="",
#                 coco_url="",
#                 date_captured=0
#             ))
#         for ann in json_data['annotations']:
#
#             annotations.append(dict(
#                 id=num,
#                 image_id=img_idx + 1,
#                 # category_id=ann['category_id'],
#                 category_id=ann['category_id'],
#                 segmentation=ann['segmentation'],
#                 area=ann['area'],
#                 bbox=ann['bbox'],
#                 iscrowd=0
#             ))
#             num += 1
#
# fin_ann = dict(
#     info=info,
#     licenses=licenses,
#     categories=categories,
#     images=images,
#     annotations=annotations
# )
# with open(f'D:/download/annotations/instances_default_coco.json', 'w', encoding='utf-8') as new_json:
#     json.dump(fin_ann, new_json, ensure_ascii=False, indent=2, cls=ConvertEncoder)
