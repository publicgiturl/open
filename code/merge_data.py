from glob import glob
from tqdm import tqdm
import os, shutil, random
# not_match = []
#
# for i in tqdm(glob('/data/warehouse/data/images/**/*.jpg', recursive=True)):
#     # shutil.move(i, '/data/warehouse/data/labels/'+i.split('/')[-1])
#     if os.path.isfile('/data/warehouse/data/labels/'+i.split('/')[-1].replace('.jpg','.json')):
#         pass
#     else:
#         shutil.move(i, '/data/warehouse/data/not_match/'+i.split('/')[-1])
#         not_match.append(i.split('/')[-1])
#
# with open('/data/warehouse/data/err_list.txt', 'w') as f:
#     for i in not_match:
#         f.write(i+'\n')


for i in tqdm(glob('/data/warehouse/yolo/라벨링데이터10-07/**/*.json', recursive=True),desc='merge_json'):
    shutil.move(i, '/data/warehouse/yolo/labels/{}'.format(i.split('/')[-1]))

for i in tqdm(glob('/data/warehouse/yolo/작업환경/**/*.jpg', recursive=True),desc='merge_jpg'):
    shutil.move(i, '/data/warehouse/yolo/images/{}'.format(i.split('/')[-1]))

for i in tqdm(glob('/data/warehouse/yolo/images/*.jpg'),desc='not_match_file'):
    if not os.path.isfile(i.replace('images','labels').replace('.jpg','.json')):
        with open('/data/warehouse/yolo/not_match.txt', 'a', encoding='utf-8') as f:
            f.write(i+'\n')

# train, val, test
file_list = os.listdir('/data/warehouse/yolo/images')
sample_list = random.sample(file_list, int(len(file_list)*.2))
test_list = random.sample(sample_list, int(len(sample_list)*.5))

print('\nval_test :',len(sample_list), len(test_list))

for i in tqdm(test_list,desc='split_test'):
    if not os.path.isdir('/data/warehouse/yolo/test'):
        os.mkdir('/data/warehouse/yolo/test')
    if os.path.isfile('/data/warehouse/yolo/images/{}'.format(i)) and os.path.isfile('/data/warehouse/yolo/labels/{}'.format(i.replace('.jpg','.json'))):
        shutil.move('/data/warehouse/yolo/images/{}'.format(i), '/data/warehouse/yolo/test/{}'.format(i))
        shutil.move('/data/warehouse/yolo/labels/{}'.format(i.replace('.jpg','.json')), '/data/warehouse/yolo/test/{}'.format(i.replace('.jpg','.json')))

for i in tqdm(sample_list,desc='split_val'):
    if not os.path.isdir('/data/warehouse/yolo/val'):
        os.mkdir('/data/warehouse/yolo/val')
    if os.path.isfile('/data/warehouse/yolo/images/{}'.format(i)) and os.path.isfile('/data/warehouse/yolo/labels/{}'.format(i.replace('.jpg','.json'))):
        shutil.move('/data/warehouse/yolo/images/{}'.format(i), '/data/warehouse/yolo/val/{}'.format(i))
        shutil.move('/data/warehouse/yolo/labels/{}'.format(i.replace('.jpg','.json')), '/data/warehouse/yolo/val/{}'.format(i.replace('.jpg','.json')))
#
for i in tqdm(glob('/data/warehouse/yolo/labels/*.json'),desc='move_train'):
    if not os.path.isdir('/data/warehouse/yolo/train'):
        os.mkdir('/data/warehouse/yolo/train')
    shutil.move(i,'/data/warehouse/yolo/train/{}'.format(i.split('/')[-1]))
    shutil.move(i.replace('labels','images').replace('.json','.jpg'), '/data/warehouse/yolo/train/{}'.format(i.split('/')[-1].replace('.json','.jpg')))