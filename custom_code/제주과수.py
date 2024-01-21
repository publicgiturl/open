import json
import os
from datetime import datetime, date
from glob import glob
import pandas as pd
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


def getbbox(points):
	x, y = np.array(points[::2]), np.array(points[1::2])
	bbox = [round(x.min(), 2), round(y.min(), 2), round(x.max() - x.min(), 2), round(y.max() - y.min(), 2)]
	area = 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))
	return bbox, area


# # 얘만 바꾸면 됨
# src = '/home/ms/Downloads/제주/20221013'
# ####################
# dst = f'{src}/submit'
# date_path = f"{src}/{src.split('/')[-1]}"
#
# os.makedirs(dst, exist_ok=True)
# os.makedirs(date_path, exist_ok=True)
# #
# for j_file in tqdm(glob(f'{src}/**/instances_default.json', recursive=True)):
# 	file_path = '/'.join(j_file.split('/')[:-1])
# 	with open(j_file, encoding='utf-8') as json_file:
# 		json_data = json.load(json_file)
#
# 		for img in json_data['images']:
# 			width = img['width']
# 			height = img['height']
# 			img_id = img['id']
# 			for ann in json_data['annotations']:
# 				if img_id == ann['image_id']:
# 					new_json = dict(
# 						info=json_data['info'],
# 						licenses=[json_data['licenses']],
# 						categories=[{'id': 0, 'name': '감귤나무', 'supercategory': ''}],
# 						images=[dict(
# 							id=1,
# 							width=width,
# 							height=height,
# 							file_name=img['file_name'],
# 							license=0,
# 							flickr_url='',
# 							coco_url='',
# 							date_captured=0
# 						)],
# 						annotations=[dict(
# 							id=1,
# 							image_id=1,
# 							category_id=0,
# 							segmentation=ann['segmentation'],
# 							area=ann['area'],
# 							bbox=ann['bbox'],
# 							iscrowd=ann['iscrowd'],
# 							attributes=ann['attributes']
# 						)]
# 					)
# 			with open(f'{dst}/{img["file_name"].split(".")[0] + ".json"}', 'w', encoding='utf-8') as new_file:
# 				json.dump(new_json, new_file, indent=2, ensure_ascii=False, cls=ConvertEncoder)
#
# for j_file in tqdm(glob(f'{dst}/**/*.json', recursive=True)):
# 	with open(j_file, encoding='utf-8') as json_file:
# 		json_data = json.load(json_file)
#
# 	file_name = json_data['images'][0]['file_name'].split('.')[0]
# 	submit_dict = dict(
# 		info=dict(
# 			direction=file_name.split('_')[1],
# 			sep=file_name.split('_')[2][1:],
# 			NI_image=dict(
# 				filename=file_name,
# 				day=datetime.strptime(str(file_name.split('_')[0]), '%Y%m%d').strftime('%Y-%m-%d')
# 			),
# 			OI_image=dict(
# 				filename="",
# 				day=""
# 			),
# 			race="",
# 			myear="",
# 			f_ratio="",
# 			new_leaf_ratio="",
# 			man_count_day="",
# 			man_count="",
# 			man_height="",
# 			man_width_avg="",
# 			chl_day="",
# 			chl_avg="",
# 			lat="",
# 			lon="",
# 			alti="",
# 			windy_avg="",
# 			windir_avg="",
# 			deg_avg="",
# 			hum_avg="",
# 			pa_avg="",
# 			rain_avg="",
# 			snow_avg="",
# 			solar_avg="",
# 			radiat_avg="",
# 			temp1_avg="",
# 			temp2_avg="",
# 			temp3_avg="",
# 			temp4_avg="",
# 			soil1_avg="",
# 			soil2_avg="",
# 			soil3_avg="",
# 			soil4_avg="",
# 			NI_image_EXIF=dict(
# 				type="",
# 				device="",
# 				resolution="",
# 				bit="",
# 				ISO=""
# 			),
# 			OI_image_EXIF=
# 			{
# 				"type": "",
# 				"device": "",
# 				"resolution": "",
# 				"bit": "",
# 				"ISO": "",
# 				"s-Alti": ""
# 			},
# 			annotations={"polygon.id": "PLG_0001",
# 					    "polygon.class": "mandarin",
# 					    "polygon.category": "감귤나무",
# 					     "polygon.points":json_data['annotations'][0]['segmentation'][0]
# 			             }
# 		)
# 	)
# 	new_folder = f'{date_path}/{file_name.split("_")[1]}/{file_name.split("_")[2]}'
# 	os.makedirs(new_folder, exist_ok=True)
# 	with open(f'{new_folder}/{j_file.split("/")[-1]}','w',encoding='utf8') as new_file:
# 		json.dump(submit_dict, new_file, ensure_ascii=False, indent=2)

