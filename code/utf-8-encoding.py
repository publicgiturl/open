import json
from glob import glob
import os
from tqdm import tqdm

# for (path, dir, files) in os.walk('C:/Users/HumanForest/Desktop/화재 발생 예측 데이터/무관씬'):
#     for fileName in files:
#         # if fileName.end
#         try:
#             with open(os.path.join(path, fileName), encoding='utf-8-sig') as json_file:
#                 jsonData = json.load(json_file)
#                 jsonData['image']['copyrighter'] = '미디어그룹사람과숲(컨)'
#                 for i in range(len(jsonData['annotations'])):
#                     jsonData['annotations'][i]['middle classification'] = '03'
#
#
#                 with open(os.path.join('C:/Users/HumanForest/Desktop/화재 발생 예측 데이터/무관씬', fileName), 'w', encoding='utf-8') as json_change:
#                     json.dump(jsonData, json_change, indent=2, ensure_ascii=False)
#         except Exception as ex:
#             print(ex)
#             pass


fire_test = []
with open('C:/Users/HF/Desktop/산업안전/fire.txt', encoding='utf-8') as f:
    for i in f:
        fire_test.append(i.split('\n')[0].split('\t'))

fire_dict = {}
for i in fire_test[1:]:
    fire_dict[i[0][:10]] = i[1]

for i in tqdm(glob('E:/새 폴더/val/**/*.json', recursive=True)):
    with open(i, encoding='utf-8-sig') as json_file:
        file_name = i.split('\\')[-1][:10]
        json_data = json.load(json_file)

        if file_name in fire_dict.keys():
           json_data['image']['date'] = fire_dict[file_name].replace('-','')

        with open(i, 'w', encoding='utf-8') as json_change:
            json.dump(json_data, json_change, indent=2, ensure_ascii=False)