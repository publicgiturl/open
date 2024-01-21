import json
import os
from glob import glob
from tqdm import tqdm

for json_file in tqdm(glob('E:/2021/TS/2D SS GT 학습 데이터/COCO/1) 21.10.06/**/*.json',recursive=True)):
    json_file = json_file.replace('\\','/')
    with open(json_file, encoding='utf-8') as f:
        json_data = json.load(f)
        class_file = open('{}class.names'.format(json_file.split('label')[0]), 'w', encoding='utf-8')
        for key in json_data['categories']:
            class_file.write(key['name']+'\n')
        class_file.close()

        for i in json_data['images']:

            file_name = json_file.split('/')[6]+'_'+i['file_name'].split('/')[-1]
            obj_dict = []
            for ann in json_data['annotations']:
                if ann['image_id']==i['id']:
                    obj = dict(id = ann['id'],
                               image_id = ann['image_id'],
                               category_id=ann['category_id'],
                             segmentation = ann['segmentation'])
                    obj_dict.append(obj)
            if not os.path.exists(json_file.split('label')[0]+'labels'):
                os.mkdir(json_file.split('label')[0]+'labels')
            with open('{0}{1}.json'.format(json_file.split('label')[0]+'labels/',file_name.split('.')[0]),'w',encoding='utf-8') as new_json:
                json.dump(obj_dict, new_json, ensure_ascii=False, indent=1)
for root, dirs, files in os.walk('E:/2021/TS/2D SS GT 학습 데이터/COCO/1) 21.10.06'):
    for file in files:
        if file.endswith(('.jpg','.png')):
            img_path = os.path.join(root,file).replace('\\','/')
            new_file = img_path.split('/')[6]+'_'+file
            os.rename(img_path, img_path.replace(file,new_file))