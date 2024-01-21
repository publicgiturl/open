import pandas as pd
import os
from glob import glob
from tqdm import tqdm
import json
from datetime import datetime
import shutil

'''
6_01_1/20230706_015529/frame5.png 일 때
excel 기준 order = 6 seat_number = 1 (정배열), date = 20230706 
target1,target2는 피험자의 연령대,성별
'''
# 전달받은 엑셀을 커스텀해서 매칭할 수 있게 변환
origin_db = pd.read_excel('/nas/data/2023PMS/기타/Detections_class_setting.xlsx')
origin_db.fillna(0, inplace=True)


def json_to_yolo(bbox, img_width, img_height):
	x, y, w, h = bbox
	center_x = (x + w / 2) / img_width
	center_y = (y + h / 2) / img_height
	normal_w = w / img_width
	normal_h = h / img_height
	return [center_x, center_y, normal_w, normal_h]


def change_date(dates):
	return pd.to_datetime(dates).strftime('%Y%m%d')


origin_db['date'] = origin_db['date'].apply(change_date).astype(int)

com_list = ['2023pms_od_0',
            '2023pms_od_1',
            '2023pms_od_2',
            '2023pms_od_3',
            '2023pms_od_4',
            '2023pms_od_5',
            '2023pms_od_6',
            '2023pms_od_7',
            '2023pms_od_8',
            '2023pms_od_9',
            '2023pms_od_10',
            '2023pms_od_11',
            '2023pms_od_12',
            '2023pms_od_13',
            '2023pms_od_14',
            '2023pms_od_15',
            '2023pms_od_16',
            '2023pms_od_17',
            '2023pms_od_18',
            '2023pms_od_19',
            '2023pms_od_20',
            '2023pms_od_21',
            '2023pms_od_22',
            '2023pms_od_23',
            '2023pms_od_24',
            '2023pms_od_25',
            '2023pms_od_26',
            '2023pms_od_27',
            '2023pms_od_28',
            '2023pms_od_29',
            '2023pms_od_30',
            '2023pms_od_31',
            '2023pms_od_32',
            '2023pms_od_33',
            '2023pms_od_34',
            '2023pms_od_35',
            '2023pms_od_36',
            '2023pms_od_37',
            '2023pms_od_38',
            '2023pms_od_39',
            '2023pms_od_40',
            '2023pms_od_41',
            '2023pms_od_42',
            '2023pms_od_43',
            '2023pms_od_44',
            '2023pms_od_80',
            '2023pms_od_231',
            '2023pms_od_241',
            '2023pms_od_260',
            '2023pms_od_263',
            '2023pms_od_264',
            '2023pms_od_265',
            '2023pms_od_266',
            '2023pms_od_267',
            '2023pms_od_268',
            '2023pms_od_269',
            '2023pms_od_270',
            '2023pms_od_280',
            '2023pms_od_281',
            '2023pms_od_282']


# seat_order가 1이면 엑셀의 seat_number 1이 운전자 / 2일 경우 seat_number 2가 운전자
def people_class_identify(order, seat_order, dates, db):
	driver_age, driver_gender, passenger_age, passenger_gender = "", "", "", ""
	selection = db[(db['date'] == int(dates)) & (db['order'] == int(order))]

	if selection[selection['seat_number'] == 1]['나이'].values[0] < 40:
		driver_age ='young'
	elif selection[selection['seat_number'] == 1]['나이'].values[0] < 60:
		driver_age = 'middle_aged'
	else:
		driver_age = 'old_aged'

	if selection[selection['seat_number'] == 2]['나이'].values[0]< 40:
		passenger_age = 'young'
	elif selection[selection['seat_number'] == 2]['나이'].values[0]< 60:
		passenger_age = 'middle_aged'
	else:
		passenger_age = 'old_aged'

	if int(seat_order) == 1:
		driver_gender = 'man' if selection[selection['seat_number'] == 1]['성별'].values[0]=='남' else 'woman'
		passenger_gender = 'man' if selection[selection['seat_number'] == 2]['성별'].values[0]=='남' else 'woman'

	if int(seat_order) == 2:
		passenger_gender = 'man' if selection[selection['seat_number'] == 1]['성별'].values[0]=='남' else 'woman'
		driver_gender = 'man' if selection[selection['seat_number'] == 2]['성별'].values[0]=='남' else 'woman'

	driver = '_'.join([driver_age, driver_gender])
	passenger = '_'.join([passenger_age, passenger_gender])
	return driver, passenger


# 납품용 클래스 아이디
'''
categories_id 1 -> 0~5 / categories_id 2 -> 6
categories_id 3 -> 7,8 / categories_id 4 -> 9
categories_id 5 -> 10 / categories_id 6 -> 11
categories_id 7 -> 12 / categories_id 9 -> 14
categories_id 8 -> 13
dict()
'''

driver_dict = dict(young_man=0, young_woman=1, middle_aged_man=2, middle_aged_woman=3, old_aged_man=4, old_aged_woman=5)
categories_convert = {2: 6, 4: 9, 5: 10, 6: 11, 7: 12, 9: 14, 8: 13}  # 바로 변환 시킬수있는 목록들

