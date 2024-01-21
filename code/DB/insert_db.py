import gc

import pandas as pd
import numpy as np
from tqdm import tqdm
import pymysql
from glob import glob
import json
from sqlalchemy import create_engine

cls_dict = {'potted plant' :155,  'tv':156 ,'chair':157, 'person':158, 'microwave':159, 'refrigerator':160, 'book':161,
 'clock':162, 'vase':163, 'dining table':164, 'bear':165, 'bed':166, 'stop sign':167, 'truck':25, 'car':6,
 'teddy bear':0, 'skis':0, 'oven':0, 'sports ball':0, 'baseball glove':0, 'tennis racket':0,
 'handbag':0, 'backpack':0, 'bird':171, 'boat':0, 'cell phone':168, 'train':172, 'sandwich':0, 'bowl':0,
 'surfboard':0, 'laptop':169, 'mouse':0, 'keyboard':0, 'bus':24, 'cat':170, 'airplane':173, 'zebra':0,
 'tie':0, 'traffic light':18, 'apple':0, 'baseball bat':0, 'knife':0, 'cake':0, 'wine glass':0,
 'cup':0, 'spoon':0, 'banana':0, 'donut':0, 'bottle':0, 'sink':0, 'toilet':0, 'broccoli':0,
 'skateboard':0, 'fork':0, 'carrot':0, 'couch':0, 'remote':0, 'scissors':0, 'bicycle':20,
 'sheep':0, 'bench':0, 'orange':0, 'elephant':0, 'frisbee':0, 'umbrella':122, 'horse':0, 'dog':174,
 'motorcycle':5, 'kite':0, 'pizza':0, 'fire hydrant':0, 'suitcase':0, 'hot dog':0, 'cow':0,
 'giraffe':0, 'snowboard':0, 'parking meter':0, 'toothbrush':0, 'toaster':0, 'hair drier':0,}


# conn=pymysql.connect(host='192.168.0.28', user='haer',password='haer', db='onss_ai', charset='utf8')
# sql1 = "insert INTO ai_image_tbl(IMG_NAME,IMG_PATH,IMG_WIDTH,IMG_HEIGHT) VALUES (%s,%s,%s,%s);"
# sql2 = "insert INTO ai_annotation_tbl(IMG_NAME,OBJ_IDX,CLASS_CODE,ANNO_TYPE,BOX_X_MIN,BOX_Y_MIN,BOX_X_MAX,BOX_Y_MAX, POLY_XCNTS, POLY_YCNTS) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
# cur=conn.cursor()
print("annotation insert start")

### insert_DF
host_name = '192.168.100.53'
user_name ='haer'
password = 'haer'
database_name = 'onss_ai'

md_engine = create_engine('mysql+mysqlconnector://{}:{}@{}:{}/{}'.format(user_name, password, host_name, 3306, database_name))

# json_list =glob('H:/Data/05_Hanjayeon_monitoring/label/*.json')
df = pd.read_csv('D:/download/coco_val_convert_cls.csv', encoding='utf-8')
df_img = pd.DataFrame(columns=['IMG_NAME','IMG_PATH','IMG_WIDTH','IMG_HEIGHT','LOCATION'])
df_ann = pd.DataFrame(columns=['IMG_NAME','OBJ_IDX','CLASS_CODE','ANNO_TYPE','BOX_X_MIN','BOX_Y_MIN','BOX_X_MAX','BOX_Y_MAX', 'POLY_XCNTS', 'POLY_YCNTS'])
df_land = pd.DataFrame(columns=['IMG_NAME','LANDMARK_IDX','OBJ_IDX','FACE_CODE','X_CNT','Y_CNT'])

with open('D:/download/annotations_trainval2017/annotations/img_resl.json', encoding='utf-8') as new_json:
    img_dict = json.load(new_json)


