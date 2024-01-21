# import os, shutil
#
# folder_list = os.listdir('D:/정제데이터')
#
#
# for folder in folder_list:
#     for (path, dir, files) in os.walk('D:/옮길리스트/1222'):
#         for file in files:
#             if folder.split(']')[0].split('[0')[-1] == file.split('.')[0]:
#                 os.rename(os.path.join(path, file), path+'/{}.csv'.format(folder))
import json
from glob import glob
from tqdm import tqdm
import os

json_list = [
 'H:/Data/04_Industrial_safety/fire/label\S3-N0885MS80003.json',
 'H:/Data/04_Industrial_safety/fire/label\S3-N0895MS80036.json',
 'H:/Data/04_Industrial_safety/fire/label\S3-N0895MS80037.json',
 'H:/Data/04_Industrial_safety/fire/label\S3-N0895MS80182.json',
 'H:/Data/04_Industrial_safety/fire/label\S3-N0895MS80183.json',
 'H:/Data/04_Industrial_safety/fire/label\S3-N0895MS80184.json',
 'H:/Data/04_Industrial_safety/fire/label\S3-N0895MS80185.json',
 'H:/Data/04_Industrial_safety/fire/label\S3-N0895MS80186.json',
 'H:/Data/04_Industrial_safety/fire/label\S3-N0895MS80187.json',
 'H:/Data/04_Industrial_safety/fire/label\S3-N0895MS80188.json',
 'H:/Data/04_Industrial_safety/fire/label\S3-N0895MS80189.json',
 'H:/Data/04_Industrial_safety/fire/label\S3-N0895MS80190.json',
 'H:/Data/04_Industrial_safety/fire/label\S3-N0895MS80191.json',
 'H:/Data/04_Industrial_safety/fire/label\S3-N0895MS80192.json',
 'H:/Data/04_Industrial_safety/fire/label\S3-N0895MS80193.json',
 'H:/Data/04_Industrial_safety/fire/label\S3-N0895MS80194.json',
 'H:/Data/04_Industrial_safety/fire/label\S3-N0895MS80195.json',
 'H:/Data/04_Industrial_safety/fire/label\S3-N0895MS80196.json',
 'H:/Data/04_Industrial_safety/fire/label\S3-N0895MS80197.json',
 'H:/Data/04_Industrial_safety/fire/label\S3-N0895MS80198.json',
 'H:/Data/04_Industrial_safety/fire/label\S3-N0897MS80029.json',
 'H:/Data/04_Industrial_safety/fire/label\S3-N1753MN01783.json',
 'H:/Data/04_Industrial_safety/fire/label\S3-N1753MN01784.json',
 'H:/Data/04_Industrial_safety/fire/label\S3-N1753MN01785.json',
 'H:/Data/04_Industrial_safety/fire/label\S3-N1753MN01786.json',
 'H:/Data/04_Industrial_safety/fire/label\S3-N1753MN01787.json',
 'H:/Data/04_Industrial_safety/fire/label\S3-N1753MN01788.json',
 'H:/Data/04_Industrial_safety/fire/label\S3-N1753MN01789.json',
 'H:/Data/04_Industrial_safety/fire/label\S3-N1753MN01790.json',
 'H:/Data/04_Industrial_safety/fire/label\S3-N1753MN01791.json',
 'H:/Data/04_Industrial_safety/fire/label\S3-N1753MN01792.json',
 'H:/Data/04_Industrial_safety/fire/label\S3-N1753MN01793.json',
 'H:/Data/04_Industrial_safety/fire/label\S3-N1753MN01794.json',
 'H:/Data/04_Industrial_safety/fire/label\S3-N1753MN01795.json',
 'H:/Data/04_Industrial_safety/fire/label\S3-N1753MN01796.json',
 'H:/Data/04_Industrial_safety/fire/label\S3-N1753MN01797.json',
 'H:/Data/04_Industrial_safety/fire/label\S3-N1753MN01798.json',
 'H:/Data/04_Industrial_safety/fire/label\S3-N1753MN01799.json',
 'H:/Data/04_Industrial_safety/fire/label\S3-N1753MN01800.json',
 'H:/Data/04_Industrial_safety/fire/label\S3-N1753MN01801.json',
 'H:/Data/04_Industrial_safety/fire/label\S3-N1753MN01802.json',
 'H:/Data/04_Industrial_safety/fire/label\S3-N1753MN01803.json',
 'H:/Data/04_Industrial_safety/fire/label\S3-N1753MN01804.json',
 'H:/Data/04_Industrial_safety/fire/label\S3-N1753MN01805.json',
 'H:/Data/04_Industrial_safety/fire/label\S3-N1753MN01806.json',
 'H:/Data/04_Industrial_safety/fire/label\S3-N1753MN01807.json',
 'H:/Data/04_Industrial_safety/fire/label\S3-N1753MN01808.json',
 'H:/Data/04_Industrial_safety/fire/label\S3-N1753MN01809.json',
 'H:/Data/04_Industrial_safety/fire/label\S3-N1753MN01810.json',
 'H:/Data/04_Industrial_safety/fire/label\S3-N1753MN01811.json',
 'H:/Data/04_Industrial_safety/fire/label\S3-N1753MN01812.json',
 'H:/Data/04_Industrial_safety/fire/label\S3-N1753MN01813.json',
 'H:/Data/04_Industrial_safety/fire/label\S3-N1753MN01814.json',
 'H:/Data/04_Industrial_safety/fire/label\S3-N1753MN01815.json',
 'H:/Data/04_Industrial_safety/fire/label\S3-N1753MN01816.json',
 'H:/Data/04_Industrial_safety/fire/label\S3-N1753MN01817.json',
 'H:/Data/04_Industrial_safety/fire/label\S3-N1753MN01818.json',
 'H:/Data/04_Industrial_safety/fire/label\S3-N1753MN01819.json',
 'H:/Data/04_Industrial_safety/fire/label\S3-N1753MN01820.json',
 'H:/Data/04_Industrial_safety/fire/label\S3-N1753MN01821.json',
 'H:/Data/04_Industrial_safety/fire/label\S3-N1753MN01822.json',
 'H:/Data/04_Industrial_safety/fire/label\S3-N1753MN01823.json',
 'H:/Data/04_Industrial_safety/fire/label\S3-N1753MN01824.json',
 'H:/Data/04_Industrial_safety/fire/label\S3-N1753MN01825.json',
 'H:/Data/04_Industrial_safety/fire/label\S3-N1753MN01826.json',
 'H:/Data/04_Industrial_safety/fire/label\S3-N1753MN01827.json',
 'H:/Data/04_Industrial_safety/fire/label\S3-N1753MN01828.json',
 'H:/Data/04_Industrial_safety/fire/label\S3-N1753MN01829.json',
 'H:/Data/04_Industrial_safety/fire/label\S3-N1753MN01830.json',
 'H:/Data/04_Industrial_safety/fire/label\S3-N1753MN01831.json',
 'H:/Data/04_Industrial_safety/fire/label\S3-N1753MN01832.json',
 'H:/Data/04_Industrial_safety/fire/label\S3-N1753MN01833.json',
 'H:/Data/04_Industrial_safety/fire/label\S3-N1753MN01834.json'
]

for j_file in tqdm(json_list):
    with open(j_file, encoding='utf-8-sig') as json_file:
        json_data = json.load(json_file)

        if json_data['image']['filename'] != j_file.split('\\')[-1].replace('.json','.jpg'):
            json_data['image']['filename'] = j_file.split('\\')[-1].replace('.json','.jpg')

    with open(j_file, 'w', encoding='utf-8') as new_json:
        json.dump(json_data, new_json, ensure_ascii=False, indent=2)