json_folder = glob('/nas/data/2023PMS/od_검수완료/*.json')
for json_path in tqdm(json_folder):
	if f"2023pms_{json_path.split('/')[-1].split('.json')[0]}" in com_list:
		with open(json_path) as json_file:
			json_data = json.load(json_file)
			for img_info in json_data['images']:
				order, _, seat_order = img_info['file_name'].split('/')[0].split('_')  # seat_order는 정배열일 때 1 / 역배열일 때 2
				dates, _ = img_info['file_name'].split('/')[1].split('_')
				txt_name = img_info['file_name'].replace('.png', '.txt')  # 변환될 파일이름
				img_width, img_height = img_info['width'], img_info['height']
				img_id = img_info['id']
				anntations_dict = dict()  # image_id에 맞는 annotations 가져오기
				new_txt_list = []  # txt file에 들어갈 category, ord 값
				n = 0  # 변환 전/후 오브젝트 개수 확인
				for ann_info in json_data['annotations']:
					if img_id == ann_info['image_id']:
						if ann_info['category_id'] not in anntations_dict.keys():
							anntations_dict[ann_info['category_id']] = []
						anntations_dict[ann_info['category_id']].append(ann_info)
						n += 1
				if len(anntations_dict[1]) == 2:
					if anntations_dict[1][0]['bbox'][0] > anntations_dict[1][1]['bbox'][0]:
						driver, passenger = people_class_identify(order, seat_order, dates, origin_db)
						new_txt_list.append(
							[driver_dict[driver], *json_to_yolo(anntations_dict[1][0]['bbox'], img_width, img_height)])
						new_txt_list.append(
							[driver_dict[passenger], *json_to_yolo(anntations_dict[1][1]['bbox'], img_width, img_height)])
					else:
						driver, passenger = people_class_identify(order, seat_order, dates, origin_db)
						new_txt_list.append(
							[driver_dict[passenger], *json_to_yolo(anntations_dict[1][0]['bbox'], img_width, img_height)])
						new_txt_list.append(
							[driver_dict[driver], *json_to_yolo(anntations_dict[1][1]['bbox'], img_width, img_height)])
				elif len(anntations_dict[1]) == 1:  # 한 명만 디텍 되었을 때는 이미지 크기를 기준으로 좌/우에 위치해있는지 확인 후 클래스 부여
					driver, passenger = people_class_identify(order, seat_order, dates, origin_db)
					if anntations_dict[1][0]['bbox'][0] < (img_width / 2):
						new_txt_list.append(
							[driver_dict[passenger], *json_to_yolo(anntations_dict[1][0]['bbox'], img_width, img_height)])
					else:
						new_txt_list.append(
							[driver_dict[driver], *json_to_yolo(anntations_dict[1][0]['bbox'], img_width, img_height)])
				for dict_idx in anntations_dict.keys():
					for cnt in range(len(anntations_dict[dict_idx])):
						if dict_idx == 1:  # 사람은 위에서 처리 (중복방지)
							continue
						pre_category_id = anntations_dict[dict_idx][cnt]['category_id']
						if pre_category_id in categories_convert.keys():
							new_category_id = categories_convert[pre_category_id]
						if pre_category_id == 3 and anntations_dict[dict_idx][cnt]['attributes'][
							'occluded']:  # 뜬 눈 감은 눈 처리 occluded : True 이면 감은 눈
							new_category_id = 8
						if pre_category_id == 3 and anntations_dict[dict_idx][cnt]['attributes']['occluded'] == False:
							new_category_id = 7
						new_txt_list.append(
							[new_category_id, *json_to_yolo(anntations_dict[dict_idx][cnt]['bbox'], img_width, img_height)])
				labels_path = txt_name.replace('frame', 'labels/frame')
				pngs_path = img_info['file_name'].replace('frame', 'images/frame')
				if not os.path.exists(
						f'/data/save_900/{os.path.split(labels_path)[0]}'):
					os.makedirs(f'/data/save_900/{os.path.split(labels_path)[0]}',
					            exist_ok=True)
				with open(f'/data/save_900/{labels_path}', 'w') as txt_file:
					for new_txt_line in new_txt_list:
						line = ' '.join(map(str, new_txt_line)) + '\n'
						txt_file.write(line)

				if not os.path.exists(
						f'/data/save_900/{os.path.split(pngs_path)[0]}'):
					os.makedirs(f'/data/save_900/{os.path.split(pngs_path)[0]}',
					            exist_ok=True)
				try :
					shutil.copy(f'/nas/data/2023PMS/ObjectDetections/{img_info["file_name"]}',
					            f'/data/save_900/{pngs_path}')
				except FileNotFoundError as not_found:
					shutil.copy(f'/nas/data/2023PMS/2차수령/ObjectDetections/{img_info["file_name"]}',
					            f'/data/save_900/{pngs_path}')
