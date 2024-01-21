# import json
# from glob import glob
# from tqdm import tqdm
# import numpy as np
# import pymysql
# import pandas as pd
#
# # Connect DB
# # conn = pymysql.connect(host = '192.168.100.53', user = 'haer', password = 'haer', db='onss_ai')
# # curs = conn.cursor()
#
# # sql = "INSERT INTO ai_image_tbl(IMG_NAME,IMG_PATH,IMG_WIDTH,IMG_HEIGHT,LOCATION) VALUES (%s,%s,%s,%s,%s);"
# # sql2 = "INSERT INTO ai_annotation_tbl(IMG_NAME,OBJ_IDX,CLASS_CODE,ANNO_TYPE,BOX_X_MIN,BOX_Y_MIN,BOX_X_MAX,BOX_Y_MAX,POLY_XCNTS,POLY_YCNTS) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
#
# # print("img tbl insert start")
# img_dummy = []
# dummy_list = []
#
# for j_file in tqdm(glob('H:/Data/04_Industrial_safety/fire/label/*.json')):
#     with open(j_file, encoding='utf-8-sig') as json_file:
#         json_data = json.load(json_file)
#
#         img_name = json_data["image"]["filename"]
#         # img_path = '04_Industrial_safety/fire/image'
#         #
#         # width, height = json_data["image"]["resolution"][0], json_data["image"]["resolution"][1]
#         # if json_data['image']['location'] == '01':
#         #     location = '경기도 용인시 기흥구 지삼로331'
#         # elif json_data['image']['location'] == '02':
#         #     location = '경기용인기흥구청덕동'
#         # elif json_data['image']['location'] == '03':
#         #     location = '화성시 양감면 정문송산로93번길 10-59'
#         # elif json_data['image']['location'] == '04':
#         #     location = '광주시 오포읍 고산리 242-6 1동'
#         # elif json_data['image']['location'] == '05':
#         #     location = '용인시 기흥구 강남로 12 스카이프라자 704-2'
#         # elif json_data['image']['location'] == '06':
#         #     location = '청주시 서원구 창직로 114'
#         # elif json_data['image']['location'] == '07':
#         #     location = '전주시 덕진구 원만성로 21'
#         # elif json_data['image']['location'] == '08':
#         #     location = '경기도가평군청평면대성리56-4'
#         # elif json_data['image']['location'] == '09':
#         #     location = '충북 충주시 동량면 하천리'
#         # elif json_data['image']['location'] == '10':
#         #     location = '용인시 기흥구 죽전로10 장은프라자'
#         # elif json_data['image']['location'] == '11':
#         #     location = '화성시 정남면 수면리 133-1'
#         # elif json_data['image']['location'] == '12':
#         #     location = '경기도 용인시 기흥구 청덕동 214-2'
#         # elif json_data['image']['location'] == '13':
#         #     location = '화성시 양감면 정문송산로93번길 10-59'
#         # elif json_data['image']['location'] == '14':
#         #     location = '경기도 용인시 기흥구 청명산로 41번지'
#         # elif json_data['image']['location'] == '15':
#         #     location = '충남 부여군 내산면 금지리 산43'
#         # elif json_data['image']['location'] == '16':
#         #     location = '화성시 양감면 정문송산로93번길 10-59'
#         # elif json_data['image']['location'] == '17':
#         #     location = '경기화성송동727'
#         # elif json_data['image']['location'] == '18':
#         #     location = '라오스, 비엔티엔'
#         #
#         # img_dummy.append([img_name, img_path, width, height, location])
#
#         if json_data["image"]["filename"] != j_file.split('\\')[-1].replace('.json','.jpg'):
#             print(f'파일이름 다르다 : {j_file}')
#
#         obj_idx = 1
#
#         for ann in json_data['annotations']:
#             if ann["class"] == "01":  # 검정색 연기
#                 db_code = 28
#             elif ann["class"] == "02":  # 회색연기
#                 db_code = 30
#             elif ann["class"] == "03":  # 흰색연기
#                 db_code = 29
#             elif ann["class"] == "04":  # 불꽃
#                 db_code = 33
#             elif ann["class"] == "05":  # 구름
#                 db_code = 31
#             elif ann["class"] == "06":  # 안개 연무
#                 db_code = 34
#             elif ann["class"] == "07":  # 조명
#                 db_code = 32
#             elif ann["class"] == "08":  # 햇빛
#                 db_code = 35
#             elif ann['class'] in ['11','09','10']:
#                 continue
#
#             if 'box' in ann.keys():
#                 anno = 'box'
#                 xmin = ann["box"][0]
#                 ymin = ann["box"][1]
#                 xmax = ann["box"][2]
#                 ymax = ann["box"][3]
#                 x_arr = None
#                 y_arr = None
#             try:
#                 if 'polygon' in ann.keys():
#                     anno = 'polygon'
#                     poly_point = np.array(ann['polygon'])
#                     x_arr = poly_point[:, 0].flatten().tolist()
#                     y_arr = poly_point[:, 1].flatten().tolist()
#                     xmax = poly_point[:, 0].max()
#                     xmin = poly_point[:, 0].min()
#                     ymin = poly_point[:, 1].min()
#                     ymax = poly_point[:, 1].max()
#
#                 dummy_list.append([img_name, obj_idx, db_code, anno, xmin, ymin, xmax, ymax, x_arr, y_arr])
#                 obj_idx += 1
#             except Exception as ee:
#                 print(f'폴리곤 좌표쪽 에러 : {ee}')
#                 print(f'폴리곤 좌표쪽 에러 파일 : {j_file}')
#                 print(f'인서트 형태 : {dummy_list}')
#                 pass
#
# #         try :
# #             if len(img_dummy) % 1000 == 0:
# #                 curs.executemany(sql, img_dummy)
# #                 conn.commit()
# #                 img_dummy = []
# #
# #                 # curs.executemany(sql2, dummy_list)
# #                 # conn.commit()
# #                 # dummy_list = []
# #         except Exception as e:
# #                 conn.commit()
# #                 # conn.close()
# #                 # json_file.close()
# #                 print(f'인서트 에러 : {e}')
# #                 print(f'인서트 파일에러 : {j_file}')
# #                 pass
# # conn.close()
# # print("annotation tbl insert finish")
# #
#
import json
import numpy as np
import pymysql

