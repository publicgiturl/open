import gc

import pandas as pd
import numpy as np
from tqdm import tqdm
import pymysql
from glob import glob
import json
from sqlalchemy import create_engine
### have to pip install mysql-connector before install sqlalchemy

### insert_DF
host_name = '192.168.0.28'
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

json_list =glob('H:/Data/02_Product/label/*.json')

df = pd.DataFrame(columns=['IMG_NAME','OBJ_IDX','CLASS_CODE','ANNO_TYPE','BOX_X_MIN','BOX_Y_MIN','BOX_X_MAX','BOX_Y_MAX', 'POLY_XCNTS', 'POLY_YCNTS'])
# df = pd.read_csv('F:/2022/air_file.csv', index_col=False)
for idx, j_file in enumerate(tqdm(json_list)):

    with open(j_file, encoding='utf-8')as json_file:
        json_data= json.load(json_file)
        img_name = j_file.split('\\')[-1].replace('.json','.jpg')
        # img_path = '06_TS/2D_SS/image'
        # width, height = json_data["Source_Image_Info"]['Resolution'][0],json_data["Source_Image_Info"]['Resolution'][1]
        # dummy_image.append([img_name,img_path, width,height])

        num = 1
        for anno_data in json_data['regions']:
            obj_idx = num

            if anno_data['type'] != 'box':
                continue

            if anno_data["class"] == "Sports Shoes":
                db_code = 93
            elif anno_data["class"] == '2단우산' or anno_data["class"] == '3단우산':
                db_code = 126
            elif anno_data["class"] == '장우산':
                db_code = 125
            elif anno_data["class"] == 'Aqua shoes':
                db_code = 95
            elif anno_data["class"] == 'Sneakers slip-on':
                db_code = 94
            elif anno_data["class"] == "Women's Shoes":
                db_code = 96
            elif anno_data["class"] == "Hill Pumps":
                db_code = 97
            elif anno_data["class"] == "Women's Boots Walker":
                db_code = 98
            elif anno_data["class"] == "Women's sandals":
                db_code = 99
            elif anno_data["class"] == "Men's Suits":
                db_code = 100
            elif anno_data["class"] == "Men's Casual Shoes":
                db_code = 101
            elif anno_data["class"] == "Men's Walker Boots":
                db_code = 102
            elif anno_data["class"] == 'Slippers':
                db_code = 103
            elif anno_data["class"] == 'Functionalization':
                db_code = 104
            elif anno_data["class"] == "Children's Sandals":
                db_code = 105
            elif anno_data["class"] == "Children's Shoes":
                db_code = 106
            elif anno_data["class"] == "Children's Sneakers":
                db_code = 107
            elif anno_data["class"] == 'Casual Bag':
                db_code = 108
            elif anno_data["class"] == "Women's Bag":
                db_code = 109
            elif anno_data["class"] == 'Travel Bag':
                db_code = 111
            elif anno_data["class"] == 'Exercise Bag':
                db_code = 112
            elif anno_data["class"] == "Children's Backpack":
                db_code = 113
            elif anno_data["class"] == "Children's Outing Travel Bag":
                db_code = 114
            elif anno_data["class"] == "'Women Wallet":
                db_code = 115
            elif anno_data["class"] == "Men's Wallet":
                db_code = 116
            elif anno_data["class"] == 'Other Wallet':
                db_code = 117
            elif anno_data["class"] == 'Fashion Hat':
                db_code = 118
            elif anno_data["class"] == 'Child Hat':
                db_code = 119
            elif anno_data["class"] == 'Sunglasses':
                db_code = 120
            elif anno_data["class"] == 'Eyeglass Frames' or anno_data["class"] == '안경테':
                db_code = 121
            elif anno_data["class"] == 'Umbrella':
                db_code = 122
            elif anno_data["class"] == 'Fashion Watch' or anno_data["class"] == '패션시계':
                db_code = 123
            elif anno_data["class"] == 'Other Watches' or anno_data["class"] == '기타시계':
                db_code = 124
            else :
                continue

            num+=1
            anno = 'bbox'
            # try:
            #     points = np.array(anno_data['Coordinate'], np.int32)
            # except Exception as e:
            #     continue
            # poly_x = points[:,0].tolist()
            # poly_y = points[:,1].tolist()
            xmin = anno_data["boxcorners"][0]
            ymin = anno_data["boxcorners"][1]
            xmax = anno_data["boxcorners"][2]
            ymax = anno_data["boxcorners"][3]
            poly_x = None
            poly_y = None
            # xmin = min(poly_x)
            # ymin = min(poly_y)
            # xmax = max(poly_x)
            # ymax = max(poly_y)
            df.loc[len(df)] = [img_name, obj_idx, db_code, anno, xmin, ymin, xmax, ymax, poly_x, poly_y]

    if idx % 3000 ==0:
        conn = md_engine.connect()
        df.to_sql('ai_annotation_tbl', con=md_engine, if_exists='append', chunksize=10000, index=False, method='multi')
        conn.close()
        # df.to_csv(f'F:/2022/Guide/db/ts_ss_db_annotation/ts_ss_db_{idx}.csv', encoding='utf-8', index=False)
        del df
        gc.collect()
        df = pd.DataFrame(columns=['IMG_NAME','OBJ_IDX','CLASS_CODE','ANNO_TYPE','BOX_X_MIN','BOX_Y_MIN','BOX_X_MAX','BOX_Y_MAX', 'POLY_XCNTS', 'POLY_YCNTS'])

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
        df.to_sql('ai_annotation_tbl', con=md_engine, if_exists='append', chunksize=10000, index=False)
        conn.close()
#         # cur.executemany(sql1, dummy_image)
#         cur.executemany(sql2, dummy_list)
#         conn.commit()
#
# conn.close()