# for idx, j_file in enumerate(tqdm(json_list)):
for idx in tqdm(range(len(df))):

    # with open(j_file, encoding='utf-8')as json_file:
    #     json_data= json.load(json_file)
    img_name = df.loc[idx,'IMG_NAME']
    img_path = f'coco_data/images/'
    width, height = img_dict[img_name]
    location = None
        # img_name = j_file.split('\\')[-1].replace('.json','.jpg')
        # img_path = '05_Hanjayeon_monitoring/images'
        # width, height = json_data["images"]['resolution'][0], json_data["images"]['resolution'][1]
        # location = None


    df_img.loc[len(df_img)] = [img_name, img_path, width, height, location]
        #
        # num = 1
        # anno_data = json_data['annotations']
        # obj_idx = num
        #
        # num+=1
        # anno = 'bbox'
        # try:
        #     points = np.array(anno_data['Coordinate'], np.int32)
        # except Exception as e:
        #     continue
        # poly_x = points[:,0].tolist()
        # poly_y = points[:,1].tolist()
        # xmin = min(poly_x)
        # ymin = min(poly_y)
        # xmax = max(poly_x)
        # ymax = max(poly_y)
    if cls_dict[df.loc[idx,'CLASS_CODE']]==0:
        continue
    else:
        db_code = cls_dict[df.loc[idx,'CLASS_CODE']]

    if df.loc[idx,'ANNO_TYPE'] =='bbox':
        anno = df.loc[idx,'ANNO_TYPE']
        xmin = df.loc[idx,'BOX_X_MIN']
        ymin = df.loc[idx, 'BOX_Y_MIN']
        xmax = df.loc[idx, 'BOX_X_MAX']
        ymax = df.loc[idx, 'BOX_Y_MAX']
        poly_x = None
        poly_y = None
    else:
        anno = df.loc[idx, 'ANNO_TYPE']
        poly_x = df.loc[idx, 'POLY_XCNTS']
        poly_y = df.loc[idx,'POLY_YCNTS']
        xmin = df.loc[idx,'BOX_X_MIN']
        ymin = df.loc[idx, 'BOX_Y_MIN']
        xmax = df.loc[idx, 'BOX_X_MAX']
        ymax = df.loc[idx, 'BOX_Y_MAX']
        # xmin = anno_data["face_rectangle"]['begin_x']
        # ymin = anno_data["face_rectangle"]['begin_y']
        # xmax = anno_data["face_rectangle"]['end_x']
        # ymax = anno_data["face_rectangle"]['end_y']
        # poly_x = None
        # poly_y = None
        # db_code = 27
    obj_idx = df.loc[idx,'OBJ_IDX']
    # df_ann.loc[len(df_ann)] = [img_name, obj_idx, db_code, anno, xmin, ymin, xmax, ymax, poly_x, poly_y]
        # land_idx = 1
        # for k, v in anno_data['jaw'].items():
        #     df_land.loc[len(df_land)] = [img_name, land_idx, obj_idx, 1, v[0], v[1]]
        #     land_idx +=1
        # for k, v in anno_data['left_eye_brow'].items():
        #     df_land.loc[len(df_land)] = [img_name, land_idx, obj_idx, 2, v[0], v[1]]
        #     land_idx += 1
        # for k, v in anno_data['right_eye_brow'].items():
        #     df_land.loc[len(df_land)] = [img_name, land_idx, obj_idx, 3, v[0], v[1]]
        #     land_idx += 1
        # for k, v in anno_data['left_eye'].items():
        #     df_land.loc[len(df_land)] = [img_name, land_idx, obj_idx, 4, v[0], v[1]]
        #     land_idx += 1
        # for k, v in anno_data['right_eye'].items():
        #     df_land.loc[len(df_land)] = [img_name, land_idx, obj_idx, 5, v[0], v[1]]
        #     land_idx += 1
        # for k, v in anno_data['nose'].items():
        #     df_land.loc[len(df_land)] = [img_name, land_idx, obj_idx, 6, v[0], v[1]]
        #     land_idx += 1
        # for k, v in anno_data['mouth'].items():
        #     df_land.loc[len(df_land)] = [img_name, land_idx, obj_idx, 7, v[0], v[1]]
        #     land_idx += 1
df_img.drop_duplicates(['IMG_NAME'],inplace=True)

# df_ann.to_csv('D:/download/annotations_trainval2017/annotations/ann_tbl.csv', sep=',',index=False)
df_img.to_csv('D:/download/annotations_trainval2017/annotations/img_tbl.csv', sep=',',index=False)
    # if idx % 1000 ==0:
    #     conn = md_engine.connect()
    #     df_img.to_sql('ai_image_tbl', con=md_engine, if_exists='append', chunksize=20000, index=False, method='multi')
    #     df_ann.to_sql('ai_annotation_tbl', con=md_engine, if_exists='append', chunksize=20000, index=False,
    #                   method='multi')
    #     df_land.to_sql('ai_landmark_annotation_tbl', con=md_engine, if_exists='append', chunksize=20000, index=False,
    #                   method='multi')
    #     del [[df_img, df_ann, df_land]]
    #     conn.close()
    #     gc.collect()
    #     df_img = pd.DataFrame(columns=['IMG_NAME', 'IMG_PATH', 'IMG_WIDTH', 'IMG_HEIGHT', 'LOCATION'])
    #     df_ann = pd.DataFrame(
    #         columns=['IMG_NAME', 'OBJ_IDX', 'CLASS_CODE', 'ANNO_TYPE', 'BOX_X_MIN', 'BOX_Y_MIN', 'BOX_X_MAX',
    #                  'BOX_Y_MAX', 'POLY_XCNTS', 'POLY_YCNTS'])
    #     df_land = pd.DataFrame(columns=['IMG_NAME', 'LANDMARK_IDX', 'OBJ_IDX', 'FACE_CODE', 'X_CNT', 'Y_CNT'])

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
#     elif idx==len(json_list)-1:
#         conn = md_engine.connect()
#         df_img.to_sql('ai_image_tbl', con=md_engine, if_exists='append', chunksize=20000, index=False, method='multi')
#         df_ann.to_sql('ai_annotation_tbl', con=md_engine, if_exists='append', chunksize=20000, index=False,
#                       method='multi')
#         df_land.to_sql('ai_landmark_annotation_tbl', con=md_engine, if_exists='append', chunksize=20000, index=False,
#                        method='multi')
#         conn.close()
#         # cur.executemany(sql1, dummy_image)
#         cur.executemany(sql2, dummy_list)
#         conn.commit()
#
# conn.close()
