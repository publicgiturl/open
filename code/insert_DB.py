# import os, shutil
# import pymysql
# folder_list = ['20210114','20210121']
# # for i in folder_list:
#     # for (path, dir, files) in os.walk('Z:/origin_image/{}'.format(i)): # 경로 설정
# for path, dir, files in os.walk('Z:/origin_image/20201208'):
#     for filename in files:
#         if filename.endswith('.jpg'):
#             conn = pymysql.connect(host = '172.16.0.20', user = 'humanf', password = '1234', port = 3307, database = 'unidentify') ### 20서버 DB접속
#             # conn = pymysql.connect(host = '172.16.0.5', user = 'uniden', password = 'uniden2020!@', port = 3306, database = 'indentify')  ### 5서버 DB접속
#             curs = conn.cursor()
#
#             sql = 'replace into imagetbl (Img_Name, Img_Path) values (%s, %s)'
#             curs.execute(sql, (filename, path.split('\\')[-1]))
#             conn.commit()
#             conn.close()

import os, shutil

import pandas as pd
import pymysql
from tqdm import tqdm
import json
from functools import reduce
from glob import glob
import numpy as np
#for file_name in glob('E:/화재자료/1. Training/라벨링데이터/*.json'):
# for file_name in tqdm(glob('E:/aaa/label/*.json')):
#     try :
#         with open(file_name, encoding='utf-8') as json_file:
#             json_data = json.load(json_file)
#             img = json_data['image']
#             ann = json_data['annotations']
#             count = 1
#             conn = pymysql.connect(host='192.168.0.22', user='isafe', password='isafe2020!@', port=3306,
#                                    database='industrial_safety')  ### 20서버 DB접속
#             curs = conn.cursor()
#             # print(img['date'])
#             # data_img = pd.DataFrame(
#             #     {'IMG_NAME': img['filename'], 'WORK_ANNOTATION': 'N', 'ANNO_WORKER': 'NULL',
#             #      'ANNO_DATE': img['date'], 'WORK_INSPECTION': 'N', 'INSP_WORKER': 'NULL', 'INSP_DATE': '2021-05-04',
#             #      'WORK_EXCEPTION': 'N', 'EXCE_WORKER': 'NULL', 'EXCE_DATE': '2021-05-04', 'WORK_FINAL': 'N',
#             #      'FIN_WORKER': 'NULL', 'FIN_DATE': '2021-05-04', 'CNT': 0, 'COMPLETE_YN': 'N', 'COMMENT': 'NULL',
#             #      'DATE': img['date'], 'H_DPI': img['H_DPI'], 'LOCATION': img['location'], 'V_DPI': img['V_DPI'],
#             #      'BIT': '24', 'RESOLUTION': img['resolution']})
#             # data = (img['filename'], i+1, img['date'], img['filename'][:11]+'00001', img['H_DPI'], img['V_DPI'], img['location'], 'box', j['middle classification'], j['class'], j['box'], j['flags'], j['data ID'])
#             # sql = "update ai_image_tbl (IMG_NAME, WORK_ANNOTATION, ANNO_WORKER, ANNO_DATE, WORK_INSPECTION, INSP_WORKER, INSP_DATE, WORK_EXCEPTION, EXCE_WORKER, EXCE_DATE, WORK_FINAL, FIN_WORKER, FIN_DATE, CNT, COMPLETE_YN, COMMENT, DATE, H_DPI, LOCATION, V_DPI, BIT, RESOLUTION) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
#
#
#             sql = "UPDATE ai_image_tbl SET DATE=%s where IMG_NAME=%s;"
#             img_data = (img['date'], img['filename'])
#             curs.execute(sql, img_data)
#             conn.commit()
#
#             for j in ann:
#                 if 'box' in j:
#                     coor = [",".join([str(x) for x in j['box']])]
#                     # data = pd.DataFrame({'SEQ_NO':count, 'IMG_NAME':img['filename'], 'DATE_':img['date'], 'PATH_':img['filename'][:11] + '00001', 'H_DPI':img['H_DPI'], 'V_DPI':img['V_DPI'], 'LOCATION':img['location'], 'CLASS_TYPE':'box', 'Middle_classification':j['middle classification'], 'CLASS_ID':j['class'], 'COORDINATES':j['box'], 'FLAGS':j['flags'], 'DATA_ID':j['data ID']})
#                     data_box = pd.DataFrame({'SEQ_NO':count, 'IMG_NAME':img['filename'], 'CLASSIFICATION':j['data ID'], 'DIVISION':j['middle classification'], 'GATEGORY_NAME':'','CLASS_TYPE':'box', 'CLASS_ID':j['class'], 'CLASS_NAME':'','COORDINATES':coor, 'FLAGS':j['flags']})
#                     sql = "INSERT INTO tmp_json (SEQ_NO, IMG_NAME, CLASSIFICATION, DIVISION, GATEGORY_NAME, CLASS_TYPE, CLASS_ID, CLASS_NAME, COORDINATES, FLAGS) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
#                     bb_box = [tuple(x) for x in data_box.values]
#                     # sql = "insert into ai_annotation_tbl set COORDINATES=coor, DIVISION=j['middle classification'], CLASS_ID=j['class'], CLASS_TYPE='box' where IMG_NAME"
#                     curs.executemany(sql, bb_box)
#                     count +=1
#                     conn.commit()
#
#                 elif 'polygon' in j:
#                     # coor = ()
#
#                     # coor = [",".join([str(x) for x in j['polygon']])]
#                     coor = [",".join([str(x) for x in j['polygon']])]
#
#                     # data = pd.DataFrame({'SEQ_NO':count, 'IMG_NAME':img['filename'], 'DATE_':img['date'], 'PATH_':img['filename'][:11] + '00001', 'H_DPI':img['H_DPI'], 'V_DPI':img['V_DPI'], 'LOCATION':img['location'], 'CLASS_TYPE':'box', 'Middle_classification':j['middle classification'], 'CLASS_ID':j['class'], 'COORDINATES':j['box'], 'FLAGS':j['flags'], 'DATA_ID':j['data ID']})
#                     data_ann = pd.DataFrame({'SEQ_NO':count, 'IMG_NAME':img['filename'], 'CLASSIFICATION':j['data ID'], 'DIVISION':j['middle classification'], 'GATEGORY_NAME':'','CLASS_TYPE':'polygon', 'CLASS_ID':j['class'], 'CLASS_NAME':'','COORDINATES':coor, 'FLAGS':j['flags']})
#                     sql = "INSERT INTO tmp_json (SEQ_NO, IMG_NAME, CLASSIFICATION, DIVISION, GATEGORY_NAME, CLASS_TYPE, CLASS_ID, CLASS_NAME, COORDINATES, FLAGS) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
#                     # sql = "INSERT IGNORE INTO ai_annotation_tbl (SEQ_NO, IMG_NAME, CLASSIFICATION, DIVISION, GATEGORY_NAME, CLASS_TYPE, CLASS_ID, CLASS_NAME, COORDINATES, FLAGS) VALUES (count, img['filename'], j['data ID'], j['middle classification'], 'NULL', 'polygon', j['class'], 'NULL', j['polygon'], j['flags']);"
#                     # print(str(data_ann['COORDINATES']))
#                     # print(coor1)
#                     poly = [tuple(x) for x in data_ann.values]
#                     curs.executemany(sql, poly)
#                     count += 1
#                     conn.commit()
#
#             conn.close()
#     except Exception as e:
#         conn.commit()
#         conn.close()
#         json_file.close()
#         print(e)
#         print(file_name)
#         pass

