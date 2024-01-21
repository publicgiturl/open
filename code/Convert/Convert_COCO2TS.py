import json
import os
import os.path as osp
import numpy as np
import shutil
import random
from glob import glob
import cv2
from tqdm import tqdm

# def preprocessing_data(file_path):
#     for json_file in tqdm(glob('{}/**/*.json'.format(file_path),recursive=True),desc='split_json'):
#         with open(json_file, encoding='utf-8') as f:
#             json_data = json.load(f)
#             class_file = open('{}class.names'.format(json_file.split('label')[0]), 'w', encoding='utf-8')
#             for key in json_data['categories']:
#                 class_file.write(key['name']+'\n')
#             class_file.close()
#
#             for i in json_data['images']:
#                 file_name = json_file.split('/')[5]+'_'+i['file_name'].split('/')[-1]
#                 obj_dict = []
#                 for ann in json_data['annotations']:
#                     if ann['image_id']==i['id']:
#                         obj = dict(file_name = file_name,
#                                    id = ann['id'],
#                                    category_id=ann['category_id'],
#                                  segmentation = ann['segmentation'])
#                         obj_dict.append(obj)
#                 if not os.path.exists(json_file.split('label')[0]+'labels'):
#                     os.mkdir(json_file.split('label')[0]+'labels')
#                 with open('{0}{1}.json'.format(json_file.split('label')[0]+'labels/',file_name.split('.')[0]),'w',encoding='utf-8') as new_json:
#                     json.dump(obj_dict, new_json, ensure_ascii=False, indent=1)
#     for root, dirs, files in tqdm(os.walk(file_path),desc='change_image'):
#         for file in files:
#             if file.endswith(('.jpg','.png')):
#                 img_path = os.path.join(root,file)
#                 new_file = img_path.split('/')[5]+'_'+file
#                 os.rename(img_path, img_path.replace(file,new_file))
#
#     for i in tqdm(glob('{}/**/*.json'.format(file_path), recursive=True),desc='move_json'):
#         shutil.move(i,'/data/labels/'+i.split('/')[-1])
#     for root, dirs, files in tqdm(os.walk(file_path),desc='move_img'):
#         for file in files:
#             if file.endswith(('.jpg','.png')):
#                 shutil.move(os.path.join(root,file), '/data/images/'+file)
#
# data_list = os.listdir('/data/TS/COCO/images')
# val_list = random.sample(data_list, int(len(data_list)*.1))
#
# for i in val_list:
#     shutil.move('/data/TS/COCO/images/{}'.format(i), '/data/TS/COCO/val/{}'.format(i))
#     shutil.move('/data/TS/COCO/labels/{}'.format(i.split('.')[0]+'.json'),'/data/TS/COCO/val/{}'.format(i.split('.')[0]+'.json'))
# for i in os.listdir('/data/TS/COCO/images'):
#     shutil.move('/data/TS/COCO/images/{}'.format(i),
#                 '/data/TS/COCO/train/{}'.format(i))
#     shutil.move('/data/TS/COCO/labels/{}'.format(i.split('.')[0] + '.json'),
#                 '/data/TS/COCO/train/{}'.format(i.split('.')[0] + '.json'))

all_data = {}
for i in glob('/data/TS/COCO/train/*.json'):
    try:
        with open(i, encoding='utf-8') as j_file:
            json_data = json.load(j_file)
            all_data[json_data[0]['file_name']] = json_data
    except Exception as e:
        print(i)

with open('/data/TS/COCO/raw_train.json', 'w', encoding='utf-8') as new_file:
    json.dump(all_data, new_file, ensure_ascii=False, indent=1)

all_data = {}
for i in glob('/data/TS/COCO/val/*.json'):
    try:
        with open(i, encoding='utf-8') as j_file:
            json_data = json.load(j_file)
            all_data[json_data[0]['file_name']] = json_data
    except Exception as e:
        print(i)
with open('/data/TS/COCO/raw_val.json', 'w', encoding='utf-8') as new_file:
    json.dump(all_data, new_file, ensure_ascii=False, indent=1)


def getbbox(points):
    raw_np = np.array(points).flatten()
    res_int = raw_np.shape
    polygons = raw_np.reshape(res_int[0]//2,2)
    x,y = polygons[:,0], polygons[:,1]
    bbox = [round(x.min(),2),round(y.min(),2), round(x.max()-x.min(),2),round(y.max()-y.min(),2)]
    area = 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))
    return bbox, area

def change_class(class_path):
    with open(class_path,encoding='utf-8') as f:
        cls_dict = []
        for idx, cls in enumerate(f):
            cls_dict.append(dict(id=idx+1,name=cls.split('\n')[0]))
    return cls_dict
# print(change_class('/data/ai_dataSet/Data_Set/2DSS/ts_class.names'))
def convert_TS2COCO(input_file, out_file, image_prefix):
    with open(input_file, encoding='utf-8') as json_file:
        json_info = json.load(json_file)

        annotations = []
        images = []
        obj_count = 0
        img_num = {}
        num = 0
        for key, val in tqdm(json_info.items()):
            img_path = osp.join(image_prefix, key)
            height, width = cv2.imread(img_path).shape[:2]
            if key not in images:
                img_num[key] = num
                images.append(dict(
                    id=img_num[key],
                    file_name=key,
                    height=height,
                    width=width
                ))
                num +=1
            bboxes = []
            labels = []
            masks = []
            for obj in val:
                if obj['category_id'] not in [11,13]:
                    if obj['category_id'] == 12:
                        poly = obj['segmentation']
                        bbox, area = getbbox(poly)
                        data_anno = dict(
                                        image_id=img_num[obj['file_name']],
                                        id=obj_count,
                                        category_id=11,
                                        bbox= bbox,
                                        area=area,
                                        segmentation=poly,
                                        iscrowd=0
                                    )
                        annotations.append(data_anno)
                        obj_count += 1
                    else:
                        poly = obj['segmentation']
                        bbox, area = getbbox(poly)
                        data_anno = dict(
                            image_id=img_num[obj['file_name']],
                            id=obj_count,
                            category_id=obj['category_id'],
                            bbox=bbox,
                            area=area,
                            segmentation=poly,
                            iscrowd=0
                        )
                        annotations.append(data_anno)
                        obj_count += 1
        coco_format_json = dict(
            images=images,
            annotations=annotations,
            categories=  change_class('/data/TS/COCO/class.names')
            )

        with open(out_file, 'w', encoding='utf-8') as json_out_file:
            json.dump(coco_format_json, json_out_file, ensure_ascii=False, indent=1)



# preprocessing_data('/data/TS/COCO')

convert_TS2COCO('/data/TS/COCO/raw_train.json', '/data/TS/COCO/train.json','/data/TS/COCO/train')
convert_TS2COCO('/data/TS/COCO/raw_val.json', '/data/TS/COCO/val.json','/data/TS/COCO/val')