# file_list = []
# for j_file in tqdm(glob('/home/ms/Downloads/제주/ori/**/*.json', recursive=True)):
# 	file_list.append(j_file.split('/')[-1])
#
# num=0
# print(len(file_list))
# print(len(set(file_list)))
# for j_file in tqdm(glob('/home/ms/Downloads/제주/submit/**/*.json', recursive=True)):
# 	file_name = j_file.split('/')[-1]
#
# 	if file_name not in file_list:
# 		num+=1
# 		# print(file_name)
# print(num)

num = 1
# df = pd.DataFrame(columns=['file_name','width','height'])
# for j_file in tqdm(glob('/home/ms/Downloads/제주/ori/**/*.json', recursive=True)):
# 	if j_file.split('/')[-1]=='instances_default.json':
# 		with open(j_file) as json_file:
# 			json_data = json.load(json_file)
#
# 			for images in json_data['images']:
# 				w = images['width']
# 				h = images['height']
# 				file_name = images['file_name'].split('.')[0]+".json"
# 				df.loc[len(df)] = [file_name, w, h]
				# if w!=4032 or h !=3024:
				# 	num+=1
					# print(w,h, images['file_name'])
# df.to_csv('/home/ms/Downloads/제주/df.csv',index=False)
# df = pd.read_csv('/home/ms/Downloads/제주/df.csv')
#
# for j_file in tqdm(glob('/home/ms/Downloads/제주/ori/**/*.json', recursive=True)):
# 	file_name = j_file.split('/')[-1]
#
# 	# if file_name!='instances_default.json':
# 	if file_name not in list(df['file_name']):
# 		# 28 , 30
# 		if file_name =='instances_default.json':
# 			continue
# 		else:
# 			a,b,c,d,e = file_name.split('_')[0],file_name.split('_')[1],file_name.split('_')[2],file_name.split('_')[3],file_name.split('_')[4]
# 			while e.startswith('0'):
# 				e = e[1:]
# 				if len(e)==8:
# 					break
#
# 			file_name = f'{a}_{b}_{c}_{d}_{e}'
# 			if file_name not in list(df['file_name']):
# 				continue
#
# 	#20221020_N_T1715_NI_00217
# 	with open(j_file) as json_file:
# 		json_data = json.load(json_file)
#
# 	width = df.loc[df['file_name']==file_name,'width'].values[0]
# 	height = df.loc[df['file_name']==file_name,'height'].values[0]
# 	coord = json_data['annotations']['polygon.points']
# 	x,y = coord[::2], coord[1::2]
#
# 	new_x = [x_val / 1920 * width for x_val in x]
# 	new_y = [y_val / 1080 * height for y_val in y]
#
# 	arr =np.array(list(zip(new_x, new_y)))
# 	json_data['annotations']['polygon.points'] = arr.flatten().tolist()
#
# 	new_folder =f'/home/ms/Downloads/제주/last/{file_name.split("_")[0]}/submit/{file_name.split("_")[1]}/{file_name.split("_")[2]}'
# 	os.makedirs(new_folder,exist_ok=True)
# 	if len(file_name)!=30:
# 		idx = 30-len(file_name)
# 		a,b,c,d,e = file_name.split('_')[0],file_name.split('_')[1],file_name.split('_')[2],file_name.split('_')[3],file_name.split('_')[4]
# 		file_name = f'{a}_{b}_{c}_{d}_{"0"*idx}{e}'
# 	with open(f'{new_folder}/{file_name}', 'w') as new_json:
# 		json.dump(json_data, new_json, ensure_ascii=False, indent=2, cls=ConvertEncoder)

anno = []

# with open('/home/ms/Downloads/ttt/annotations/instances_default.json') as jeju_json:
# 	jeju_data = json.load(jeju_json)
#
# 	for img in tqdm(jeju_data['images']):
# 		file_name = img['file_name'].split('.')[0] + '.json'
# 		for j_file in glob('/home/ms/Downloads/제주/last/20221018/**/*.json', recursive=True):
# 			if file_name == j_file.split('/')[-1]:
# 				with open(j_file) as ann_file:
# 					json_data = json.load(ann_file)
# 					new_coord = json_data['annotations']['polygon.points']
# 					bbox, area = getbbox(new_coord)
# 					anno.append(dict(
# 						id=num,
# 						image_id=img['id'],
# 						category_id=1,
# 						segmentation=[new_coord],
# 						bbox=bbox,
# 						area=area,
# 						iscrowd=0
# 					))
# 					num+=1
#
# 	jeju_data['annotations']=anno
# 	jeju_data['categories'] = [{"id": 1, "name": "tree", "supercategory": ""}]
# 	with open('/home/ms/Downloads/ttt/instances_default.json','w', encoding='utf-8') as new_file:
# 		json.dump(jeju_data,new_file, ensure_ascii=False, cls=ConvertEncoder)

file_list = []
for i in tqdm(glob('/home/ms/Downloads/제주/last/**/*.json',recursive=True)):
	file_list.append(i.split('/')[-1])
# 34007
for i in tqdm(glob('/home/ms/Downloads/제주/ori/**/*.json',recursive=True)):
	if i.split('/')[-1] not in file_list:
		print(i)