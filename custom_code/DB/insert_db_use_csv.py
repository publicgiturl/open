import gc

import pandas as pd
import numpy as np
from tqdm import tqdm
import pymysql
from glob import glob
import json
from sqlalchemy import create_engine

# host_name = '192.168.0.28'
# user_name ='haer'
# password = 'haer'
# database_name = 'onss_ai'
#
# md_engine = create_engine('mysql+mysqlconnector://{}:{}@{}:{}/{}'.format(user_name, password, host_name, 3306, database_name))
# #
# for csv_file in tqdm(glob('F:/2022/Guide/db/ts_ss_db_annotation/*.csv')):
#     conn = md_engine.connect()
#     # df = pd.read_csv('F:/2022/Guide/db/ts_ss_db_annotation/ts_ss_db_1000.csv', low_memory=False)
#     df = pd.read_csv(csv_file, low_memory=False)
#     df.to_sql('ai_annotation_tbl', con=md_engine, if_exists='append', chunksize=10000, index=False, method='multi')
#     conn.close()


### have to pip install mysql-connector before install sqlalchemy

### insert_DF
host_name = '192.168.100.53'
user_name ='haer'
password = 'haer'
database_name = 'onss_ai'

md_engine = create_engine('mysql+mysqlconnector://{}:{}@{}:{}/{}'.format(user_name, password, host_name, 3306, database_name))

### insert_json
# conn=pymysql.connect(host='192.168.0.28', user='haer',password='haer', db='onss_ai', charset='utf8')
# sql1 = "insert INTO ai_image_tbl(IMG_NAME,IMG_PATH,IMG_WIDTH,IMG_HEIGHT) VALUES (%s,%s,%s,%s);"
# sql2 = "insert INTO ai_annotation_tbl(IMG_NAME,OBJ_IDX,db_code,ANNO_TYPE,BOX_X_MIN,BOX_Y_MIN,BOX_X_MAX,BOX_Y_MAX, POLY_XCNTS, POLY_YCNTS) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
# cur=conn.cursor()
print("annotation insert start")

json_list =glob('H:/Data/07_warehouse/label/*.json')

df_img = pd.DataFrame(columns=['IMG_NAME','IMG_PATH','IMG_WIDTH','IMG_HEIGHT','LOCATION'])
df_ann = pd.DataFrame(columns=['IMG_NAME','OBJ_IDX','CLASS_CODE','ANNO_TYPE','BOX_X_MIN','BOX_Y_MIN','BOX_X_MAX','BOX_Y_MAX', 'POLY_XCNTS', 'POLY_YCNTS'])
# df = pd.read_csv('F:/2022/air_file.csv', index_col=False)
class_dict ={'WO-01':44, 'WO-02':44, 'WO-03':61,'WO-04':53,'WO-05':129,'WO-06':130,'WO-07':131,'SO-01':133,'WO-08':132,'SO-02':134,'SO-04':46,
             'SO-06':135,'SO-08':136,'SO-09':137,'SO-10':137,'SO-12':88,'SO-03':45}
for idx, j_file in enumerate(tqdm(json_list)):

    with open(j_file, encoding='utf-8')as json_file:
        json_data= json.load(json_file)
        img_name = j_file.split('\\')[-1].replace('.json','.jpg')
        img_path = '07_warehouse/images'
        width, height = json_data["Raw data Info."]['resolution'][0],json_data["Raw data Info."]['resolution'][1]
        location = json_data['Raw data Info.']['location_ID']
        df_img.loc[len(df_img)] = [img_name, img_path, width, height, location]
        # dummy_image.append([img_name,img_path, width,height])

        num = 1
        for anno_data in json_data['Learning data info.']['annotation']:
            obj_idx = num

            if anno_data['class_id'] not in class_dict.keys():
                continue
            else :
                db_code = class_dict[anno_data['class_id']]

            if anno_data['type'] == 'box':
                anno = 'bbox'
                xmin = anno_data["coord"][0]
                ymin = anno_data["coord"][1]
                xmax = anno_data["coord"][2]+xmin
                ymax = anno_data["coord"][3]+ymin
                poly_x = None
                poly_y = None
            elif anno_data['type'] == 'polygon':
                anno = 'polygon'
                try:
                    points = np.array(anno_data['coord'], np.int32)
                except Exception as e:
                    print(e)
                    print(j_file)
                    continue
                poly_x = points[:, 0].tolist()
                poly_y = points[:, 1].tolist()
                xmin = min(poly_x)
                ymin = min(poly_y)
                xmax = max(poly_x)
                ymax = max(poly_y)
            else:
                continue

            num+=1

            df_ann.loc[len(df_ann)] = [img_name, obj_idx, db_code, anno, xmin, ymin, xmax, ymax, poly_x, poly_y]

    if idx % 1000 == 0:
        conn = md_engine.connect()
        df_img.to_sql('ai_image_tbl', con=md_engine, if_exists='append', chunksize=10000, index=False, method='multi')
        # df_ann.to_sql('ai_annotation_tbl', con=md_engine, if_exists='append', chunksize=10000, index=False, method='multi')
        df_ann.to_csv(f'F:/2022/Guide/db/warehouse_db_annotation/warehouse_db_{idx}.csv', encoding='utf-8', index=False)
        conn.close()
        # df.to_csv(f'F:/2022/Guide/db/ts_ss_db_annotation/ts_ss_db_{idx}.csv', encoding='utf-8', index=False)
        del df_img
        del df_ann
        gc.collect()
        df_img = pd.DataFrame(columns=['IMG_NAME','IMG_PATH','IMG_WIDTH','IMG_HEIGHT','LOCATION'])
        df_ann = pd.DataFrame(columns=['IMG_NAME','OBJ_IDX','CLASS_CODE','ANNO_TYPE','BOX_X_MIN','BOX_Y_MIN','BOX_X_MAX','BOX_Y_MAX', 'POLY_XCNTS', 'POLY_YCNTS'])

#         try:
#             # cur.executemany(sql1, dummy_image)
#             cur.executemany(sql2, dummy_list)
#             # del dummy_image
#             del dummy_list
#             # dummy_image=[]
#             dummy_list =[]
#             conn.commit()
#         except Exception as e:
#             print(e)
#             print(dummy_list)
#             # del dummy_image
#             del dummy_list
#             # dummy_image = []
#             dummy_list = []
#             pass
    elif idx==len(json_list)-1:
        # df.to_csv(f'F:/2022/Guide/db/ts_ss_db_annotation/ts_ss_db_{idx}.csv', encoding='utf-8', index=False)
        conn = md_engine.connect()
        df_img.to_sql('ai_image_tbl', con=md_engine, if_exists='append', chunksize=10000, index=False, method='multi')
        # df_ann.to_sql('ai_annotation_tbl', con=md_engine, if_exists='append', chunksize=10000, index=False, method='multi')
        df_ann.to_csv(f'F:/2022/Guide/db/warehouse_db_annotation/warehouse_db_{idx}.csv', encoding='utf-8', index=False)
        conn.close()
#         # cur.executemany(sql1, dummy_image)
#         cur.executemany(sql2, dummy_list)
#         conn.commit()
#
# conn.close()