### 상품 데이터 DB작업
# pro_csv = pd.read_csv('E:/product_final.csv', encoding='utf-8', index_col=0)
# pro_db = pro_csv.copy()
# # print(pro_db.loc[0])
# pro_db.drop(['file_path', 'img_size'], axis=1, inplace=True)
# pro_db.rename(columns={'file_name':'IMG_NAME', 'type':'TYPE_','class':'CLASS', 'ann':'COORDINATES'}, inplace=True)
# # print(pro_db.loc[0])
conn = pymysql.connect(host='127.0.0.1', user='root', password='1234', port=3306, database='humanf')
curs = conn.cursor()
#
# sql = "INSERT ignore INTO ai_data_annotation_tbl (IMG_NAME, TYPE_, CLASS, COORDINATES) VALUES (%s, %s, %s, %s);"
sql = "select IMG_PATH from ai_data_img_tbl;"
# data = [tuple(x) for x in pro_db.values]
# print(sql)
curs.execute(sql)
result_list = curs.fetchall()
f = open('E:/name_.txt', 'a', encoding='utf-8')
for i in result_list:
    f.write('/'.join(i[0].split('/')[:-1])+'/'+'\n')
f.close()
conn.commit()
conn.close()
with open('E:/name_.txt') as f:
    for i in f:
        print(i)


