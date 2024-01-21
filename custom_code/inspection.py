import json
from glob import glob
from tqdm import tqdm
import shutil

# for j_file in tqdm(glob('/nas/data/2023PMS/0905_keypoint/**/*.json',recursive=True)):
#     new_name = j_file.split('/')[-3]
#     shutil.move(j_file, f'/nas/data/2023PMS/0901_keypoint/jsons/{new_name}.json')

# 라벨링 vis코드가 하나의 값으로만 된 것
vis_checklist = open('/data/data/pms/keypoint/vis_check_list_1004.txt','w', encoding='utf-8')
# 라벨링 개수가 1개이거나 3개이상
obj_check_list = open('/data/data/pms/keypoint/obj_check_list_1004.txt','w', encoding='utf-8')
# 라벨링이 안되어 있는 거
zero_img_list = open('/data/data/pms/keypoint/zero_check_list_1004.txt','w', encoding='utf-8')
#ann값에 img_id가 몇개 있는지 (2개 이상 혹은 1개이하 인것 체크)
imgid_list = dict()

for j_file in tqdm(glob(f'/nas/data/2023PMS/aa/**/*.json',recursive=True)):
    json_name = j_file.split('/')[-3]+'.json'
    vis = False
    obj = False
    with open(j_file) as json_file:
        json_data = json.load(json_file)
        for images in json_data['images']:
            img_id = images['id']
            imgid_list[img_id] = dict(file_name = images['file_name'], cnt=0)

        for ann in json_data['annotations']:
            image_id = ann['image_id']
            if image_id in imgid_list.keys():
                imgid_list[image_id]['cnt'] += 1

            v_values = ann['keypoints'][2::3]

            if len(set(v_values)) <= 1 and set(v_values) !=2:
                vis = True
                vis_checklist.write(f"{json_name} : {imgid_list[image_id]['file_name']}\n")

    notsecond = []
    for ids, cnt in imgid_list.items():
        if cnt['cnt'] == 0:
            zero_img_list.write(f"{json_name} : {cnt['file_name']}\n")
        elif cnt['cnt'] != 2:
            notsecond.append(ids-1)
    if notsecond:
        obj = True
        obj_check_list.write(str({json_name:sorted(notsecond)})+'\n')

    if vis is False and obj is False:
        # print(j_file)
        shutil.move(j_file, f'/data/key_검수완료/{json_name}')
    else:
        shutil.move(j_file, f'/data/key_err/{json_name}')

vis_checklist.close()
obj_check_list.close()
zero_img_list.close()

