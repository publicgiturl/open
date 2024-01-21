import os
from glob import glob
from tqdm import tqdm
import pandas as pd
import random
import shutil

# df = pd.read_csv('/nas/data/2023PMS/납품/세코닉스/face.csv', encoding='cp949')
# new_df = pd.read_csv('/nas/data/2023PMS/납품/에프에스솔루션/face.csv', encoding='cp949')
han_df = pd.read_csv('/nas/data/2023PMS/납품/한자연/face.csv', encoding='cp949')
file_list = []
# for i in tqdm(df['file_name']):
# 	file_name ='/'.join(i.split('/')[2:]).replace('/frame','/images/frame')
# 	folder_path = '/nas/data/2023PMS/납품/ladnmark'
# 	file_list.append(file_name)
# for i in tqdm(new_df['file_name']):
# 	file_name ='/'.join(i.split('/')[2:])
# 	folder_path = '/nas/data/2023PMS/납품/ladnmark'
# 	file_list.append(file_name)
# for i in tqdm(han_df['file_name']):
# 	file_name ='/'.join(i.split('/')[2:])
# 	folder_path = '/nas/data/2023PMS/납품/ladnmark'
# 	file_list.append(file_name)
# 	# label_name = file_name.replace('images', 'labels').replace('.png', '.json')
# 	#
# 	# os.makedirs('/nas/data/2023PMS/납품/세코닉스/Face/'+'/'.join(file_name.split('/')[:-1]),exist_ok=True)
# 	# os.makedirs('/nas/data/2023PMS/납품/세코닉스/Face/'+'/'.join(label_name.split('/')[:-1]),exist_ok=True)
# 	# shutil.copy(f'{folder_path}/{file_name}',f'/nas/data/2023PMS/납품/세코닉스/Face/{file_name}')
# 	# shutil.copy(f'{folder_path}/{label_name}', f'/nas/data/2023PMS/납품/세코닉스/Face/{label_name}')
# new_list = []
# for i in tqdm(glob('/nas/data/2023PMS/납품/ladnmark/**/images/*.png',recursive=True)):
# 	file_name = '/'.join(i.split('/')[6:])
# 	if file_name in file_list:
# 		# print(f'/nas/data/2023PMS/납품/한자연/face_result/{file_name.replace("images/","")}')
# 		os.makedirs(f'/nas/data/2023PMS/납품/한자연/face_result/{"/".join(file_name.replace("images/","").split("/")[:-1])}', exist_ok=True)
# 	# file_name
# 		shutil.copy(i.replace('images','result'), f'/nas/data/2023PMS/납품/한자연/face_result/{file_name.replace("images/","")}')
	# if file_name in file_list:
	# 	continue
	# else:
	# 	new_list.append(i)
#
#
# han = random.sample(new_list, 16400)

#
# for i in tqdm(han):
# 	label_name =i.replace('images','labels').replace('.png','.json')
# 	os.makedirs('/nas/data/2023PMS/납품/한자연/Face/'+'/'.join('/'.join(i.split('/')[6:]).split('/')[:-1]),exist_ok=True)
# 	os.makedirs('/nas/data/2023PMS/납품/한자연/Face/'+'/'.join('/'.join(label_name.split('/')[6:]).split('/')[:-1]),exist_ok=True)
# 	shutil.copy(i,f'/nas/data/2023PMS/납품/한자연/Face/{"/".join(i.split("/")[6:])}')
# 	shutil.copy(label_name, f'/nas/data/2023PMS/납품/한자연/Face/{"/".join(label_name.split("/")[6:])}')
# df = pd.DataFrame(han, columns=['file_name'])
# df.to_csv('/data/han.csv')

for i in tqdm(glob('/nas/data/2023PMS/납품/한자연/face_result/**/*.png', recursive=True)):
	break