### 랜드마크 데이터 DB작업
# landmark_db = pd.read_csv('G:/landmark/landmark_final.csv', encoding='utf-8', index_col=0)
#
# # print(landmark_db.loc[0])
# # landmark_db.drop(['type', 'class','ann','instance'], axis=1, inplace=True)
# landmark_db.drop(['file_path', 'img_size'], axis=1, inplace=True)
# landmark_db.rename(columns={'file_name':'IMG_NAME', 'type':'TYPE_','class':'CLASS', 'ann':'COORDINATES', 'instance':'INSTANCE'}, inplace=True)
# # landmark_db.rename(columns={'file_name':'IMG_NAME', 'file_path':'IMG_PATH','img_size':'RESOLUTION'}, inplace=True)
# # print(landmark_db.loc[0])
# conn = pymysql.connect(host='127.0.0.1', user='root', password='1234', port=3306, database='humanf')
# curs = conn.cursor()
#
# # sql = "INSERT INTO temp_image_tbl (IMG_PATH, IMG_NAME, RESOLUTION) VALUES (%s, %s, %s);"
# sql = "INSERT INTO temp_annotation_tbl (IMG_NAME, TYPE_, CLASS, COORDINATES, INSTANCE) VALUES (%s, %s, %s, %s, %s);"
# data = [tuple(x) for x in landmark_db.values]
# # # # print(sql)
# curs.executemany(sql, data)
# #
# conn.commit()
# conn.close()

ruins_db = pd.read_csv('E:/con_df_final.csv', encoding='utf-8', index_col=0)
# ruins_db.drop(['file_path', 'img_size'], axis=1, inplace=True)
# ruins_db.drop(['SEQ_NO', 'location', 'type', 'Instance', 'ann'], axis=1, inplace=True)
# print(ruins_db.columns)
# ruins_db.fillna('NULL', inplace=True)
# # ruins_db.rename(columns={'file_path':'IMG_PATH', 'file_name':'IMG_NAME', 'img_size':'RESOLUTION'}, inplace=True)
# # print(ruins_db.columns)
# ruins_db.rename(columns={'file_name':'IMG_NAME', 'type':'TYPE_', 'Instance':'INSTANCE', 'ann':'COORDINATES', 'location':'LOCATION'}, inplace=True)
# ruins_db = ruins_db[['IMG_NAME', 'SEQ_NO', 'TYPE_', 'COORDINATES', 'INSTANCE','LOCATION']]
conn = pymysql.connect(host='127.0.0.1', user='root', password='1234', port=3306, database='humanf')
curs = conn.cursor()
# sql = "insert ignore into temp_annotation_tbl (IMG_NAME, SEQ_NO, TYPE_, COORDINATES, INSTANCE, LOCATION) values (%s, %s, %s, %s, %s, %s);"
# sql = "insert ignore into temp_image_tbl (IMG_PATH, IMG_NAME, RESOLUTION) values (%s, %s, %s);"
sql = "insert into temp (file_path, file_name, SEQ_NO, img_size, location, type, Instance, ann) values (%s, %s, %s, %s, %s, %s, %s, %s);"
data = [tuple(x) for x in ruins_db.values]

curs.executemany(sql, data)
conn.commit()
conn.close()