# conn = pymysql.connect(host = '192.168.100.53', user = 'haer', password = 'haer', db='onss_ai')
# curs = conn.cursor()
#
# sql = "INSERT INTO ai_image_tbl(IMG_NAME,IMG_PATH,IMG_WIDTH,IMG_HEIGHT,LOCATION) VALUES (%s,%s,%s,%s,%s);"
# sql2 = "INSERT INTO ai_annotation_tbl(IMG_NAME,OBJ_IDX,CLASS_CODE,ANNO_TYPE,BOX_X_MIN,BOX_Y_MIN,BOX_X_MAX,BOX_Y_MAX,POLY_XCNTS,POLY_YCNTS) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"

print("img tbl insert start")
img_dummy = []

dummy_list = []
with open('H:/Data/04_Industrial_safety/fire/label/S3-N0805MS01738.json', encoding='utf-8-sig') as json_file:
    json_data = json.load(json_file)

    img_name = json_data["image"]["filename"]
    img_path = '04_Industrial_safety/fire/image'

    # if json_data["image"]["filename"] != j_file.split('\\')[-1].replace('.json', '.jpg'):
    #     print(f'파일이름 다르다 : {j_file}')
    #     continue

    width, height = json_data["image"]["resolution"][0], json_data["image"]["resolution"][1]
    if json_data['image']['location'] == '01':
        location = '경기도 용인시 기흥구 지삼로331'
    elif json_data['image']['location'] == '02':
        location = '경기용인기흥구청덕동'
    elif json_data['image']['location'] == '03':
        location = '화성시 양감면 정문송산로93번길 10-59'
    elif json_data['image']['location'] == '04':
        location = '광주시 오포읍 고산리 242-6 1동'
    elif json_data['image']['location'] == '05':
        location = '용인시 기흥구 강남로 12 스카이프라자 704-2'
    elif json_data['image']['location'] == '06':
        location = '청주시 서원구 창직로 114'
    elif json_data['image']['location'] == '07':
        location = '전주시 덕진구 원만성로 21'
    elif json_data['image']['location'] == '08':
        location = '경기도가평군청평면대성리56-4'
    elif json_data['image']['location'] == '09':
        location = '충북 충주시 동량면 하천리'
    elif json_data['image']['location'] == '10':
        location = '용인시 기흥구 죽전로10 장은프라자'
    elif json_data['image']['location'] == '11':
        location = '화성시 정남면 수면리 133-1'
    elif json_data['image']['location'] == '12':
        location = '경기도 용인시 기흥구 청덕동 214-2'
    elif json_data['i
        location = '라오스, 비엔티엔'

    img_dummy.append([img_name, img_path, width, height, location])

    obj_idx = 1

    for ann in json_data['annotations']:
        px = []
        py = []

        if ann["class"] == "01":  # 검정색 연기
            db_code = 28
        elif ann["class"] == "02":  # 회색연기
            db_code = 30
        elif ann["class"] == "03":  # 흰색연기
            db_code = 29mage']['location'] == '13':
        location = '화성시 양감면 정문송산로93번길 10-59'
    elif json_data['image']['location'] == '14':
        location = '경기도 용인시 기흥구 청명산로 41번지'
    elif json_data['image']['location'] == '15':
        location = '충남 부여군 내산면 금지리 산43'
    elif json_data['image']['location'] == '16':
        location = '화성시 양감면 정문송산로93번길 10-59'
    elif json_data['image']['location'] == '17':
        location = '경기화성송동727'
    elif json_data['image']['location'] == '18':
        elif ann["class"] == "04":  # 불꽃
            db_code = 33
        elif ann["class"] == "05":  # 구름
            db_code = 31
        elif ann["class"] == "06":  # 안개 연무
            db_code = 34
        elif ann["class"] == "07":  # 조명
            db_code = 32
        elif ann["class"] == "08":  # 햇빛
            db_code = 35
        elif ann['class'] in ['11', '09', '10']:
            continue

        if 'box' in ann.keys():
            anno = 'box'
            xmin = ann["box"][0]
            ymin = ann["box"][1]
            xmax = ann["box"][2]
            ymax = ann["box"][3]
            x_arr = None
            y_arr = None
        try:
            if 'polygon' in ann.keys():
                arr = np.array(ann['polygon'])
                # print(arr[:,1])
                try:
                    if len(ann['polygon'][0]) == 2:
                        anno = 'polygon'
                        poly_point = np.array(ann['polygon'])
                        x_arr = poly_point[:, 0].flatten().tolist()
                        y_arr = poly_point[:, 1].flatten().tolist()
                        xmax = poly_point[:, 0].max()
                        xmin = poly_point[:, 0].min()
                        ymin = poly_point[:, 1].min()
                        ymax = poly_point[:, 1].max()

                except TypeError as TE:
                    arr = np.array(ann['polygon']).reshape(-1, 2)
                    anno = 'polygon'
                    # poly_point = np.array(ann['polygon'])
                    x_arr = arr[:, 0].flatten().tolist()
                    y_arr = arr[:, 1].flatten().tolist()
                    xmax = arr[:, 0].max()
                    xmin = arr[:, 0].min()
                    ymin = arr[:, 1].min()
                    ymax = arr[:, 1].max()
                    print(x_arr)
                    print(ymin)


            dummy_list.append([img_name, obj_idx, db_code, anno, xmin, ymin, xmax, ymax, x_arr, y_arr])
            obj_idx += 1
        except Exception as ee:
            print(f'폴리곤 좌표쪽 에러 : {ee}')
            print(f'폴리곤 좌표쪽 에러 파일 : {json_data["image"]["filename"]}')
            pass

    # try:
    #     if len(img_dummy) % 1000 == 0:
#     curs.executemany(sql, img_dummy)
#     conn.commit()
#     img_dummy = []
#
#     curs.executemany(sql2, dummy_list)
#     conn.commit()
#     dummy_list = []
#     # except Exception as e:
#     #     conn.commit()
#     #     # conn.close()
#     #     # json_file.close()
#     #     print(f'인서트 에러 : {e}')
#     #     print(f'인서트 파일에러 : {json_data["filename"]}')
#     #     pass
# conn.close()
# print("annotation tbl insert finish")