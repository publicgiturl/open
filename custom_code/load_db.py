import json
import os

import pandas as pd
from tqdm import tqdm
import pymysql
import cv2
import shutil
from glob import glob
from datetime import datetime

### DF_info
host_name = '192.168.0.13'
user_name = 'land'
password = 'land2021!@'
database_name = 'landdb'

# md_engine = create_engine('mysql+mysqlconnector://{}:{}@{}:{}/{}'.format(user_name, password, host_name, 3306, database_name))
conn = pymysql.connect(host=host_name,
                       user=user_name,
                       password=password,
                       db=database_name,
                       port=3306)

# sql = """
# 	select
# 		IMG_NAME, SEQ_NO, XLOCATION, YLOCATION, WORK_ID
# 	from
# 		ai_annotation_tbl
# 	where
# 		IMG_NAME in (select IMG_NAME
# 		from ai_image_tbl
# 		where date_format(ANNO_DATE,'%y-%m-%d')>'23-08-22' and WORK_ANNOTATION='Y' and ANNO_WORKER!='ms');
# """
sql = """
select IMG_NAME, SEQ_NO, XLOCATION, YLOCATION, WORK_ID from ai_annotation_tbl
where IMG_NAME in (
select IMG_NAME from ai_image_tbl 
where WORK_ANNOTATION='Y');
"""

cursor = conn.cursor()
cursor.execute(sql)

rows = cursor.fetchall()
conn.commit()
conn.close()

df = pd.DataFrame(rows,
                  columns=['IMG_NAME', 'SEQ_NO', 'XLOCATION', 'YLOCATION', 'WORK_ID'])
new_ef = df.sort_values(by=['IMG_NAME', 'SEQ_NO'], ascending=[True, True]).reset_index()


# 이미지 그리기 함수 정의
def draw_coordinates_on_image(img, coordinates, w, h):
	landmark_dict = {}
	for idx, coord in enumerate(coordinates):
		x,y  = int(coord[0]), int(coord[1])
		if x > w:
			x = w
		elif x <0:
			x=0
		if y>h:
			y=h
		elif y<0:
			y=0
		x = int(x)
		y = int(y)
		landmark_dict[idx] = [x,y]
		cv2.circle(img, (x, y), 2, (255, 0, 0), -1)
	return landmark_dict

# 각 이미지별로 그리기
# err_list = open('/data/data/pms/0808/err_list.txt', 'w')
unique_images = df['IMG_NAME'].unique()
for img_name in tqdm(unique_images):
	img_coordinates = df[df['IMG_NAME'] == img_name][['XLOCATION', 'YLOCATION']].values

	image_path = f'/data/data/pms/0808/land/Landmarks/{img_name.split("-")[0]}/{img_name.split("-")[1]}/{img_name.split("-")[-1]}'  # 이미지 경로 설정
	img = cv2.imread(image_path)  # 이미지 로드
	h,w = img.shape[:-1]
	# 좌표값 그리기 함수 호출
	landmark_dict = draw_coordinates_on_image(img, img_coordinates, w, h)
	folder_path =f'/data/data/pms/0808/land/submit/{img_name.split("-")[0]}/{img_name.split("-")[1]}/result'
	file_name = img_name.split("-")[-1]
	if not os.path.isdir(folder_path):
		os.makedirs(folder_path, exist_ok=True)
		os.makedirs(folder_path.replace('result','labels'), exist_ok=True)
		os.makedirs(folder_path.replace('result','images'), exist_ok=True)
	# 이미지에 추가된 좌표값을 표시한 이미지를 저장하거나 표시
	# cv2.imshow('Annotated Image', img)
	cv2.imwrite(f'{folder_path}/{file_name}', img)
	shutil.copy(image_path, f"{folder_path.replace('result','images')}/{file_name}")
	with open(f"{folder_path.replace('result','labels')}/{file_name.replace('.png','.json')}", 'w') as json_file:
		json.dump(landmark_dict, json_file, indent=2, ensure_ascii=False)
	# cv2.waitKey(0)
	# cv2.destroyAllWindows()
	# cv2.imshow('img', img)
	# keycode = cv2.waitKey()
	# if keycode == ord('x'):
	# 	err_list.write(img_name + '\n')
	# elif keycode == ord('q'):
	# 	cv2.destroyAllWindows()
	# 	break
	# else:
	# 	continue
# cv2.imwrite(f'/data/data/pms/0808/land/results_2/{img_name}',img)

# err_list.close()